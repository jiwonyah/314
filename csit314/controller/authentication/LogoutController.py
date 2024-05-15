from flask import Blueprint, session, jsonify, g

bp = Blueprint('logout', __name__, template_folder='boundary/templates')

@bp.route('/logout/')
def logout():
    if not g.user:
        return jsonify({'success': False, 'message': 'You are already anonymous.'})
    session.pop('user_id', None)
    session.clear()
    return jsonify({'success': True, 'message': 'Logout successful'})
