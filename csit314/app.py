import bcrypt
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
    app.config['UPLOAD_FOLDER'] = '/csit314/boundary/static/images/property_listings'
    app.config.from_object(config)
    app.config['SECRET_KEY'] = '1q2w3e4r!'
    # # JWTManager 초기화
    app.config['JWT_SECRET_KEY'] = 'csit314'  # JWT 시크릿 키 설정
    # jwt = JWTManager(app)

    # Load app configuration from config.py
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS

    # with app.app_context():
    #     db.create_all()
    #     admin = User(
    #         userid="admin",
    #         email="jiwon0502@gmail.com",
    #         password="$2y$10$/U0fxuv5TH2liyswZNWsAeLdd4/UgLgE..7XrjAtNk5dpPJ55t8Di",
    #         first_name=None,
    #         last_name=None,
    #         role=Role.ADMIN.value,
    #         status=None
    #     )
    #     db.session.add(admin)
    #     db.session.commit()
    # Enum 객체를 직렬화할 수 있는 커스텀 JSONEncoder 정의
    class CustomJSONEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Enum):
                return obj.value
            return super().default(obj)
    # Flask 애플리케이션에 커스텀 JSONEncoder 설정
    app.json_encoder = CustomJSONEncoder
    jwt = JWTManager(app)

    # ORM
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    # Blueprint
    from csit314.controller.authentication import (SignUpController, LoginController, LogoutController)
    from csit314.controller.propertyListing import (ViewPropertyListingController, AgentCreatePropertyListingController,
                                                    AgentEditPropertyListingController,
                                                    AgentRemovePropertyListingController,
                                                    SearchFilterPropertyListing,
                                                    BuyerViewOldPropertyListing)
    from csit314.controller.profile import ViewProfileController
    from csit314.controller.review import (AgentViewReviewController, BuyerSellerWriteReviewController)
    from csit314.controller.favourite import (SaveFavouriteController, ViewSavedFavouriteController)
    from csit314.controller.mortgage import BuyerCalculateMortgageController
    from csit314.controller.admin import (AdminHomePageController, AccountDashboardController,
                                          CreateUserAccountController, ViewUserAccountController)
    app.register_blueprint(SignUpController.bp)
    app.register_blueprint(ViewPropertyListingController.bp)
    app.register_blueprint(AgentCreatePropertyListingController.bp)
    app.register_blueprint(AgentEditPropertyListingController.bp)
    app.register_blueprint(AgentRemovePropertyListingController.bp)
    app.register_blueprint(LoginController.bp)
    app.register_blueprint(LogoutController.bp)
    app.register_blueprint(ViewProfileController.bp)
    app.register_blueprint(AgentViewReviewController.bp)
    app.register_blueprint(BuyerSellerWriteReviewController.bp)
    app.register_blueprint(SaveFavouriteController.bp)
    app.register_blueprint(ViewSavedFavouriteController.bp)
    app.register_blueprint(SearchFilterPropertyListing.bp)
    app.register_blueprint(BuyerCalculateMortgageController.bp)
    app.register_blueprint(BuyerViewOldPropertyListing.bp)
    app.register_blueprint(AdminHomePageController.bp)
    app.register_blueprint(AccountDashboardController.bp)
    app.register_blueprint(CreateUserAccountController.bp)
    app.register_blueprint(ViewUserAccountController.bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app



