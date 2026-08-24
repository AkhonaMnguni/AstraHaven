from flask import Blueprint, render_template
from flask_login import login_required

from ..models import Alert, Transaction

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    return render_template(
        "dashboard.html",
        transaction_count=Transaction.query.count(),
        open_alerts=Alert.query.filter_by(resolved=False).count(),
        recent_transactions=Transaction.query.order_by(Transaction.created_at.desc()).limit(5).all(),
    )
