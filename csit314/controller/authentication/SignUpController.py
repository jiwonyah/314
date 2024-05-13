from csit314.entity.User import User, Role
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from flask import Blueprint, render_template, request, jsonify, flash
import bcrypt

bp = Blueprint('signup', __name__, template_folder='boundary/templates')


class UserCreateForm(FlaskForm):
    """
    Form for user sign up.
    """
    userid = StringField('ID', validators=[
        DataRequired(),
        Length(min=5, max=25, message='ID length must be 5~25.')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=25, message='Password must be 8~25.')
    ])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(), Length(min=8, max=25)
    ])
    email = EmailField('Email', validators=[
        DataRequired(),
        Email()
    ])
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    role = SelectField('Role', choices=[
        (Role.SELLER.value, 'Seller'),
        (Role.BUYER.value, 'Buyer'),
        (Role.AGENT.value, 'Agent')
    ], validators=[DataRequired()])

@bp.route('/signup/')
def index():
    form = UserCreateForm()
    return render_template('authentication/SignUpBoundary.html', form=form)

@bp.route('/signup/', methods=['POST'])
def signUp():
    userid = request.form['userid']
    password = request.form['password']
    password2 = request.form['password2']
    email = request.form['email']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    role = request.form['role']
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_details = {
        'userid': userid,
        'password': hashed_password.decode('utf-8'),  # 해싱된 비밀 번호 저장
        'email': email,
        'firstName': firstName,
        'lastName': lastName,
        'role': role
    }
    if password != password2:
        return jsonify({'success': False, 'error': 'Password does not match.'})

    success = User.createNewUser(user_details)
    userid_exists = User.query.filter_by(userid=user_details["userid"]).one_or_none()
    email_exists = User.query.filter_by(email=user_details["email"]).one_or_none()

    if success:
        return jsonify({'success': True, 'message': 'User created successfully'})
    else:
        if userid_exists:
            return jsonify({'success': False, 'error': 'The ID is already registered.'})
        if email_exists:
            return jsonify({'success': False, 'error': 'The email is already registered.'})
        if len(userid) < 5 or len(userid) > 25:
            return jsonify({'success': False, 'error': 'ID length must be 5~25.'})
        if len(password) < 8 or len(password) > 25:
            return jsonify({'success': False, 'error': 'Password must be 8~25.'})



