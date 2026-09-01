from AstraHaven.alerts.rules import detect_transaction_alerts
from AstraHaven.models import Transaction
from datetime import date, timedelta
from decimal import Decimal

from AstraHaven.alerts.rules import (
 classify_score,
 detect_expense_spike,
)
from AstraHaven.extensions import db
from AstraHaven.models import (
 Branch,
 Employee,
 Supplier,
 Transaction,
)


def test_high_value_transaction_creates_alert():
    transaction = Transaction(reference="TX-1", amount=12000, supplier="Vendor")
    alerts = detect_transaction_alerts(transaction)
    assert any(alert["severity"] == "high" for alert in alerts)




def test_classification():
 assert classify_score(10) == "LOW"
 assert classify_score(40) == "MEDIUM"
 assert classify_score(65) == "HIGH"
 assert classify_score(90) == "CRITICAL"


def test_expense_spike_detection(app):
 with app.app_context():

 branch = Branch(
 name="Test Branch",
 location="Test",
 size=10,
 )

 supplier = Supplier(
 name="Test Supplier",
 category="Cleaning",
 )

 employee_one = Employee(
 name="Employee One",
 role="Manager",
 branch=branch,
 )

 employee_two = Employee(
 name="Employee Two",
 role="Manager",
 branch=branch,
 )

 db.session.add_all(
 [
 branch,
 supplier,
 employee_one,
 employee_two,
 ]
 )

 db.session.flush()

 for index in range(3):

 db.session.add(
 Transaction(
 amount=Decimal("1000"),
 category="Cleaning",
 description="Normal",
 invoice_reference=f"N-{index}",
 transaction_date=(
 date.today()
 - timedelta(days=30 * (index + 1))
 ),
 branch_id=branch.id,
 supplier_id=supplier.id,
 selected_by_id=employee_one.id,
 approved_by_id=employee_two.id,
 )
 )

 db.session.commit()

 suspicious = Transaction(
 amount=Decimal("3000"),
 category="Cleaning",
 description="Large purchase",
 invoice_reference="SUSP-1",
 transaction_date=date.today(),
 branch_id=branch.id,
 supplier_id=supplier.id,
 selected_by_id=employee_one.id,
 approved_by_id=employee_one.id,
 )

 db.session.add(suspicious)
 db.session.commit()

 result = detect_expense_spike(
 )

 assert result is not None
 assert result["risk_score"] >= 40
 assert result["severity"] in {
 "MEDIUM",
 "HIGH",
 "CRITICAL",
 }