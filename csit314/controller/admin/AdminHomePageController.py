from flask import Blueprint, render_template, g, jsonify
from csit314.entity.User import Role
from csit314.controller.role_service.decorators import login_required, admin_only
bp = Blueprint('adminHome', __name__, template_folder="/boundary/templates")

@bp.route('/admin/')
@login_required
@admin_only
def adminHomePage():
    return render_template('AdminHomePage.html')
