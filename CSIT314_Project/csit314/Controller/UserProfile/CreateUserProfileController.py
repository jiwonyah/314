from flask import Blueprint, jsonify, request

from csit314.Entity.UserProfile import UserProfile


bp = Blueprint('createProfile', __name__, template_folder="/boundary/templates")


@bp.route('/create_user_account', methods=['POST'])
def createUserProfile():
    profileName = request.form['profileName']
    profileDescription = request.form['profileDescription']

    profile_details = {
        'profileName': profileName,
        'profileDescription': profileDescription,
    }

    results = UserProfile.createUserProfile(profile_details)
    if results:
        return jsonify({'success': True, 'message': 'User Profile created successfully'})
    elif UserProfile.profileNameExists(profile_details):
        return jsonify({'success': False, 'error': 'Profile Name Exists'})


