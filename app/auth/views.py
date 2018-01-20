from datetime import datetime

from flask import jsonify, g, current_app, redirect, url_for
from flask_login import login_user, logout_user, login_required
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from . import auth
from .forms import RegistrationForm, LoginForm
from .. import db
from ..decorators import validate_form
from ..email import send_email
from ..models import User


# 处理用户注册
@auth.route('/register', methods=['GET', 'POST'])
@validate_form(form_class=RegistrationForm)  # 处理表单验证的装饰器
def register():
    form = g.form  # 运行到这里的时候，表单验证通过

    # 接下来处理注册逻辑
    username = form.username.data
    password = form.password.data
    email = form.email.data
    telephone = form.telephone.data
    user_desc = form.user_desc.data
    city = form.city.data
    address = form.address.data
    flag = form.flag.data
    create_time = datetime.now()

    user = User(username=username, password=password, email=email, telephone=telephone, user_desc=user_desc, city=city,
                address=address, flag=flag, create_time=create_time)
    db.session.add(user)
    db.session.commit()

    # 发送电子邮件确认信息
    token = user.generate_confirmation_token()
    send_email(user.email, '确认你的账户', 'auth/email/confirm', user=user, token=token)

    if User.query.filter_by(username=username).first():
        return jsonify(code=201, message='注册成功！系统已发送一封邮件到您的邮箱，为了让您忘记密码时能通过邮箱找回密码，请在一小时内前往确认！'), 201
    return jsonify(code=500, message='服务器出现内部错误！'), 500


# 处理电子邮件确认请求
@auth.route('/confirm/<token>')
def confirm(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except:
        return jsonify(code=400, message='参数不正确')
    id = data.get('confirm')
    user = User.query.filter_by(id=id).first()
    if user.confirmed:
        return redirect(url_for('main.index', message='您的账户已经确认过了！'))
    if user.confirm(token):
        return redirect(url_for('main.index', message='谢谢！您已成功激活账户！'))
    else:
        return redirect(url_for('main.index', message='链接无效或过期，请到客户端用户资料页重新发送！'))
    return redirect(url_for('main.index', message='您的账户已经确认过了！'))


# 处理登录
@auth.route('/login', methods=['GET', 'POST'])
@validate_form(form_class=LoginForm)  # 验证登录表单
def login():
    form = g.form
    user = User.query.filter_by(username=form.username.data).first()
    if user is not None and user.verify_password(form.password.data):
        login_user(user)

        if user.last_login_time is not None:
            last_login_time = user.last_login_time
        else:
            last_login_time = '您是第一次登录！'

        # 记录并修改登录时间
        login_time = datetime.now()
        user.last_login_time = login_time
        db.session.add(user)
        db.session.commit()

        return jsonify(code=200, message='登录成功！上次登录时间为：' + str(last_login_time), username=user.username,
                       confirm_status=user.confirmed)
    else:
        return jsonify(code=401, message='用户名或密码错误！')


# 处理登出
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify(code=200, message='成功退出系统！')
