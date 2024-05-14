from flask import Blueprint, render_template, request, jsonify

from csit314.Entity.UserAccount import UserAccount

bp = Blueprint('suspendAccount', __name__, template_folder="/boundary/templates")

@bp.route('/suspend_user_account')
def display_suspend_form():
    return render_template('UserAccount/SuspendUserAccountPage.html')

@bp.route('/suspend_account', methods =['POST'])
def suspend_account():
    username = request.form['username']
    results = UserAccount.suspend_account(username)
    if results:
        return jsonify({'success': True, 'message': 'User Account suspended successfully'})
    elif UserAccount.getUserDetails(username) is None:
        return jsonify({'success': False, 'message': 'Username does not exist'})
    else:
        return jsonify({'success': False, 'message': 'User Account already suspended'})