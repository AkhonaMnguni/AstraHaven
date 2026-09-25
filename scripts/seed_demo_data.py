"""Seed the application database with demo branches, users, suppliers, and transactions."""
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from datetime import date, timedelta
from decimal import Decimal

from AstraHaven import create_app
from AstraHaven.alerts.rules import generate_alerts_for_transaction
from AstraHaven.extensions import db
from AstraHaven.models import Branch, Employee, Supplier, Transaction, User

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    cape_town = Branch(name="Cape Town Central", location="Cape Town", size=100)
    durban = Branch(name="Durban Central", location="Durban", size=95)
    johannesburg = Branch(name="Johannesburg Central", location="Johannesburg", size=110)

    db.session.add_all([cape_town, durban, johannesburg])
    db.session.flush()

    owner = User(username="owner", email="owner@astrahaven.local", role="OWNER", branch_id=cape_town.id)
    owner.set_password("OwnerPassword123!")

    admin = User(username="admin", email="admin@astrahaven.local", role="ADMIN", branch_id=cape_town.id)
    admin.set_password("AdminPassword123!")

    analyst = User(username="analyst", email="analyst@astrahaven.local", role="ANALYST", branch_id=cape_town.id)
    analyst.set_password("AnalystPassword123!")

    db.session.add_all([owner, admin, analyst])

    supplier_normal = Supplier(name="Reliable Cleaning Supplies", category="Cleaning", active=True)
    supplier_new = Supplier(name="RapidClean Holdings", category="Cleaning", active=True)
    supplier_durban = Supplier(name="Durban Cleaning Co", category="Cleaning", active=True)
    supplier_jhb = Supplier(name="Johannesburg Cleaning Co", category="Cleaning", active=True)

    db.session.add_all([supplier_normal, supplier_new, supplier_durban, supplier_jhb])
    db.session.flush()

    employee_manager = Employee(name="Manager X", role="MANAGER", branch_id=cape_town.id)
    employee_manager_2 = Employee(name="Manager Y", role="MANAGER", branch_id=cape_town.id)
    durban_employee = Employee(name="Durban Manager", role="MANAGER", branch_id=durban.id)
    jhb_employee = Employee(name="Johannesburg Manager", role="MANAGER", branch_id=johannesburg.id)

    db.session.add_all([employee_manager, employee_manager_2, durban_employee, jhb_employee])
    db.session.flush()

    start_date = date.today() - timedelta(days=330)

    for month in range(6):
        db.session.add(
            Transaction(
                amount=Decimal("3000000.00"),
                category="Cleaning",
                description="Monthly cleaning supplies",
                invoice_reference=f"CLEAN-HIST-{month}",
                transaction_date=start_date + timedelta(days=month * 30),
                branch_id=cape_town.id,
                supplier_id=supplier_normal.id,
                selected_by_id=employee_manager_2.id,
                approved_by_id=employee_manager.id,
                status="APPROVED",
            )
        )

    for month in range(3):
        db.session.add(
            Transaction(
                amount=Decimal("3200000.00"),
                category="Cleaning",
                description="Durban cleaning supplies",
                invoice_reference=f"DURBAN-{month}",
                transaction_date=start_date + timedelta(days=month * 30),
                branch_id=durban.id,
                supplier_id=supplier_durban.id,
                selected_by_id=durban_employee.id,
                approved_by_id=durban_employee.id,
                status="APPROVED",
            )
        )

        db.session.add(
            Transaction(
                amount=Decimal("3100000.00"),
                category="Cleaning",
                description="Johannesburg cleaning supplies",
                invoice_reference=f"JHB-{month}",
                transaction_date=start_date + timedelta(days=month * 30),
                branch_id=johannesburg.id,
                supplier_id=supplier_jhb.id,
                selected_by_id=jhb_employee.id,
                approved_by_id=jhb_employee.id,
                status="APPROVED",
            )
        )

    db.session.commit()

    suspicious = Transaction(
        amount=Decimal("9000000.00"),
        category="Cleaning",
        description="Monthly cleaning supplies",
        invoice_reference="INV-SUSPICIOUS-001",
        transaction_date=date.today(),
        branch_id=cape_town.id,
        supplier_id=supplier_new.id,
        selected_by_id=employee_manager.id,
        approved_by_id=employee_manager.id,
        status="APPROVED",
    )

    db.session.add(suspicious)
    db.session.commit()

    generate_alerts_for_transaction(suspicious)
