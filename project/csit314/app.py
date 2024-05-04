from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__,
                static_folder='boundary/static',
                template_folder='boundary/templates')
    app.config.from_object(config)
    app.config['SECRET_KEY'] = '1q2w3e4r!'

    # Load app configuration from config.py
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from csit314.entity import PropertyListing, User

    # Blueprint
    from csit314.controller.authentication import (SignUpController, ViewPropertyListingController,
                                                   LoginController, LogoutController)
    app.register_blueprint(SignUpController.bp)
    app.register_blueprint(ViewPropertyListingController.bp)
    app.register_blueprint(LoginController.bp)
    app.register_blueprint(LogoutController.bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app



