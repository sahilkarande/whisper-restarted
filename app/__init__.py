from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # App configuration
    app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a strong secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:your_mysql_password@localhost/neuroAI_user_system'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Set login route
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'

    # Import and register blueprints or routes
    from .routes import main
    app.register_blueprint(main)

    return app
