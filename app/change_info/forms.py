from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField, DateField, FloatField
from wtforms.validators import DataRequired
from wtforms_components import TimeField


class IDForm(FlaskForm):
    ID = IntegerField('图像ID')


class ChangeCoImageForm(FlaskForm):
    """
    修改已诊断图片信息的表单
    """

    ID = IntegerField('图像ID')
    image_num = StringField('图像编号')
    power_company_province = StringField('省级供电公司')
    power_company_cityorcounty = StringField('市县级供电公司')
    suborlineorzone_name = StringField('变电站（线路、台区）名')
    location_detail = TextAreaField('详细位置')
    location_nature = TextAreaField('地点性质')
    production_date = DateField('出厂日期')
    run_date = DateField('投运日期')
    detection_date = DateField('检测日期')
    report_date = DateField('报告日期')
    instrument_model = StringField('仪器型号')
    instrument_num = StringField('仪器编号')
    reporter = StringField('报告人')
    principal = StringField('负责人')
    inspector = StringField('检测人')
    reviewer = StringField('校阅人')
    auditor = StringField('审核人')
    rated_current = FloatField('额定电流')
    load_current = FloatField('负荷电流')
    voltage_level = FloatField('电压等级')
    weather = StringField('天气')
    E = FloatField('辐射系数')
    wind_speed = FloatField('风速')
    DST = FloatField('测试距离')
    TATM = FloatField('环境温度')
    RH = FloatField('环境湿度')
    device_name = StringField('设备名称')
    device_type = StringField('设备类型')
    interval_name = StringField('间隔名称')
    test_unit = StringField('实验单位')
    test_nature = StringField('检测性质')
    defect_part = TextAreaField('缺陷部位')
    defect_type = TextAreaField('缺陷类型')
    trouble_rank = TextAreaField('缺陷等级')
    diagnose_analyse = TextAreaField('诊断分析')
    processing_way = TextAreaField('处理建议')
    hot_mode = TextAreaField('致热类型')


class ChangeNoCoImageForm(FlaskForm):
    """
    更改未诊断图片信息的表单
    """

    ID = IntegerField('图像ID')
    image_num = StringField('图像编号', validators=[DataRequired()])
    power_company_province = StringField('省级供电公司')
    power_company_cityorcounty = StringField('市县级供电公司')
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
    principal = StringField('负责人')
    inspector = StringField('检测人')
    reviewer = StringField('校阅人')
    auditor = StringField('审核人')
    rated_current = FloatField('额定电流')
    load_current = FloatField('负荷电流')
    voltage_level = FloatField('电压等级')
    weather = StringField('天气')
    E = FloatField('辐射系数')
    wind_speed = FloatField('风速')
    DST = FloatField('测试距离')
    im_h_tm = FloatField('最高温度')
    im_l_tm = FloatField('最低温度')
    TATM = FloatField('环境温度')
    RH = FloatField('环境湿度')
    device_name = StringField('设备名称')
    device_type = StringField('设备类型')
    interval_name = StringField('间隔名称')
    test_unit = StringField('实验单位')
    test_nature = StringField('检测性质')
