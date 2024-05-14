from flask import Blueprint, jsonify, request, render_template
from csit314.controller.role_service.decorators import login_required, admin_only
from csit314.entity.User import User

bp = Blueprint('viewAccount', __name__, template_folder="/boundary/templates")


#for displaying the user account page
@bp.route('/admin/view_user_account')
@login_required
@admin_only
def view_user_accounts():
    userList = User.getUserAccounts()
    return render_template("UserAccount/ViewUserAccountPage.html", users=userList)

#for retrieving user account details of a specific username
@bp.route('/admin/view_user_account_details/<userid>')
@login_required
@admin_only
def view_account_details(userid):
    #getting the user object from UserAccount class method
    user = User.getUserDetails(userid)
    full_name = f"{user.firstName} {user.lastName}" if user.firstName and user.lastName else None
    serialized_role = user.serialize_enum()
    return jsonify({
        'firstName': user.firstName,
        'lastName': user.lastName,
        'email': user.email,
        'userid': user.userid,
        'password': user.password,
        'role': serialized_role,
        'status': user.status,
        'full_name': full_name
    })
