from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import db, create_tables
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .main import main
    from .authentication import auth

    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    create_tables(app)

    return app
