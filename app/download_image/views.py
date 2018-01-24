from . import download_image
from .forms import QueryForm


@download_image.route('/report_query_image', methods=['GET', 'POST'])
def report_query_image():
    form = QueryForm()
    location_nature = form.location_nature.data
    power_company_province = form.power_company_province.data
    power_company_cityorcounty = form.power_company_cityorcounty.data
    suborlineorzone_name = form.suborlineorzone_name.data
    defect_type = form.defect_type.data
    device_type = form.device_type.data
    start_time = form.start_time.data
    end_time = form.end_time.data
