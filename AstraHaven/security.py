# from functools import wraps
#
# from flask import abort
# from flask_login import current_user
#
#
# def roles_required(*roles):
#     def decorator(view):
#         @wraps(view)
#         def wrapped(*args, **kwargs):
#             if not current_user.is_authenticated:
#                 abort(401)
#             if current_user.role not in roles:
#                 abort(403)
#             return view(*args, **kwargs)
#
#         return wrapped
#
#     return decorator



from functools import wraps

from flask import abort, session


ROLES = {
    "OWNER",
    "ADMIN",
    "AUDITOR",
    "MANAGER",
    "ANALYST",
}


def current_user_id():
    return session.get("user_id")


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user_id():
            return abort(401)

        return view(*args, **kwargs)

    return wrapped


def roles_required(*allowed_roles):
    invalid = set(allowed_roles) - ROLES

    if invalid:
        raise ValueError(
            f"Unknown roles: {invalid}"
        )

    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user_id():
                return abort(401)

            if session.get("role") not in allowed_roles:
                return abort(403)

            return view(*args, **kwargs)

        return wrapped

    return decorator


def is_owner():
    return session.get("role") == "OWNER"


def is_admin():
    return session.get("role") in {
        "OWNER",
        "ADMIN",
    }

