from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, DateField


class BigRectInfoForm(FlaskForm):
    start_point_x = FloatField('矩形框起始点 x 坐标')
    start_point_y = FloatField('矩形框起始点 y 坐标')
    end_point_x = FloatField('矩形框终止点 x 坐标')
    end_point_y = FloatField('矩形框终止点 y 坐标')
    power_company_province = StringField('省级供电公司')
    power_company_cityorcounty = StringField('市县级供电公司')
    suborlineorzone_name = StringField('变电站（线路、台区）名')
    location_detail = StringField('详细位置')
    location_nature = StringField('地点性质')
    detection_date = DateField('检测日期')
