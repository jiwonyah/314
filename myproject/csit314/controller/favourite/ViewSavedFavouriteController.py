from flask import Blueprint, render_template, g
from csit314.entity.Favourite import Favourite
from sqlalchemy import desc

bp = Blueprint('view_saved_favourite_controller', __name__, template_folder='boundary/templates')

@bp.route('/shortlisted')
def view_my_favourites():
    # Retrieve the favorites that match the current user's userid, ordered by created_date in descending order.
    favourites = Favourite.query.filter_by(user_userid=g.user.userid).order_by(desc(Favourite.create_date)).all()
    favourite_listings = [f.propertyListing for f in favourites]
    return render_template('viewSavedFavouriteBoundary.html', favourite_listings=favourite_listings)
