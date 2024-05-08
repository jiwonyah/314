from flask import Blueprint, render_template
from csit314.entity.PropertyListing import PropertyListing
from csit314.app import db
from csit314.controller.authentication.LoginController import login_required, agent_only
from flask import Blueprint, render_template, request, url_for, g
from csit314.entity.User import User

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

@bp.route('/agent/history/')
@login_required
@agent_only
def viewPropertyListingHistory():
    # 현재 로그인한 사용자의 id를 가져옵니다.
    agent_id = g.user.id
    # 해당 사용자가 작성한 모든 PropertyListing을 가져옵니다.
    agent_listings = PropertyListing.query.filter_by(agent_id=agent_id).all()
    return render_template('property_listing/private_page/AgentPropertyListingHistoryPage.html',
                           agent_listings=agent_listings )

@bp.route('/seller/my_property_listing/')
@login_required
def sellerViewOwnPropertyListing():
    # 현재 로그인한 판매자의 client_id를 가져옴 (예: g.user.client_id로 접근)
    client_id = g.user.userid

    # 해당 client_id에 해당하는 판매자의 매물 목록을 데이터베이스에서 조회
    propertylistings = PropertyListing.query.filter_by(client_id=client_id).all()

    # 매물 목록을 판매자 매물 목록 페이지로 렌더링하여 표시
    return render_template('property_listing/private_page/SellerPropertyListingPage.html',
                           propertylistings=propertylistings)
