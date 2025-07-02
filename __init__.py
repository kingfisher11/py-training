from dotenv import load_dotenv
load_dotenv()
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_migrate import Migrate

import psycopg2
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

    # Database config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@127.0.0.1/edums_hep'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize DB
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from einvoicing.user.views import user
    from einvoicing.invoice.views import invoice
    from einvoicing.student.views import student

    app.register_blueprint(user, url_prefix='/usr')
    app.register_blueprint(invoice, url_prefix='/inv')
    app.register_blueprint(student, url_prefix='/std')
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max 16MB

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # DB test route
    @app.route("/test-db")
    def test_db_connection():
        try:
            db.session.execute(text('SELECT 1'))
            return "Database connected successfully!"
        except Exception as e:
            return f"Database connection failed: {str(e)}"

    return app