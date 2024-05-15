from flask import jsonify, Blueprint, render_template, session
from csit314.entity.UserAccount import UserAccount
from flask import request, g
import bcrypt
from .Form.UserLoginForm import UserLoginForm
from csit314.controller.role_service.decorators import already_logged_in, is_logged_in


bp = Blueprint('login', __name__, template_folder='boundary/templates')


@bp.route('/login/')    # GET
@already_logged_in
def index():
    form = UserLoginForm()
    return render_template('authentication/login.html', form=form)

@bp.route('/login/', methods=['POST'])
@already_logged_in
def login():
    credential = request.json
    userid = credential['userid']
    password = credential['password']
    user = UserAccount.findAUserByUserID(userid=userid)
    if user and bcrypt.checkpw(password.encode('UTF-8'), user.password.encode('UTF-8')):
        session['user_id'] = user.id

        return jsonify({'success': True, 'message': 'Login successful', 'role': user.role})
    return jsonify({'success': False, 'error': 'User information does not exist.'}), 401

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = UserAccount.query.get(user_id)



