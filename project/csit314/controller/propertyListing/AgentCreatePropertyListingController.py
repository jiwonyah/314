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
    subject = StringField('Subject', validators=[DataRequired('Subject은 필수입력 항목입니다.')])
    content = TextAreaField('Content')
    price = IntegerField('Price', validators=[DataRequired('Price은 필수입력 항목입니다.')])
    address = StringField('Address', validators=[DataRequired('Address은 필수입력 항목입니다.')])
    floorSize = IntegerField('Floor Size', validators=[DataRequired('Floor Size는 필수입력 항목입니다.')])
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
    builtYear = IntegerField('Built Year', validators=[DataRequired('Built year는 필수입력 항목입니다.')])



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
                            create_date=datetime.now(), user=g.user)
        db.session.add(propertyListing)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('propertyListingCreatingForm.html', form=form)
