from flask import Blueprint, render_template, request, jsonify

from csit314.Entity.UserProfile import UserProfile

bp = Blueprint('suspendProfile', __name__, template_folder="/boundary/templates")

@bp.route('/suspend_user_profile')
def display_suspend_form():
    return render_template('UserProfile/SuspendUserProfilePage.html')

@bp.route('/suspend_profile', methods=['POST'])
def suspend_profile():
    profileName = request.form['profileName']
    results = UserProfile.suspend_profile(profileName)
    if results:
        return jsonify({'success': True, 'message': 'User Profile suspended successfully'})
    elif UserProfile.getProfile(profileName) is None:
        return jsonify({'success': False, 'message': 'Profile Name does not exist'})
    else:
        return jsonify({'success': False, 'message': 'User Profile already suspended'})
