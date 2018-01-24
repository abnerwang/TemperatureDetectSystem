from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Email, Regexp, EqualTo

from ..models import User


class RegistrationForm(FlaskForm):
    """
    用户注册表单
    """
    username = StringField("Username", validators=[DataRequired()])
    telephone = StringField("Telephone", validators=[Regexp('1[34578][0-9]{9}', message='手机号码格式不正确')])
    city = StringField("City")
    address = StringField("Address")
    email = StringField("Email", validators=[DataRequired(), Email(message="邮箱格式不正确")])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('password2', message='两次输入的密码不一致')])
    password2 = PasswordField("Confirm password",
                              validators=[DataRequired(), EqualTo('password', message='两次输入的密码不一致')])
    user_desc = TextAreaField("User description")
    flag = StringField('User Role')
    submit = SubmitField('Regiser')

    def validate_username(self, field):
        """
        验证用户名是否存在
        :param field: 客户端传来的用户名值
        :return: 是否出错
        """
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已存在')

    def validate_email(self, field):
        """
        验证邮箱是否存在
        :param field: 客户端传来的邮箱值
        :return: 是否出错
        """
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已经注册了')


class LoginForm(FlaskForm):
    """
    用户登录表单
    """
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class EmailForResPwd(FlaskForm):
    """
    输入电子邮件用以重设密码
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')


class PasswordResetViaEmailForm(FlaskForm):
    """
    根据电子邮件重设密码表单
    """
    password = PasswordField('新密码', validators=[DataRequired(), EqualTo('password2', message='两次输入的密码不一致')])
    password2 = PasswordField('确认新密码', validators=[DataRequired(), EqualTo('password', message='两次输入的密码不一致')])
    submit = SubmitField('提交')


class UserInfoForm(FlaskForm):
    """
    修改当前登录用户信息的表单
    """
    telephone = StringField("Telephone")
    email = StringField("Email")
    city = StringField("City")
    address = StringField("Address")
    submit = SubmitField('确认修改')


class ChangePasswordForm(FlaskForm):
    """
    修改当前登录用户密码的表单
    """
    old_password = PasswordField('旧密码')
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('password2', message='两次输入的密码不一致')])
    password2 = PasswordField("Confirm password",
                              validators=[DataRequired(), EqualTo('password', message='两次输入的密码不一致')])
    submit = SubmitField('确认修改')
