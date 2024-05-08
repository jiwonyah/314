from flask import Blueprint, g, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, HiddenField, RadioField, SubmitField
from wtforms.validators import DataRequired

from csit314.entity.Review import Review
from csit314.entity.User import User, Role
from csit314.app import db

class WriteReviewForm(FlaskForm):
    agent_id = HiddenField('Agent ID')
    rating = RadioField('Rating',
                        validators=[DataRequired('Rating is mandatory field')],
                        choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    content = TextAreaField('Content', validators=[DataRequired('Content is mandatory field')])
    submit = SubmitField('Submit Review')

bp = Blueprint('write_review_controller', __name__)

@bp.route('/agentList')
def agent_list():
    agents = User.query.filter_by(role='agent').all()
    return agents

@bp.route('/write-review/<int:agent_id>', methods=['GET', 'POST'])
def write_review(agent_id):
    form = WriteReviewForm()

    if request.method == 'POST' and form.validate_on_submit():
        rating = form.rating.data
        content = form.content.data

        if g.user:
            current_user_username = g.user.userid
        else:
            flash('Please log in to submit a review.', 'error')
            return redirect(url_for('login'))

        new_review = Review(author_userid=current_user_username, agent_id=agent_id, rating=rating, content=content)
        db.session.add(new_review)
        db.session.commit()

        flash('Your review has been submitted!', 'success')
        return redirect(url_for('index'))

    return {
        'form': form,
        'agent_id': agent_id
    } # 리턴값: 딕셔너리


"""
# 시도 해봤는데 잘 안되던거. DB에 반영이 안됨
from flask import Blueprint, render_template, g, redirect, url_for, request, flash, jsonify
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

# 수정중
@bp.route('/write-review/<int:agent_id>', methods=('GET', 'POST'))
def write_review(agent_id):
    form = WriteReviewForm()

    if request.method == 'GET':
        # GET 요청 시, 폼을 렌더링합니다.
        return render_template('writeReviewForm.html', form=form, agent_id=agent_id)

    elif request.method == 'POST' and form.validate_on_submit():
        rating = form.rating.data
        content = form.content.data
        agent_id = form.agent_id.data

        # 현재 로그인한 사용자의 userid를 가져옵니다.
        if g.user:
            current_user_userid = g.user.userid
        else:
            # 사용자가 로그인하지 않았다면 로그인 페이지로 리다이렉트합니다.
            flash('리뷰를 제출하려면 로그인해야 합니다.', 'error')
            return redirect(url_for('login'))

        # 리뷰 객체를 생성하고 데이터베이스에 추가합니다.
        new_review = Review(author_userid=current_user_userid, agent_id=agent_id, rating=rating, content=content)
        db.session.add(new_review)
        db.session.commit()

        # 성공 메시지를 JSON 형태로 반환합니다.
        return jsonify({'status': 'success', 'message': '리뷰가 제출되었습니다!'})

    # 유효하지 않은 폼 제출의 경우 에러 메시지를 반환합니다.
    return jsonify({'status': 'error', 'message': '유효하지 않은 폼 제출입니다.'})
"""




'''
# 수정 아예 전
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
'''
