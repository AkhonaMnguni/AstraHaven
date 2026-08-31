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
    from ..models import Supplier
    from ..security import login_required, roles_required


    suppliers_bp = Blueprint(
     "suppliers",
     __name__,
     url_prefix="/suppliers",
    )


    @suppliers_bp.get("/")
    @login_required
    def index():
     suppliers = db.session.scalars(
     db.select(Supplier)
    .order_by(Supplier.name)
     ).all()

     return render_template(
         "suppliers.html",
    suppliers=suppliers,
     )


    @suppliers_bp.post("/new")
    @roles_required(
     "OWNER",
     "ADMIN",
     "MANAGER",
    )
    def create():
   name = request.form.get(
     "name",
    "",
     ).strip()

     category = request.form.get(
         "category",
        "",
     ).strip()

     if not name or not category:
        flash(
         "Supplier name and category are required.",
         "error",
     )

     return redirect(
        url_for("suppliers.index")
     )

     supplier = Supplier(
        name=name,
         category=category,
         active=True,
         )

    db.session.add(supplier)
     db.session.commit()

     record_audit(
     "SUPPLIER_CREATED",
     "Supplier",
    supplier.id,
     )

     flash(
        "Supplier created.",
        "success",
     )

     return redirect(
       url_for("suppliers.index")
     )
