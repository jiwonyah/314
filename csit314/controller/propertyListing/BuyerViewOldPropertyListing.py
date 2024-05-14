from flask import Blueprint, render_template, g, jsonify
from csit314.entity.PropertyListing import PropertyListing
from csit314.entity.UserAccount import UserAccount    #, Role
from csit314.controller.role_service.decorators import login_required, buyer_only

bp = Blueprint('viewOldPropertyListings', __name__, template_folder='boundary/templates')

@bp.route('/oldPropertyListing')
@login_required
@buyer_only
def view_old_property_listings_index():
    return render_template('old_property_listing/oldPropertyListingTable.html')

@bp.route('/api/oldPropertyListing')
@login_required
@buyer_only
def view_old_property_listings():
    old_property_listings = PropertyListing.displayAllSoldPropertyListing()
    old_property_listing_data = [
        {
            'subject': listing.subject,
            'create_date': listing.create_date.strftime('%Y-%m-%d %H:%M:%S'),
            'agent_id': listing.agent_id,
            'is_sold': listing.is_sold,
            'id': listing.id,
            'modify_date': listing.modify_date.strftime('%Y-%m-%d') if listing.modify_date else None
        } for listing in old_property_listings
    ]
    return jsonify(old_property_listings=old_property_listing_data)

