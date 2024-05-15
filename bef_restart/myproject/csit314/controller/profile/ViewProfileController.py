from flask import Blueprint, render_template
from csit314.entity.User import User
from csit314.app import db
from flask import Blueprint, url_for, render_template, flash, request, redirect, session, g
from csit314.controller.authentication.LoginController import login_required

bp = Blueprint('profile', __name__)

@bp.route('/profile/<userid>/')
@login_required
def profile(userid):
    user = User.query.filter_by(userid=userid).first()
    if not user:
        # error if user doesn't exist
        return render_template('error/error.html', message='User not found'), 404

    return render_template('profile/profile.html', user=user)