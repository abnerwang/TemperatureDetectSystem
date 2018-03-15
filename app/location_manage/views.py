from flask import jsonify

from . import location_manage
from .forms import PowerProvinceForm, AddCityCouForm, AddTranOrLineForm, CityCountyForm, TransformerOrLineForm
from .. import db
from ..models import TranProCompany, TranCityCouCompany, Transformer, LineProCompany, LineCityCouCompany, Line


@location_manage.route('/add_tran_province', methods=['GET', 'POST'])
def add_tran_province():
    form = PowerProvinceForm()
    power_company_province = form.power_company_province.data
    tran_pro_company = TranProCompany(company_name=power_company_province)

    db.session.add(tran_pro_company)
    db.session.commit()

    tran_pro_company = TranProCompany.query.filter_by(company_name=form.power_company_province.data).first()

    if tran_pro_company is not None:
        return jsonify(code=201, message='省级供电公司成功添加！'), 201
    else:
        return jsonify(code=400, message='参数错误！'), 200


@location_manage.route('/add_tran_city_county', methods=['GET', 'POST'])
def add_tran_city_county():
    form = AddCityCouForm()
    tran_city_cou_company = TranCityCouCompany()
    tran_city_cou_company.company_name = form.power_company_cityorcounty.data
    tran_pro_company = form.power_company_province.data
    tran_pro_company = TranProCompany.query.filter_by(company_name=tran_pro_company).first()
    tran_pro_company_id = tran_pro_company.ID
    tran_city_cou_company.father_company = tran_pro_company_id

    db.session.add(tran_city_cou_company)
    db.session.commit()

    tran_city_cou_company = TranCityCouCompany.query.filter_by(
        company_name=form.power_company_cityorcounty.data).first()

    if tran_city_cou_company is not None:
        return jsonify(code=201, message='市县级供电公司成功添加！'), 201
    else:
        return jsonify(code=400, message='参数错误！'), 200


@location_manage.route('/add_transformer', methods=['GET', 'POST'])
def add_transformer():
    form = AddTranOrLineForm()
    transformer = Transformer()
    transformer.trans_name = form.suborlineorzone_name.data
    tran_city_cou_company = form.power_company_cityorcounty.data
    tran_city_cou_company = TranCityCouCompany.query.filter_by(company_name=tran_city_cou_company).first()
    tran_city_cou_company_id = tran_city_cou_company.ID
    transformer.father_company = tran_city_cou_company_id

    db.session.add(transformer)
    db.session.commit()

    transformer = Transformer.query.filter_by(
        trans_name=form.suborlineorzone_name.data).first()

    if transformer is not None:
        return jsonify(code=201, message='变电站添加成功'), 201
    else:
        return jsonify(code=400, message='参数错误！'), 200


@location_manage.route('/get_tran_provinces', methods=['GET', 'POST'])
def get_tran_provinces():
    tran_provinces = TranProCompany.query.all()
    names = []
    for tran_province in tran_provinces:
        names.append(tran_province.company_name)
    return jsonify(code=200, data=names), 200


@location_manage.route('/get_tran_cityorcounty', methods=['GET', 'POST'])
def get_tran_cityorcounty():
    form = PowerProvinceForm()
    power_company_province = form.power_company_province.data
    power_company_province = TranProCompany.query.filter_by(company_name=power_company_province).first()
    power_company_province_id = power_company_province.ID
    cities_or_counties = TranCityCouCompany.query.filter_by(father_company=power_company_province_id).all()
    names = []
    for city_or_county in cities_or_counties:
        names.append(city_or_county.company_name)

    return jsonify(code=200, data=names), 200


@location_manage.route('/get_transformers', methods=['GET', 'POST'])
def get_transformers():
    form = CityCountyForm()
    power_company_cityorcounty = form.power_company_cityorcounty.data
    power_company_cityorcounty = TranCityCouCompany.query.filter_by(company_name=power_company_cityorcounty).first()
    power_company_cityorcounty_id = power_company_cityorcounty.ID
    transformers = Transformer.query.filter_by(father_company=power_company_cityorcounty_id).all()
    names = []
    for transformer in transformers:
        names.append(transformer.trans_name)

    return jsonify(code=200, data=names), 200


@location_manage.route('/del_tran_pro', methods=['GET', 'POST'])
def del_tran_pro():
    form = PowerProvinceForm()
    power_company_province = form.power_company_province.data
    power_company_province = TranProCompany.query.filter_by(company_name=power_company_province).first()
    power_company_province_id = power_company_province.ID

    db.session.delete(power_company_province)

    cities_or_counties = TranCityCouCompany.query.filter_by(father_company=power_company_province_id).all()

    for city_or_county in cities_or_counties:
        city_or_county_id = city_or_county.ID
        db.session.delete(city_or_county)
        transformers = Transformer.query.filter_by(father_company=city_or_county_id).all()
        for transformer in transformers:
            db.session.delete(transformer)

    db.session.commit()

    return jsonify(code=200, message='省级供电公司已成功删除！'), 200


@location_manage.route('/del_tran_cityorcounty', methods=['GET', 'POST'])
def del_tran_cityorcounty():
    form = CityCountyForm()
    power_company_cityorcounty = form.power_company_cityorcounty.data
    power_company_cityorcounty = TranCityCouCompany.query.filter_by(company_name=power_company_cityorcounty).first()
    power_company_cityorcounty_id = power_company_cityorcounty.ID

    db.session.delete(power_company_cityorcounty)

    transformers = Transformer.query.filter_by(father_company=power_company_cityorcounty_id).all()
    for transformer in transformers:
        db.session.delete(transformer)

    db.session.commit()

    return jsonify(code=200, message='市县级供电公司已成功删除！'), 200


@location_manage.route('/del_transformer', methods=['GET', 'POST'])
def del_transformer():
    form = TransformerOrLineForm()
    suborlineorzone_name = form.suborlineorzone_name.data
    transformer = Transformer.query.filter_by(trans_name=suborlineorzone_name).first()
    db.session.delete(transformer)
    db.session.commit()

    return jsonify(code=200, message='变电站已成功删除！'), 200


@location_manage.route('/add_line_province', methods=['GET', 'POST'])
def add_line_province():
    form = PowerProvinceForm()
    power_company_province = form.power_company_province.data
    line_pro_company = LineProCompany(company_name=power_company_province)

    db.session.add(line_pro_company)
    db.session.commit()

    line_pro_company = LineProCompany.query.filter_by(company_name=form.power_company_province.data).first()

    if line_pro_company is not None:
        return jsonify(code=201, message='省级供电公司成功添加！'), 201
    else:
        return jsonify(code=400, message='参数错误！'), 200


@location_manage.route('/add_line_city_county', methods=['GET', 'POST'])
def add_line_city_county():
    form = AddCityCouForm()
    line_city_cou_company = LineCityCouCompany()
    line_city_cou_company.company_name = form.power_company_cityorcounty.data
    line_pro_company = form.power_company_province.data
    line_pro_company = LineProCompany.query.filter_by(company_name=line_pro_company).first()
    line_pro_company_id = line_pro_company.ID
    line_city_cou_company.father_company = line_pro_company_id

    db.session.add(line_city_cou_company)
    db.session.commit()

    line_city_cou_company = LineCityCouCompany.query.filter_by(
        company_name=form.power_company_cityorcounty.data).first()

    if line_city_cou_company is not None:
        return jsonify(code=201, message='市县级供电公司成功添加！'), 201
    else:
        return jsonify(code=400, message='参数错误！'), 200


@location_manage.route('/add_line', methods=['GET', 'POST'])
def add_line():
    form = AddTranOrLineForm()
    line = Line()
    line.line_name = form.suborlineorzone_name.data
    line_city_cou_company = form.power_company_cityorcounty.data
    line_city_cou_company = LineCityCouCompany.query.filter_by(company_name=line_city_cou_company).first()
    line_city_cou_company_id = line_city_cou_company.ID
    line.father_company = line_city_cou_company_id

    db.session.add(line)
    db.session.commit()

    line = Line.query.filter_by(
        line_name=form.suborlineorzone_name.data).first()

    if line is not None:
        return jsonify(code=201, message='线路添加成功'), 201
    else:
        return jsonify(code=400, message='参数错误！'), 200


@location_manage.route('/get_line_provinces', methods=['GET', 'POST'])
def get_line_provinces():
    line_provinces = LineProCompany.query.all()
    names = []
    for line_province in line_provinces:
        names.append(line_province.company_name)
    return jsonify(code=200, data=names), 200


@location_manage.route('/get_line_cityorcounty', methods=['GET', 'POST'])
def get_line_cityorcounty():
    form = PowerProvinceForm()
    power_company_province = form.power_company_province.data
    power_company_province = LineProCompany.query.filter_by(company_name=power_company_province).first()
    power_company_province_id = power_company_province.ID
    cities_or_counties = LineCityCouCompany.query.filter_by(father_company=power_company_province_id).all()

    names = []
    for city_or_county in cities_or_counties:
        names.append(city_or_county.company_name)

    return jsonify(code=200, data=names), 200


@location_manage.route('/get_lines', methods=['GET', 'POST'])
def get_lines():
    form = CityCountyForm()
    power_company_cityorcounty = form.power_company_cityorcounty.data
    power_company_cityorcounty = LineCityCouCompany.query.filter_by(company_name=power_company_cityorcounty).first()
    power_company_cityorcounty_id = power_company_cityorcounty.ID
    lines = Line.query.filter_by(father_company=power_company_cityorcounty_id).all()

    names = []
    for line in lines:
        names.append(line.line_name)

    return jsonify(code=200, data=names), 200


@location_manage.route('/del_line_pro', methods=['GET', 'POST'])
def del_line_pro():
    form = PowerProvinceForm()
    power_company_province = form.power_company_province.data
    power_company_province = LineProCompany.query.filter_by(company_name=power_company_province).first()
    power_company_province_id = power_company_province.ID

    db.session.delete(power_company_province)

    cities_or_counties = LineCityCouCompany.query.filter_by(father_company=power_company_province_id).all()

    for city_or_county in cities_or_counties:
        city_or_county_id = city_or_county.ID
        db.session.delete(city_or_county)
        lines = Line.query.filter_by(father_company=city_or_county_id).all()
        for line in lines:
            db.session.delete(line)

    db.session.commit()

    return jsonify(code=200, message='省级供电公司已成功删除！'), 200


@location_manage.route('/del_line_cityorcounty', methods=['GET', 'POST'])
def del_line_cityorcounty():
    form = CityCountyForm()
    power_company_cityorcounty = form.power_company_cityorcounty.data
    power_company_cityorcounty = LineCityCouCompany.query.filter_by(company_name=power_company_cityorcounty).first()
    power_company_cityorcounty_id = power_company_cityorcounty.ID

    db.session.delete(power_company_cityorcounty)

    lines = Line.query.filter_by(father_company=power_company_cityorcounty_id).all()
    for line in lines:
        db.session.delete(line)

    db.session.commit()

    return jsonify(code=200, message='市县级供电公司已成功删除！'), 200


@location_manage.route('/del_line', methods=['GET', 'POST'])
def del_line():
    form = TransformerOrLineForm()
    suborlineorzone_name = form.suborlineorzone_name.data
    line = Line.query.filter_by(line_name=suborlineorzone_name).first()
    db.session.delete(line)
    db.session.commit()

    return jsonify(code=200, message='线路已成功删除！'), 200
