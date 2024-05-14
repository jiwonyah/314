from flask import Blueprint, render_template, g, jsonify
from csit314.entity.Favourite import Favourite
from csit314.entity.User import User, Role
bp = Blueprint('view_saved_favourite_controller', __name__, template_folder='boundary/templates')

@bp.route('/shortlisted')
def view_my_favourites_index():
    if not g.user:
        return jsonify(success=False,
                       error='Login required to view old property listing'), 401
    elif g.user.role != Role.BUYER:
        return jsonify(success=False,
                       error='You are not authorized to view old property listings'), 403
    #favourites = Favourite.query.filter_by(user_userid=g.user.userid).order_by(desc(Favourite.create_date)).all()
    favourites = Favourite.displayShortlist()
    return render_template('favourite/viewSavedFavouriteBoundary.html', favourites=favourites)

@bp.route('/api/shortlisted')
def view_my_favourites():
    if not g.user:
        return jsonify(success=False,
                       error='You need to login as buyer if you want your shortlists.'), 401
    elif g.user.role != Role.BUYER:
        return jsonify(success=False,
                       error='You are not authorized to make and view shortlists.'), 403
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
