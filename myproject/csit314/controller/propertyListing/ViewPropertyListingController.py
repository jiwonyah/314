from flask import Blueprint, render_template
from csit314.entity.PropertyListing import PropertyListing
from csit314.app import db
from csit314.controller.role_service.decorators import login_required, agent_only, seller_only
from flask import Blueprint, render_template, request, url_for, g, jsonify
from csit314.entity.User import User
from functools import wraps

bp = Blueprint('viewPropertyListing', __name__, template_folder='boundary/templates')

@bp.route('/propertyListing/')
def index():
    propertyListing_table = PropertyListing.query.order_by(PropertyListing.create_date.desc())
    return render_template('property_listing/propertyListingTable.html',
                           propertyListing_table=propertyListing_table)

@bp.route('/propertyListing/detail/<int:propertyListing_id>/')
def detail(propertyListing_id):
    propertyListing = PropertyListing.query.get(propertyListing_id)

    propertyListing.view_counts += 1
    db.session.commit()
    return render_template('property_listing/propertyListingDetailPage.html',
                           propertyListing=propertyListing)


# ----------------------------------private pages-------------------------------------
# 이 페이지는 인증된 유저 본인만 접속할 수 있는 페이지이다.

@bp.route('/agent/history/')
def viewPropertyListingHistory():
    # 현재 로그인한 사용자의 id를 가져옵니다.
    agent_id = g.user.id
    # 해당 사용자가 작성한 모든 PropertyListing을 가져옵니다.
    agent_listings = PropertyListing.query.filter_by(agent_id=agent_id).all()
    return render_template('property_listing/private_page/AgentPropertyListingHistoryPage.html',
                           agent_listings=agent_listings)


@bp.route('/seller/my_property_listing/')
def sellerViewOwnPropertyListing():
    # 현재 로그인한 판매자의 client_id를 가져옴 (예: g.user.client_id로 접근)
    client_id = g.user.userid

    # 해당 client_id에 해당하는 판매자의 매물 목록을 데이터베이스에서 조회
    #propertylistings = PropertyListing.query.filter_by(client_id=client_id).all()
    # ---------------- 정렬 수정 시작 ----------------
    # GET 파라미터에서 정렬 옵션을 가져옴
    sort_by = request.args.get('sort_by', 'recent')

    # 쿼리를 정렬 옵션에 따라 조정
    if sort_by == 'most_viewed':
        propertylistings = PropertyListing.sortByMostView(client_id)
    elif sort_by == 'most_favourited':
        propertylistings = PropertyListing.sortByMostFavourite(client_id)
    else:
        propertylistings = PropertyListing.sortByRecent(client_id)
    # ---------------- 정렬 수정 끝 ----------------

    # 매물 목록을 판매자 매물 목록 페이지로 렌더링하여 표시
    return render_template('property_listing/private_page/SellerPropertyListingPage.html',
                           propertylistings=propertylistings, sort_by=sort_by) # 여기 sort_by=sort_by 추가
