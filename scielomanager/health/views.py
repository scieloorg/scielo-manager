# coding: utf-8
from django.template.context import RequestContext
from django.shortcuts import render_to_response

from health import domain


def home(request):
    status_checker = domain.StatusChecker()

    try:
        statuses = status_checker.overall_status()
        is_fully_operational = status_checker.is_fully_operational
        elapsed_time = status_checker.elapsed_time[2:7]
    except domain.BackendUnavailable as e:
        statuses = None
        is_fully_operational = None
        elapsed_time = None
        is_backend_available = False

    else:
        is_backend_available = True

    return render_to_response(
        'health/overall_status.html',
        {
            'statuses': statuses,
            'is_fully_operational': is_fully_operational,
            'is_backend_available': is_backend_available,
            'elapsed_time': elapsed_time,
        },
        context_instance=RequestContext(request)
    )
