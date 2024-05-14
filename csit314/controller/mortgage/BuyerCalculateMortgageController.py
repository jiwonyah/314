from flask import Blueprint, render_template, g, jsonify
from csit314.entity.User import User, Role

bp = Blueprint('calculate_mortgage', __name__, template_folder='boundary/templates')

# Calculating mortgage is only for BUYER.
@bp.route('/mortgage')
def calculateMortgage():
    if not g.user:
        return jsonify(success=False,
                       error='Login required to calculate mortgage.'), 401
    elif g.user.role != Role.BUYER:
        return jsonify(success=False,
                       error='You are not authorized to calculate mortgage.'), 403
    return render_template('mortgage/calculateMortgage.html')