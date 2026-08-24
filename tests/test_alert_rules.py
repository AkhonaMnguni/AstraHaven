from AstraHaven.alerts.rules import detect_transaction_alerts
from AstraHaven.models import Transaction


def test_high_value_transaction_creates_alert():
    transaction = Transaction(reference="TX-1", amount=12000, supplier="Vendor")
    alerts = detect_transaction_alerts(transaction)
    assert any(alert["severity"] == "high" for alert in alerts)
