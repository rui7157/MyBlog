from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
import logging
import logging.config
toolbar = DebugToolbarExtension()
loginManager = LoginManager()
csrf = CsrfProtect()
db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    from config import Configuration
    logging.config.fileConfig(Configuration.LOGGING_CONFIG_PATH)
    app.config.from_object(Configuration)
    db.init_app(app)
    csrf.init_app(app)
    loginManager.init_app(app)
    toolbar.init_app(app)
    from .blog import main
    app.register_blueprint(main)
    from .admin import adm
    app.register_blueprint(adm, url_prefix="/adm")
    return app
