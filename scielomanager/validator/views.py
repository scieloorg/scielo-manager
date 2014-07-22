# coding: utf-8
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from waffle.decorators import waffle_flag

from . import forms
from . import utils

# "http://192.168.1.162:7000/api/v1/article?code=S1516-635X2014000100012&format=xmlrsps"

def __prepare_and_analyze(data_type, data_input):
    """ Normalize input to feed the stylechecker and obtain results """
    results = utils.stylechecker_analyze(data_type, data_input)
    return results


@waffle_flag('packtools_validator')
def packtools_home(request, template_name='validator/packtools.html'):
    context = {
        'SETTINGS_MAX_UPLOAD_SIZE' : settings.VALIDATOR_MAX_UPLOAD_SIZE,
    }

    form = forms.StyleCheckerForm()
    if request.method == 'POST':
        form = forms.StyleCheckerForm(request.POST, request.FILES)
        if form.is_valid():
            type = form.cleaned_data['type']
            if type == 'url':
                url = form.cleaned_data['url']
                results = __prepare_and_analyze(type, url)
            else:
                xml_file = request.FILES['file']
                results = __prepare_and_analyze(type, xml_file)
            context['results'] = results
    else:
        form = forms.StyleCheckerForm()

    context['form'] = form

    return render_to_response(
        template_name,
        context,
        context_instance=RequestContext(request)
    )
