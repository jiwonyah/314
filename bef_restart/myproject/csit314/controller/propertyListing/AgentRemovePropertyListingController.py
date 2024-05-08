from flask import Blueprint, render_template, request, url_for, g, flash
from csit314.controller.authentication.LoginController import login_required, agent_only
from csit314.app import db
from csit314.entity.PropertyListing import PropertyListing
from werkzeug.utils import redirect

bp = Blueprint('removePropertyListing', __name__, template_folder='boundary/templates')

@bp.route('/propertyListing/remove/<int:propertyListing_id>/')
@login_required
def removePropertyListing(propertyListing_id):
    propertyListing = PropertyListing.query.get(propertyListing_id)
    if g.user != propertyListing.agent:
        return render_template('error/error.html',
                               message='You don\'t have authority to remove the post.'), 404
    db.session.delete(propertyListing)
    db.session.commit()
    return redirect(url_for('viewPropertyListing.index'))