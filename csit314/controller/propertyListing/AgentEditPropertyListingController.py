from flask import Blueprint, render_template, request, g, jsonify
from .AgentCreatePropertyListingController import PropertyListingForm
from csit314.entity.PropertyListing import PropertyListing
from werkzeug.utils import redirect
from csit314.controller.role_service.decorators import login_required, agent_only
from datetime import datetime

bp = Blueprint('editPropertyListing', __name__, template_folder='boundary/templates')


@bp.route('/propertyListing/edit/<int:propertyListing_id>/') #methods=['GET']
def index(propertyListing_id):
    propertyListing = PropertyListing.query.get(propertyListing_id)
    if g.user != propertyListing.agent:
        return render_template('error/error.html',
                               message='You don\'t have authority to edit the post.'), 404
    else:
        form = PropertyListingForm(obj=propertyListing)
        return render_template('property_listing/propertyListingEditForm.html', form=form)

@bp.route('/propertyListing/edit/<int:propertyListing_id>/', methods=['POST'])
@login_required
def editPropertyListing(propertyListing_id):
    propertyListing = PropertyListing.query.get(propertyListing_id)
    if not propertyListing:
        return jsonify({'success': False, 'error': 'Property listing not found'}), 404
    form = PropertyListingForm(request.form)
    if form.validate():
        # 요청 데이터에서 수정할 내용 추출
        details = {
            'id': propertyListing_id,
            'subject': form.subject.data,
            'content': form.content.data,
            'price': form.price.data,
            'address': form.address.data,
            'floorSize': form.floorSize.data,
            'floorLevel': form.floorLevel.data,
            'propertyType': form.propertyType.data,
            'furnishing': form.furnishing.data,
            'builtYear': form.builtYear.data,
            'is_sold': form.is_sold.data,  # 요청 데이터에서 is_sold 값 추출
            'client_id': form.client_id.validate,
            'modify_date': datetime.now()  # 수정 날짜 업데이트
        }

        # PropertyListing 수정 시도
        success = PropertyListing.editPropertyListing(details)
        if success:
            return jsonify({'success': True, 'message': 'Property listing updated successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to update property listing'}), 500
    else:
        errors = [{'field': field, 'message': ', '.join(error)} for field, error in form.errors.items()]
        return jsonify({'success': False, 'errors': errors}), 422





