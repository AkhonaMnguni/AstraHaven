from flask import Blueprint, render_template
from flask_login import login_required

from ..models import Transaction

suppliers_bp = Blueprint("suppliers", __name__, url_prefix="/suppliers")


@suppliers_bp.route("/")
@login_required
def index():
    suppliers = {}
    for transaction in Transaction.query.order_by(Transaction.created_at.desc()).all():
        suppliers.setdefault(transaction.supplier, []).append(transaction)
    return render_template("suppliers.html", suppliers=suppliers)
