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
