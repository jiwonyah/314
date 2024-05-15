from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import config
from sqlalchemy import MetaData
from flask_jwt_extended import JWTManager
import json
from enum import Enum


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
    app.config['UPLOAD_FOLDER'] = 'csit314/boundary/static/images/property_listings/'
    app.config.from_object(config)
    app.config['SECRET_KEY'] = '1q2w3e4r!'
    app.config['JWT_SECRET_KEY'] = 'csit314'

    # Load app configuration from config.py
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS

    # class CustomJSONEncoder(json.JSONEncoder):
    #     def default(self, obj):
    #         if isinstance(obj, Enum):
    #             return obj.value
    #         return super().default(obj)
    #
    # app.json_encoder = CustomJSONEncoder

    # ORM
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    # Blueprint
    from csit314.controller.authentication import (SignUpController, LoginController, LogoutController)
    from csit314.controller.profile import ViewProfileController
    from csit314.controller.review import (AgentViewReviewController, BuyerSellerWriteReviewController)
    from csit314.controller.favourite import (SaveFavouriteController, ViewSavedFavouriteController)
    from csit314.controller.mortgage import BuyerCalculateMortgageController

    app.register_blueprint(SignUpController.bp)
    app.register_blueprint(LoginController.bp)
    app.register_blueprint(LogoutController.bp)
    app.register_blueprint(ViewProfileController.bp)
    app.register_blueprint(AgentViewReviewController.bp)
    app.register_blueprint(BuyerSellerWriteReviewController.bp)
    app.register_blueprint(SaveFavouriteController.bp)
    app.register_blueprint(ViewSavedFavouriteController.bp)
    app.register_blueprint(BuyerCalculateMortgageController.bp)

#-----------------------------------------------------------------------------------
    # NEW STRUCTURE
    from csit314.controller.propertyListing import (agent_create_property_listing_controller,
                                                    agent_edit_property_listing_controller,
                                                    agent_remove_property_listing_controller,
                                                    view_property_listing_controller,
                                                    buyer_view_old_property_listing_controller,
                                                    search_property_listing_controller)

    from csit314.controller.admin.UserAccount import (create_account_controller, update_account_controller,
                                                      view_account_controller, search_account_controller,
                                                      suspend_account_controller, AccountDashboardController)
    from csit314.controller.admin.UserProfile import (create_profile_controller, update_profile_controller,
                                                      view_profile_controller, search_profile_controller,
                                                      suspend_profile_controller, ProfileDashboardController)

    #Property Listing
    app.register_blueprint(agent_create_property_listing_controller)
    app.register_blueprint(agent_edit_property_listing_controller)
    app.register_blueprint(agent_remove_property_listing_controller)
    app.register_blueprint(view_property_listing_controller)
    app.register_blueprint(buyer_view_old_property_listing_controller)
    app.register_blueprint(search_property_listing_controller)

    #Admin Home
    from csit314.controller.admin.UserAccount import AdminHomePageController
    app.register_blueprint(AdminHomePageController.bp)

    #UserAccount
    app.register_blueprint(AccountDashboardController.bp)
    app.register_blueprint(create_account_controller)
    app.register_blueprint(view_account_controller)
    app.register_blueprint(update_account_controller)
    app.register_blueprint(search_account_controller)
    app.register_blueprint(suspend_account_controller)

    #UserProfile
    app.register_blueprint(ProfileDashboardController.bp)
    app.register_blueprint(create_profile_controller)
    app.register_blueprint(view_profile_controller)
    app.register_blueprint(update_profile_controller)
    app.register_blueprint(search_profile_controller)
    app.register_blueprint(suspend_profile_controller)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app



