from django.shortcuts import render
from django.http import JsonResponse

from organisations.models import NHSgpPractice, OrganisationGeneralPractice


def create_organisation(request):
    header_title = 'Add New Organisation'
    return render(request, 'organisations/create_organisation.html', {
        'header_title': header_title,
    })


def get_nhs_data(request, **kwargs):
    code = request.GET.get('code', '')
    if code:
        nhs_gp = NHSgpPractice.objects.filter(code=code).first()
        if nhs_gp:
            data = {
                'name': nhs_gp.name,
                'address': ' '.join(
                    (
                        nhs_gp.address_line1,
                        nhs_gp.address_line2,
                        nhs_gp.address_line3,
                        nhs_gp.country,
                        nhs_gp.post_code
                     )
                )
            }
        else:
            organisation_gp = OrganisationGeneralPractice.objects.filter(practice_code=code).first()
            data = {
                'name': organisation_gp.trading_name,
                'address': organisation_gp.address
            }

    if kwargs.get('need_dict'):
        return data

    return JsonResponse(data)


def get_nhs_autocomplete(request):
    data = {'items': []}
    search = request.GET.get('search', '')
    if search:
        nhs_gps = NHSgpPractice.objects.filter(name__icontains=search)
        if nhs_gps.exists():
            for nhs_gp in nhs_gps:
                data['items'].append({'id': nhs_gp.code, 'text':nhs_gp.name})

        organisation_gps = OrganisationGeneralPractice.objects.filter(trading_name__icontains=search)
        if organisation_gps.exists():
            for organisation_gp in organisation_gps:
                data['items'].append({'id': organisation_gp.practice_code, 'text': organisation_gp.trading_name})
    return JsonResponse(data)