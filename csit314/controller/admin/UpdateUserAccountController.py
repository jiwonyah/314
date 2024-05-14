from flask import Blueprint, jsonify, request, render_template
from csit314.controller.role_service.decorators import login_required, admin_only
from csit314.entity.UserAccount import UserAccount

bp = Blueprint('updateAccount', __name__, template_folder="/boundary/templates")


#for displaying all users page
@bp.route('/update_user_account')
@login_required
@admin_only
def view_user_accounts():
    userList = UserAccount.getUserAccounts()
    return render_template("UserAccount/UpdateUserAccountPage.html", users=userList)


#for displaying the account update form
@bp.route('/update_user_account/<userid>')
@login_required
@admin_only
def display_update_form(userid):
    user = UserAccount.getUserDetails(userid)
    return render_template("UserAccount/UpdateUserAccountForm.html", user=user)


@bp.route('/update_user_account/<userid>', methods=['POST'])
@login_required
@admin_only
def update_user_account(userid):
    user = UserAccount.getUserDetails(userid)
    full_name = request.form['full_name']
    email = request.form['email']
    new_username = request.form['userid']
    password = request.form['password']
    role = request.form['role']

    if 'suspended' in request.form:
        status = 'Active'
    else:
        status = 'Suspended'

    updateDetails = {
        'full_name': full_name,
        'email': email,
        'userid': new_username,
        'password': password,
        'role': role,
        'status': status
    }

    results = UserAccount.updateUserAccount(user.userid, updateDetails)
    if results:
        return jsonify({'success': True, 'message': 'User Account updated successfully'})
    elif new_username != user.userid and UserAccount.useridExists(updateDetails):
        return jsonify({'success': False, 'error': 'Username Exists'})
    elif email != user.email and UserAccount.emailExists(updateDetails):
        return jsonify({'success': False, 'error': 'Email Exists'})
