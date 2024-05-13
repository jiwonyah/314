from flask import Blueprint, render_template, g, jsonify
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from csit314.entity.Favourite import Favourite
from csit314.app import db
from sqlalchemy import desc

bp = Blueprint('view_saved_favourite_controller', __name__, template_folder='boundary/templates')

@bp.route('/shortlisted')
def view_my_favourites_index():
    favourites = Favourite.query.filter_by(user_userid=g.user.userid).order_by(desc(Favourite.create_date)).all()
    return render_template('favourite/viewSavedFavouriteBoundary.html', favourites=favourites)

@bp.route('/api/shortlisted')
def view_my_favourites():
    # View created_date favorites that match the userid of the current user in descending order
    favourites = Favourite.query.filter_by(user_userid=g.user.userid).order_by(desc(Favourite.create_date)).all()
    favourite_listings = [
        {
            'id': f.propertyListing.id,
            'subject': f.propertyListing.subject,
            'create_date': f.create_date.strftime('%Y-%m-%d')
        } for f in favourites
    ]
    return jsonify(favourite_listings)