import logging

logger = logging.getLogger("AstraHaven.audit")


def record_event(actor, action, resource):
    logger.info("actor=%s action=%s resource=%s", actor, action, resource)
