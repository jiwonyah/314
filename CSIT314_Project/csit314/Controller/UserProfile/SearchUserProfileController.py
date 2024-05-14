from flask import Blueprint, render_template, request, jsonify

from csit314.Entity.UserProfile import UserProfile

bp = Blueprint('searchProfile', __name__, template_folder="/boundary/templates")

@bp.route('/search_user_profile')
def search_page():
    return render_template("UserProfile/SearchUserProfilePage.html")

@bp.route('/search_profile')
def search_profile():
    searchQuery = request.args.get('search')
    profiles = UserProfile.search_profile(searchQuery)
    if profiles:
        return jsonify({'profiles': profiles})
    else:
        return jsonify({'error': "No profiles found"})