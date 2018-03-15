from flask_wtf import FlaskForm
from wtforms import TextAreaField


class PowerProvinceForm(FlaskForm):
    power_company_province = TextAreaField('省级供电公司名称')


class AddCityCouForm(FlaskForm):
    power_company_province = TextAreaField('市县级供电公司所属省级供电公司名称')
    power_company_cityorcounty = TextAreaField('市县级供电公司名称')


class AddTranOrLineForm(FlaskForm):
    power_company_cityorcounty = TextAreaField('变电站或线路所属的市县级供电公司名称')
    suborlineorzone_name = TextAreaField('变电站或线路名称')


class CityCountyForm(FlaskForm):
    power_company_cityorcounty = TextAreaField('市县级供电公司')


class TransformerOrLineForm(FlaskForm):
    suborlineorzone_name = TextAreaField('变电站或线路名')
