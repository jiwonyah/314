from flask import Blueprint, jsonify, g
from csit314.app import db
from csit314.entity.Favourite import Favourite
from sqlalchemy.exc import SQLAlchemyError
from csit314.controller.favourite import seller_view_save_count_controller
from csit314.controller.role_service.decorators import suspended, login_required, buyer_only


class BuyerSavePropertyListingController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule("/toggle_favourite/<int:propertyListing_id>", view_func=self.toggle_favourite, methods=['POST'])
        self.add_url_rule("/get_favourites", view_func=self.get_favourites,
                          methods=['GET'])

    @login_required
    @buyer_only
    @suspended
    def toggle_favourite(self, propertyListing_id):
        user_id = g.user.userid  # Get user_id from g.user

        try:
            # Check if is already added into shortlist
            favourite = Favourite.query.filter_by(user_userid=user_id, propertyListing_id=propertyListing_id).first()

            if favourite:
                # Delete from shortlist
                successBool = Favourite.removeShortlist(propertyListing_id=propertyListing_id, user_userid=user_id)
                seller_view_save_count_controller.update_shortlist_count()  # Count shortlisted count
                return jsonify({'success': successBool})
            else:
                # Add to shortlist
                successBool = Favourite.createPropertyShortlist(propertyListing_id=propertyListing_id, user_userid=user_id)
                seller_view_save_count_controller.update_shortlist_count()  # Count shortlisted count
                return jsonify({'success': successBool})

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': 'Database error: ' + str(e)}), 500

    def get_favourites(self):
        user_id = g.user.userid
        favourites = Favourite.query.filter_by(user_userid=user_id).all()
        favourite_ids = [f.propertyListing_id for f in favourites]
        return jsonify({'favourites': favourite_ids})

