from flask import Blueprint
from flask_login import current_user

from ..models import Permission

main = Blueprint('main', __name__)


@main.app_context_processor
def inject_global_variable():
    """ 注入全局变量，在 jinja2 模板中可用
    """
    return dict(Permission=Permission,
                current_user=current_user)


from . import views, errors     # 避免循环导入模块
