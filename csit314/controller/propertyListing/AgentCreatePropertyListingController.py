from flask import Blueprint, render_template, request, jsonify, session
from csit314.entity.PropertyListing import PropertyListing, FloorLevel, PropertyType, Furnishing, PropertyImage
from wtforms import StringField, IntegerField, SelectField, TextAreaField, BooleanField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from csit314.controller.role_service.decorators import agent_only
from werkzeug.utils import secure_filename
from csit314.app import db
import os

bp = Blueprint('createPropertyListing', __name__, template_folder='boundary/templates')

class PropertyListingForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    images = FileField('Images', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    content = TextAreaField('Content')
    price = IntegerField('Price', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    floorSize = IntegerField('Floor Size', validators=[DataRequired()])
    floorLevel = SelectField('Floor Level', choices=[
        (FloorLevel.LOW.value, 'Low'),
        (FloorLevel.MEDIUM.value, 'Medium'),
        (FloorLevel.HIGH.value, 'High')
    ], validators=[DataRequired()])
    propertyType = SelectField('Property Type', choices=[
        (PropertyType.HDB.value, 'HDB'),
        (PropertyType.CONDO.value, 'Condo'),
        (PropertyType.APARTMENT.value, 'Apartment'),
        (PropertyType.STUDIO.value, 'Studio')
    ], validators=[DataRequired()])
    furnishing = SelectField('Furnishing', choices=[
        (Furnishing.PartiallyFurnished.value, 'Partially furnished'),
        (Furnishing.FullyFurnished.value, 'Fully furnished'),
        (Furnishing.NotFurnished.value, 'Not furnished')
    ], validators=[DataRequired()])
    builtYear = IntegerField('Built Year', validators=[DataRequired()])
    client_id = StringField('Client',  validators=[DataRequired()])
    is_sold = BooleanField('Is Sold')

@bp.route('/propertyListing/create/')
@agent_only
def index():
    form = PropertyListingForm()
    return render_template('property_listing/propertyListingCreatingForm.html',
                           form=form)

@bp.route('/propertyListing/create/', methods=['POST'])
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

