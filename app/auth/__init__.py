from flask import Blueprint

# 注册 auth 蓝图
auth = Blueprint('auth', __name__)

from . import views
