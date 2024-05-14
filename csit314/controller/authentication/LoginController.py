from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length
from flask import jsonify, Blueprint, url_for, render_template, redirect, session
from csit314.entity.UserAccount import UserAccount
from flask import request, g, flash
import bcrypt

bp = Blueprint('login', __name__, template_folder='boundary/templates')

class UserLoginForm(FlaskForm):
    """
    Form for user login.
    """
    userid = StringField('ID', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])

def is_logged_in():
    # check logged in status
    return 'user_id' in session

@bp.route('/login/')    # GET
def index():
    if is_logged_in():
        flash('You are already logged in. Please log out first.')
        return redirect(url_for('index'))
    form = UserLoginForm()
    return render_template('authentication/login.html', form=form)

@bp.route('/login/', methods=['POST'])
def login():
    if is_logged_in():
        return jsonify({'error': 'Already logged in'}), 400
    credential = request.json
    userid = credential['userid']
    password = credential['password']
    user = UserAccount.findAUserByUserID(userid=userid)
    if user and bcrypt.checkpw(password.encode('UTF-8'), user.password.encode('UTF-8')):
        session['user_id'] = user.id
        #serialized_role = user.serialize_enum()
        return jsonify({'success': True, 'message': 'Login successful'})
    return jsonify({'success': False, 'error': 'User information does not exist.'}), 401

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = UserAccount.query.get(user_id)

