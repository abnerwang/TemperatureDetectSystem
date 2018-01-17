from . import db


class User(db.Model):
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
    flag = db.Column(db.CHAR)


class NoCoImage(db.Model):
    __tablename__ = 'no_co_images'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    image_name = db.Column(db.String(64), nullable=False)
    image_num = db.Column(db.String(64))
    power_company_province = db.Column(db.String(64))
    power_company_cityorcountry = db.Column(db.String(64))
    suborlineorzone_name = db.Column(db.String(64))
    location_detail = db.Column(db.text)
    location_nature = db.Column(db.String(10))
    original_image_path = db.Column(db.text)
    ccd_image_path = db.Column(db.text)
    matrix_path = db.Column(db.text)
    production_date = db.Column(db.Date)
    run_date = db.Column(db.Date)
    detection_date = db.Column(db.Date)
    detection_time = db.Column(db.Time)
    report_date = db.Column(db.Date)

