from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

import psycopg2
import os

db = SQLAlchemy()
def create_app():
    app = Flask(__name__)

    # Database config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@127.0.0.1/edums_hep'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize DB
    db.init_app(app)

    # Register Blueprints
    from einvoicing.user.views import user
    from einvoicing.invoice.views import invoice

    app.register_blueprint(user, url_prefix='/usr')
    app.register_blueprint(invoice, url_prefix='/inv')

    # DB test route
    @app.route("/test-db")
    def test_db_connection():
        try:
            db.session.execute(text('SELECT 1'))
            return "Database connected successfully!"
        except Exception as e:
            return f"Database connection failed: {str(e)}"

    return app