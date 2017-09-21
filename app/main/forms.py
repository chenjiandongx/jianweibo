from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, TextAreaField,
                     BooleanField, SelectField, ValidationError)
from wtforms.validators import DataRequired, Length, Email

from ..models import Role, User


class PostForm(FlaskForm):
    """
    微博发布表单
    """
    body = TextAreaField('此刻的感想？', validators=[DataRequired()])
    submit = SubmitField('发布')


class CommentForm(FlaskForm):
    """
    评论表单
    """
    body = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField('确认')


class EditProfileForm(FlaskForm):
    """
    用户编辑个人信息表单
    """
    realname = StringField('真实姓名', validators=[Length(0, 64)])
    sex = SelectField('性别', choices=[(0, '男'), (1, '女')], coerce=int)
    location = StringField('地区', validators=[Length(0, 64)])
    confirmed = BooleanField('保持登陆')
    about_me = TextAreaField('个人简介')
    submit = SubmitField('提交')


class EditProfileAdminForm(FlaskForm):
    """
    管理员编辑个人信息表单
    """
    emali = StringField('邮件',
                        validators=[DataRequired(),
                                    Length(1, 64),
                                    Email()])
    username = StringField('用户名',
                           validators=[DataRequired(),
                                       Length(1, 16)])
    realname = StringField('真实姓名', validators=[Length(0, 16)])
    sex = SelectField('性别', choices=[(0, '男'), (1, '女')], coerce=int)
    location = StringField('地区', validators=[Length(0, 64)])
    confirmed = BooleanField('保持登陆')
    role = SelectField('角色', coerce=int)
    about_me = TextAreaField('个人简介')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 下拉角色选择列表
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, filed):
        """ 验证邮箱是否已被注册。魔法方法 """
        if filed.data != self.user.email and \
                User.query.filter_by(email=filed.data).first():
            raise ValidationError('该邮箱已经被注册')

    def validate_username(self, filed):
        """ 验证用户名是否已被使用。魔法方法 """
        if filed.data != self.user.username and \
                User.query.filter_by(username=filed.data).first():
            raise ValidationError('该用户名已被使用')
