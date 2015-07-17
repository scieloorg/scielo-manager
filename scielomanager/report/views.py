# coding: utf-8

import json
from django.conf import settings
from django.http import HttpResponse
from django.template import loader, Context
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test

from celery.task.control import revoke
from djcelery import views as celery_views

from django_countries.data import COUNTRIES

from editorialmanager.models import EditorialMember
from journalmanager.models import Collection, SubjectCategory
from scielomanager.tools import get_paginated
from journalmanager import choices

from scielomanager import tasks


def _user_has_access(user):
    return user.get_profile().is_librarian


@login_required
@user_passes_test(_user_has_access, login_url=settings.AUTHZ_REDIRECT_URL)
def report_index(request):
    """
    View to show a list of report available.
    """
    return render_to_response('report/report_list.html',
                              context_instance=RequestContext(request))


@login_required
@user_passes_test(_user_has_access, login_url=settings.AUTHZ_REDIRECT_URL)
def member_list(request):
    """
    View to filter by some atribute of the members in Editorial Board

    Search by: ``collection``, ``country``, ``study_areas`` and ``subject_categories``

    Return a list with the members and start a task to export CSV file if send
    by GET parameter export_csv=true.
    """

    filters = {}

    if request.GET.get('collection'):
        filters['board__issue__journal__collections__in'] = request.GET.getlist('collection')

    if request.GET.get('country'):
        filters['country__in'] = request.GET.getlist('country')

    if request.GET.get('study_area'):
        filters['board__issue__journal__study_areas__study_area__in'] = request.GET.getlist('study_area')

    if request.GET.get('subject_category'):
        filters['board__issue__journal__subject_categories__in'] = request.GET.getlist('subject_category')

    distinct_list = ['first_name', 'last_name', 'email', 'institution', 'city', 'state', 'country']

    if filters:
        members = EditorialMember.objects.order_by('first_name').filter(**filters).distinct(*distinct_list)
    else:
        members = EditorialMember.objects.order_by('first_name').distinct(*distinct_list)

    # Get all itens of filters
    collections = Collection.objects.all()

    study_area = choices.SUBJECTS

    subject_categories = SubjectCategory.objects.all()

    # Start a task to export a CSV file with members
    if request.is_ajax() and request.GET.get('export_csv'):
        context = Context({'members': members})
        res = tasks.export_csv.delay(context,
                                     'editorialmanager/member/export_member_csv.txt',
                                     'download.csv')

        response_data = json.dumps({"task_id": str(res.id)})

        return HttpResponse(response_data, mimetype="application/json")

    objects = get_paginated(members, request.GET.get('page', 1))

    return render_to_response('editorialmanager/member/member_list.html',
                              {'members': objects,
                               'collections': collections,
                               'countries': COUNTRIES,
                               'study_areas': study_area,
                               'subject_categories': subject_categories,
                               'selc_collections': [int(i) for i in request.GET.getlist('collection')],
                               'selc_contries': request.GET.getlist('country'),
                               'selc_study_areas': request.GET.getlist('study_area'),
                               'selc_subject_categories': [int(i) for i in request.GET.getlist('subject_category')]},
                              context_instance=RequestContext(request))


@login_required
@user_passes_test(_user_has_access, login_url=settings.AUTHZ_REDIRECT_URL)
def task_status(request, task_id):
    """
    View to verify the status of the task.

    @param: request (Django request object)
    @param: task_id (Celery auto id, ex.: ``6b363141-d8e4-448a-a622-e9175d99d091``)

    Return a JSON with ``executed`` atribute and the ``id``, ex.:
            {
                task: {
                    executed: true,
                    id: "6b363141-d8e4-448a-a622-e9175d99d091"
                }
            }
    """
    if request.is_ajax():
        return celery_views.is_task_successful(request, task_id)
    else:
        raise Http404("Requested Issue does not exist")


@login_required
@user_passes_test(_user_has_access, login_url=settings.AUTHZ_REDIRECT_URL)
def export_csv(request, task_id):
    """
    View to get the result of task export_csv on Celery.

    @param: request (Django request object)
    @param: task_id (Celery auto id, ex.: ``6b363141-d8e4-448a-a622-e9175d99d091``)

    Return the HTTP Django response, content a CSV format.
    """
    return tasks.export_csv.AsyncResult(task_id).get()
