from flask import Blueprint, render_template, g, redirect, url_for, request, flash, jsonify
from csit314.entity.Review import Review
from csit314.entity.User import User
from csit314.app import db

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
"""
@bp.route('/api/agent/reviews/')
def agentViewReviews():
    # 현재 로그인한 사용자(agent)의 id를 사용하여 리뷰를 조회합니다.
    reviews = Review.query.filter_by(agent_id=g.user.id).all()

    review_data = []
    for review in reviews:
        user = User.query.filter_by(userid=review.author_userid).first()
        review_data.append({
            'id': review.id,
            'author_name': f"{user.firstName} {user.lastName}",
            'rating': review.rating,
            'content': review.content
        })
    return jsonify(review_data)
"""
@bp.route('/agent/reviewDetail/<int:review_id>')
def review_detail_index(review_id):
    review = Review.query.filter_by(id=review_id).first()
    return render_template('review/reviewDetailPage.html', review=review)
@bp.route('/api/agent/reviewDetail/<int:review_id>')
def review_detail(review_id):
    # 리뷰 id에 따른 리뷰 디테일 페이지 반환. 리뷰 아이디가 존재하지 않는 다면 에러 페이지 반환.
    review = Review.query.filter_by(id=review_id).first()
    if not review:
        return jsonify({'error': 'The review ID doesn\'t exist'}), 404

    # 본인에 대한 리뷰가 아니면 접속 할 수 없어야 함.
    if g.user.id != review.agent_id:
        return jsonify({'error': 'You do not have permission to access the review detail page.'}), 404

    # 리뷰 디테일 정보를 JSON 형식으로 반환합니다.
    return jsonify({
        'id': review.id,
        'author_userid': review.author_userid,
        'rating': review.rating,
        'content': review.content
    })


'''
bp = Blueprint('view_review_controller', __name__, template_folder='boundary/templates')

@bp.route('/agent/reviews/')
@login_required
@agent_only
def agentViewReviews():
    # 현재 로그인한 사용자(agent)의 id를 사용하여 리뷰를 조회합니다.
    reviews = Review.query.filter_by(agent_id=g.user.id).all()
    return render_template('review/viewReviewList.html', reviews=reviews)


@bp.route('/agent/reviewDetail/<int:review_id>/')
def review_detail(review_id):
    # 리뷰 id에 따른 리뷰 디테일 페이지 반환. 리뷰 아이디가 존재하지 않는 다면 에러 페이지 반환.
    review = Review.query.filter_by(id=review_id).first()
    if not review:
        return render_template('error/error.html',
                               message='The review ID doesn\'t exist'), 404

    # 본인에 대한 리뷰가 아니면 접속 할 수 없어야 함.
    if g.user.id != review.agent_id:
        return render_template('error/error.html',
                               message='You do not have permission to access the review detail page.'), 404

    # 리뷰 디테일 페이지를 렌더링합니다.
    # review_detail.html 템플릿에 review 객체를 전달합니다.
    return render_template('review/reviewDetailPage.html', review=review)
'''
