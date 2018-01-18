from datetime import datetime

from flask import jsonify, g

from . import auth
from .forms import RegistrationForm
from .. import db
from ..decorators import validate_form
from ..models import User


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
    create_time = datetime.utcnow()

    user = User(username=username, password=password, email=email, telephone=telephone, user_desc=user_desc, city=city,
                address=address, flag=flag, create_time=create_time)
    db.session.add(user)
    db.session.commit()

    if User.query.filter_by(username=username).first():
        return jsonify(code=200, message='用户注册成功！'), 200
    return jsonify(code=500, message='服务器出现内部错误！'), 500
