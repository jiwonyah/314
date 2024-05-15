from flask import Blueprint, request, g, redirect, url_for, jsonify, render_template
from csit314.entity.Review import Review
from csit314.entity.UserAccount import UserAccount
from csit314.app import db
from .Form.WriteReviewForm import WriteReviewForm
from datetime import datetime
from csit314.controller.role_service.decorators import login_required, buyer_seller_only, suspended

bp = Blueprint('write_review_controller', __name__, template_folder='boundary/templates')


@bp.route('/write-review/<int:agent_id>', methods=['GET'])
@login_required
@buyer_seller_only
@suspended
def show_reviewForm_index(agent_id):
    form = WriteReviewForm()
    user = UserAccount.query.get(agent_id)
    return render_template('review/writeReviewForm.html', agent_id=agent_id, form=form, user=user)

@bp.route('/write-review/<int:agent_id>', methods=['POST'])
@login_required
@buyer_seller_only
@suspended
def write_review(agent_id):
    form = WriteReviewForm(request.form)
    if form.validate_on_submit():
        rating = form.rating.data
        content = form.content.data
        if g.user:
            current_user_username = g.user.userid
        else:
            return jsonify({'error': 'Please log in to submit a review.'}), 401
        user = UserAccount.query.get(agent_id)
        new_review = Review(author_userid=current_user_username, agent_id=agent_id, rating=rating, content=content,  create_date=datetime.now())
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for('write_review_controller.agent_list_index'))
    else:
        return jsonify({'error': 'Invalid form data.'}), 400


@bp.route('/agents')
@suspended
def agent_list_index():
    return render_template('review/agentListPage.html')

@bp.route('/api/agents')
@suspended
def agent_list():
    agents = UserAccount.query.filter_by(role='agent').all()
    agent_data = [
        {
            'id': agent.id,
            'userid': agent.userid,
            'firstName': agent.firstName,
            'lastName': agent.lastName,
            'email': agent.email,
            'role': agent.role  # agent.role.value
        } for agent in agents
    ]
    return jsonify(agents=agent_data)
