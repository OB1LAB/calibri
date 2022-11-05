from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
api = Api(app)
jwt._set_error_handler_callbacks(app)
CORS(app, supports_credentials=True)

from app import routes, models
