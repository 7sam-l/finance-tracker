import os
from flask import Flask
from flask_cors import CORS
from .extensions import db, migrate


def create_app(config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL") or "sqlite:///finance.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"] = False

    if config:
        app.config.update(config)

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.transactions import bp as transactions_bp
    from .routes.categories import bp as categories_bp
    from .routes.summary import bp as summary_bp
    from .routes.categorize import bp as categorize_bp
    from .routes.forecast import bp as forecast_bp
    from .routes.analytics import bp as analytics_bp

    app.register_blueprint(transactions_bp, url_prefix="/api/transactions")
    app.register_blueprint(categories_bp, url_prefix="/api/categories")
    app.register_blueprint(summary_bp, url_prefix="/api/summary")
    app.register_blueprint(categorize_bp, url_prefix="/api/categorize")
    app.register_blueprint(forecast_bp, url_prefix="/api/forecast")
    app.register_blueprint(analytics_bp, url_prefix="/api/analytics")

    return app
