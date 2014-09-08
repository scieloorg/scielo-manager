#coding: utf-8

from django.conf import settings
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import permission_required


@permission_required('journalmanager.list_editor_journal', login_url=settings.AUTHZ_REDIRECT_URL)
def index(request):
    return render_to_response('journal/journal_list.html', {},
        context_instance=RequestContext(request))


@permission_required('journalmanager.list_editor_journal', login_url=settings.AUTHZ_REDIRECT_URL)
def journal_detail(request):
    return render_to_response('journal/journal_detail.html', {},
        context_instance=RequestContext(request))


@permission_required('journalmanager.list_editor_journal', login_url=settings.AUTHZ_REDIRECT_URL)
def journal_edit(request, journal_id):
    return render_to_response('journal/journal_edit.html', {},
        context_instance=RequestContext(request))


@permission_required('journalmanager.list_editor_journal', login_url=settings.AUTHZ_REDIRECT_URL)
def board(request):
    return render_to_response('board/board_list.html', {},
        context_instance=RequestContext(request))
