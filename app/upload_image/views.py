import hashlib
import time

from flask import jsonify
from flask_login import login_required, current_user

from . import upload_image
from .forms import UploadNoCoImageForm
from .. import db
from .. import no_co_images
from ..models import NoCoImage


@upload_image.route('/no_co_image', methods=['GET', 'POST'])
@login_required
def upload_no_co_image():
    form = UploadNoCoImageForm()

    if form.validate_on_submit():
        filename = form.no_co_image.data.filename

        # 使用当前登录用户的用户名+时间戳的 MD5 值选择适当长度作为文件名
        name = hashlib.md5((current_user.username + str(time.time())).encode('utf-8')).hexdigest()[:15]
        ext = filename.split('.')[1]

        # 检测图像编号是否存在
        if NoCoImage.query.filter_by(image_num=form.image_num.data) is not None:
            return jsonify(code=409, message='图像编号已存在！请重新输入！')

        filename = no_co_images.save(form.no_co_image.data, name=name + '.')

        image_name = filename
        image_num = form.image_num.data
        power_company_province = form.power_company_province.data
        power_company_cityorcountry = form.power_company_cityorcountry.data
        suborlineorzone_name = form.suborlineorzone_name.data
        location_detail = form.location_detail.data
        location_nature = form.location_nature.data
        original_image_path = no_co_images.path(filename)
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
                                original_image_path=original_image_path,
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

        if NoCoImage.query.filter_by(image_num=image_num).first() and original_image_path is not None:
            return jsonify(code=201, message='图片上传成功！')
        else:
            return jsonify(code=400, message='参数错误，图片上传失败！')
    else:
        return jsonify(code=400, message=form.errors)
