from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class RegistrationForm(FlaskForm):
    """
    用户注册表单
    """
    username = StringField("Username", validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                                         '用户名必须是字字母、数字、'
                                                                                         '点号或下划线的组合')])
    telephone = StringField("Telephone", validators=[Regexp('1[34578][0-9]{9}', message='手机号码格式不正确')])
    city = StringField("City", Length(1, 64))
    address = StringField("Address")
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email(message="邮箱格式不正确")])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('password2', message='两次输入的密码不一致')])
    password2 = PasswordField("Confirm password",
                              validators=[DataRequired(), EqualTo('password', message='两次输入的密码不一致')])
    user_desc = TextField("User description")

    # 缺一个用户角色

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
