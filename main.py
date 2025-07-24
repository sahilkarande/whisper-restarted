from flask import Flask
from fastapi.middleware.wsgi import WSGIMiddleware
from api_fastapi import api  # This is your FastAPI app

from app.routes_flask import routes  # Flask routes
from app.models import db  # SQLAlchemy db object
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL DB Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB and register Flask blueprint
db.init_app(app)
app.register_blueprint(routes)

# Mount Flask app under FastAPI route
api.mount("/flask", WSGIMiddleware(app))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don’t exist
    import uvicorn
    uvicorn.run(api, host="127.0.0.1", port=8000)

