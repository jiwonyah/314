from flask import Blueprint, request, g, jsonify, render_template, session
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, TextAreaField, HiddenField, RadioField, SubmitField
from datetime import datetime
from csit314.entity.Review import Review
from csit314.entity.User import User, Role
from csit314.app import db

bp = Blueprint('write_review_controller', __name__, template_folder='boundary/templates')

class WriteReviewForm(FlaskForm):
    agent_id = HiddenField('Agent ID')  # Hidden field for storing agent ID
    rating = RadioField('Rating',
                        validators=[DataRequired('Rating is mandatory field')],
                        choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])  # Radio button to select between 1-5
    content = TextAreaField('Content', validators=[DataRequired('Content is mandatory field')])  # Textarea to enter review content
    submit = SubmitField('Submit Review')  # Review submit button

@bp.route('/write-review/<int:agent_id>', methods=['GET'])
def show_reviewForm_index(agent_id):
    form = WriteReviewForm()
    user = User.query.get(agent_id)
    return render_template('review/writeReviewForm.html', agent_id=agent_id, form=form, user=user)

@bp.route('/write-review/<int:agent_id>', methods=['POST'])
def write_review(agent_id):
    json_data = request.get_json()  # JSON 데이터 받기
    form = WriteReviewForm(data=json_data)  # 폼 인스턴스 생성 시 JSON 데이터 사용
    #form = WriteReviewForm(request.form)

    if not form.validate_on_submit():
        # 폼 유효성 검사에 실패한 경우 JSON 응답 반환
        errors = [{'field': field, 'message': ', '.join(error)} for field, error in form.errors.items()]
        return jsonify({'success': False, 'errors': errors}), 422
    else:
        rating = form.rating.data
        content = form.content.data

        details = {
            'rating': rating,
            'content': content,
            'author_userid': g.user.userid if g.user else None,  # Optional: Include author_userid based on logged-in user
            'agent_id': agent_id
        }
        success = Review.createReview(details, agent_id)
        if success:
            return jsonify({'success': True, 'message': 'Review is submitted successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to submit review'})

"""
        if g.user:
            current_user_username = g.user.userid
        else:
            return jsonify({'success': False, 'error': 'Please log in to submit a review.'}), 401

        user = User.query.get(agent_id)
        new_review = Review(author_userid=current_user_username, agent_id=agent_id, rating=rating, content=content, create_date=datetime.now())
        db.session.add(new_review)
        db.session.commit()

        #return redirect(url_for('write_review_controller.agent_list_index'))
        return jsonify({'success': True, 'message': 'Your review has been submitted!'}), 200
    else:
        return jsonify({'success': False, 'error': 'Invalid form data.'}), 400
"""
@bp.route('/agents')
def agent_list_index():
    return render_template('review/agentListPage.html')
@bp.route('/api/agents')
def agent_list():
    agents = User.query.filter_by(role='agent').all()
    agent_data = [
        {
            'id': agent.id,
            'userid': agent.userid,
            'firstName': agent.firstName,
            'lastName': agent.lastName,
            'email': agent.email,
            'role': agent.role.value  # convert Enum value into string
        } for agent in agents
    ]
    return jsonify(agents=agent_data)