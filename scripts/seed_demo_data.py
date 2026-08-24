from AstraHaven import create_app
from AstraHaven.extensions import db
from AstraHaven.models import Alert, Transaction, User

app = create_app()

with app.app_context():
    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", role="admin")
        admin.set_password("admin-password")
        db.session.add(admin)
    if not Transaction.query.first():
        db.session.add_all([
            Transaction(reference="TX-1001", amount=1250, supplier="Northwind Parts", status="approved"),
            Transaction(reference="TX-1002", amount=18500, supplier="Contoso Freight", status="pending"),
        ])
    if not Alert.query.first():
        db.session.add(Alert(title="Review high-value transaction", severity="high", description="TX-1002 requires analyst review."))
    db.session.commit()
    print("Demo data seeded. Login with admin / admin-password")
