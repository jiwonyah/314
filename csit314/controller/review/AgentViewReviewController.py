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
    return render_template('review/viewReviewList.html')

@bp.route('/api/agent/reviews/')
@login_required
@agent_only
@suspended
def agentViewReviews():
    reviews = Review.displayReviewsList()
    review_data = []
    for review in reviews:
        user = UserAccount.query.filter_by(userid=review.author_userid).first()
        review_data.append({
            'id': review.id,
            'author_name': f"{user.firstName} {user.lastName}",
            'create_date': review.create_date.strftime('%a, %d %b %Y'),
            'rating': review.rating,
            'content': review.content
        })
    return jsonify(reviews=review_data)

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
    review = Review.displayReviewDetails(review_id)
    if not review:
        return jsonify({'error': 'The review ID doesn\'t exist'}), 404
    if g.user.id != review.agent_id:
        return jsonify({'error': 'You do not have permission to access the review detail page.'}), 404

    user = UserAccount.query.filter_by(userid=review.author_userid).first()
    return jsonify({
        'id': review.id,
        'author_name': f"{user.firstName} {user.lastName}",
        'create_date': review.create_date.strftime('%a, %d %b %Y %H:%M:%S GMT'),
        'rating': review.rating,
        'content': review.content
    })
