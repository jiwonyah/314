from csit314.entity.User import User, Role
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask import Blueprint, url_for, render_template, flash, request, redirect, session, g
from werkzeug.security import check_password_hash
from werkzeug.utils import redirect
import functools
from functools import wraps
from csit314.entity.User import User


class UserLoginForm(FlaskForm):
    userid = StringField('ID', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])

# decorator to protect view which requires login
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            flash("To access the page, login first.")
            return redirect(url_for('login.login', next=_next))
        return view(*args, **kwargs)
    return wrapped_view

# decorator to protect view which requires agent authority
def agent_only(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        # get current user
        user = g.user

        # accept access requirement only if when user is authenticated and role is agent
        if user and user.role.value == 'agent':
            return view(*args, **kwargs)
        else:
            # 인증되지 않은 경우 또는 역할이 'agent'가 아닌 경우 접근 거부
            return render_template("NotAgentAlert.html")  # 로그인 페이지로 리디렉션
    return wrapped_view


bp = Blueprint('login', __name__, template_folder='boundary/templates')

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(userid=form.userid.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            _next = request.args.get('next', '')
            if _next:
                return redirect(_next)
            else:
                return redirect(url_for('index'))
        flash(error)
    return render_template('login.html', form=form)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

