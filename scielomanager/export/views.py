from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import redirect

from scielomanager.export import forms
from scielomanager.export import markupfiles


def markup_files(request):

    if request.method == 'POST':

        if 'ahead' in request.POST['issue']:
            year = request.POST['issue'].split(':')[1]
            bundle_url = markupfiles.generate_ahead(request.POST['journal'], year)
            return redirect(bundle_url)
        else:
            form = forms.MarkupFilesForm(request.POST, user=request.user)

            if form.is_valid():
                bundle_url = markupfiles.generate(form.cleaned_data['journal'],
                                                form.cleaned_data['issue'])
                return redirect(bundle_url)

    form = forms.MarkupFilesForm(user=request.user)
    return render_to_response('export/markup_files.html',
                              {'form': form},
                              context_instance=RequestContext(request))
