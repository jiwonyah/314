from flask import Blueprint, jsonify, request, render_template

from csit314.Entity.UserAccount import UserAccount

bp = Blueprint('viewAccount', __name__, template_folder="/boundary/templates")


#for displaying the user account page
@bp.route('/view_user_account')
def view_user_accounts():
    userList = UserAccount.getUserAccounts()
    return render_template("UserAccount/ViewUserAccountPage.html", users=userList)


#for retrieving user account details of a specific username
@bp.route('/view_user_account_details/<username>')
def view_account_details(username):
    #getting the user object from UserAccount class method
    user = UserAccount.getUserDetails(username)
    return jsonify({
        'full_name': user.full_name,
        'email': user.email,
        'username': user.username,
        'password': user.password,
        'role': user.role,
        'status': user.status
    })
