from flask import Blueprint, render_template, g, redirect, url_for, request, flash
from csit314.entity.Review import Review
from csit314.entity.User import User, Role
from csit314.app import db

bp = Blueprint('view_review_controller', __name__, template_folder='boundary/templates')

def is_agent():
    # g.user는 현재 로그인한 사용자의 정보를 담고 있다고 가정합니다.
    # 여기서는 사용자 모델에 role 속성이 있다고 가정하며, 해당 역할이 'agent'인지 확인합니다.
    return g.user is not None and g.user.role.value == 'agent'

@bp.route('/myreviews')
def my_reviews():
    if not is_agent():
        return render_template('NotAgentAlert.html'), 403  # NotAgentAlert.html

    # 현재 로그인한 사용자(agent)의 id를 사용하여 리뷰를 조회합니다.
    reviews = Review.query.filter_by(agent_id=g.user.id).all()
    return render_template('viewReviewList.html', reviews=reviews)


@bp.route('/reviewDetail/<int:review_id>')
def review_detail(review_id):
    # 리뷰 ID를 사용하여 리뷰 정보를 조회합니다.
    review = Review.query.get_or_404(review_id)

    # 리뷰 디테일 페이지를 렌더링합니다.
    # review_detail.html 템플릿에 review 객체를 전달합니다.
    return render_template('reviewDetailPage.html', review=review)
