from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required

from ..extensions import db
from ..models import Alert
from ..security import roles_required

alerts_bp = Blueprint("alerts", __name__, url_prefix="/alerts")


@alerts_bp.route("/")
@login_required
def index():
    return render_template("alerts.html", alerts=Alert.query.order_by(Alert.created_at.desc()).all())


@alerts_bp.route("/<int:alert_id>")
@login_required
def detail(alert_id):
    return render_template("alert_detail.html", alert=db.get_or_404(Alert, alert_id))


@alerts_bp.route("/<int:alert_id>/resolve", methods=["POST"])
@roles_required("admin", "analyst")
def resolve(alert_id):
    alert = db.get_or_404(Alert, alert_id)
    alert.resolved = True
    db.session.commit()
    return redirect(url_for("alerts.detail", alert_id=alert.id))
