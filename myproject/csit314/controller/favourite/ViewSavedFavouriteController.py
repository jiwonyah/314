from flask import Blueprint, render_template, g, redirect, url_for, request, flash
from csit314.entity.Review import Review
from csit314.entity.Favourite import Favourite
from csit314.entity.PropertyListing import PropertyListing
from csit314.entity.User import User, Role
from csit314.app import db
from csit314.controller.authentication.LoginController import login_required

bp = Blueprint('view_saved_favourite_controller', __name__, template_folder='boundary/templates')

# 즐겨찾기 목록 조회 함수 예시
@bp.route('/shortlisted')
@login_required
def view_my_favourites():
    favourites = Favourite.query.filter_by(user_userid=g.user.userid).all()
    favourite_listings = [f.property_listing for f in favourites]
    return render_template('viewSavedFavouriteBoundary.html', favourite_listings=favourite_listings)
