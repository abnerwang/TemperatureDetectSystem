import datetime
import json

from flask import jsonify, send_from_directory, current_app

from . import query_image
from .forms import QueryForm, IDForm
from ..models import CoImage, NoCoImage


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, datetime.time):
            return obj.strftime("%H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


@query_image.route('/co_image_info', methods=['GET', 'POST'])
def query_co_image_info():
    form = QueryForm()
    location_nature = form.location_nature.data
    power_company_province = form.power_company_province.data
    power_company_cityorcounty = form.power_company_cityorcounty.data
    suborlineorzone_name = form.suborlineorzone_name.data
    defect_type = form.defect_type.data
    device_type = form.device_type.data
    start_date = form.start_date.data
    end_date = form.end_date.data

    if location_nature == '所有地点':
        co_image1 = CoImage.query
    else:
        co_image1 = CoImage.query.filter(CoImage.location_nature == location_nature)

    if defect_type == '所有类型':
        co_image2 = co_image1
    else:
        co_image2 = co_image1.filter(CoImage.defect_type == defect_type)

    if device_type == '所有类型':
        co_image3 = co_image2
    else:
        co_image3 = co_image2.filter(CoImage.device_type == device_type)

    if power_company_province == '':
        co_image4 = co_image3
    else:
        co_image4 = co_image3.filter(CoImage.power_company_province == power_company_province)

    if power_company_cityorcounty == '':
        co_image5 = co_image4
    else:
        co_image5 = co_image4.filter(CoImage.power_company_cityorcounty == power_company_cityorcounty)

    if suborlineorzone_name == '':
        co_image6 = co_image5
    else:
        co_image6 = co_image5.filter(CoImage.suborlineorzone_name == suborlineorzone_name)

    images = co_image6.filter(CoImage.detection_date.between(start_date, end_date)).all()

    images_info = []

    for image in images:
        t = {}
        t['ID'] = image.id
        t['安装地点'] = image.location_detail
        t['报告人'] = image.reporter
        t['缺陷性质'] = image.trouble_rank
        t['缺陷类型'] = image.defect_type
        images_info.append(t)

    return jsonify(code=200, data=images_info), 200


@query_image.route('/report_via_id', methods=['GET', 'POST'])
def report_via_id():
    form = IDForm()
    id = form.ID.data

    image = CoImage.query.filter_by(id=id).first()

    image_name = image.image_name
    image_num = image.image_num
    power_company_province = image.power_company_province
    power_company_cityorcountry = image.power_company_cityorcountry
    suborlineorzone_name = image.suborlineorzone_name
    location_detail = image.location_detail
    location_nature = image.location_nature
    production_date = image.production_date
    run_date = image.run_date
    # detection_date = json.dumps(image.detection_date, cls=CJsonEncoder)
    # detection_time = json.dumps(image.detection_time, cls=CJsonEncoder)
    detection_date = image.detection_date.strftime('%Y-%m-%d')
    detection_time = image.detection_time.strftime('%H:%M:%S')
    report_date = image.report_date
    instrument_model = image.instrument_model
    instrument_num = image.instrument_num
    reporter = image.reporter
    principal = image.principal
    inspector = image.inspector
    reviewer = image.reviewer
    auditor = image.auditor
    rated_current = image.rated_current
    load_current = image.load_current
    voltage_level = image.voltage_level
    weather = image.weather
    E = image.E
    wind_speed = image.wind_speed
    DST = image.DST
    im_h_tm = image.im_h_tm
    im_l_tm = image.im_l_tm
    TATM = image.TATM
    RH = image.RH
    device_name = image.device_name
    device_type = image.device_type
    interval_name = image.interval_name
    test_unit = image.test_unit
    test_nature = image.test_nature
    defect_part = image.defect_part
    defect_type = image.defect_type
    trouble_rank = image.trouble_rank
    diagnose_analyse = image.diagnose_analyse
    processing_way = image.processing_way
    rrg_tem = image.rrg_tem
    hot_mode = image.hot_mode
    r1_name = image.r1_name
    r2_name = image.r2_name
    r3_name = image.r3_name
    r4_name = image.r4_name
    r5_name = image.r5_name
    phase1_name = image.phase1_name
    phase2_name = image.phase2_name
    phase3_name = image.phase3_name
    phase4_name = image.phase4_name
    phase5_name = image.phase5_name
    high_tm1 = image.high_tm1
    high_tm2 = image.high_tm2
    high_tm3 = image.high_tm3
    high_tm4 = image.high_tm4
    high_tm5 = image.high_tm5
    low_tm1 = image.low_tm1
    low_tm2 = image.low_tm2
    low_tm3 = image.low_tm3
    low_tm4 = image.low_tm4
    low_tm5 = image.low_tm5
    re_tm1 = image.re_tm1
    re_tm2 = image.re_tm2
    re_tm3 = image.re_tm3
    re_tm4 = image.re_tm4
    re_tm5 = image.re_tm5
    rtd = image.rtd
    td = image.td

    return jsonify(code=200, image_name=image_name, image_num=image_num,
                   power_company_province=power_company_province,
                   power_company_cityorcounty=power_company_cityorcountry,
                   suborlineorzone_name=suborlineorzone_name,
                   location_detail=location_detail, location_nature=location_nature,
                   production_date=production_date,
                   run_date=run_date, detection_date=detection_date, detection_time=detection_time,
                   report_date=report_date,
                   instrument_model=instrument_model, instrument_num=instrument_num, reporter=reporter,
                   principal=principal,
                   inspector=inspector, reviewer=reviewer, auditor=auditor, rated_current=rated_current,
                   load_current=load_current,
                   voltage_level=voltage_level, weather=weather, E=E, wind_speed=wind_speed, DST=DST,
                   im_h_tm=im_h_tm,
                   im_l_tm=im_l_tm, TATM=TATM, RH=RH, device_name=device_name, device_type=device_type,
                   interval_name=interval_name,
                   test_unit=test_unit, test_nature=test_nature, defect_part=defect_part,
                   defect_type=defect_type,
                   trouble_rank=trouble_rank, diagnose_analyse=diagnose_analyse,
                   processing_way=processing_way,
                   rrg_tem=rrg_tem, hot_mode=hot_mode, r1_name=r1_name, r2_name=r2_name, r3_name=r3_name,
                   r4_name=r4_name,
                   r5_name=r5_name, phase1_name=phase1_name, phase2_name=phase2_name,
                   phase3_name=phase3_name, phase4_name=phase4_name,
                   phase5_name=phase5_name, high_tm1=high_tm1, high_tm2=high_tm2, high_tm3=high_tm3,
                   high_tm4=high_tm4,
                   high_tm5=high_tm5, low_tm1=low_tm1, low_tm2=low_tm2, low_tm3=low_tm3, low_tm4=low_tm4,
                   low_tm5=low_tm5,
                   re_tm1=re_tm1, re_tm2=re_tm2, re_tm3=re_tm3, re_tm4=re_tm4, re_tm5=re_tm5, rtd=rtd,
                   td=td), 200


@query_image.route('/export_co_image_via_id', methods=['GET', 'POST'])
def export_co_image_via_id():
    form = IDForm()
    id = form.ID.data

    image = CoImage.query.filter_by(id=id).first()
    image_name = image.image_name

    return send_from_directory(current_app.config['UPLOADED_COIMAGES_DEST'], image_name,
                               as_attachment=True), 200


@query_image.route('/export_ccd_image_via_id', methods=['GET', 'POST'])
def export_ccd_image_via_id():
    form = IDForm()
    id = form.ID.data

    image = CoImage.query.filter_by(id=id).first()
    ccd_image_path = image.ccd_image_path
    if ccd_image_path != '':
        ccd_image_name = ccd_image_path.split('/')[-1]
        return send_from_directory(current_app.config['UPLOADED_CCDIMAGES_DEST'], ccd_image_name,
                                   as_attachment=True), 200
    else:
        return jsonify(code=200, message='您尚未上传此图像相关的可见光图像！'), 200


@query_image.route('/export_co_image_matrix', methods=['GET', 'POST'])
def export_co_image_matrix():
    form = IDForm()
    id = form.ID.data

    image = CoImage.query.filter_by(id=id).first()
    matrix_temp_path = image.matrix_temp_path
    matrix_temp_name = matrix_temp_path.split('/')[-1]
    return send_from_directory(current_app.config['UPLOADED_MATRIXTEMP_DEST'], matrix_temp_name,
                               as_attachment=True), 200


@query_image.route('/no_co_image_info', methods=['GET', 'POST'])
def query_no_co_image_info():
    form = QueryForm()
    location_nature = form.location_nature.data
    power_company_province = form.power_company_province.data
    power_company_cityorcounty = form.power_company_cityorcounty.data
    suborlineorzone_name = form.suborlineorzone_name.data
    defect_type = form.defect_type.data
    device_type = form.device_type.data
    start_date = form.start_date.data
    end_date = form.end_date.data

    if location_nature == '所有地点':
        no_co_image1 = NoCoImage.query
    else:
        no_co_image1 = NoCoImage.query.filter(NoCoImage.location_nature == location_nature)

    if defect_type == '所有类型':
        no_co_image2 = no_co_image1
    else:
        no_co_image2 = no_co_image1.filter(NoCoImage.defect_type == defect_type)

    if device_type == '所有类型':
        no_co_image3 = no_co_image2
    else:
        no_co_image3 = no_co_image2.filter(NoCoImage.device_type == device_type)

    if power_company_province == '':
        no_co_image4 = no_co_image3
    else:
        no_co_image4 = no_co_image3.filter(NoCoImage.power_company_province == power_company_province)

    if power_company_cityorcounty == '':
        no_co_image5 = no_co_image4
    else:
        no_co_image5 = no_co_image4.filter(NoCoImage.power_company_cityorcounty == power_company_cityorcounty)

    if suborlineorzone_name == '':
        no_co_image6 = no_co_image5
    else:
        no_co_image6 = no_co_image5.filter(NoCoImage.suborlineorzone_name == suborlineorzone_name)

    images = no_co_image6.filter(NoCoImage.detection_date.between(start_date, end_date)).all()

    images_info = []

    for image in images:
        t = {}
        t['ID'] = image.id
        t['安装地点'] = image.location_detail
        images_info.append(t)

    return jsonify(code=200, data=images_info), 200


@query_image.route('/export_no_co_image_matrix', methods=['GET', 'POST'])
def export_no_co_image_matrix():
    form = IDForm()
    id = form.ID.data

    image = NoCoImage.query.filter_by(id=id).first()
    matrix_temp_path = image.matrix_path
    matrix_temp_name = matrix_temp_path.split('/')[-1]
    return send_from_directory(current_app.config['UPLOADED_MATRIXTEMP_DEST'], matrix_temp_name,
                               as_attachment=True), 200
