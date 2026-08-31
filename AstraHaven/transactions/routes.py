# from flask import Blueprint, flash, redirect, render_template, request, url_for
# from flask_login import login_required
#
# from ..audit import record_event
# from ..extensions import db
# from ..models import Transaction
# from ..security import roles_required
#
# transactions_bp = Blueprint("transactions", __name__, url_prefix="/transactions")
#
#
# @transactions_bp.route("/")
# @login_required
# def index():
#     return render_template("transactions.html", transactions=Transaction.query.order_by(Transaction.created_at.desc()).all())
#
#
# @transactions_bp.route("/new", methods=["POST"])
# @login_required
# def create():
#     if not request.form.get("reference") or not request.form.get("supplier"):
#         flash("Reference and supplier are required.", "error")
#         return redirect(url_for("transactions.index"))
#     transaction = Transaction(
#         reference=request.form["reference"].strip(),
#         supplier=request.form["supplier"].strip(),
#         amount=float(request.form.get("amount", 0)),
#     )
#     db.session.add(transaction)
#     db.session.commit()
#     record_event("user", "create_transaction", transaction.reference)
#     return redirect(url_for("transactions.index"))
#
#
# @transactions_bp.route("/<int:transaction_id>/approve", methods=["POST"])
# @roles_required("admin", "analyst")
# def approve(transaction_id):
#     transaction = db.get_or_404(Transaction, transaction_id)
#     transaction.status = "approved"
#     db.session.commit()
#     return redirect(url_for("transactions.index"))





from datetime import date
from decimal import Decimal, InvalidOperation

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from ..audit import record_audit
from ..extensions import db
from ..models import (
    Branch,
    Employee,
    Supplier,
    Transaction,
)
from ..security import login_required, roles_required


transactions_bp = Blueprint(
    "transactions",
    __name__,
    url_prefix="/transactions",
)


@transactions_bp.get("/")
@login_required
def index():
    transactions = db.session.scalars(
        db.select(Transaction)
        .order_by(
            Transaction.transaction_date.desc()
        )
    ).all()

    return render_template(
        "transactions.html",
        transactions=transactions,
    )


@transactions_bp.route(
    "/new",
    methods=["GET", "POST"],
)
@roles_required(
    "OWNER",
    "ADMIN",
    "MANAGER",
)
def create():
    branches = db.session.scalars(
        db.select(Branch)
    ).all()

    suppliers = db.session.scalars(
        db.select(Supplier)
    ).all()

    employees = db.session.scalars(
        db.select(Employee)
    ).all()

    if request.method == "POST":
        try:
            amount = Decimal(
                request.form["amount"]
            )

            if amount <= 0:
                raise ValueError

            transaction_date = date.fromisoformat(
                request.form["transaction_date"]
            )

            branch_id = int(
                request.form["branch_id"]
            )

            supplier_id = int(
                request.form["supplier_id"]
            )

            selected_by_id = int(
                request.form["selected_by_id"]
            )

            approved_by_id = int(
                request.form["approved_by_id"]
            )

        except (
            KeyError,
            ValueError,
            InvalidOperation,
        ):
            flash(
                "Invalid transaction data.",
                "error",
            )

            return redirect(
                url_for(
                    "transactions.create"
                )
            )

        if selected_by_id == approved_by_id:
            flash(
                "Segregation of duties violation: "
                "the selector and approver should normally "
                "be different employees.",
                "error",
            )

            return redirect(
                url_for(
                    "transactions.create"
                )
            )

        transaction = Transaction(
            amount=amount,
            category=request.form[
                "category"
            ].strip(),
            description=request.form[
                "description"
            ].strip(),
            invoice_reference=request.form[
                "invoice_reference"
            ].strip(),
            transaction_date=transaction_date,
            branch_id=branch_id,
            supplier_id=supplier_id,
            selected_by_id=selected_by_id,
            approved_by_id=approved_by_id,
            status="APPROVED",
        )

        db.session.add(transaction)
        db.session.commit()

        record_audit(
            "TRANSACTION_CREATED",
            "Transaction",
            transaction.id,
        )

        flash(
            "Transaction created.",
            "success",
        )

        return redirect(
            url_for(
                "transactions.index"
            )
        )

    return render_template(
        "transactions.html",
        transactions=[],
        branches=branches,
        suppliers=suppliers,
        employees=employees,
        create_mode=True,
    )

