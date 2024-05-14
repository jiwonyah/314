from flask import Blueprint, jsonify, render_template, request

from csit314.Entity.UserProfile import UserProfile

bp = Blueprint('updateProfile', __name__, template_folder="/boundary/templates")


@bp.route('/update_user_profile')
def view_user_profile():
    profileList = UserProfile.getAllProfiles()
    return render_template('UserProfile/UpdateUserProfilePage.html', profiles=profileList)


@bp.route('/update_user_profile/<profileName>')
def display_update_form(profileName):
    profile = UserProfile.getProfile(profileName)
    return render_template("UserProfile/UpdateUserProfileForm.html", profile=profile)


@bp.route('/update_user_profile/<profileName>', methods=['POST'])
def update_user_profile(profileName):
    profile = UserProfile.getProfile(profileName)
    new_profileName = request.form['profileName']
    profileDescription = request.form['profileDescription']

    if 'suspended' in request.form:
        status = 'Active'
    else:
        status = 'Suspended'

    updateDetails = {
        'profileName': new_profileName,
        'profileDescription': profileDescription,
        'status': status
    }

    results = UserProfile.updateUserProfile(profile.profileName, updateDetails)
    if results:
        return jsonify({'success': True, 'message': 'User Profile updated successfully'})
    elif new_profileName != profile.profileName and UserProfile.profileNameExists(updateDetails):
        return jsonify({'success': False, 'error': 'Role Name Exists'})
