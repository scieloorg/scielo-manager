# coding: utf-8
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from waffle.decorators import waffle_flag

from . import forms
from . import utils


@waffle_flag('packtools_validator')
def packtools_home(request, template_name='validator/packtools.html'):
    context = {
        'SETTINGS_MAX_UPLOAD_SIZE' : settings.VALIDATOR_MAX_UPLOAD_SIZE,
        'packtools_version': utils.PACKTOOLS_VERSION,
    }

    form = forms.StyleCheckerForm()
    if request.method == 'POST':
        form = forms.StyleCheckerForm(request.POST, request.FILES)
        if form.is_valid():
            type = form.cleaned_data['type']
            if type == 'url':
                xml_file = form.cleaned_data['url']
            else:
                xml_file = request.FILES['file']

            results, exc = utils.analyze_xml(xml_file)
            context['results'] = results
            context['xml_exception'] = getattr(exc, 'message', None)

    else:
        form = forms.StyleCheckerForm()

    context['form'] = form

    return render_to_response(
        template_name,
        context,
        context_instance=RequestContext(request)
    )
