from flask import Blueprint, jsonify, request, render_template

from csit314.Entity.UserAccount import UserAccount
from csit314.Entity.UserProfile import UserProfile

class CreateUserAccountController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule("/create_user_account", view_func=self.create_user_account, methods=['GET', 'POST'])

    def create_user_account(self):
        # if request is get display the create page
        if request.method == 'GET':
            profiles = UserProfile.getAllProfiles()
            return render_template('UserAccount/CreateUserAccountPage.html', profiles=profiles)

        # if request method is post do validation and return success type
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
