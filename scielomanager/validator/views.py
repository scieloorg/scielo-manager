# coding: utf-8
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from django.templatetags.static import static
import packtools
from . import forms
from . import utils

SETTINGS_MAX_UPLOAD_SIZE = settings.VALIDATOR_MAX_UPLOAD_SIZE  # TODO: change to get_settings_or_raise
PACKTOOLS_VERSION = utils.PACKTOOLS_VERSION  # TODO: change to get_settings_or_raise
CSS_URL = static('css/htmlgenerator/styles.css')


def packtools_home(request, template_name='validator/stylechecker.html'):
    context = {
        'SETTINGS_MAX_UPLOAD_SIZE': SETTINGS_MAX_UPLOAD_SIZE,
        'PACKTOOLS_VERSION': PACKTOOLS_VERSION,
    }

    form = forms.XMLUploadForm()
    if request.method == 'POST':
        form = forms.XMLUploadForm(request.POST, request.FILES)
        if form.is_valid():
            xml_file = request.FILES['file']

            if form.cleaned_data.get('add_scielo_br_rules', False):
                extra_sch = packtools.catalogs.SCHEMAS['scielo-br']
            else:
                extra_sch = None

            results, exc = utils.analyze_xml(xml_file,
                    extra_schematron=extra_sch)
            context['results'] = results
            context['xml_exception'] = getattr(exc, 'message', None)

    else:
        form = forms.XMLUploadForm()

    context['form'] = form

    return render_to_response(
        template_name,
        context,
        context_instance=RequestContext(request)
    )


def packtools_preview_html(request, template_name='validator/preview_html.html'):
    context = {
        'SETTINGS_MAX_UPLOAD_SIZE': settings.VALIDATOR_MAX_UPLOAD_SIZE,
        'PACKTOOLS_VERSION': utils.PACKTOOLS_VERSION,
    }

    form = forms.XMLUploadForm()
    if request.method == 'POST':
        form = forms.XMLUploadForm(request.POST, request.FILES)
        if form.is_valid():
            xml_file = request.FILES['file']
            previews = []
            try:
                for lang, html_output in packtools.HTMLGenerator.parse(
                        xml_file, valid_only=False, css=CSS_URL):
                    previews.append({'lang': lang, 'html': html_output})
            except Exception as e:
                print e.message
                # qualquer exeção aborta a pre-visualização mas continua com o resto
                previews = []
            context['previews'] = previews
    else:
        form = forms.XMLUploadForm()

    context['form'] = form

    return render_to_response(
        template_name,
        context,
        context_instance=RequestContext(request)
    )
