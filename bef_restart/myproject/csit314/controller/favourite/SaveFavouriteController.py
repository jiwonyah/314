from flask import Blueprint, request, jsonify, g
from datetime import datetime
from csit314.app import db
from csit314.entity.Favourite import Favourite
from sqlalchemy.exc import SQLAlchemyError
from csit314.controller.favourite.SellerViewSaveCountController import update_shortlist_count
#from csit314.controller.authentication.LoginController import login_required

bp = Blueprint('save_favourite_controller', __name__, template_folder='boundary/templates')

@bp.route('/toggle_favourite/<int:propertyListing_id>', methods=['POST'])
def toggle_favourite(propertyListing_id):
    # If g.user is not set, it is considered that the user is not logged in.
    if not g.user:
        return jsonify({'success': False, 'error': 'Authentication required'}), 401

    user_id = g.user.userid  # Get user_id from g.user

    try:
        # Check if is is already added into shortlist
        favourite = Favourite.query.filter_by(user_userid=user_id, propertyListing_id=propertyListing_id).first()

        if favourite:
            # Delete from shortlist
            db.session.delete(favourite)
            db.session.commit()
            update_shortlist_count() # Count shortlisted count
            return jsonify({'success': True})
        else:
            # Add to shortlist
            new_favourite = Favourite(user_userid=user_id, propertyListing_id=propertyListing_id,
                                      create_date=datetime.now())
            db.session.add(new_favourite)
            db.session.commit()
            update_shortlist_count()  # Count shortlisted count
            return jsonify({'success': True})

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Database error: ' + str(e)}), 500

'''
@bp.route('/toggle_favourite/<int:propertyListing_id>', methods=['POST'])
def toggle_favourite(propertyListing_id):
    # g.user가 설정되지 않았다면, 로그인하지 않은 것으로 간주
    if not g.user:
        return jsonify({'error': 'Authentication required'}), 401

    user_id = g.user.userid  # g.user에서 user_id를 가져옴

    try:
        # 이미 즐겨찾기에 추가된 항목인지 확인
        favourite = Favourite.query.filter_by(user_userid=user_id, propertyListing_id=propertyListing_id).first()

        if favourite:
            # 즐겨찾기에서 삭제
            db.session.delete(favourite)
            db.session.commit()
            return jsonify({'message': 'Removed from favourites'}), 200
        else:
            # 즐겨찾기에 추가
            new_favourite = Favourite(user_userid=user_id, propertyListing_id=propertyListing_id,
                                      create_date=datetime.now())
            db.session.add(new_favourite)
            db.session.commit()
            return jsonify({'message': 'Added to favourites'}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'message': str(e)}), 500
'''

'''
from flask import Blueprint, render_template, g, redirect, url_for, request, flash, jsonify
from csit314.entity.Review import Review
from csit314.entity.Favourite import Favourite
from csit314.entity.PropertyListing import PropertyListing
from csit314.entity.User import User, Role
from csit314.app import db
from csit314.controller.authentication.LoginController import login_required
bp = Blueprint('save_favourite_controller', __name__, template_folder='boundary/templates')

@bp.route('/toggle_favourite/<int:propertyListing_id>', methods=['POST'])
@login_required
def toggle_favourite(propertyListing_id):
    if g.user is None:
        # 로그인하지 않은 사용자는 에러 메시지 반환
        return jsonify({'error': '로그인이 필요합니다.'}), 401 # 로그인 페이지로 리다이렉트 하게 수정

    property_listing = PropertyListing.query.get_or_404(propertyListing_id)
    favourite = Favourite.query.filter_by(user_userid=g.user.userid, propertyListing_id=propertyListing_id).first()

    if favourite:
        # 이미 즐겨찾기에 있으면 제거
        db.session.delete(favourite)
        db.session.commit()
        return jsonify(result="removed")
    else:
        # 즐겨찾기에 없으면 추가
        new_favourite = Favourite(user_userid=g.user.userid, propertyListing_id=propertyListing_id)
        db.session.add(new_favourite)
        db.session.commit()
        return jsonify(result="added")
'''
