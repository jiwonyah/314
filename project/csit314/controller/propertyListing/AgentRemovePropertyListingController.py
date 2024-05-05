from flask import Blueprint, render_template, request, url_for, g, flash
from csit314.controller.authentication.LoginController import login_required, agent_only
from csit314.app import db
from csit314.entity.PropertyListing import PropertyListing
from werkzeug.utils import redirect

bp = Blueprint('removePropertyListing', __name__, template_folder='boundary/templates')

@bp.route('/propertyListing/remove/<int:propertyListing_id>/')
@login_required
def removePropertyListing(propertyListing_id):
    propertyListing = PropertyListing.query.get_or_404(propertyListing_id)
    if g.user != propertyListing.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('viewPropertyListing.detail', propertyListing_id=propertyListing.id))
    db.session.delete(propertyListing)
    db.session.commit()
    return redirect(url_for('viewPropertyListing.index'))
