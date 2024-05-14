from flask import Blueprint, render_template, g, jsonify
from csit314.entity.User import Role

bp = Blueprint('adminHome', __name__, template_folder="/boundary/templates")

@bp.route('/admin/')
def adminHomePage():
    if not g.user:
        return jsonify(success=False,
                       error='Login required to view old property listing.'), 401
    elif g.user.role != Role.ADMIN:
        return jsonify(success=False,
                       error='Only buyers can view old property listings.'), 403
    return render_template('AdminHomePage.html')
