from flask import Blueprint, render_template, request, jsonify, session
from csit314.entity.PropertyListing import PropertyListing
from csit314.controller.role_service.decorators import login_required, agent_only
from werkzeug.utils import secure_filename
from .Form.PropertyListingForm import PropertyListingForm
import os

bp = Blueprint('createPropertyListing', __name__, template_folder='boundary/templates')

@bp.route('/propertyListing/create/')
@login_required
@agent_only
def index():
    form = PropertyListingForm()
    return render_template('property_listing/propertyListingCreatingForm.html',
                           form=form)

@bp.route('/propertyListing/create/', methods=['POST'])
@login_required
@agent_only
def createPropertyListing():
    form = PropertyListingForm(request.form)
    details = {
        'subject': form.subject.data,
        'content': request.form['content'],
        'price': request.form['price'],
        'address': request.form['address'],
        'floorSize': request.form['floorSize'],
        'floorLevel': request.form['floorLevel'],
        'propertyType': request.form['propertyType'],
        'furnishing': request.form['furnishing'],
        'builtYear': request.form['builtYear'],
        'client_id': request.form['client_id'],
        'agent_id': session['user_id']
    }
    UPLOAD_FOLDER = 'csit314/boundary/static/images/property_listings'
    image_files = []
    if 'images' in request.files:
        images = request.files.getlist('images')
        for image in images:
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                image.save(filepath)
                image_files.append(filepath)
    success = PropertyListing.createPropertyListing(details, image_files)
    if success:
        return jsonify({'success': True, 'message': 'Property listing created successfully'})
    else:
        try:
            PropertyListing.validate_client_id(details['client_id'])
        except ValueError as e:
            return jsonify({'success': False, 'error': str(e)}), 400


#----------------------------------------------------------------------------------------------------

@bp.errorhandler(ValueError)
def handle_value_error(error):
    return jsonify({'success': False, 'error': str(error)}), 400
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

