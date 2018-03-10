from flask import jsonify, request

from . import upload_image
from .forms import UploadNoCoImageForm, UploadCoImageForm
from .. import db
from .. import no_co_images, co_images, clean_images, ccd_images, matrix_temp, original_images
from ..models import NoCoImage, CoImage


@upload_image.route('/no_co_image', methods=['GET', 'POST'])
def upload_no_co_image():
    """
    上传图片到未诊断库
    :return: 上传是否成功
    """
    form = UploadNoCoImageForm()

    if form.validate_on_submit():
        filename = no_co_images.save(form.no_co_image.data)
        if form.ccd_image.data is None:
            ccd_image_name = ''
        else:
            ccd_image_name = ccd_images.save(form.ccd_image.data)
        matrix_filename = matrix_temp.save(form.matrix_file.data)

        image_name = filename
        image_num = form.image_num.data
        power_company_province = form.power_company_province.data
        power_company_cityorcountry = form.power_company_cityorcountry.data
        suborlineorzone_name = form.suborlineorzone_name.data
        location_detail = form.location_detail.data
        location_nature = form.location_nature.data
        original_image_path = no_co_images.path(filename)
        if ccd_image_name == '':
            ccd_image_path = ''
        else:
            ccd_image_path = ccd_images.path(ccd_image_name)
        matrix_temp_path = matrix_temp.path(matrix_filename)
        production_date = form.production_date.data
        run_date = form.run_date.data
        detection_date = form.detection_date.data
        detection_time = form.detection_time.data
        report_date = form.report_date.data
        instrument_model = form.instrument_model.data
        instrument_num = form.instrument_num.data
        reporter = form.reporter.data
        steward = form.steward.data
        inspector = form.inspector.data
        reviewer = form.reviewer.data
        auditor = form.auditor.data
        rated_current = form.rated_current.data
        load_current = form.load_current.data
        voltage_level = form.voltage_level.data
        weather = form.weather.data
        emissivity = form.emissivity.data
        wind_speed = form.wind_speed.data
        test_distance = form.test_distance.data
        max_temp = form.max_temp.data
        min_temp = form.min_temp.data
        env_temp = form.env_temp.data
        env_humi = form.env_humi.data
        device_name = form.device_name.data
        device_type = form.device_type.data
        interval_name = form.interval_name.data
        test_unit = form.test_unit.data
        test_nature = form.test_nature.data

        no_co_image = NoCoImage(image_name=image_name, image_num=image_num,
                                power_company_province=power_company_province,
                                power_company_cityorcountry=power_company_cityorcountry,
                                suborlineorzone_name=suborlineorzone_name,
                                location_detail=location_detail, location_nature=location_nature,
                                original_image_path=original_image_path, ccd_image_path=ccd_image_path,
                                matrix_path=matrix_temp_path,
                                production_date=production_date, run_date=run_date, detection_date=detection_date,
                                detection_time=detection_time, report_date=report_date,
                                instrument_model=instrument_model,
                                instrument_num=instrument_num, reporter=reporter, steward=steward, inspector=inspector,
                                reviewer=reviewer, auditor=auditor, rated_current=rated_current,
                                load_current=load_current,
                                voltage_level=voltage_level, weather=weather, emissivity=emissivity,
                                wind_speed=wind_speed,
                                test_distance=test_distance, max_temp=max_temp, min_temp=min_temp, env_temp=env_temp,
                                env_humi=env_humi, device_name=device_name, device_type=device_type,
                                interval_name=interval_name,
                                test_unit=test_unit, test_nature=test_nature)
        db.session.add(no_co_image)
        db.session.commit()

        if NoCoImage.query.filter_by(image_name=image_name).first() and original_image_path is not None:
            return jsonify(code=201, message='图片上传成功！'), 201
        else:
            return jsonify(code=400, message='参数错误，图片上传失败！'), 200
    else:
        return jsonify(code=400, message=form.errors), 200


@upload_image.route('/co_image', methods=['GET', 'POST'])
def upload_co_image():
    """
    上传图片到已诊断库
    :return: 上传是否成功
    """
    form = UploadCoImageForm()

    if form.validate_on_submit():
        original_image_name = original_images.save(form.original_image.data)
        clean_image_name = clean_images.save(form.clean_image.data)
        diagnosed_image_name = co_images.save(form.co_image.data)
        if form.ccd_image.data is None:
            ccd_image_name = ''
        else:
            ccd_image_name = ccd_images.save(form.ccd_image.data)
        matrix_filename = matrix_temp.save(form.matrix_file.data)

        image_name = diagnosed_image_name
        image_num = form.image_num.data
        power_company_province = form.power_company_province.data
        power_company_cityorcountry = form.power_company_cityorcountry.data
        suborlineorzone_name = form.suborlineorzone_name.data
        location_detail = form.location_detail.data
        location_nature = form.location_nature.data
        original_image_path = original_images.path(original_image_name)
        clean_image_path = clean_images.path(clean_image_name)
        diagnose_image_path = co_images.path(diagnosed_image_name)
        if ccd_image_name == '':
            ccd_image_path = ''
        else:
            ccd_image_path = ccd_images.path(ccd_image_name)
        matrix_temp_path = matrix_temp.path(matrix_filename)
        production_date = form.production_date.data
        run_date = form.run_date.data
        detection_date = form.detection_date.data
        detection_time = form.detection_time.data
        report_date = form.report_date.data
        instrument_model = form.instrument_model.data
        instrument_num = form.instrument_num.data
        reporter = form.reporter.data
        principal = form.principal.data
        inspector = form.inspector.data
        reviewer = form.reviewer.data
        auditor = form.auditor.data
        rated_current = form.rated_current.data
        load_current = form.load_current.data
        voltage_level = form.voltage_level.data
        weather = form.weather.data
        E = form.E.data
        wind_speed = form.wind_speed.data
        DST = form.DST.data
        im_h_tm = form.im_h_tm.data
        im_l_tm = form.im_l_tm.data
        TATM = form.TATM.data
        RH = form.RH.data
        device_name = form.device_name.data
        device_type = form.device_type.data
        interval_name = form.interval_name.data
        test_unit = form.test_unit.data
        test_nature = form.test_nature.data
        defect_part = form.defect_part.data
        defect_type = form.defect_type.data
        trouble_rank = form.trouble_rank.data
        diagnose_analyse = form.diagnose_analyse.data
        processing_way = form.processing_way.data
        rrg_tem = form.rrg_tem.data
        hot_mode = form.hot_mode.data
        r1_name = form.r1_name.data
        r2_name = form.r2_name.data
        r3_name = form.r3_name.data
        r4_name = form.r4_name.data
        r5_name = form.r5_name.data
        phase1_name = form.phase1_name.data
        phase2_name = form.phase2_name.data
        phase3_name = form.phase3_name.data
        phase4_name = form.phase4_name.data
        phase5_name = form.phase5_name.data
        high_tm1 = form.high_tm1.data
        high_tm2 = form.high_tm2.data
        high_tm3 = form.high_tm3.data
        high_tm4 = form.high_tm4.data
        high_tm5 = form.high_tm5.data
        low_tm1 = form.low_tm1.data
        low_tm2 = form.low_tm2.data
        low_tm3 = form.low_tm3.data
        low_tm4 = form.low_tm4.data
        low_tm5 = form.low_tm5.data
        re_tm1 = form.re_tm1.data
        re_tm2 = form.re_tm2.data
        re_tm3 = form.re_tm3.data
        re_tm4 = form.re_tm4.data
        re_tm5 = form.re_tm5.data
        rtd = form.rtd.data
        td = form.td.data

        image = CoImage.query.filter_by(detection_date=detection_date, power_company_province=power_company_province,
                                        power_company_cityorcountry=power_company_cityorcountry,
                                        suborlineorzone_name=suborlineorzone_name,
                                        location_detail=location_detail).first()

        if image is not None:
            return jsonify(code=200, message='此条信息已存在，请到重新诊断中进行修改！'), 200

        co_image = CoImage(image_name=image_name, image_num=image_num,
                           power_company_province=power_company_province,
                           power_company_cityorcountry=power_company_cityorcountry,
                           suborlineorzone_name=suborlineorzone_name,
                           location_detail=location_detail, location_nature=location_nature,
                           original_image_path=original_image_path,
                           clean_image_path=clean_image_path,
                           diagnose_image_path=diagnose_image_path, ccd_image_path=ccd_image_path,
                           matrix_temp_path=matrix_temp_path,
                           production_date=production_date, run_date=run_date, detection_date=detection_date,
                           detection_time=detection_time, report_date=report_date,
                           instrument_model=instrument_model,
                           instrument_num=instrument_num, reporter=reporter, principal=principal, inspector=inspector,
                           reviewer=reviewer, auditor=auditor, rated_current=rated_current,
                           load_current=load_current,
                           voltage_level=voltage_level, weather=weather, E=E,
                           wind_speed=wind_speed,
                           DST=DST, im_h_tm=im_h_tm, im_l_tm=im_l_tm, TATM=TATM,
                           RH=RH, device_name=device_name, device_type=device_type,
                           interval_name=interval_name,
                           test_unit=test_unit, test_nature=test_nature, defect_part=defect_part,
                           defect_type=defect_type,
                           trouble_rank=trouble_rank,
                           diagnose_analyse=diagnose_analyse, processing_way=processing_way, rrg_tem=rrg_tem,
                           hot_mode=hot_mode,
                           r1_name=r1_name, r2_name=r2_name, r3_name=r3_name, r4_name=r4_name, r5_name=r5_name,
                           phase1_name=phase1_name,
                           phase2_name=phase2_name, phase3_name=phase3_name, phase4_name=phase4_name,
                           phase5_name=phase5_name,
                           high_tm1=high_tm1, high_tm2=high_tm2, high_tm3=high_tm3, high_tm4=high_tm4,
                           high_tm5=high_tm5, low_tm1=low_tm1,
                           low_tm2=low_tm2, low_tm3=low_tm3, low_tm4=low_tm4, low_tm5=low_tm5, re_tm1=re_tm1,
                           re_tm2=re_tm2, re_tm3=re_tm3,
                           re_tm4=re_tm4, re_tm5=re_tm5, rtd=rtd, td=td)
        db.session.add(co_image)
        db.session.commit()

        if CoImage.query.filter_by(image_name=image_name).first() and diagnose_image_path is not None:
            return jsonify(code=201, message='图片上传成功！'), 201
        else:
            return jsonify(code=400, message='参数错误，图片上传失败！'), 200
    else:
        return jsonify(code=400, message=form.errors), 200


@upload_image.route('/multipleNoCoImages', methods=['GET', 'POST'])
def upload_multiple_no_co_images():
    """
    多图上传
    :return: 上传是否成功
    """
    for filename in request.files.getlist('image'):
        no_co_images.save(filename)

    return jsonify(code=200, message='图片上传成功！')
