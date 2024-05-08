from datetime import datetime
from flask import Blueprint, render_template, request, url_for, g
from werkzeug.utils import redirect
from csit314.app import db
from csit314.entity.PropertyListing import PropertyListing, FloorLevel, PropertyType, Furnishing
from wtforms import StringField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from csit314.controller.authentication.LoginController import agent_only


class PropertyListingForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired('Subject is a required field.')])
    content = TextAreaField('Content')
    price = IntegerField('Price', validators=[DataRequired('Price is a required field.')])
    address = StringField('Address', validators=[DataRequired('Address is a required field.')])
    floorSize = IntegerField('Floor Size', validators=[DataRequired('Floor Size is a required field.')])
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
    builtYear = IntegerField('Built Year', validators=[DataRequired('Built year is a required field.')])
    client_id = StringField('Client',  validators=[DataRequired('Client is a required field.')])


bp = Blueprint('createPropertyListing', __name__, template_folder='boundary/templates')


@bp.route('/propertyListing/create/', methods=('GET', 'POST'))
@agent_only
def createPropertyListing():
    form = PropertyListingForm()
    if request.method == 'POST' and form.validate_on_submit():
        propertyListing = PropertyListing(subject=form.subject.data, content=form.content.data,
                                          price=form.price.data, address=form.address.data,
                                          floorSize=form.floorSize.data, floorLevel=form.floorLevel.data,
                                          propertyType=form.propertyType.data,
                                          furnishing=form.furnishing.data, builtYear=form.builtYear.data,
                                          client_id=form.client_id.data, create_date=datetime.now(),
                                          agent=g.user)
        db.session.add(propertyListing)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('property_listing/propertyListingCreatingForm.html',
                           form=form)
