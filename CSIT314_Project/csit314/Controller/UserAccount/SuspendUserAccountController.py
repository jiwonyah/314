from flask import Blueprint, render_template, request, jsonify

from csit314.Entity.UserAccount import UserAccount

class SuspendUserAccountController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule("/suspend_user_account", view_func=self.display_suspend_form, methods=['GET'])
        self.add_url_rule("/suspend_account", view_func=self.suspend_account, methods=['POST'])
    def display_suspend_form(self):
        return render_template('UserAccount/SuspendUserAccountPage.html')

    def suspend_account(self):
        username = request.form['username']
        results = UserAccount.suspend_account(username)
        if results:
            return jsonify({'success': True, 'message': 'User Account suspended successfully'})
        elif UserAccount.getUserDetails(username) is None:
            return jsonify({'success': False, 'message': 'Username does not exist'})
        else:
            return jsonify({'success': False, 'message': 'User Account already suspended'})