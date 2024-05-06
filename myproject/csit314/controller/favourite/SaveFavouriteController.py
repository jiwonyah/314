from flask import Blueprint, request, jsonify, g
from datetime import datetime
from csit314.app import db
from csit314.entity.Favourite import Favourite
from sqlalchemy.exc import SQLAlchemyError
from csit314.controller.favourite.SellerViewSaveCountController import update_shortlist_count
#from csit314.controller.authentication.LoginController import login_required

bp = Blueprint('save_favourite_controller', __name__, template_folder='boundary/templates')

@bp.route('/toggle_favourite/<int:propertyListing_id>', methods=['POST'])
def toggle_favourite(propertyListing_id):
    # If g.user is not set, it is considered that the user is not logged in.
    if not g.user:
        return jsonify({'success': False, 'error': 'Authentication required'}), 401

    user_id = g.user.userid  # Get user_id from g.user

    try:
        # Check if is is already added into shortlist
        favourite = Favourite.query.filter_by(user_userid=user_id, propertyListing_id=propertyListing_id).first()

        if favourite:
            # Delete from shortlist
            db.session.delete(favourite)
            db.session.commit()
            update_shortlist_count() # Count shortlisted count
            return jsonify({'success': True})
        else:
            # Add to shortlist
            new_favourite = Favourite(user_userid=user_id, propertyListing_id=propertyListing_id,
                                      create_date=datetime.now())
            db.session.add(new_favourite)
            db.session.commit()
            update_shortlist_count()  # Count shortlisted count
            return jsonify({'success': True})

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Database error: ' + str(e)}), 500

