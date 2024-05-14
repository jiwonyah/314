from flask import Blueprint, render_template, jsonify

from csit314.controller.role_service.decorators import buyer_only
from csit314.entity.Favourite import Favourite

bp = Blueprint('view_saved_favourite_controller', __name__, template_folder='boundary/templates')

@buyer_only
@bp.route('/shortlisted')
def view_my_favourites_index():
    #favourites = Favourite.query.filter_by(user_userid=g.user.userid).order_by(desc(Favourite.create_date)).all()
    favourites = Favourite.displayShortlist()
    return render_template('favourite/viewSavedFavouriteBoundary.html', favourites=favourites)
@buyer_only
@bp.route('/api/shortlisted')
def view_my_favourites():
    # View created_date favorites that match the userid of the current user in descending order
    #favourites = Favourite.query.filter_by(user_userid=g.user.userid).order_by(desc(Favourite.create_date)).all()
    favourites = Favourite.displayShortlist()
    favourite_listings = [
        {
            'id': f.propertyListing.id,
            'subject': f.propertyListing.subject,
            'create_date': f.create_date.strftime('%Y-%m-%d')
        } for f in favourites
    ]
    return jsonify(favourite_listings)
