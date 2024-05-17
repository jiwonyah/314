from flask import Blueprint, session, jsonify, g
from csit314.entity.UserAccount import UserAccount

bp = Blueprint('logout', __name__, template_folder='boundary/templates')

@bp.route('/logout/')
def logout():
    if not g.user:
        return jsonify({'success': False, 'message': 'You are already anonymous.'})
    userid = g.user.userid
    userKey = UserAccount.getKey(userid)
    session.pop(userKey, None)
    session.clear()
    return jsonify({'success': True, 'message': 'Logout successful'})
