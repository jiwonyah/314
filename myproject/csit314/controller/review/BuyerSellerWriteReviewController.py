from flask import Blueprint, request, g, jsonify, render_template, session
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import TextAreaField, HiddenField, RadioField, SubmitField
from csit314.entity.Review import Review
from csit314.entity.User import User

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
    if user is None:
        return jsonify({'error': 'Agent not found'}), 404
    return render_template('review/writeReviewForm.html', agent_id=agent_id, form=form, user=user)
@bp.route('/write-review/<int:agent_id>', methods=['POST'])
def write_review(agent_id):
    json_data = request.get_json()
    print(f"Received JSON data: {json_data}")

    form = WriteReviewForm(data=json_data)

    if not form.validate_on_submit():
        errors = [{'field': field, 'message': ', '.join(error)} for field, error in form.errors.items()]
        print(f"Form validation errors: {errors}")
        return jsonify({'success': False, 'errors': errors}), 422
    else:
        rating = form.rating.data
        content = form.content.data

        details = {
            'rating': rating,
            'content': content,
            'author_userid': g.user.userid if g.user else None,
            'agent_id': agent_id
        }
        print(f"Details to be used for creating review: {details}")

        success = Review.createReview(details, agent_id)
        if success:
            return jsonify({'success': True, 'message': 'Review is submitted successfully'}), 201
        else:
            return jsonify({'success': False, 'error': 'Failed to submit review'}), 500

@bp.route('/agents')
def agent_list_index():
    return render_template('review/agentListPage.html'), 200
@bp.route('/api/agents')
def agent_list():
    agents = User.query.filter_by(role='agent').all()
    if not agents:
        return jsonify({'error': 'No agents found'}), 404
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
    return jsonify(agents=agent_data), 200
