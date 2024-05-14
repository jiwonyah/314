from flask import Blueprint, render_template

bp = Blueprint('profileDashboard', __name__, template_folder="/boundary/templates")


#for displaying profile dashboard
@bp.route('/user_profile_dashboard')
def dashboard():
    return render_template("UserProfile/UserProfileDashboardPage.html")
