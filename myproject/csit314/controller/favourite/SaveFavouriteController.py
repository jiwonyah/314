from flask import Blueprint, jsonify, g
from csit314.app import db
from csit314.entity.Favourite import Favourite
from sqlalchemy.exc import SQLAlchemyError
from csit314.controller.favourite.SellerViewSaveCountController import update_shortlist_count

bp = Blueprint('save_favourite_controller', __name__, template_folder='boundary/templates')

@bp.route('/toggle_favourite/<int:propertyListing_id>', methods=['POST'])
def toggle_favourite(propertyListing_id):
    # If g.user is not set, it is considered that the user is not logged in.
    if not g.user:
        return jsonify({'success': False, 'error': 'Authentication required'}), 401

    user_id = g.user.userid  # Get user_id from g.user

    try:
        # Check if is already added into shortlist
        favourite = Favourite.query.filter_by(user_userid=user_id, propertyListing_id=propertyListing_id).first()

        if favourite:
            # Delete from shortlist
            successBool = Favourite.removeShortlist(propertyListing_id=propertyListing_id, user_userid=user_id)
            update_shortlist_count()  # Count shortlisted count
            return jsonify({'success': successBool})
        else:
            # Add to shortlist
            successBool = Favourite.createPropertyShortlist(propertyListing_id=propertyListing_id, user_userid=user_id)
            update_shortlist_count()  # Count shortlisted count
            return jsonify({'success': successBool})

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Database error: ' + str(e)}), 500
