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
    propertyListing = PropertyListing.query.get_or_404(propertyListing_id)

    if g.user != propertyListing.user:
        #flash('You don\'t have authority to edit the post.')
        # return redirect(url_for('viewPropertyListing.index',
        #                         propertyListing_id=propertyListing_id))
        return render_template("NoAuthorityEditPropertyListing.html")

    if request.method == 'POST':
        form = PropertyListingForm()
        if form.validate_on_submit():
            form.populate_obj(propertyListing)
            propertyListing.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('viewPropertyListing.detail', propertyListing_id=propertyListing_id))
    else:
        form = PropertyListingForm(obj=propertyListing)
    return render_template('propertyListingCreatingForm.html', form=form)