# main.py

from flask import Flask
from app.routes_flask import routes
from app.models import db
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

from fastapi.middleware.wsgi import WSGIMiddleware
from api_fastapi import api

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(routes)

# Mount Flask app inside FastAPI
api.mount("/flask", WSGIMiddleware(app))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    import uvicorn
    uvicorn.run(api, host="127.0.0.1", port=8000)
