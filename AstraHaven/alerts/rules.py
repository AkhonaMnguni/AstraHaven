from decimal import Decimal

from sqlalchemy import func

from ..extensions import db
from ..models import Alert, Transaction


HIGH_VALUE_THRESHOLD = 10000
EXPENSE_SPIKE_MULTIPLIER = Decimal("2.0")
HIGH_PEER_VARIANCE = Decimal("1.50")


def detect_transaction_alerts(transaction):
    """Return a simple alert list for large or pending transactions."""
    alerts = []
    reference = getattr(transaction, "invoice_reference", getattr(transaction, "reference", "unknown"))

    if transaction.amount >= HIGH_VALUE_THRESHOLD:
        alerts.append(
            {
                "title": "High-value transaction",
                "severity": "high",
                "description": f"Transaction {reference} exceeds the review threshold.",
            }
        )

    if str(getattr(transaction, "status", "")).lower() == "pending":
        alerts.append(
            {
                "title": "Pending transaction",
                "severity": "low",
                "description": f"Transaction {reference} is awaiting approval.",
            }
        )

    return alerts


def suspicious_transactions():
    """Fetch transactions above the review threshold for manual follow-up."""
    return db.session.scalars(
        db.select(Transaction).where(Transaction.amount >= HIGH_VALUE_THRESHOLD)
    ).all()


def classify_score(score):
    """Map a score to a risk-level label used for alerts."""
    if score >= 80:
        return "CRITICAL"
    if score >= 60:
        return "HIGH"
    if score >= 30:
        return "MEDIUM"
    return "LOW"


def calculate_historical_average(transaction):
    """Return the average amount of earlier transactions in the same branch and category."""
    if not transaction.branch_id or not transaction.category or transaction.transaction_date is None:
        return Decimal("0")

    previous = db.session.scalars(
        db.select(Transaction)
        .where(
            Transaction.branch_id == transaction.branch_id,
            Transaction.category == transaction.category,
            Transaction.transaction_date < transaction.transaction_date,
        )
        .order_by(Transaction.transaction_date.desc())
        .limit(12)
    ).all()

    if not previous:
        return Decimal("0")

    total = sum((item.amount for item in previous), Decimal("0"))
    return total / Decimal(len(previous))


def calculate_peer_average(transaction):
    """Return the average amount from comparable transactions in other branches."""
    peer_transactions = db.session.scalars(
        db.select(Transaction)
        .where(
            Transaction.category == transaction.category,
            Transaction.id != transaction.id,
            Transaction.branch_id != transaction.branch_id,
        )
        .order_by(Transaction.transaction_date.desc())
        .limit(12)
    ).all()

    if not peer_transactions:
        return Decimal("0")

    total = sum((item.amount for item in peer_transactions), Decimal("0"))
    return total / Decimal(len(peer_transactions))


def detect_expense_spike(transaction):
    """Flag a transaction that is unusually high compared with past and peer activity."""
    historical_average = calculate_historical_average(transaction)
    if historical_average <= 0:
        return None

    threshold = historical_average * EXPENSE_SPIKE_MULTIPLIER
    if transaction.amount < threshold:
        return None

    increase_percent = ((transaction.amount - historical_average) / historical_average) * Decimal("100")
    score = 40
    reasons = [f"Expense increased by {float(increase_percent):.1f}% above the historical average."]

    peer_average = calculate_peer_average(transaction)
    if peer_average > 0:
        peer_ratio = transaction.amount / peer_average
        if peer_ratio >= HIGH_PEER_VARIANCE:
            score += 30
            reasons.append("Transaction is more than 50% above the peer-branch average.")

    if (
        transaction.selected_by_id
        and transaction.approved_by_id
        and transaction.selected_by_id == transaction.approved_by_id
    ):
        score += 20
        reasons.append("The same employee selected and approved the transaction.")

    score = min(score, 100)
    severity = classify_score(score)
    explanation = "\n".join(f"• {reason}" for reason in reasons)
    recommendation = (
        "Verify the invoice, supplier pricing, delivery evidence and approval history. "
        "Compare the transaction with comparable branches before drawing conclusions."
    )

    return {
        "alert_type": "EXPENSE_SPIKE",
        "severity": severity,
        "risk_score": score,
        "title": "Expense pattern requires investigation",
        "explanation": explanation,
        "recommendation": recommendation,
    }


def detect_supplier_concentration(transaction):
    """Detect when one supplier dominates a branch's transaction activity."""
    if not transaction.supplier_id:
        return None

    transactions = db.session.scalars(
        db.select(Transaction).where(
            Transaction.branch_id == transaction.branch_id,
            Transaction.supplier_id == transaction.supplier_id,
        )
    ).all()

    if len(transactions) < 3:
        return None

    total_branch_transactions = db.session.scalar(
        db.select(func.count(Transaction.id)).where(Transaction.branch_id == transaction.branch_id)
    ) or 0

    if total_branch_transactions == 0:
        return None

    concentration = (len(transactions) / total_branch_transactions) * 100
    if concentration < 70:
        return None

    score = 30
    return {
        "alert_type": "SUPPLIER_CONCENTRATION",
        "severity": classify_score(score),
        "risk_score": score,
        "title": "High supplier concentration",
        "explanation": (
            f"• Supplier represents {concentration:.1f}% of branch transactions in the available dataset."
        ),
        "recommendation": (
            "Review supplier selection, pricing, contract terms and whether alternative suppliers were considered."
        ),
    }


def analyze_transaction(transaction):
    """Run the configured rules and combine any alerts generated for one transaction."""
    results = []

    expense_alert = detect_expense_spike(transaction)
    if expense_alert:
        results.append(expense_alert)

    supplier_alert = detect_supplier_concentration(transaction)
    if supplier_alert:
        results.append(supplier_alert)

    return results


def generate_alerts_for_transaction(transaction):
    """Persist all alerts generated for a transaction into the database."""
    results = analyze_transaction(transaction)
    created = []

    for result in results:
        alert = Alert(
            alert_type=result["alert_type"],
            severity=result["severity"],
            risk_score=result["risk_score"],
            title=result["title"],
            explanation=result["explanation"],
            recommendation=result["recommendation"],
            transaction_id=transaction.id,
            status="OPEN",
        )
        db.session.add(alert)
        created.append(alert)

    db.session.commit()
    return created
