import functools

from flask import request, jsonify, g
from werkzeug.datastructures import MultiDict


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
                return jsonify(code=200, message=form.errors), 200

            g.form = form
            return view_func(*args, **kwargs)

        return inner

    return decorator
