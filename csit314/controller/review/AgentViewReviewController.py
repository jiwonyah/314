from flask import Blueprint, render_template, g, redirect, url_for, request, flash, jsonify
from csit314.entity.Review import Review
from csit314.entity.UserAccount import UserAccount    #, Role
from csit314.app import db
from csit314.controller.role_service.decorators import login_required, agent_only, suspended

bp = Blueprint('view_review_controller', __name__, template_folder='boundary/templates')

@bp.route('/agent/reviews/')
@login_required
@agent_only
@suspended
def agentViewReviews_index():
    reviews = Review.query.filter_by(agent_id=g.user.id).all()
    return render_template('review/viewReviewList.html', reviews=reviews)

@bp.route('/api/agent/reviews/')
@login_required
@agent_only
@suspended
def agentViewReviews():
    reviews = Review.query.filter_by(agent_id=g.user.id).all()
    review_data = [
        {
            'id': review.id,
            'author_userid': review.author_userid,
            'rating': review.rating,
            'content': review.content
        } for review in reviews
    ]
    return jsonify(review_data)

@bp.route('/agent/reviewDetail/<int:review_id>')
@login_required
@agent_only
@suspended
def review_detail_index(review_id):
    review = Review.query.filter_by(id=review_id).first()
    return render_template('review/reviewDetailPage.html', review=review)

@bp.route('/api/agent/reviewDetail/<int:review_id>')
@login_required
@agent_only
@suspended
def review_detail(review_id):
    review = Review.query.filter_by(id=review_id).first()
    if not review:
        return jsonify({'error': 'The review ID doesn\'t exist'}), 404
    if g.user.id != review.agent_id:
        return jsonify({'error': 'You do not have permission to access the review detail page.'}), 404
    return jsonify({
        'id': review.id,
        'author_userid': review.author_userid,
        'rating': review.rating,
        'content': review.content
    })

