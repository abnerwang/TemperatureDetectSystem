from flask_wtf import FlaskForm
from wtforms import StringField, DateField


class QueryForm(FlaskForm):
    location_nature = StringField('地点类型')
    power_company_province = StringField('省级供电公司')
    power_company_cityorcounty = StringField('市县级供电公司')
    suborlineorzone_name = StringField('名称')
    defect_type = StringField('有无故障')
    device_type = StringField('设备类型')
    start_time = DateField('起始时间')
    end_time = DateField('终止时间')
