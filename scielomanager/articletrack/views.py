from articletrack import models
from django.shortcuts import render_to_response
from django.template.context import RequestContext


def attempts_index(request):

    attempts = models.Attempt.objects.all().order_by('-created_at')

    return render_to_response(
        'articletrack/attempts_list.html',
        {
            'attempts': attempts,
        },
        context_instance=RequestContext(request)
    )
