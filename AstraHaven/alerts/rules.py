from ..models import Transaction


HIGH_VALUE_THRESHOLD = 10000


def detect_transaction_alerts(transaction):
    alerts = []
    if transaction.amount >= HIGH_VALUE_THRESHOLD:
        alerts.append({"title": "High-value transaction", "severity": "high", "description": f"Transaction {transaction.reference} exceeds the review threshold."})
    if transaction.status == "pending":
        alerts.append({"title": "Pending transaction", "severity": "low", "description": f"Transaction {transaction.reference} is awaiting approval."})
    return alerts


def suspicious_transactions():
    return Transaction.query.filter(Transaction.amount >= HIGH_VALUE_THRESHOLD).all()


from collections import defaultdict
from decimal import Decimal

from sqlalchemy import func

from ..extensions import db
from ..models import Alert, Transaction


EXPENSE_SPIKE_MULTIPLIER = Decimal("2.0")
HIGH_PEER_VARIANCE = Decimal("1.50")


def classify_score(score):
    if score >= 80:
        return "CRITICAL"

 if score >= 60:
    return "HIGH"

 if score >= 30:
    return "MEDIUM"

    return "LOW"


def calculate_historical_average(transaction):
     previous = db.session.scalars(
     db.select(Transaction)
     .where(
    Transaction.branch_id
     == transaction.branch_id,
     Transaction.category
     == transaction.category,
     Transaction.transaction_date
     < transaction.transaction_date,
     )
     .order_by(
     Transaction.transaction_date.desc()
     )
     .limit(12)
     ).all()

  if not previous:
    return Decimal("0")

     total = sum(
     (item.amount for item in previous),
     Decimal("0"),
     )

        return total / len(previous)


def calculate_peer_average(transaction):


  if not peer_transactions:
    return Decimal("0")

     total = sum(
     (
     item.amount
    for item in peer_transactions
     ),
     Decimal("0"),
     )

        return total / len(peer_transactions)


def detect_expense_spike(transaction):
     historical_average = (
    calculate_historical_average(
     transaction
     )
     )

 if historical_average <= 0:
    return None

     threshold = (
     historical_average
     * EXPENSE_SPIKE_MULTIPLIER
     )

 if transaction.amount < threshold:
    return None

     increase_percent = (
     (
     transaction.amount
     - historical_average
     )
     / historical_average
     ) * 100

     score = 40

     reasons = [
     (
     "Expense increased by "
     f"{increase_percent:.1f}% "
     "above the historical average."
     )
     ]

     peer_average = (
     calculate_peer_average(
     transaction
     )
    )

    if peer_average > 0:
         transaction.amount
         / peer_average
         )

    if peer_ratio >= HIGH_PEER_VARIANCE:
     score += 30

     reasons.append(
    (
     "Transaction is more than "
     "50% above the peer-branch average."
       )
     )

     if (
    transaction.selected_by_id
     and transaction.approved_by_id
     and transaction.selected_by_id
     == transaction.approved_by_id
     ):
    score += 20

     reasons.append(
     (
     "The same employee selected "
     "and approved the transaction."
     )
     )

     score = min(score, 100)

     severity = classify_score(score)

     explanation = "\n".join(
    f"• {reason}"
     for reason in reasons
     )

     recommendation = (
     "Verify the invoice, supplier pricing, "
     "delivery evidence and approval history. "
     "Compare the transaction with comparable "
     "branches before drawing conclusions."
     )

     return {
     "alert_type": "EXPENSE_SPIKE",
     "severity": severity,
     "risk_score": score,
    "title": (
     "Expense pattern requires investigation"
     ),
     "explanation": explanation,
    "recommendation": recommendation,
     }


def detect_supplier_concentration(transaction):
    if not transaction.supplier_id:
        return None

     transactions = db.session.scalars(
     db.select(Transaction)
    .where(
    Transaction.branch_id
     == transaction.branch_id,
     Transaction.supplier_id
     == transaction.supplier_id,
     )
     ).all()

 if len(transactions) < 3:
    return None

     total_branch_transactions = db.session.scalar(
     db.select(
     func.count(Transaction.id)
     ).where(
     Transaction.branch_id
     == transaction.branch_id
     )
     ) or 0

 if total_branch_transactions == 0:
    return None

     concentration = (
     len(transactions)
     / total_branch_transactions
     ) * 100

     if concentration < 70:
     return None

     score = 30

return {
     "alert_type": "SUPPLIER_CONCENTRATION",
     "severity": classify_score(score),
     "risk_score": score,
         "title": (
         "High supplier concentration"
     ),
     "explanation": (
     f"• Supplier represents "
    f"{concentration:.1f}% of branch "
     "transactions in the available dataset."
     ),
     "recommendation": (
     "Review supplier selection, pricing, "
     "contract terms and whether alternative "
     "suppliers were considered."
     ),
     }


def analyze_transaction(transaction):
 results = []

 expense_alert = detect_expense_spike(
 transaction
 )

if expense_alert:
     results.append(expense_alert)

     supplier_alert = (
     detect_supplier_concentration(
     transaction
     )
     )

 if supplier_alert:
 results.append(supplier_alert)

 return results


def generate_alerts_for_transaction(
     transaction,
    ):
     results = analyze_transaction(
     transaction
     )

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