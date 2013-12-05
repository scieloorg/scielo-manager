from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import redirect

from . import forms, markupfile


@login_required
def markup_files(request):

    if request.method == 'POST':

        if 'ahead' in request.POST['issue']:
            year = request.POST['issue'].split(':')[1]
            bundle_url = markupfile.generate_ahead(request.POST['journal'], year)
            return redirect(bundle_url)
        else:
            form = forms.MarkupFilesForm(request.POST, user=request.user)

            if form.is_valid():
                bundle_url = markupfile.generate(form.cleaned_data['journal'],
                                                form.cleaned_data['issue'])
                return redirect(bundle_url)

    form = forms.MarkupFilesForm(user=request.user)
    return render_to_response('export/markup_files.html',
                              {'form': form},
                              context_instance=RequestContext(request))
