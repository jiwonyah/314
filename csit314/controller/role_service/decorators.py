from flask import g, request, flash, url_for, render_template, jsonify
import functools
from functools import wraps
from werkzeug.utils import redirect
from csit314.entity.User import User, Role

# role-based decorators
# def agent_only(view):
#     @wraps(view)
#     def wrapped_view(*args, **kwargs):
#         # get current user
#         user = g.user
#         # accept access requirement only if when user is authenticated and role is agent
#         if user and user.role.value == 'agent':
#             return view(*args, **kwargs)
#         else:
#             # 인증되지 않은 경우 또는 역할이 'agent'가 아닌 경우 접근 거부
#             return render_template("error/NotAgentAlert.html")  # 로그인 페이지로 리디렉션
#     return wrapped_view

def agent_only(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        # accept access requirement only if when user is authenticated and role is agent
        if g.user.role.value == 'agent':
            return view(*args, **kwargs)
        else:
            return render_template('error/error.html',
                                   message='Available only to agents.'), 403
    return wrapped_view

def buyer_only(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        # accept access requirement only if when user is authenticated and role is agent
        if g.user.role.value == 'buyer':
            return view(*args, **kwargs)
        else:
            return render_template('error/error.html',
                                   message='Available only to buyers.'), 403
    return wrapped_view

def seller_only(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user.role.value == 'seller':
            return view(*args, **kwargs)
        else:
            return render_template('error/error.html',
                                   message='Available only to sellers.'), 403
    return wrapped_view

def buyer_seller_only(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user.role.value == 'buyer' or g.user.role.value == 'seller':
            return view(*args, **kwargs)
        else:
            # 인증되지 않은 경우 또는 역할이 'agent'가 아닌 경우 접근 거부
            return render_template('error/error.html',
                                   message='Available only to buyers and sellers.'), 403
    return wrapped_view


def admin_only(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user.role.value == 'admin':
            return view(*args, **kwargs)
        else:
            # 인증되지 않은 경우 또는 역할이 'agent'가 아닌 경우 접근 거부
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

#login-required
# decorator to protect view which requires login
# def login_required(view):
#     @functools.wraps(view)
#     def wrapped_view(*args, **kwargs):
#         if g.user is None:
#             _next = request.url if request.method == 'GET' else ''
#             flash("To access the page, login first.")
#             return redirect(url_for('login.index', next=_next))
#         return view(*args, **kwargs)
#     return wrapped_view