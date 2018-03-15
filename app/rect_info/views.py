from flask import jsonify

from . import rect_info
from .forms import BigRectInfoForm
from .. import db
from ..models import CoImage, BigRectInformation


@rect_info.route('/big_upload', methods=['GET', 'POST'])
def big_upload():
    form = BigRectInfoForm()
    power_company_province = form.power_company_province.data
    power_company_cityorcounty = form.power_company_cityorcounty.data
    suborlineorzone_name = form.suborlineorzone_name.data
    location_detail = form.location_detail.data
    location_nature = form.location_nature.data
    detection_date = form.detection_date.data
    start_point_x = form.start_point_x.data
    start_point_y = form.start_point_y.data
    end_point_x = form.end_point_x.data
    end_point_y = form.end_point_y.data

    co_image = CoImage.query.filter(CoImage.power_company_province == power_company_province,
                                    CoImage.power_company_cityorcountry == power_company_cityorcounty,
                                    CoImage.suborlineorzone_name == suborlineorzone_name,
                                    CoImage.location_detail == location_detail,
                                    CoImage.location_nature == location_nature,
                                    CoImage.detection_date == detection_date)

    co_image_table_ID = co_image.id

    big_rect = BigRectInformation(co_image_table_ID=co_image_table_ID, start_point_x=start_point_x,
                                  start_point_y=start_point_y, end_point_x=end_point_x, end_point_y=end_point_y)

    db.session.add(big_rect)
    db.session.commit()

    return jsonify(code=200, message='大矩形框信息已成功上传！'), 200
