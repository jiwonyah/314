from flask import Blueprint, render_template

bp = Blueprint('calculate_mortgage', __name__, template_folder='boundary/templates')

@bp.route('/mortgage')
def calculateMortgage():
    return render_template('mortgage/calculateMortgage.html')
