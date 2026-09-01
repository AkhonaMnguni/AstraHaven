# from flask import Blueprint, render_template
# from flask_login import login_required
#
# from ..models import Alert, Transaction
#
# dashboard_bp = Blueprint("dashboard", __name__)
#
#
# @dashboard_bp.route("/")
# @login_required
# def index():
#     return render_template(
#         "dashboard.html",
#         transaction_count=Transaction.query.count(),
#         open_alerts=Alert.query.filter_by(resolved=False).count(),
#         recent_transactions=Transaction.query.order_by(Transaction.created_at.desc()).limit(5).all(),
#     )


from flask import (
    Blueprint,
    render_template,
)

from sqlalchemy import func

from ..extensions import db
from ..models import Alert, Transaction
from ..security import login_required


dashboard_bp = Blueprint(
    "dashboard",
    __name__,
)


@dashboard_bp.get("/")
@login_required
def index():
    """Summarize key exposure metrics such as transaction totals, open alerts, and recent activity."""
    total_transactions = db.session.scalar(
        db.select(
            func.count(Transaction.id)
        )
    ) or 0

    total_value = db.session.scalar(
        db.select(
            func.coalesce(
                func.sum(Transaction.amount),
                0,
            )
        )
    )

    open_alerts = db.session.scalar(
        db.select(
            func.count(Alert.id)
        ).where(
            Alert.status == "OPEN"
        )
    ) or 0

    high_alerts = db.session.scalar(
        db.select(
            func.count(Alert.id)
        ).where(
            Alert.severity.in_(
                ["HIGH", "CRITICAL"]
            ),
            Alert.status == "OPEN",
        )
    ) or 0

    recent_alerts = db.session.scalars(
        db.select(Alert)
        .order_by(
            Alert.created_at.desc()
        )
        .limit(10)
    ).all()

    return render_template(
        "dashboard.html",
        total_transactions=total_transactions,
        total_value=total_value,
        open_alerts=open_alerts,
        high_alerts=high_alerts,
        recent_alerts=recent_alerts,
    )

