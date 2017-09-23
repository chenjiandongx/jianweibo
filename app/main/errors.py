from flask import render_template, request, jsonify
from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    """ 使用 app_errorhandler 注册全局 404（网页未找到） 错误处理

    :param e: 接收异常
    """
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        resp = jsonify({'error': 'page not found'})
        resp.status_code = 404
        return resp
    return render_template('404.html'), 404


@main.app_errorhandler(403)
def forbidden(e):
    """ 使用 app_errorhandler 注册全局 403（禁止访问） 错误处理

    :param e: 接收异常
    """
    return render_template('403.html'), 403


@main.app_errorhandler(500)
def internal_server_error(e):
    """ 使用 app_errorhandler 注册全局 500（网络错误） 错误处理

    :param e: 接收异常
    """
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        resp = jsonify({'error': 'internal server error'})
        resp.status_code = 500
        return resp
    return render_template('500.html'), 500
