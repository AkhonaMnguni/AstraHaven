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

from flask import abort, redirect, request, session, url_for


ROLES = {
    "OWNER",
    "ADMIN",
    "AUDITOR",
    "MANAGER",
    "ANALYST",
}


def current_user_id():
    """Return the current authenticated user id from the session."""
    return session.get("user_id")


def login_required(view):
    """Decorator that redirects unauthenticated users to the login page."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user_id():
            return redirect(url_for("auth.login", next=request.path))

        return view(*args, **kwargs)

    return wrapped


def roles_required(*allowed_roles):
    """Decorator that only allows users whose role is in the permitted set."""
    invalid = set(allowed_roles) - ROLES

    if invalid:
        raise ValueError(f"Unknown roles: {invalid}")

    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user_id():
                return redirect(url_for("auth.login", next=request.path))

            if (session.get("role") or "").upper() not in {role.upper() for role in allowed_roles}:
                return abort(403)

            return view(*args, **kwargs)

        return wrapped

    return decorator


def is_owner():
    """Check whether the current user holds the owner role."""
    return (session.get("role") or "").upper() == "OWNER"


def is_admin():
    """Check whether the current user is an owner or administrator."""
    return (session.get("role") or "").upper() in {"OWNER", "ADMIN"}

