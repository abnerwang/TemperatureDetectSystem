from datetime import datetime

from flask import jsonify, g, current_app, redirect, url_for, render_template
from flask_login import login_user, logout_user, login_required, current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from . import auth
from .forms import RegistrationForm, LoginForm, EmailForResPwd, PasswordResetViaEmailForm, UserInfoForm, \
    ChangePasswordForm, GetUserInfo, ChangeUserPwd
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
    if form.flag.data == '':
        flag = '1'
    else:
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
        return jsonify(code=201, message='注册成功！系统已发送一封邮件到您的邮箱，为了让您忘记密码时能通过邮箱找回密码，'
                                         '请在一小时内前往确认！'), 201
    return jsonify(code=500, message='服务器出现内部错误！'), 500


# 处理电子邮件确认请求
@auth.route('/confirm/<token>')
def confirm(token):
    title = '账户确认'
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except:
        return redirect(url_for('main.index', title=title, message='参数不正确'))
    id = data.get('confirm')
    user = User.query.filter_by(id=id).first()
    if user is not None:
        if user.confirmed:
            return redirect(url_for('main.index', title=title, message='您的账户已经确认过了！'))
        if user.confirm(token):
            return redirect(url_for('main.index', title=title, message='谢谢！您已成功激活账户！'))
    else:
        return redirect(url_for('main.index', title=title, message='链接无效或过期，请到客户端用户资料页重新发送！'))
    return redirect(url_for('main.index', title=title, message='您的账户已经确认过了！'))


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
                       confirm_status=user.confirmed, flag=user.flag), 200
    else:
        return jsonify(code=200, message='用户名或密码错误！'), 200


# 处理登出
@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return jsonify(code=200, message='成功退出系统！'), 200


# 发送电子邮件修改密码
@auth.route('/resPwdViaEmail', methods=['GET', 'POST'])
@validate_form(form_class=EmailForResPwd)
def res_pwd_via_email():
    form = g.form
    email = form.email.data
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify(code=200, message='该邮件尚未注册此系统！请重新输入！'), 200

    token = user.generate_res_pwd_token()
    send_email(email, '重设密码', 'auth/email/reset_password', user=user, token=token)

    return jsonify(code=200, message='系统已向您发送一封邮件用于重设密码，一小时内有效！'), 200


# 重设密码的路由
@auth.route('/resPwdViaEmail/<token>', methods=['GET', 'POST'])
def password_reset(token):
    title = '重设密码'
    form = PasswordResetViaEmailForm()
    if form.validate_on_submit():
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return redirect(url_for('main.index', title=title, message='参数不正确'))
        id = data.get('reset')
        user = User.query.filter_by(id=id).first()
        title = '重设密码'
        if user.reset_password_token(token=token, new_password=form.password.data):
            return redirect(url_for('main.index', title=title, message='重设密码成功！您现在可以用新密码登录系统了！'))
        else:
            return redirect(url_for('main.index', title=title, message='您的链接无效或过期！请到客户端重新发送重设密码邮件！'))
    return render_template('auth/reset_password.html', form=form)


# 返回当前登录用户的基本信息
@auth.route('/currentUserInfo', methods=['GET', 'POST'])
@login_required  # 用户必须先登录
def return_user_info():
    user = current_user
    telephone = user.telephone
    email = user.email
    city = user.city
    address = user.address

    return jsonify(code=200, telephone=telephone, email=email, city=city, address=address), 200


# 修改当前登录用户的基本信息
@auth.route('/changeInfo', methods=['GET', 'POST'])
@login_required  # 用户必须先登录
def change_user_info():
    flag = False  # 用户是否修改了邮箱
    form = UserInfoForm()
    user = current_user
    if form.telephone.data != '':
        user.telephone = form.telephone.data
    if form.email.data != '':
        if form.email.data != user.email:
            user.confirmed = False
            flag = True
        user.email = form.email.data
    if form.city.data != '':
        user.city = form.city.data
    if form.address.data != '':
        user.address = form.address.data

    db.session.add(user)
    db.session.commit()

    if flag:
        # 发送电子邮件确认信息
        token = user.generate_confirmation_token()
        send_email(user.email, '确认你的账户', 'auth/email/confirm', user=user, token=token)
        return jsonify(code=200, message='成功修改信息，系统检测到您修改了邮箱，已自动向新的邮箱发送了账户认证消息，'
                                         '为了您的账户安全，请一小时内前往认证！'), 200

    return jsonify(code=200, message='信息已成功修改!'), 200


# 向用户邮箱重新发送认证消息
@auth.route('/reConfirm', methods=['GET', 'POST'])
@login_required  # 要求用户先登录
def send_recon_info():
    user = current_user
    token = user.generate_confirmation_token()
    send_email(user.email, '确认你的账户', 'auth/email/confirm', user=user, token=token)
    return jsonify(code=200, message='确认邮件已发送成功，请一小时内前往确认，过期无效！'), 200


# 修改当前登录用户的密码
@auth.route('/changePassword', methods=['GET', 'POST'])
@login_required  # 要求用户先登录
def change_password():
    user = current_user
    form = ChangePasswordForm()

    if not user.verify_password(form.old_password.data):
        return jsonify(code=200, message='您输入的旧密码不正确!'), 200

    if user.reset_password(new_password=form.password.data):
        return jsonify(code=200, message='密码修改成功！'), 200


@auth.route('/getUserInfo', methods=['GET', 'POST'])
@validate_form(GetUserInfo)
def get_user_info():
    form = g.form
    username = form.username.data
    user = User.query.filter_by(username=username).first()

    if user is None:
        return jsonify(code=200, message='您所查找的用户不存在，请重新输入！')

    telephone = user.telephone
    email = user.email
    city = user.city
    address = user.address

    return jsonify(code=200, telephone=telephone, email=email, city=city, address=address)


@auth.route('/changePwdViaAdmin', methods=['GET', 'POST'])
@validate_form(ChangeUserPwd)
def change_pwd_via_admin():
    form = g.form
    username = form.username.data
    user = User.query.filter_by(username=username).first()

    if user is None:
        return jsonify(code=200, message='用户不存在，请重新输入！')

    password = form.password.data

    user.reset_password(password)

    return jsonify(code=200, message='您的密码已更改！')
