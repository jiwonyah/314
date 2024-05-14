from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__, template_folder=('boundary/templates'))
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)

    #import statements
    from csit314.Controller.UserAccount import (CreateUserAccountController, UpdateUserAccountController,
                                                ViewUserAccountController, AccountDashboardController,
                                                SearchUserAccountController, SuspendUserAccountController)
    from csit314.Controller.UserProfile import (ProfileDashboardController, CreateUserProfileController,
                                                ViewUserProfileController, UpdateUserProfileController,
                                                SearchUserProfileController, SuspendUserProfileController)
    from csit314.Controller.UserProfile import create_profile_controller

    #registering of blueprints
    app.register_blueprint(AccountDashboardController.bp)
    app.register_blueprint(CreateUserAccountController.bp)
    app.register_blueprint(ViewUserAccountController.bp)
    app.register_blueprint(UpdateUserAccountController.bp)
    app.register_blueprint(SearchUserAccountController.bp)
    app.register_blueprint(SuspendUserAccountController.bp)

    app.register_blueprint(ProfileDashboardController.bp)
    app.register_blueprint(create_profile_controller)
    app.register_blueprint(ViewUserProfileController.bp)
    app.register_blueprint(UpdateUserProfileController.bp)
    app.register_blueprint(SearchUserProfileController.bp)
    app.register_blueprint(SuspendUserProfileController.bp)

    @app.route('/')
    def adminHomePage():
        return render_template('AdminHomePage.html')

    return app
