from flask import Blueprint, jsonify, request, render_template

from csit314.Entity.UserAccount import UserAccount

bp = Blueprint('updateAccount', __name__, template_folder="/boundary/templates")


#for displaying all users page
@bp.route('/update_user_account')
def view_user_accounts():
    userList = UserAccount.getUserAccounts()
    return render_template("UserAccount/UpdateUserAccountPage.html", users=userList)


#for displaying the account update form
@bp.route('/update_user_account/<username>')
def display_update_form(username):
    user = UserAccount.getUserDetails(username)
    return render_template("UserAccount/UpdateUserAccountForm.html", user=user)


@bp.route('/update_user_account/<username>', methods=['POST'])
def update_user_account(username):
    user = UserAccount.getUserDetails(username)
    full_name = request.form['full_name']
    email = request.form['email']
    new_username = request.form['username']
    password = request.form['password']
    role = request.form['role']

    if 'suspended' in request.form:
        status = 'Active'
    else:
        status = 'Suspended'

    updateDetails = {
        'full_name': full_name,
        'email': email,
        'username': new_username,
        'password': password,
        'role': role,
        'status': status
    }

    results = UserAccount.updateUserAccount(user.username, updateDetails)
    if results:
        return jsonify({'success': True, 'message': 'User Account updated successfully'})
    elif new_username != user.username and UserAccount.usernameExists(updateDetails):
        return jsonify({'success': False, 'error': 'Username Exists'})
    elif email != user.email and UserAccount.emailExists(updateDetails):
        return jsonify({'success': False, 'error': 'Email Exists'})

