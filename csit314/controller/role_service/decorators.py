from flask import g, request, flash, url_for, render_template, jsonify
import functools
from functools import wraps
from werkzeug.utils import redirect
from csit314.entity.UserAccount import UserAccount  #, Role

def agent_only(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        # accept access requirement only if when user is authenticated and role is agent
        # if g.user.role.value == 'agent':
        if g.user.role == 'agent':
            return view(*args, **kwargs)
        else:
            return render_template('error/error.html',
                                   message='Available only to agents.'), 403
    return wrapped_view

def buyer_only(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        # accept access requirement only if when user is authenticated and role is agent
        #if g.user.role.value == 'buyer':
        if g.user.role == 'buyer':
            return view(*args, **kwargs)
        else:
            return render_template('error/error.html',
                                   message='Available only to buyers.'), 403
    return wrapped_view

def seller_only(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        # if g.user.role.value == 'seller':
        if g.user.role == 'seller':
            return view(*args, **kwargs)
        else:
            return render_template('error/error.html',
                                   message='Available only to sellers.'), 403
    return wrapped_view

def buyer_seller_only(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        # if g.user.role.value == 'buyer' or g.user.role.value == 'seller':
        if g.user.role == 'buyer' or g.user.role == 'seller':
            return view(*args, **kwargs)
        else:
            return render_template('error/error.html',
                                   message='Available only to buyers and sellers.'), 403
    return wrapped_view


def admin_only(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        # if g.user.role.value == 'admin':
        if g.user.role == 'admin':
            return view(*args, **kwargs)
        else:
            return render_template('error/error.html',
                                   message='Available only to admin.'), 403
    return wrapped_view

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user:
            return view(*args, **kwargs)
        else:
            return render_template('error/error.html',
                                   message='Login required'), 401
    return wrapped_view