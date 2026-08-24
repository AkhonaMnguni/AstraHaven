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
