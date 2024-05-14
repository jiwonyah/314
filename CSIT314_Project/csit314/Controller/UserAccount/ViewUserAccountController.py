from flask import Blueprint, jsonify, request, render_template

from csit314.Entity.UserAccount import UserAccount

class ViewUserAccountController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule("/view_user_account", view_func=self.view_user_accounts, methods=['GET'])
        self.add_url_rule("/view_user_account_details/<username>",
                          view_func=self.view_account_details, methods=['GET'])

    #for displaying the user account page
    def view_user_accounts(self):
        userList = UserAccount.getUserAccounts()
        return render_template("UserAccount/ViewUserAccountPage.html", users=userList)


    #for retrieving user account details of a specific username
    def view_account_details(self, username):
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
