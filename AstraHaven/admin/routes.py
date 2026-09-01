from flask import Blueprint, render_template
from flask_login import login_required

from ..models import User
from ..security import roles_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/users")
@login_required
@roles_required("admin")
def users():
    return render_template("admin_users.html", users=User.query.order_by(User.username).all())


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
    from ..models import User
    from ..security import roles_required


    admin_bp = Blueprint(
        "admin",
        __name__,
        url_prefix="/admin",
    )


    @admin_bp.get("/users")
    @roles_required(
        "OWNER",
        "ADMIN",
    )
    def users():
        users = db.session.scalars(
            db.select(User)
            .order_by(User.username)
        ).all()

        return render_template(
            "admin_users.html",
            users=users,
        )


    @admin_bp.post("/users/<int:user_id>/role")
    @roles_required("OWNER")
    def change_role(user_id):
        user = db.get_or_404(
            User,
            user_id,
        )

        role = request.form.get(
            "role",
            "",
        ).strip().upper()

        valid_roles = {
            "OWNER",
            "ADMIN",
            "AUDITOR",
            "MANAGER",
            "ANALYST",
        }

        if role not in valid_roles:
            flash(
                "Invalid role.",
                "error",
            )

            return redirect(
                url_for("admin.users")
            )

        user.role = role

        db.session.commit()

        record_audit(
            "USER_ROLE_CHANGED",
            "User",
            user.id,
            f"New role: {role}",
        )

        flash(
            "User role updated.",
            "success",
        )

        return redirect(
            url_for("admin.users")
        )

