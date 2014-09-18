#coding: utf-8

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _
from django.template.context import RequestContext
from django.forms.models import inlineformset_factory
from django.contrib.auth.decorators import permission_required, user_passes_test

from journalmanager.models import Journal, JournalMission, Issue
from journalmanager.forms import RestrictedJournalForm, JournalMissionForm

from scielomanager.tools import get_paginated
from . import forms
from . import models


def _user_has_access(user):
    return user.is_superuser or user.get_profile().is_editor or user.get_profile().is_librarian

def _get_journals_by_user_access(user):
    user_profile = user.get_profile()
    if user_profile.is_editor:
        journals = Journal.userobjects.active().filter(editor=user)
    elif user_profile.is_librarian or user.is_superuser:
        journals = Journal.userobjects.active()
    else:
        journals = []
    return journals

def _get_journal_or_404_by_user_access(user, journal_id):
    journals = _get_journals_by_user_access(user)
    return get_object_or_404(journals, id=journal_id)

#@permission_required('journalmanager.list_editor_journal', login_url=settings.AUTHZ_REDIRECT_URL)
@user_passes_test(_user_has_access, login_url=settings.AUTHZ_REDIRECT_URL)
def index(request):
    journals = _get_journals_by_user_access(request.user)

    objects = get_paginated(journals, request.GET.get('page', 1))
    context = {
        'objects_journal': objects,
    }
    return render_to_response('journal/journal_list.html', context, context_instance=RequestContext(request))


#@permission_required('journalmanager.list_editor_journal', login_url=settings.AUTHZ_REDIRECT_URL)
@user_passes_test(_user_has_access, login_url=settings.AUTHZ_REDIRECT_URL)
def journal_detail(request, journal_id):
    #journal = get_object_or_404(Journal.userobjects.active().filter(editor=request.user), id=journal_id)
    journal = _get_journal_or_404_by_user_access(request.user, journal_id)
    context = {
        'journal': journal,
    }
    return render_to_response('journal/journal_detail.html', context, context_instance=RequestContext(request))


# @permission_required('journalmanager.list_editor_journal', login_url=settings.AUTHZ_REDIRECT_URL)
@user_passes_test(_user_has_access, login_url=settings.AUTHZ_REDIRECT_URL)
def edit_journal(request, journal_id):
    user_profile = request.user.get_profile()
    if request.user.is_superuser or user_profile.is_librarian:
        # redirect to full edit view:
        return HttpResponseRedirect(reverse('journal.edit', args=[journal_id, ]))

    journal = _get_journal_or_404_by_user_access(request.user, journal_id)

    if journal_id is None:
        journal = Journal()

    JournalMissionFormSet = inlineformset_factory(Journal, JournalMission, form=JournalMissionForm, extra=1, can_delete=True)

    if request.method == "POST":
        journalform = RestrictedJournalForm(request.POST, request.FILES, instance=journal, prefix='journal')
        missionformset = JournalMissionFormSet(request.POST, instance=journal, prefix='mission')

        if journalform.is_valid() and missionformset.is_valid():
            journal = journalform.save()
            missionformset.save()

            messages.success(request, _('Journal updated successfully.'))

            return HttpResponseRedirect(reverse('editorial.index'))
        else:
            messages.error(request, _('Check mandatory fields.'))

    else:
        journalform = RestrictedJournalForm(instance=journal, prefix='journal')
        missionformset = JournalMissionFormSet(instance=journal, prefix='mission')

    return render_to_response('journal/edit_journal.html', {
                              'add_form': journalform,
                              'missionformset': missionformset,
                              }, context_instance=RequestContext(request))


#@permission_required('journalmanager.list_editor_journal', login_url=settings.AUTHZ_REDIRECT_URL)
@user_passes_test(_user_has_access, login_url=settings.AUTHZ_REDIRECT_URL)
def board(request, journal_id):
    journal = _get_journal_or_404_by_user_access(request.user, journal_id)
    issues = journal.issue_set.all().order_by('-publication_year', '-volume', '-number')
    context = {
        'journal': journal,
        'issues': issues,
    }
    return render_to_response('board/board_list.html', context, context_instance=RequestContext(request))


@permission_required('editorialmanager.change_editorialmember', login_url=settings.AUTHZ_REDIRECT_URL)
def edit_board_member(request, journal_id, member_id):
    if request.is_ajax():
        template_name = 'board/board_member_edit_form.html'
    else:
        template_name = 'board/board_member_edit.html'

    # check if user have correct access to view the journal:
    if not Journal.userobjects.active().filter(pk=journal_id).exists():
        messages.error(request, _('The journal is not available for you.'))
        return HttpResponseRedirect(reverse('editorial.index'))

    board_member = get_object_or_404(models.EditorialMember, id=member_id)
    post_url = reverse('editorial.board.edit', args=[journal_id, member_id, ])
    board_url = reverse('editorial.board', args=[journal_id, ])
    context = {
        'board_member': board_member,
        'post_url': post_url,
        'board_url': board_url,
    }

    if request.method == "POST":
        form = forms.EditorialMemberForm(request.POST, instance=board_member)
        if form.is_valid():
            form.save()
            messages.success(request, _('Board Member updated successfully.'))
            return HttpResponseRedirect(board_url)
        else:
            messages.error(request, _('Check mandatory fields.'))
            context['form'] = form
            return render_to_response(template_name, context, context_instance=RequestContext(request))
    else:
        form = forms.EditorialMemberForm(instance=board_member)

    context['form'] = form
    return render_to_response(template_name, context, context_instance=RequestContext(request))


@permission_required('editorialmanager.add_editorialmember', login_url=settings.AUTHZ_REDIRECT_URL)
def add_board_member(request, journal_id, issue_id):
    if request.is_ajax():
        template_name = 'board/board_member_edit_form.html'
    else:
        template_name = 'board/board_member_edit.html'

    # check if user have correct access to view the journal:
    if not Journal.userobjects.active().filter(pk=journal_id).exists():
        messages.error(request, _('The journal is not available for you.'))
        return HttpResponseRedirect(reverse('editorial.index'))

    # get the issue, then the board if exist
    issue = Issue.userobjects.active().filter(pk=issue_id)
    if len(issue) != 1:
        messages.error(request, _('The issue is not available for you.'))
        return HttpResponseRedirect(reverse('editorial.index'))

    issue = issue[0]
    # get the related issue::board, if none: create one
    if not hasattr(issue, 'editorialboard'):
        board = models.EditorialBoard(issue=issue)
        board.save()

    board = issue.editorialboard

    board_url = reverse('editorial.board', args=[journal_id, ])
    post_url = reverse('editorial.board.add', args=[journal_id, issue_id, ])

    context = {
        'post_url': post_url,
        'board_url': board_url,
    }
    if request.method == "POST":
        form = forms.EditorialMemberForm(request.POST)
        if form.is_valid():
            new_member = form.save(commit=False)
            new_member.board = board
            new_member.save()
            messages.info(request, _('Board Member created successfully.'))
            return HttpResponseRedirect(board_url)
        else:
            messages.error(request, _('Check mandatory fields.'))
            context['form'] = form
            return render_to_response(template_name, context, context_instance=RequestContext(request))
    else:
        form = forms.EditorialMemberForm()

    context['form'] = form
    return render_to_response(template_name, context, context_instance=RequestContext(request))


@permission_required('editorialmanager.delete_editorialmember', login_url=settings.AUTHZ_REDIRECT_URL)
def delete_board_member(request, journal_id, member_id):
    # check if user have correct access to view the journal:
    if not Journal.userobjects.active().filter(pk=journal_id).exists():
        messages.error(request, _('The journal is not available for you.'))
        return HttpResponseRedirect(reverse('editorial.index'))

    if request.is_ajax():
        template_name = 'board/board_member_delete_data.html'
    else:
        template_name = 'board/board_member_delete.html'

    board_member = get_object_or_404(models.EditorialMember, id=member_id)
    board_url = reverse('editorial.board', args=[journal_id, ])
    post_url = reverse('editorial.board.delete', args=[journal_id, member_id, ])
    context = {
        'board_member': board_member,
        'post_url': post_url,
        'board_url': board_url,
    }
    if request.method == "POST":
        # record audit log
        board_member.delete()
        messages.success(request, _('Board Member DELETED successfully.'))
        return HttpResponseRedirect(board_url)

    return render_to_response(template_name, context, context_instance=RequestContext(request))
