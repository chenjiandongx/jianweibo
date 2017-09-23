from flask import g
from flask_httpauth import HTTPBasicAuth

from ..models import User, AnonymousUser
from . import api

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    # 没有参数视为匿名用户
    if email_or_token == "":
        g.current_user = AnonymousUser()
        return True
    # 只有一个参数，将该参数视为 token
    if password == "":
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True     # 使用 token 验证
        return g.current_user is not None
    # 两个参数使用邮箱和密码验证
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False        # 使用邮箱和密码验证
    return user.verify_password(password)


@api.before_request
@auth.login_required
def before_request():
    # 确认账户已验证
    if not g.current_user.is_anonymous and not g.current_user.confirmed:
        return 'Unconfirmed account\n'
