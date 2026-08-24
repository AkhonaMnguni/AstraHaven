from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from ..audit import record_event
from ..extensions import db
from ..models import Transaction
from ..security import roles_required

transactions_bp = Blueprint("transactions", __name__, url_prefix="/transactions")


@transactions_bp.route("/")
@login_required
def index():
    return render_template("transactions.html", transactions=Transaction.query.order_by(Transaction.created_at.desc()).all())


@transactions_bp.route("/new", methods=["POST"])
@login_required
def create():
    if not request.form.get("reference") or not request.form.get("supplier"):
        flash("Reference and supplier are required.", "error")
        return redirect(url_for("transactions.index"))
    transaction = Transaction(
        reference=request.form["reference"].strip(),
        supplier=request.form["supplier"].strip(),
        amount=float(request.form.get("amount", 0)),
    )
    db.session.add(transaction)
    db.session.commit()
    record_event("user", "create_transaction", transaction.reference)
    return redirect(url_for("transactions.index"))


@transactions_bp.route("/<int:transaction_id>/approve", methods=["POST"])
@roles_required("admin", "analyst")
def approve(transaction_id):
    transaction = db.get_or_404(Transaction, transaction_id)
    transaction.status = "approved"
    db.session.commit()
    return redirect(url_for("transactions.index"))
