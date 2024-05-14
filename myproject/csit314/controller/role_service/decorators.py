from flask import g, request, flash, url_for, render_template, jsonify
import functools
from functools import wraps
from werkzeug.utils import redirect

# role-based decorators
def agent_only(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        # get current user
        user = g.user
        # accept access requirement only if when user is authenticated and role is agent
        if user and user.role.value == 'agent':
            return view(*args, **kwargs)
        else:
            # 인증되지 않은 경우 또는 역할이 'agent'가 아닌 경우 접근 거부
            return render_template("error/NotAgentAlert.html")  # 로그인 페이지로 리디렉션
    return wrapped_view

def buyer_seller_only(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        # get current user
        user = g.user
        # accept access requirement only if when user is authenticated and role is agent
        if user.role.value == 'buyer' or user.role.value == 'seller':
            return view(*args, **kwargs)
        else:
            # 인증되지 않은 경우 또는 역할이 'agent'가 아닌 경우 접근 거부
            return render_template('error/error.html',
                                   message='Only Buyer or Seller can write review.'), 404  # 로그인 페이지로 리디렉션
    return wrapped_view

def buyer_only(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        # get current user
        user = g.user
        # accept access requirement only if when user is authenticated and role is agent
        if user.role.value == 'buyer':
            return view(*args, **kwargs)
        else:
            # 인증되지 않은 경우 또는 역할이 'agent'가 아닌 경우 접근 거부
            return render_template('error/error.html',
                                   message='This page is only available for buyer.'), 404  # 로그인 페이지로 리디렉션
    return wrapped_view

def seller_only(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        # get current user
        user = g.user
        # accept access requirement only if when user is authenticated and role is agent
        if user.role.value == 'seller':
            return view(*args, **kwargs)
        else:
            # 인증되지 않은 경우 또는 역할이 'agent'가 아닌 경우 접근 거부
            return render_template('error/error.html',
                                   message='This page is only available for seller.'), 404  # 로그인 페이지로 리디렉션
    return wrapped_view

#login-required
# decorator to protect view which requires login
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            flash("To access the page, login first.")
            return redirect(url_for('login.index', next=_next))
        return view(*args, **kwargs)
    return wrapped_view


# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwagrs):
#         access_token = request.headers.get('Authorization')  # 요청의 토큰 정보를 받아옴
#         if access_token is not None:  # 토큰이 있는 경우
#             payload = check_access_token(access_token)  # 토큰 유효성 확인
#             if payload is None:  # 토큰 decode 실패 시 401 반환
#                 return Response(status=401)
#         else:  # 토큰이 없는 경우 401 반환
#             return Response(status=401)
#
#         return f(*args, **kwagrs)
#
#     return decorated_function