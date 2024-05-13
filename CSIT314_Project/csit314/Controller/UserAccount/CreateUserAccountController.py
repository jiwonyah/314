from flask import Blueprint, jsonify, request, render_template

from csit314.Entity.UserAccount import UserAccount


bp = Blueprint('createAccount', __name__, template_folder="/boundary/templates")


@bp.route('/create_user_account', methods=['GET','POST'])
def createUserAccount():
    #if request is get display the create page
    if request.method == 'GET':
        return render_template('UserAccount/CreateUserAccountPage.html')

    #if request method is post do validation and return success type
    elif request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        status = 'Active'

        account_details = {
            'full_name': full_name,
            'email': email,
            'username': username,
            'password': password,
            'role': role,
            'status': status
        }

        results = UserAccount.createUserAccount(account_details)
        if results:
            return jsonify({'success': True, 'message': 'User Account created successfully'})
        elif UserAccount.usernameExists(account_details):
            return jsonify({'success': False, 'error': 'Username Exists'})
        elif UserAccount.emailExists(account_details):
            return jsonify({'success': False, 'error': 'Email Exists'})

