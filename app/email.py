from threading import Thread

from flask import current_app, render_template
from flask_mail import Message

from . import mail


def send_async_email(app, msg):
    with app.app_context():     # 确保程序上下文被激活
        mail.send(msg)


def send_mail(to, subject, template, **kwargs):
    """ 使用新线程异步发送邮箱

    :param to: 收件人
    :param subject: 主题
    :param template: 邮件模板
    :param kwargs:
    :return: 执行线程
    """
    app = current_app._get_current_object()
    msg = Message(app.config['FLASK_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASK_MAIL_SENDER'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()
    return thread
