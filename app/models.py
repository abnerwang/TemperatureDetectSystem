from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(64), unique=True, index=True)
    telephone = db.Column(db.String(12))
    create_time = db.Column(db.DateTime)
    last_login_time = db.Column(db.DateTime)
    user_desc = db.Column(db.Text)
    city = db.Column(db.String(64))
    address = db.Column(db.Text)
    flag = db.Column(db.String(10), default='1')
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password 不是一个可读属性')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        """
        加载用户的回调函数
        :user_id: Unicode 字符串形式表示的用户标志符
        :return: 能找到用户则返回用户对象，否则返回 None
        """
        return User.query.get(int(user_id))

    @login_manager.request_loader
    def load_user_from_request(request):
        username = request.form.get('username')

        return User.query.filter_by(username=username).first()

    def generate_confirmation_token(self, expiration=3600):
        """
        根据用户 id 生成确认邮件用的确认令牌
        :param expiration: 该令牌的有效时间，以秒为单位
        :return: 返回生成的确认令牌
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        """
        电子邮件确认用户账户
        :param token: 确认账户用的令牌
        :return: 用户确认是否成功
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def generate_res_pwd_token(self, expiration=3600):
        """
        生成根据邮箱重设密码用到的 token
        :param expiration: token 的有效时间为一个小时，即 3600 秒
        :return: token
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password_token(self, token, new_password):
        """
        根据电子邮件重设账户密码
        :param token: 用到的验证 token
        :param new_password: 新的密码
        :return: 重设密码是否成功
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        db.session.commit()
        return True

    def reset_password(self, new_password):
        """
        在用户资料页修改密码
        :param new_password: 新的密码
        :return: 密码是否成功修改
        """
        self.password = new_password
        db.session.add(self)
        db.session.commit()
        return True


class NoCoImage(db.Model):
    __tablename__ = 'no_co_images'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    image_name = db.Column(db.String(64), nullable=False)
    image_num = db.Column(db.String(64))
    power_company_province = db.Column(db.String(64))
    power_company_cityorcountry = db.Column(db.String(64))
    suborlineorzone_name = db.Column(db.String(64))
    location_detail = db.Column(db.Text)
    location_nature = db.Column(db.String(10))
    original_image_path = db.Column(db.Text)
    ccd_image_path = db.Column(db.Text)
    matrix_path = db.Column(db.Text)
    production_date = db.Column(db.Date)
    run_date = db.Column(db.Date)
    detection_date = db.Column(db.Date)
    detection_time = db.Column(db.Time)
    instrument_model = db.Column(db.String(20))
    instrument_num = db.Column(db.String(20))
    steward = db.Column(db.String(20))
    inspector = db.Column(db.String(20))
    reviewer = db.Column(db.String(20))
    auditor = db.Column(db.String(20))
    rated_current = db.Column(db.Float)
    load_current = db.Column(db.Float)
    voltage_level = db.Column(db.Float)
    weather = db.Column(db.String(20))
    emissivity = db.Column(db.Float)
    wind_speed = db.Column(db.Float)
    test_distance = db.Column(db.Float)
    max_temp = db.Column(db.Float)
    min_temp = db.Column(db.Float)
    env_temp = db.Column(db.Float)
    env_humi = db.Column(db.Float)
    device_name = db.Column(db.String(50))
    device_type = db.Column(db.String(20))
    interval_name = db.Column(db.String(50))
    test_unit = db.Column(db.String(50))
    test_nature = db.Column(db.String(20))


class CoImage(db.Model):
    __tablename__ = 'co_images'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    image_name = db.Column(db.String(64), nullable=False)
    image_num = db.Column(db.String(64))
    power_company_province = db.Column(db.String(64))
    power_company_cityorcountry = db.Column(db.String(64))
    suborlineorzone_name = db.Column(db.String(64))
    location_detail = db.Column(db.Text)
    location_nature = db.Column(db.String(10))
    original_image_path = db.Column(db.Text)
    clean_image_path = db.Column(db.Text)
    diagnose_image_path = db.Column(db.Text)
    ccd_image_path = db.Column(db.Text)
    matrix_temp_path = db.Column(db.Text)
    production_date = db.Column(db.Date)
    run_date = db.Column(db.Date)
    detection_date = db.Column(db.Date)
    detection_time = db.Column(db.Time)
    report_date = db.Column(db.Date)
    instrument_model = db.Column(db.String(20))
    instrument_num = db.Column(db.String(20))
    reporter = db.Column(db.String(20))
    principal = db.Column(db.String(20))
    inspector = db.Column(db.String(20))
    reviewer = db.Column(db.String(20))
    auditor = db.Column(db.String(20))
    rated_current = db.Column(db.Float)
    load_current = db.Column(db.Float)
    voltage_level = db.Column(db.Float)
    weather = db.Column(db.String(20))
    E = db.Column(db.Float)
    wind_speed = db.Column(db.Float)
    DST = db.Column(db.Float)
    im_h_tm = db.Column(db.Float)
    im_l_tm = db.Column(db.Float)
    TATM = db.Column(db.Float)
    RH = db.Column(db.Float)
    device_name = db.Column(db.String(50))
    device_type = db.Column(db.String(20))
    interval_name = db.Column(db.String(50))
    test_unit = db.Column(db.String(50))
    test_nature = db.Column(db.String(20))
    defect_part = db.Column(db.String(50))
    defect_type = db.Column(db.String(20))
    trouble_rank = db.Column(db.String(20))
    diagnose_analyse = db.Column(db.Text)
    processing_way = db.Column(db.Text)
    rrg_tem = db.Column(db.Float)
    hot_mode = db.Column(db.String(20))
    r1_name = db.Column(db.String(50))
    r2_name = db.Column(db.String(50))
    r3_name = db.Column(db.String(50))
    r4_name = db.Column(db.String(50))
    r5_name = db.Column(db.String(50))
    phase1_name = db.Column(db.String(10))
    phase2_name = db.Column(db.String(10))
    phase3_name = db.Column(db.String(10))
    phase4_name = db.Column(db.String(10))
    phase5_name = db.Column(db.String(10))
    high_tm1 = db.Column(db.Text)
    high_tm2 = db.Column(db.Text)
    high_tm3 = db.Column(db.Text)
    high_tm4 = db.Column(db.Text)
    high_tm5 = db.Column(db.Text)
    low_tm1 = db.Column(db.Text)
    low_tm2 = db.Column(db.Text)
    low_tm3 = db.Column(db.Text)
    low_tm4 = db.Column(db.Text)
    low_tm5 = db.Column(db.Text)
    re_tm1 = db.Column(db.Text)
    re_tm2 = db.Column(db.Text)
    re_tm3 = db.Column(db.Text)
    re_tm4 = db.Column(db.Text)
    re_tm5 = db.Column(db.Text)
    rtd = db.Column(db.Float)
    td = db.Column(db.Float)

# class BigRectInfo(db.Model):
#     co_image_table_ID = db.Column(db.Integer)
#     start_point_x = db.Column(db.Float)
#     start_point_y = db.Column(db.Float)
#     end_point_x = db.Column(db.Float)
#     end_point_y = db.Column(db.Float)
