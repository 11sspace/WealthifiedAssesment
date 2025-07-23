from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy


from config import Config

db = SQLAlchemy()
app = Flask(__name__)
rest_api = Api(app, title="Mutual Fund Dashboard")
def create_app():

    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        from .api.dashboard_services import purchase_route
        rest_api.add_namespace(purchase_route)
        db.create_all()

    return app
