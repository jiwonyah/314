from flask import Blueprint, render_template, request, url_for, g, flash
from csit314.controller.propertyListing.AgentCreatePropertyListingController import PropertyListingForm
from csit314.app import db
from csit314.entity.PropertyListing import PropertyListing
from werkzeug.utils import redirect
from csit314.controller.authentication.LoginController import login_required, agent_only
from datetime import datetime

bp = Blueprint('editPropertyListing', __name__, template_folder='boundary/templates')

@bp.route('/propertyListing/edit/<int:propertyListing_id>/', methods=('GET', 'POST'))
@login_required
def editPropertyListing(propertyListing_id):
    propertyListing = PropertyListing.query.get(propertyListing_id)

    if g.user != propertyListing.agent:
        return render_template('error/error.html',
                               message='You don\'t have authority to edit the post.'), 404

    if request.method == 'POST':
        form = PropertyListingForm()
        if form.validate_on_submit():
            form.populate_obj(propertyListing)
            propertyListing.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('viewPropertyListing.detail', propertyListing_id=propertyListing_id))
    else:
        form = PropertyListingForm(obj=propertyListing)
    return render_template('property_listing/propertyListingCreatingForm.html', form=form)



