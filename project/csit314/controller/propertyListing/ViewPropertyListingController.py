from flask import Blueprint, render_template
from csit314.entity.PropertyListing import PropertyListing
from csit314.app import db

bp = Blueprint('viewPropertyListing', __name__, template_folder='boundary/templates')

@bp.route('/propertyListing/')
def index():
    propertyListing_table = PropertyListing.query.order_by(PropertyListing.create_date.desc())
    return render_template('propertyListingTable.html',
                           propertyListing_table=propertyListing_table)

@bp.route('/detail/<int:propertyListing_id>/')
def detail(propertyListing_id):
    propertyListing = PropertyListing.query.get(propertyListing_id)
    return render_template('propertyListingDetailPage.html',
                           propertyListing=propertyListing)