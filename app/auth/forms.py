from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import (DataRequired, Length, Email,
                                EqualTo, ValidationError)

from ..models import User


class LoginForm(FlaskForm):
    """
    登录表单
    """
    email = StringField('邮箱',
                        validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('保持登录状态')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    """
    注册表单
    """
    email = StringField('邮箱',
                        validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名',
                           validators=[DataRequired(), Length(1, 16)])
    password = PasswordField('密码',
                             validators=[DataRequired(), Length(4, 20),
                                         EqualTo('password_confirm',
                                                 message='两次输入密码不一致')])
    password_confirm = PasswordField('密码确认',
                                     validators=[DataRequired(), Length(4, 20)])
    submit = SubmitField('注册')

    def validate_email(self, field):
        """ 验证邮箱是否已被注册。实际上是一个魔法方法。源码中是这样描述的：
            Validates the form by calling `validate` on each field, passing any
        extra `Form.validate_<fieldname>` validators to the field validator.

        :param field: 表单邮箱数据
        """
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册')

    def validate_username(self, field):
        """ 验证用户名是否已被使用。如上，同为魔法方法。

        :param field: 表单用户名数据
        """
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被使用')


class ChangePasswordForm(FlaskForm):
    """
    修改密码表单
    """
    old_password = PasswordField('原密码',
                                 validators=[DataRequired()])
    new_password = PasswordField('新密码',
                                 validators=[DataRequired(), Length(4, 20)])
    submit = SubmitField('提交')
