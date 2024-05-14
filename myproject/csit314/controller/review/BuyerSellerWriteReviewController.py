from flask import Blueprint, request, g, redirect, url_for, jsonify, render_template
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import TextAreaField, HiddenField, RadioField, SubmitField
from datetime import datetime

from csit314.controller.role_service.decorators import buyer_seller_only
from csit314.entity.Review import Review
from csit314.entity.User import User
from csit314.app import db

bp = Blueprint('write_review_controller', __name__, template_folder='boundary/templates')

class WriteReviewForm(FlaskForm):
    agent_id = HiddenField('Agent ID')  # Hidden field for storing agent ID
    rating = RadioField('Rating',
                        validators=[DataRequired('Rating is mandatory field')],
                        choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])  # Radio button to select between 1-5
    content = TextAreaField('Content', validators=[DataRequired('Content is mandatory field')])  # Textarea to enter review content
    submit = SubmitField('Submit Review')  # Review submit button

@buyer_seller_only
@bp.route('/write-review/<int:agent_id>', methods=['GET'])
def show_reviewForm_index(agent_id):
    form = WriteReviewForm()
    user = User.query.get(agent_id)
    return render_template('review/writeReviewForm.html', agent_id=agent_id, form=form, user=user)
@buyer_seller_only
@bp.route('/write-review/<int:agent_id>', methods=['POST'])
def write_review(agent_id):
    form = WriteReviewForm(request.form)
    if form.validate_on_submit():
        rating = form.rating.data
        content = form.content.data

        if g.user:
            current_user_username = g.user.userid
        else:
            return jsonify({'error': 'Please log in to submit a review.'}), 401

        user = User.query.get(agent_id)
        new_review = Review(author_userid=current_user_username, agent_id=agent_id, rating=rating, content=content, create_date=datetime.now())
        db.session.add(new_review)
        db.session.commit()

        return redirect(url_for('write_review_controller.agent_list_index'))
        #return jsonify({'message': 'Your review has been submitted!', 'successAlert': successAlert}), 200
    else:
        return jsonify({'error': 'Invalid form data.'}), 400

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
