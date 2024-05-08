from flask import Blueprint, render_template, g, jsonify
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from csit314.entity.Favourite import Favourite
from csit314.app import db
from sqlalchemy import desc

bp = Blueprint('view_saved_favourite_controller', __name__, template_folder='boundary/templates')

@bp.route('/shortlisted')
def view_my_favourites():
    # 현재 사용자의 userid와 일치하는 즐겨찾기를 created_date 내림차순으로 조회
    favourites = Favourite.query.filter_by(user_userid=g.user.userid).order_by(desc(Favourite.create_date)).all()
    favourite_listings = [f.propertyListing for f in favourites]
    return render_template('viewSavedFavouriteBoundary.html', favourite_listings=favourite_listings)
