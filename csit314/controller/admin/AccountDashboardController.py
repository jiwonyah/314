from flask import Blueprint, render_template
from csit314.controller.role_service.decorators import login_required, admin_only

bp = Blueprint('accountDashboard', __name__, template_folder="/boundary/templates")

#for displaying account dashboard
@login_required
@admin_only
@bp.route('/admin/user_account_dashboard')
def dashboard():
    return render_template("UserAccount/UserAccountDashboard.html")