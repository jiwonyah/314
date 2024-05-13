from flask import Blueprint, render_template, request, url_for, g, flash, jsonify
from csit314.controller.propertyListing.AgentCreatePropertyListingController import PropertyListingForm
from csit314.app import db
from csit314.entity.PropertyListing import PropertyListing
from werkzeug.utils import redirect
from csit314.controller.role_service.decorators import login_required, agent_only
from datetime import datetime
from csit314.entity.User import User, Role


bp = Blueprint('viewOldPropertyListings', __name__, template_folder='boundary/templates')

@bp.route('/oldPropertyListing')
def view_old_property_listings_index():
    if not g.user:
        return jsonify(success=False,
                       error='Login required to view old property listing'), 401
    elif g.user.role != Role.BUYER:
        return jsonify(success=False,
                       error='You are not authorized to view old property listings'), 403
    else:
        return render_template('old_property_listing/oldPropertyListingTable.html')

@bp.route('/api/oldPropertyListing')
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

