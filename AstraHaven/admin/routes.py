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
