from flask import Blueprint, g, jsonify
from csit314.entity.PropertyListing import PropertyListing

bp = Blueprint('removePropertyListing', __name__, template_folder='boundary/templates')


@bp.route('/propertyListing/remove/<int:listing_id>/', methods=['DELETE'])
def remove_property_listing(listing_id):
    if not g.user:
        return jsonify(success=False,
                       message='Login required to delete property listing'), 401
    property_listing = PropertyListing.query.get(listing_id)
    if not property_listing:
        return jsonify(success=False, message='Property listing not found'), 404
    if g.user.id != property_listing.agent_id:
        return jsonify(success=False, message='You are not authorized to delete this property listing'), 403
    PropertyListing.removePropertyListing(listing_id)
    return jsonify(success=True, message='Property listing successfully removed.'), 200
