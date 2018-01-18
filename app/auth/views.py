import functools
from werkzeug.datastructures import MultiDict
from flask import request, jsonify, g
from datetime import datetime

from . import auth
from .forms import RegistrationForm
from ..models import User
from .. import db


def validate_form(form_class):
    """
    处理表单验证的装饰器
    :param form_class: 处理验证的表单类
    :return: 验证结果
    """

    def decorator(view_func):
        @functools.wraps(view_func)
        def inner(*args, **kwargs):
            if request.method == 'GET':
                formdata = request.args
            else:
                if request.json:
                    formdata = MultiDict(request.json)
                else:
                    formdata = request.form
            form = form_class(formdata=formdata)
            if not form.validate():
                return jsonify(code=400, message=form.errors), 400

            g.form = form
            return view_func(*args, **kwargs)

        return inner

    return decorator


@auth.route('/register', methods=['GET', 'POST'])
@validate_form(form_class=RegistrationForm)
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
