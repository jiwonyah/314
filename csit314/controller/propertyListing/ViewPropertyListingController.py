from flask import Blueprint, render_template
from csit314.entity.PropertyListing import PropertyListing
from csit314.app import db
from csit314.controller.role_service.decorators import login_required, agent_only, seller_only
from flask import Blueprint, render_template, request, url_for, g, jsonify
from csit314.entity.User import User
from functools import wraps

bp = Blueprint('viewPropertyListing', __name__, template_folder='boundary/templates')

@bp.route('/propertyListing/')
def index():
    propertyListing_table = PropertyListing.query.order_by(PropertyListing.create_date.desc())
    return render_template('property_listing/propertyListingTable.html',
                           propertyListing_table=propertyListing_table)

@bp.route('/propertyListing/detail/<int:propertyListing_id>/')
def detail(propertyListing_id):
    propertyListing = PropertyListing.query.get(propertyListing_id)

    propertyListing.view_counts += 1
    db.session.commit()
    return render_template('property_listing/propertyListingDetailPage.html',
                           propertyListing=propertyListing)


# ----------------------------------private pages-------------------------------------
# 이 페이지는 인증된 유저 본인만 접속할 수 있는 페이지이다.

@bp.route('/agent/history/')
@login_required
@agent_only
def viewPropertyListingHistory():
    agent_id = g.user.id
    agent_listings = PropertyListing.query.filter_by(agent_id=agent_id).all()
    return render_template('property_listing/private_page/AgentPropertyListingHistoryPage.html',
                           agent_listings=agent_listings)

@bp.route('/seller/my_property_listing/')
@login_required
@seller_only
def sellerViewOwnPropertyListing():
    client_id = g.user.userid
    propertylistings = PropertyListing.query.filter_by(client_id=client_id).all()
    return render_template('property_listing/private_page/SellerPropertyListingPage.html',
                           propertylistings=propertylistings)

