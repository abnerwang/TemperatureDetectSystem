from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, DateField, FloatField
from wtforms.validators import DataRequired
from wtforms_components import TimeField

from .. import no_co_images


class UploadNoCoImageForm(FlaskForm):
    no_co_image = FileField('未诊断图片', validators=[FileAllowed(no_co_images, '只能上传图片！'), FileRequired('尚未选取图片！')])
    image_num = StringField('图像编号', validators=[DataRequired()])
    power_company_province = StringField('省级供电公司')
    power_company_cityorcountry = StringField('市县级供电公司')
    suborlineorzone_name = StringField('变电站（线路、台区）名')
    location_detail = TextAreaField('详细位置')
    location_nature = TextAreaField('地点性质')
    production_date = DateField('出厂日期')
    run_date = DateField('投运日期')
    detection_date = DateField('检测日期')
    detection_time = TimeField('详细时间')
    report_date = DateField('报告日期')
    instrument_model = StringField('仪器型号')
    instrument_num = StringField('仪器编号')
    reporter = StringField('报告人')
    steward = StringField('负责人')
    inspector = StringField('检测人')
    reviewer = StringField('校阅人')
    auditor = StringField('审核人')
    rated_current = FloatField('额定电流')
    load_current = FloatField('负荷电流')
    voltage_level = FloatField('电压等级')
    weather = StringField('天气')
    emissivity = FloatField('辐射系数')
    wind_speed = FloatField('风速')
    test_distance = FloatField('测试距离')
    max_temp = FloatField('最高温度')
    min_temp = FloatField('最低温度')
    env_temp = FloatField('环境温度')
    env_humi = FloatField('环境湿度')
    device_name = StringField('设备名称')
    device_type = StringField('设备类型')
    interval_name = StringField('间隔名称')
    test_unit = StringField('实验单位')
    test_nature = StringField('检测性质')
