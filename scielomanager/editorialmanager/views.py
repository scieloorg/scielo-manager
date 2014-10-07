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
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test

from journalmanager.models import Journal, JournalMission, Issue
from journalmanager.forms import RestrictedJournalForm, JournalMissionForm

from scielomanager.tools import get_paginated, get_users_by_group
from scielomanager import tasks
from audit_log import helpers

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


@login_required
@user_passes_test(_user_has_access, login_url=settings.AUTHZ_REDIRECT_URL)
def index(request):
    journals = _get_journals_by_user_access(request.user)

    objects = get_paginated(journals, request.GET.get('page', 1))
    context = {
        'objects_journal': objects,
    }
    return render_to_response('journal/journal_list.html', context, context_instance=RequestContext(request))


@login_required
@user_passes_test(_user_has_access, login_url=settings.AUTHZ_REDIRECT_URL)
def journal_detail(request, journal_id):
    journal = _get_journal_or_404_by_user_access(request.user, journal_id)
    context = {
        'journal': journal,
    }
    return render_to_response('journal/journal_detail.html', context, context_instance=RequestContext(request))


@login_required
@user_passes_test(_user_has_access, login_url=settings.AUTHZ_REDIRECT_URL)
def edit_journal(request, journal_id):
    """
    Handles only existing journals
    """
    user_profile = request.user.get_profile()
    if request.user.is_superuser or user_profile.is_librarian:
        # redirect to full edit view:
        return HttpResponseRedirect(reverse('journal.edit', args=[journal_id, ]))

    journal = _get_journal_or_404_by_user_access(request.user, journal_id)

    JournalMissionFormSet = inlineformset_factory(Journal, JournalMission, form=JournalMissionForm, extra=1, can_delete=True)

    if request.method == "POST":
        journalform = RestrictedJournalForm(request.POST, request.FILES, instance=journal, prefix='journal')
        missionformset = JournalMissionFormSet(request.POST, instance=journal, prefix='mission')

        # this view only handle existing journals, so always exist previous values.
        audit_old_values = helpers.collect_old_values(journal, journalform, [missionformset,])

        if journalform.is_valid() and missionformset.is_valid():
            journal = journalform.save()
            missionformset.save()

            audit_data = {
                'user': request.user,
                'obj': journal,
                'message': helpers.construct_change_message(journalform, [missionformset, ]),
                'old_values': audit_old_values,
                'new_values': helpers.collect_new_values(journalform, [missionformset, ]),
            }
            # this view only handle existing journals, so always log changes.
            helpers.log_change(**audit_data)

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


@login_required
@user_passes_test(_user_has_access, login_url=settings.AUTHZ_REDIRECT_URL)
def board(request, journal_id):
    journal = _get_journal_or_404_by_user_access(request.user, journal_id)
    issues = journal.issue_set.all().order_by('-publication_year', '-volume', '-number')
    context = {
        'journal': journal,
        'issues': issues,
    }
    return render_to_response('board/board_list.html', context, context_instance=RequestContext(request))


@login_required
@permission_required('editorialmanager.change_editorialmember', login_url=settings.AUTHZ_REDIRECT_URL)
def edit_board_member(request, journal_id, member_id):
    """
    Handles only existing editorial board member
    """

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
        # this view only handle existing editorial board member, so always exist previous values.
        audit_old_values = helpers.collect_old_values(board_member, form)

        if form.is_valid():
            saved_obj = form.save()

            audit_data = {
                'user': request.user,
                'obj': saved_obj,
                'message': helpers.construct_change_message(form),
                'old_values': audit_old_values,
                'new_values': helpers.collect_new_values(form),
            }
            # this view only handle existing editorial board member, so always log changes.
            helpers.log_change(**audit_data)

            if form.has_changed():
                try:
                    users_librarian = get_users_by_group('Librarian')
                except ObjectDoesNotExist:
                    messages.error(request, _("We can not send e-mail to Librarians group"))
                else:
                    tasks.send_mail_by_template.delay(
                        _('Editorial board of %s changed') % saved_obj.board.issue.journal,
                        [user.email for user in users_librarian], 'email/change_editorial_board.txt',
                        {
                            'message': audit_data['message'],
                            'issue': saved_obj.board.issue,
                            'user': request.user
                        })

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


@login_required
@permission_required('editorialmanager.add_editorialmember', login_url=settings.AUTHZ_REDIRECT_URL)
def add_board_member(request, journal_id, issue_id):
    """
    Handles only NEW editorial board member
    """
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

            audit_data = {
                'user': request.user,
                'obj': new_member,
                'message': helpers.construct_create_message(form),
                'old_values': None,
                'new_values': helpers.collect_new_values(form),
            }
            # this view only handle NEW editorial board member, so always log create.
            helpers.log_create(**audit_data)

            if form.has_changed():
                try:
                    users_librarian = get_users_by_group('Librarian')
                except ObjectDoesNotExist:
                    messages.error(request, _("We can not send e-mail to Librarians group"))
                else:
                    tasks.send_mail_by_template.delay(
                        _('New member added to journal %s') % new_member.board.issue.journal,
                        [user.email for user in users_librarian], 'email/add_member_editorial_board.txt',
                        {
                            'message': audit_data['message'],
                            'issue': new_member.board.issue,
                            'user': request.user
                        })


            messages.success(request, _('Board Member created successfully.'))
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
        # save the audit log
        audit_message = helpers.construct_delete_message(board_member)
        helpers.log_delete(request.user, board_member, audit_message)

        try:
            users_librarian = get_users_by_group('Librarian')
        except ObjectDoesNotExist:
            messages.error(request, _("We can not send e-mail to Librarians group"))
        else:

            issue = board_member.board.issue

            tasks.send_mail_by_template.delay(
                _('Editorial member removed from journal %s, issue %s') % (issue.journal, issue),
                [user.email for user in users_librarian], 'email/add_member_editorial_board.txt',
                {
                    'message': "The user %s was deleted from issue %s" % (board_member.get_full_name(), issue),
                    'issue': issue,
                    'user': request.user
                })

        # delete member!
        board_member.delete()

        messages.success(request, _('Board Member DELETED successfully.'))
        return HttpResponseRedirect(board_url)

    return render_to_response(template_name, context, context_instance=RequestContext(request))
