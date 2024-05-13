from flask import Blueprint, session, url_for, jsonify
from werkzeug.utils import redirect

bp = Blueprint('logout', __name__, template_folder='boundary/templates')

@bp.route('/logout/')
def logout():
    # Delete user information from the session when logging out.
    session.pop('user_id', None)
    session.clear()
    return jsonify({'success': True, 'message': 'Logout successful'})
