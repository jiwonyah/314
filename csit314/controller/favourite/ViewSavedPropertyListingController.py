from flask import Blueprint, render_template, g, jsonify
from csit314.entity.Favourite import Favourite


bp = Blueprint('view_saved_favourite_controller', __name__, template_folder='boundary/templates')

class ViewSavedPropertyListingController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule("/shortlisted", view_func=self.view_my_favourites_index, methods=['GET'])
        self.add_url_rule("/api/shortlisted", view_func=self.view_my_favourites,
                          methods=['GET'])

    @bp.route('/shortlisted')
    def view_my_favourites_index(self):
        if not g.user:
            return render_template('error/error.html',
                                    message='You need to login as buyer if you want to view your shortlists.'), 401
        if g.user.role != 'buyer':
            return render_template('error/error.html',
                                   message='Only buyers can make and view shortlists.'), 403
        if g.user.status == "Suspended":
            return render_template('error/error.html',
                                   message='Your account is suspended.'
                                           'Send Active Request to Administrator.'
                                           'admin@minyong.com'), 403
        favourites = Favourite.displayShortlist()
        return render_template('favourite/viewSavedFavouriteBoundary.html', favourites=favourites)

    @bp.route('/api/shortlisted')
    def view_my_favourites(self):
        if not g.user:
            return render_template('error/error.html',
                                    message='You need to login as buyer if you want to view your shortlists.'), 401
        if g.user.role != 'buyer':
            return render_template('error/error.html',
                                   message='Only buyers can make and view shortlists.'), 403
        if g.user.status == "Suspended":
            return render_template('error/error.html',
                                   message='Your account is suspended.'
                                           'Send Active Request to Administrator.'
                                           'admin@minyong.com'), 403
        favourites = Favourite.displayShortlist()
        favourite_listings = [
            {
                'id': f.propertyListing.id,
                'subject': f.propertyListing.subject,
                'create_date': f.create_date.strftime('%Y-%m-%d')
            } for f in favourites
        ]
        return jsonify(favourite_listings)

