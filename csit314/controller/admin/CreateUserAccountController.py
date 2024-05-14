from flask import Blueprint, jsonify, request, render_template
from csit314.entity.UserAccount import UserAccount
from csit314.controller.role_service.decorators import login_required, admin_only

bp = Blueprint('createAccount', __name__, template_folder="/boundary/templates")

@bp.route('/admin/create_user_account', methods=['GET'])
@login_required
@admin_only
def index():
    return render_template('UserAccount/CreateUserAccountPage.html')

@bp.route('/admin/create_user_account', methods=['POST'])
@login_required
@admin_only
def createUserAccount():
    #if request method is post do validation and return success type
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    email = request.form['email']
    userid = request.form['userid']
    password = request.form['password']
    role = request.form['role']
    status = 'Active'
    account_details = {
        'firstName': firstName,
        'lastName': lastName,
        'email': email,
        'userid': userid,
        'password': password,
        'role': role,
        'status': status
    }
    results = UserAccount.createUserAccount(account_details)
    if results:
        return jsonify({'success': True, 'message': 'User Account created successfully'})
    elif UserAccount.useridExists(account_details):
        return jsonify({'success': False, 'error': 'UserID Exists'})
    elif UserAccount.emailExists(account_details):
        return jsonify({'success': False, 'error': 'Email Exists'})