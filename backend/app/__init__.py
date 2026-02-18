from flask import Flask
from flask_cors import CORS
from .extensions import db, migrate


def create_app(config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///finance.db"
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

    app.register_blueprint(transactions_bp, url_prefix="/api/transactions")
    app.register_blueprint(categories_bp, url_prefix="/api/categories")
    app.register_blueprint(summary_bp, url_prefix="/api/summary")

    return app
