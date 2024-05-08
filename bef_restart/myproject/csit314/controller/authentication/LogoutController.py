from flask import Blueprint, session, url_for
from werkzeug.utils import redirect

bp = Blueprint('logout', __name__, template_folder='boundary/templates')
@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('index'))