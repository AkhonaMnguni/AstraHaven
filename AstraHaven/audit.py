import logging

logger = logging.getLogger("AstraHaven.audit")


def record_event(actor, action, resource):
    logger.info("actor=%s action=%s resource=%s", actor, action, resource)



from flask import request, session

from .extensions import db
from .models import AuditLog


def record_audit(
    action,
    resource_type=None,
    resource_id=None,
    details=None,
):
    log = AuditLog(
        user_id=session.get("user_id"),
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        ip_address=request.remote_addr,
        details=details,
    )

    db.session.add(log)
    db.session.commit()
13. smartshield/auth/routes.py
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from sqlalchemy import or_

from ..audit import record_audit
from ..extensions import db, limiter
from ..models import User


auth_bp = Blueprint(
    "auth",
    __name__,
)


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    if request.method == "POST":
        username = request.form.get(
            "username",
            "",
        ).strip()

        password = request.form.get(
            "password",
            "",
        )

        user = db.session.scalar(
            db.select(User).where(
                or_(
                    User.username == username,
                    User.email == username,
                )
            )
        )

        if (
            user
            and user.active
            and user.check_password(password)
        ):
            session.clear()

            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role
            session["branch_id"] = user.branch_id
            session.permanent = True

            record_audit(
                "LOGIN_SUCCESS",
                "User",
                user.id,
            )

            return redirect(
                url_for("dashboard.index")
            )

        flash(
            "Invalid username or password.",
            "error",
        )

        return render_template("login.html"), 401

    return render_template("login.html")


@auth_bp.post("/logout")
def logout():
    user_id = session.get("user_id")

    if user_id:
        record_audit(
            "LOGOUT",
            "User",
            user_id,
        )

    session.clear()

    return redirect(
        url_for("auth.login")
    )