# from flask import Blueprint, flash, redirect, render_template, request, url_for
# from flask_login import current_user, login_user, logout_user
#
# from ..extensions import db
# from ..models import User
#
# auth_bp = Blueprint("auth", __name__)
#
#
# @auth_bp.route("/login", methods=["GET", "POST"])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for("dashboard.index"))
#     if request.method == "POST":
#         user = db.session.scalar(db.select(User).where(User.username == request.form.get("username", "").strip()))
#         if user and user.check_password(request.form.get("password", "")):
#             login_user(user)
#             return redirect(request.args.get("next") or url_for("dashboard.index"))
#         flash("Invalid username or password.", "error")
#     return render_template("login.html")
#
#
# @auth_bp.route("/logout")
# def logout():
#     logout_user()
#     return redirect(url_for("auth.login"))




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
    """Authenticate a user by username or email and create the session on success."""
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


@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    """Clear the active session and record the logout event for auditing."""
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
