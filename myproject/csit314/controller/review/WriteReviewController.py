from flask import Blueprint, render_template, g, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, HiddenField, RadioField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

from csit314.entity.Review import Review
from csit314.entity.User import User, Role
from csit314.app import db

class WriteReviewForm(FlaskForm):
    agent_id = HiddenField('Agent ID')  # Hidden field for storing agent ID
    rating = RadioField('Rating',
                        validators=[DataRequired('Rating is mandatory field')],
                        choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])  # Radio button to select between 1-5
    content = TextAreaField('Content', validators=[DataRequired('Content is mandatory field')])  # Textarea to enter review content
    submit = SubmitField('Submit Review')  # Review submit button

bp = Blueprint('write_review_controller', __name__, template_folder='boundary/templates')

@bp.route('/agentList/')
def agent_list():
    agents = User.query.filter_by(role='agent').all()
    return render_template('agentListPage.html', agents=agents)

@bp.route('/write-review/<int:agent_id>', methods=('GET', 'POST'))
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
        return redirect(url_for('index')) # 이거 나중에 수정하기

    return render_template('writeReviewForm.html', form=form, agent_id=agent_id)

#@bp.route('/agentList')
#def agent_list():
    # g.user는 로그인한 사용자의 정보를 가지고 있습니다.
    # 로그인하지 않은 경우나 Agent 역할이 아닌 경우에만 페이지를 보여줍니다.
#    if g.user is None or g.user.role != Role.AGENT:
#        return render_template('agentListPage.html')
#    else:
        # Agent 역할을 가진 사용자의 경우 다른 페이지를 보여줄 수 있습니다.
        # 여기서는 간단히 메인 페이지로 리다이렉트한다고 가정합니다.
#        return redirect(url_for('index.html'))

