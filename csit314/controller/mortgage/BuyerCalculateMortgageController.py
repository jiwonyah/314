from flask import Blueprint, render_template, g, jsonify
from csit314.entity.UserAccount import UserAccount    #, Role
from csit314.controller.role_service.decorators import login_required, buyer_only
bp = Blueprint('calculate_mortgage', __name__, template_folder='boundary/templates')

# Calculating mortgage is only for BUYER.
@bp.route('/mortgage')
@login_required
@buyer_only
def calculateMortgage():
    return render_template('mortgage/calculateMortgage.html')