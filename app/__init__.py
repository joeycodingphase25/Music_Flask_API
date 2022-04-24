from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

login = LoginManager(app)
login.login_view = 'auth.login'
login.login_message_category = 'danger'

CORS(app)


from app.blueprints.api import api
app.register_blueprint(api)


# This feature is disabled since the purpose of this flask application is
# to be a Back-end api for my react-music-application

# from app import routes