from flask import redirect
from csit314.entity.User import User, Role
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from csit314.app import db
from flask import Blueprint, url_for, render_template, flash, request
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

class UserCreateForm(FlaskForm):
    userid = StringField('ID', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', 'Check the password')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max=25)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[
        (Role.SELLER.value, 'Seller'),
        (Role.BUYER.value, 'Buyer'),
        (Role.AGENT.value, 'Agent')
    ], validators=[DataRequired()])


bp = Blueprint('signup', __name__, template_folder='boundary/templates')

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(userid=form.userid.data).first()
        if not user:
            user = User(userid=form.userid.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data, role=form.role.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))

        else:
            flash('Existing Account')
    return render_template('user_signup_form.html', form=form)