from flask import Blueprint, jsonify, render_template

from csit314.Entity.UserProfile import UserProfile


bp = Blueprint('viewProfile', __name__, template_folder="/boundary/templates")

@bp.route('/view_user_profile')
def viewAllProfile():
    profileList = UserProfile.getAllProfiles()
    return render_template('UserProfile/ViewUserProfilePage.html', profiles=profileList)


@bp.route('/view_user_profile_details/<profileName>')
def view_account_details(profileName):
    profile = UserProfile.getProfile(profileName)
    return jsonify({
        'profileName': profile.profileName,
        'profileDescription': profile.profileDescription
    })