from flask import Blueprint, render_template, g, jsonify
from csit314.entity.Review import Review
from csit314.entity.User import User

bp = Blueprint('view_review_controller', __name__, template_folder='boundary/templates')

@bp.route('/agent/reviews/')
def agentViewReviews_index():
    reviews = Review.query.filter_by(agent_id=g.user.id).all()

    review_data = []
    for review in reviews:
        user = User.query.filter_by(userid=review.author_userid).first()
        review_data.append({
            'id': review.id,
            'author_name': f"{user.firstName} {user.lastName}",
            'create_date': review.create_date,
            'rating': review.rating,
            'content': review.content
        })

    return render_template('review/viewReviewList.html', reviews=review_data)

@bp.route('/agent/reviewDetail/<int:review_id>')
def review_detail_index(review_id):
    review = Review.query.filter_by(id=review_id).first()
    return render_template('review/reviewDetailPage.html', review=review)
@bp.route('/api/agent/reviewDetail/<int:review_id>')
def review_detail(review_id):
    # Return review detail page based on review ID. Return error page if review ID does not exist.
    review = Review.query.filter_by(id=review_id).first()
    if not review:
        return jsonify({'error': 'The review ID doesn\'t exist'}), 404

    # Only allow access to review detail page if it belongs to the current user.
    if g.user.id != review.agent_id:
        return jsonify({'error': 'You do not have permission to access the review detail page.'}), 404
    user = User.query.filter_by(userid=review.author_userid).first()
    # Return review detail information in JSON format.
    return jsonify({
        'id': review.id,
        'author_name': f"{user.firstName} {user.lastName}",
        'create_date': review.create_date,
        'rating': review.rating,
        'content': review.content
    })
