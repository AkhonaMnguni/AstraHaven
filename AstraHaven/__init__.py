from flask import Flask

from config import Config
from .extensions import csrf, db, limiter, login_manager
from .models import User


def create_app(config_class=Config):
    """Create the Flask app, attach extensions, register routes, and initialize the database."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    csrf.init_app(app)
    limiter.init_app(app)

    @app.after_request
    def add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; img-src 'self' data:;"
        )
        return response

    from .admin.routes import admin_bp
    from .alerts.routes import alerts_bp
    from .auth.routes import auth_bp
    from .dashboard.routes import dashboard_bp
    from .suppliers.routes import suppliers_bp
    from .transactions.routes import transactions_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(suppliers_bp)
    app.register_blueprint(alerts_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()

    return app


@login_manager.user_loader
def load_user(user_id):
    """Look up the logged-in user from the current session identifier."""
    return db.session.get(User, int(user_id))

