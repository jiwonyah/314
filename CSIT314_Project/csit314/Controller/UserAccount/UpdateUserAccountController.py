from flask import Blueprint, jsonify, request, render_template

from csit314.Entity.UserAccount import UserAccount

class UpdateUserAccountController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule("/update_user_account", view_func=self.view_user_accounts, methods=['GET'])
        self.add_url_rule("/update_user_account/<username>", view_func=self.display_update_form, methods=['GET'])
        self.add_url_rule("/update_user_account/<username>", view_func=self.update_user_account, methods=['POST'])

    #for displaying all users page
    def view_user_accounts(self):
        userList = UserAccount.getUserAccounts()
        return render_template("UserAccount/UpdateUserAccountPage.html", users=userList)


    #for displaying the account update form
    def display_update_form(self, username):
        user = UserAccount.getUserDetails(username)
        return render_template("UserAccount/UpdateUserAccountForm.html", user=user)


    def update_user_account(self, username):
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

