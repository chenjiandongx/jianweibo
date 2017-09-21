from functools import wraps

from flask import abort
from flask_login import current_user

from .models import Permission


def permission_required(permission):
    """ 权限验证装饰器

    :param permission: 指定权限
    :return: 装饰器
    """
    def decorator(f):
        @wraps(f)
        def inner(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return inner
    return decorator


def admin_required(f):
    """ 管理员权限验证

    :param f: 视图方法
    :return: 装饰器
    """
    return permission_required(Permission.ADMINISTER)(f)
