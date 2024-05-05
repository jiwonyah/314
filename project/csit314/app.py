from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import config
from sqlalchemy import MetaData

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
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
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    # Blueprint
    from csit314.controller.authentication import (SignUpController, LoginController, LogoutController)
    from csit314.controller.propertyListing import ViewPropertyListingController, AgentCreatePropertyListing
    app.register_blueprint(SignUpController.bp)
    app.register_blueprint(ViewPropertyListingController.bp)
    app.register_blueprint(AgentCreatePropertyListing.bp)
    app.register_blueprint(LoginController.bp)
    app.register_blueprint(LogoutController.bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app



