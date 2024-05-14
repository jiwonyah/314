from flask import Blueprint, render_template, request, g, jsonify
from .AgentCreatePropertyListingController import PropertyListingForm
from csit314.entity.PropertyListing import PropertyListing
from werkzeug.utils import redirect
from csit314.controller.role_service.decorators import login_required, agent_only
from datetime import datetime
from wtforms import StringField, IntegerField, SelectField, TextAreaField, BooleanField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from csit314.entity.PropertyListing import PropertyListing, FloorLevel, PropertyType, Furnishing, PropertyImage

bp = Blueprint('editPropertyListing', __name__, template_folder='boundary/templates')

@bp.route('/propertyListing/edit/<int:propertyListing_id>/') #methods=['GET']
def index(propertyListing_id):
    propertyListing = PropertyListing.query.get(propertyListing_id)
    if g.user != propertyListing.agent:
        return render_template('error/error.html',
                               message='You don\'t have authority to edit the post.'), 404
    else:
        form = PropertyListingForm(obj=propertyListing)
        return render_template('property_listing/propertyListingEditForm.html', form=form)

@bp.route('/propertyListing/edit/<int:propertyListing_id>/', methods=['POST'])
@login_required
def editPropertyListing(propertyListing_id):
    propertyListing = PropertyListing.query.get(propertyListing_id)
    if not propertyListing:
        return jsonify({'success': False, 'error': 'Property listing not found'}), 404
    form = PropertyListingForm(request.form)
    details = {
        'id': propertyListing_id,
        'subject': form.subject.data,
        'content': form.content.data,
        'price': form.price.data,
        'address': form.address.data,
        'floorSize': form.floorSize.data,
        'floorLevel': form.floorLevel.data,
        'propertyType': form.propertyType.data,
        'furnishing': form.furnishing.data,
        'builtYear': form.builtYear.data,
        'is_sold': form.is_sold.data,
        'client_id': form.client_id.data,
        'modify_date': datetime.now()
    }
    success = PropertyListing.editPropertyListing(details)
    if success:
        return jsonify({'success': True, 'message': 'Property listing updated successfully'})
    else:
        return jsonify({'success': False, 'message': 'Failed to update the changes.'})
        # try:
        #     PropertyListing.validate_client_id(details['client_id'])
        # except ValueError as e:
        #     return jsonify({'success': False, 'error': str(e)}), 400




