from articletrack import models
from scielomanager.tools import get_paginated
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import permission_required

AUTHZ_REDIRECT_URL = '/accounts/unauthorized/'


@permission_required('articletrack.list_checkin', login_url=AUTHZ_REDIRECT_URL)
def checkin_index(request):

    checkins = models.Checkin.userobjects.active()

    objects = get_paginated(checkins, request.GET.get('page', 1))

    return render_to_response(
        'articletrack/checkin_list.html',
        {
            'checkins': objects,
        },
        context_instance=RequestContext(request)
    )


@permission_required('articletrack.list_checkin', login_url=AUTHZ_REDIRECT_URL)
def checkin_history(request, articlepkg):

    checkins = models.Checkin.userobjects.active().filter(articlepkg_ref=articlepkg)

    objects = get_paginated(checkins, request.GET.get('page', 1))

    return render_to_response(
        'articletrack/checkin_list_by_package.html',
        {
            'checkins': objects,
        },
        context_instance=RequestContext(request)
    )


@permission_required('articletrack.list_notice', login_url=AUTHZ_REDIRECT_URL)
def notice_detail(request, checkin_id):

    notices = models.Notice.objects.filter(checkin=checkin_id)
    checkin = models.Checkin.userobjects.active().get(id=checkin_id)

    objects = get_paginated(notices, request.GET.get('page', 1))

    return render_to_response(
        'articletrack/notice_detail.html',
        {
            'notices': objects,
            'checkin': checkin
        },
        context_instance=RequestContext(request)
    )
