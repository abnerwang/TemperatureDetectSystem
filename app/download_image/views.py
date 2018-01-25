from . import download_image
from .forms import QueryForm
from ..models import CoImage

from flask import send_from_directory, make_response, jsonify

from .. import co_images, ccd_images


@download_image.route('/report_query_image', methods=['GET', 'POST'])
def report_query_image():
    form = QueryForm()
    location_nature = form.location_nature.data
    power_company_province = form.power_company_province.data
    power_company_cityorcounty = form.power_company_cityorcounty.data
    suborlineorzone_name = form.suborlineorzone_name.data
    defect_type = form.defect_type.data
    device_type = form.device_type.data
    start_date = form.start_date.data
    end_date = form.end_date.data

    images = CoImage.query.filter(CoImage.location_nature == location_nature,
                                  CoImage.power_company_province == power_company_province,
                                  CoImage.power_company_cityorcountry == power_company_cityorcounty,
                                  CoImage.suborlineorzone_name == suborlineorzone_name,
                                  CoImage.defect_type == defect_type, CoImage.device_type == device_type,
                                  CoImage.detection_date.between(start_date, end_date))

    for image in images:
        image_name = image.image_name
        image_num = image.image_num
        power_company_province = image.power_company_province
        power_company_cityorcountry = image.power_company_cityorcountry
        suborlineorzone_name = image.suborlineorzone
        location_detail = image.location_detail
        location_nature = image.location_nature
        production_date = image.production_date
        run_date = image.run_date
        detection_date = image.detection_date
        detection_time = image.detection_time
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

        ccd_image_path = image.ccd_image_path
        ccd_image_name = ccd_image_path.split('/')[-1]

        make_response(send_from_directory(co_images, image_name, as_attachment=True),
                      send_from_directory(ccd_images, ccd_image_name, as_attachment=True),
                      jsonify(code=200, image_name=image_name, image_num=image_num,
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
                              td=td))
