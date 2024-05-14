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
    from csit314.Controller.UserAccount import (create_account_controller, update_account_controller,
                                                view_account_controller, search_account_controller,
                                                suspend_account_controller, AccountDashboardController)
    from csit314.Controller.UserProfile import (create_profile_controller, update_profile_controller,
                                                view_profile_controller, search_profile_controller,
                                                suspend_profile_controller, ProfileDashboardController)


    #registering of blueprints
    app.register_blueprint(AccountDashboardController.bp)
    app.register_blueprint(create_account_controller)
    app.register_blueprint(view_account_controller)
    app.register_blueprint(update_account_controller)
    app.register_blueprint(search_account_controller)
    app.register_blueprint(suspend_account_controller)

    app.register_blueprint(ProfileDashboardController.bp)
    app.register_blueprint(create_profile_controller)
    app.register_blueprint(view_profile_controller)
    app.register_blueprint(update_profile_controller)
    app.register_blueprint(search_profile_controller)
    app.register_blueprint(suspend_profile_controller)

    @app.route('/')
    def adminHomePage():
        return render_template('AdminHomePage.html')

    return app
