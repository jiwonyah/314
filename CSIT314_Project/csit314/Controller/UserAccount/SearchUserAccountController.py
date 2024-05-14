from flask import Blueprint, render_template, request, jsonify

from csit314.Entity.UserAccount import UserAccount

bp = Blueprint('searchAccount', __name__, template_folder="/boundary/templates")

#displaying the search account page
@bp.route('/search_user_account')
def search_page():
    return render_template("/UserAccount/SearchUserAccountPage.html")


@bp.route('/search_account')
def search_account():
    searchQuery = request.args.get('search')
    accounts = UserAccount.search_account(searchQuery)
    if accounts:
        return jsonify({'accounts': accounts})
    else:
        return jsonify({'error': "No accounts found"})

