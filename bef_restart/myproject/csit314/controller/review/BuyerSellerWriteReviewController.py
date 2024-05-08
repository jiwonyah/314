from flask import Blueprint, render_template, g, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, HiddenField, RadioField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from csit314.controller.authentication.LoginController import login_required
from csit314.entity.Review import Review
from csit314.entity.User import User, Role
from csit314.app import db
from functools import wraps

class WriteReviewForm(FlaskForm):
    agent_id = HiddenField('Agent ID')  # Hidden field for storing agent ID
    rating = RadioField('Rating',
                        validators=[DataRequired('Rating is mandatory field')],
                        choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])  # Radio button to select between 1-5
    content = TextAreaField('Content', validators=[DataRequired('Content is mandatory field')])  # Textarea to enter review content
    submit = SubmitField('Submit Review')  # Review submit button

bp = Blueprint('write_review_controller', __name__, template_folder='boundary/templates')


@bp.route('/agent_list/')
@login_required
def agent_list():
    agents = User.query.filter_by(role='agent').all()
    return render_template('review/agentListPage.html', agents=agents)



#-----------------------------decorator-----------------------------------
def buyer_seller_only(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        # get current user
        user = g.user

        # accept access requirement only if when user is authenticated and role is agent
        if user.role.value == 'buyer' or user.role.value == 'seller':
            return view(*args, **kwargs)
        else:
            # 인증되지 않은 경우 또는 역할이 'agent'가 아닌 경우 접근 거부
            return render_template('error/error.html',
                                   message='Only Buyer or Seller can write review.'), 404  # 로그인 페이지로 리디렉션
    return wrapped_view





@bp.route('/write-review/<int:agent_id>', methods=('GET', 'POST'))
@login_required
@buyer_seller_only
def write_review(agent_id):
    form = WriteReviewForm()

    if request.method == 'GET':
        form.agent_id.data = agent_id  # Set the value for the agent_id field in the form upon a GET request

    if request.method == 'POST' and form.validate_on_submit():
        rating = form.rating.data
        content = form.content.data
        agent_id = form.agent_id.data

        # Retrieves the userid of the currently logged-in user from g.user.
        if g.user:
            current_user_username = g.user.userid
        else:
            flash('Please log in to submit a review.', 'error')
            return redirect(url_for('login'))  # 사용자가 로그인하지 않았다면 로그인 페이지로 리다이렉트합니다.

        new_review = Review(author_userid=current_user_username, agent_id=agent_id, rating=rating, content=content)
        db.session.add(new_review)
        db.session.commit()

        flash('Your review has been submitted!', 'success')
        return redirect(url_for('write_review_controller.agent_list')) # 이거 나중에 수정하기

    return render_template('review/writeReviewForm.html', form=form, agent_id=agent_id)