'''
# User Story: As a Seller, I want to be able to view my property listings by the number of times they have been shortlisted by buyers,
#             so that I can understand which properties are generating the most interest.
from flask import Blueprint, g, redirect, url_for, render_template
from csit314.entity.Favourite import Favourite
from csit314.entity.PropertyListing import PropertyListing
from csit314.controller.authentication.LoginController import login_required

bp = Blueprint('view_num_favourite_controller', __name__, template_folder='boundary/templates')

def get_favourite_count(propertyListing_id):
    return Favourite.query.filter_by(propertyListing_id=propertyListing_id).count()


@bp.route('/my_listings')
@login_required
def my_listings():
    if g.user is None:
        return redirect(url_for('login'))  # 로그인이 필요합니다.

    # 현재 로그인한 사용자의 프로퍼티 리스트만 필터링
    my_listings = PropertyListing.query.filter_by(seller_id=g.user.id).all()

    # 각 리스트마다 즐겨찾기 추가된 횟수를 계산
    listings_with_counts = [(listing, get_favourite_count(listing.id)) for listing in my_listings]

    # 즐겨찾기 추가 횟수에 따라 정렬
    sorted_listings = sorted(listings_with_counts, key=lambda x: x[1], reverse=True)

    return render_template('my_listings.html', listings=sorted_listings)
'''
