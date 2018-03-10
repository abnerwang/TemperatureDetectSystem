import os

from flask import jsonify

from . import change_info
from .forms import IDForm, ChangeCoImageForm, ChangeNoCoImageForm
from .. import db
from ..models import CoImage, NoCoImage


@change_info.route('/delete_co_image_info', methods=['GET', 'POST'])
def delete_co_image_info():
    form = IDForm()
    id = form.ID.data

    image = CoImage.query.filter_by(id=id).first()
    matrix_temp_path = image.matrix_temp_path
    original_image_path = image.original_image_path
    clean_image_path = image.clean_image_path
    diagnose_image_path = image.diagnose_image_path

    os.remove(matrix_temp_path)
    os.remove(original_image_path)
    os.remove(clean_image_path)
    os.remove(diagnose_image_path)

    if image.ccd_image_path != '':
        os.remove(image.ccd_image_path)

    db.session.delete(image)
    db.session.commit()

    return jsonify(code=200, message='这条信息已成功删除！'), 200


@change_info.route('/delete_no_co_image_info', methods=['GET', 'POST'])
def delete_no_co_image_info():
    form = IDForm()
    id = form.ID.data

    image = NoCoImage.query.filter_by(id=id).first()
    matrix_temp_path = image.matrix_path
    original_image_path = image.original_image_path

    os.remove(matrix_temp_path)
    os.remove(original_image_path)

    if image.ccd_image_path != '':
        os.remove(image.ccd_image_path)

    db.session.delete(image)
    db.session.commit()

    return jsonify(code=200, message='这条信息已成功删除！'), 200


@change_info.route('/change_co_image_info', methods=['GET', 'POST'])
def change_co_image_info():
    form = ChangeCoImageForm()
    id = form.ID.data

    image = CoImage.query.filter_by(id=id).first()
    image.image_num = form.image_num.data
    image.power_company_province = form.power_company_province.data
    image.power_company_cityorcountry = form.power_company_cityorcounty.data
    image.suborlineorzone_name = form.suborlineorzone_name.data
    image.location_detail = form.location_detail.data
    image.location_nature = form.location_nature.data
    image.production_date = form.production_date.data
    image.run_date = form.run_date.data
    image.detection_date = form.detection_date.data
    image.detection_time = form.detection_time.data
    image.report_date = form.report_date.data
    image.instrument_model = form.instrument_model.data
    image.instrument_num = form.instrument_num.data
    image.reporter = form.reporter.data
    image.principal = form.principal.data
    image.inspector = form.inspector.data
    image.reviewer = form.reviewer.data
    image.auditor = form.auditor.data
    image.rated_current = form.rated_current.data
    image.load_current = form.load_current.data
    image.voltage_level = form.voltage_level.data
    image.weather = form.weather.data
    image.E = form.E.data
    image.wind_speed = form.wind_speed.data
    image.DST = form.DST.data
    image.im_h_tm = form.im_h_tm.data
    image.im_l_tm = form.im_l_tm.data
    image.TATM = form.TATM.data
    image.RH = form.RH.data
    image.device_name = form.device_name.data
    image.device_type = form.device_type.data
    image.trouble_rank = form.trouble_rank.data
    image.diagnose_analyse = form.diagnose_analyse.data
    image.processing_way = form.processing_way.data
    image.rrg_tem = form.rrg_tem.data
    image.hot_mode = form.hot_mode.data
    image.r1_name = form.r1_name.data
    image.r2_name = form.r2_name.data
    image.r3_name = form.r3_name.data
    image.r4_name = form.r4_name.data
    image.r5_name = form.r5_name.data
    image.phase1_name = form.phase1_name.data
    image.phase2_name = form.phase2_name.data
    image.phase3_name = form.phase3_name.data
    image.phase4_name = form.phase4_name.data
    image.phase5_name = form.phase5_name.data
    image.high_tm1 = form.high_tm1.data
    image.high_tm2 = form.high_tm2.data
    image.high_tm3 = form.high_tm3.data
    image.high_tm4 = form.high_tm4.data
    image.high_tm5 = form.high_tm5.data
    image.low_tm1 = form.low_tm1.data
    image.low_tm2 = form.low_tm2.data
    image.low_tm3 = form.low_tm3.data
    image.low_tm4 = form.low_tm4.data
    image.low_tm5 = form.low_tm5.data
    image.re_tm1 = form.re_tm1.data
    image.re_tm2 = form.re_tm2.data
    image.re_tm3 = form.re_tm3.data
    image.re_tm4 = form.re_tm4.data
    image.re_tm5 = form.re_tm5.data
    image.rtd = form.rtd.data
    image.td = form.td.data

    db.session.add(image)
    db.session.commit()

    return jsonify(code=200, message='信息已成功更改！'), 200


@change_info.route('/change_no_co_image_info', methods=['GET', 'POST'])
def change_no_co_image_info():
    form = ChangeNoCoImageForm()
    id = form.ID.data

    image = NoCoImage.query.filter_by(id=id).first()
    image.image_num = form.image_num.data
    image.power_company_province = form.power_company_province.data
    image.power_company_cityorcountry = form.power_company_cityorcounty.data
    image.suborlineorzone_name = form.suborlineorzone_name.data
    image.location_detail = form.location_detail.data
    image.location_nature = form.location_nature.data
    image.production_date = form.production_date.data
    image.run_date = form.run_date.data
    image.detection_date = form.detection_date.data
    image.detection_time = form.detection_time.data
    image.report_date = form.report_date.data
    image.instrument_model = form.instrument_model.data
    image.instrument_num = form.instrument_num.data
    image.reporter = form.reporter.data
    image.steward = form.principal.data
    image.inspector = form.inspector.data
    image.reviewer = form.reviewer.data
    image.auditor = form.auditor.data
    image.rated_current = form.rated_current.data
    image.load_current = form.load_current.data
    image.voltage_level = form.voltage_level.data
    image.weather = form.weather.data
    image.emissivity = form.E.data
    image.wind_speed = form.wind_speed.data
    image.test_distance = form.DST.data
    image.max_temp = form.im_h_tm.data
    image.min_temp = form.im_l_tm.data
    image.env_temp = form.TATM.data
    image.env_humi = form.RH.data
    image.device_name = form.device_name.data
    image.device_type = form.device_type.data
    image.interval_name = form.interval_name.data
    image.test_unit = form.test_unit.data
    image.test_nature = form.test_nature.data

    db.session.add(image)
    db.session.commit()

    return jsonify(code=200, message='信息已成功更改！'), 200
