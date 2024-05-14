from flask import Blueprint, render_template

bp = Blueprint('accountDashboard', __name__, template_folder="/boundary/templates")

#for displaying account dashboard
@bp.route('/user_account_dashboard')
def dashboard():
    return render_template("UserAccount/UserAccountDashboard.html")