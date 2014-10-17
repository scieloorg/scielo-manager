#coding: utf-8
import logging
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _
from django.template.context import RequestContext
from django.forms.models import inlineformset_factory
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.db.models import Max
from waffle.decorators import waffle_flag

from waffle.decorators import waffle_flag

from journalmanager.models import Journal, JournalMission, Issue
from journalmanager.forms import RestrictedJournalForm, JournalMissionForm

from scielomanager.tools import get_paginated
from audit_log import helpers

from . import forms
from . import models


logger = logging.getLogger(__name__)


def _get_order_for_new_members(board, role_pk, new_member_pk):
    """
    return the value for new members order field.
    - if does not exist other members in board, return 1 (first board member)
    - if does not exist other members with the same role of the new member, return the max order of board + 1 (member with a new role on board)
    - if exist members with the same role, return the order field value of those members.
    """
    # collect all board members except the new one
    board_members = board.editorialmember_set.all().exclude(pk=new_member_pk)
    if board_members.count() > 0:  # already exist others members on this board
        # collect all others board members with the same role as the new members
        members_with_role = board_members.filter(role__pk=role_pk)
        if members_with_role.count() > 0:
            # already exist others members with the same role as the new member
            # the result will be the same order field that those members found
            return members_with_role[0].order
        else:
            # no members with this role, so return the maximum order found + 1
            max_order_of_board = board_members.aggregate(Max('order'))
            return max_order_of_board['order__max'] + 1
    else:
        # no members with this board, this should be the first one
        return 1


def _update_member_order(member, old_role):
    """
    update the @param ``member``'s order attribute, depending on this situations:
    - (A) more than one user with role == ``old_role``, ``member`` is moved to a new role that DOES NOT have any members yet.
    - (B) more than one user with role == ``old_role``, ``member`` is moved to a new role that ALREADY have other members.
    - (C) ``member`` is the last one with role == ``old_role``, ``member`` is moved to a new role that DOES NOT have any members yet.
    - (D) ``member`` is the last one with role == ``old_role``, ``member`` is moved to a new role that ALREADY have other members.
    """
    board = member.board
    board_members = board.editorialmember_set.all()
    members_of_old_role = board_members.filter(role__pk=old_role.pk).exclude(pk=member.pk)
    members_of_new_role = board_members.filter(role__pk=member.role.pk).exclude(pk=member.pk)
    new_order_value = None

    if members_of_old_role.count() == 0:
        # ``member`` WAS the only member with role == old_role
        previous_order = member.order
        if members_of_new_role.count() == 0:
            # ``member`` IS the FIRST member with role == new_role -----> (C)
            max_order_of_board = board_members.aggregate(Max('order'))
            new_order_value = max_order_of_board['order__max'] + 1
        else:
            # there are more members with role == new_role -----> (D)
            new_order_value = members_of_new_role[0].order

        # update member.order to: new_order_value
        member.order = new_order_value
        member.save()

        # decrease order by one, to avoid the empty "bucket" of old_role let by the change
        for m in board.editorialmember_set.filter(order__gte=previous_order):
            m.order = m.order - 1
            m.save()
    else:
        # there are more members with role == old_role
        if members_of_new_role.count() == 0:
            # ``member`` IS the FIRST member with role == new_role -----> (A)
            max_order_of_board = board_members.aggregate(Max('order'))
            new_order_value = max_order_of_board['order__max'] + 1
        else:
            # there are more members with role == new_role  -----> (B)
            new_order_value = members_of_new_role[0].order

        # update member.order to: new_order_value
        member.order = new_order_value
        member.save()


def _update_members_order_when_delete(member_deleted):
    """
    Checks if ``member_deleted`` is the last one of this board member with this role,
    and if any members with an order bigger than ``member_deleted.order`` then update it,
    to decrease the order value by one
    """
    board = member_deleted.board
    other_board_members = board.editorialmember_set.filter(role=member_deleted.role).exclude(pk=member_deleted.pk)
    # after member delete, still more members with this role ?
    if other_board_members.count() == 0:
        # the ``member_deleted`` was the last one of this role, so
        # update all members other greater than ``member_deleted.order`` to decrease 1
        for member in board.editorialmember_set.filter(order__gt=member_deleted.order):
            member.order -= 1
            member.save()


def _do_move_board_block(board_pk, position, direction):
    """
    moves de members the board with pk == board_pk), and with order == position, to direction ``direction`` (up, or down).
    * when direction is up, and have more members above, make a swap, updating member's order attribute.
    * when direction is down, and have more members below, make a swap, updating member's order attribute.
    """
    board = models.EditorialBoard.objects.get(pk=board_pk)

    # creating a list of members to reallocate, becasue simply querysets are lazy
    target_members = [m for m in board.editorialmember_set.filter(order=position)]

    if direction.upper() == "UP":
        position_above = int(position) - 1
        if position_above > 0:
            # move members above to target_members's current position
            board.editorialmember_set.filter(order=position_above).update(order=position)
            # move target_members's position to a higher one
            for m in target_members:
                m.order = position_above
                m.save()

    elif direction.upper() == "DOWN":
        lowest_position_possible = board.editorialmember_set.all().order_by('role__pk').distinct('role__pk').count()
        position_below = int(position) + 1
        if position_below <= lowest_position_possible:
            # move members above to target_members's current position
            board.editorialmember_set.filter(order=position_below).update(order=position)
            # move target_members's position to a lower one
            for m in target_members:
                m.order = position_below
                m.save()
    else:
        # direction is not UP nor DOWN, so, ignore it, do nothing, skip it
        logger.error("Trying to move a board (pk: %s) block (position: %s) in this direction: %s is not possible, so doing nothing!" %  (board_pk, position, direction))


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
@waffle_flag('editorialmanager')
@user_passes_test(_user_has_access, login_url=settings.AUTHZ_REDIRECT_URL)
def index(request):
    journals = _get_journals_by_user_access(request.user)

    objects = get_paginated(journals, request.GET.get('page', 1))
    context = {
        'objects_journal': objects,
    }
    return render_to_response('journal/journal_list.html', context, context_instance=RequestContext(request))


@login_required
@waffle_flag('editorialmanager')
@user_passes_test(_user_has_access, login_url=settings.AUTHZ_REDIRECT_URL)
def journal_detail(request, journal_id):
    journal = _get_journal_or_404_by_user_access(request.user, journal_id)
    context = {
        'journal': journal,
    }
    return render_to_response('journal/journal_detail.html', context, context_instance=RequestContext(request))


@login_required
@waffle_flag('editorialmanager')
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
@waffle_flag('editorialmanager')
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
@waffle_flag('editorialmanager')
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
        old_role = board_member.role
        form = forms.EditorialMemberForm(request.POST, instance=board_member)
        # this view only handle existing editorial board member, so always exist previous values.
        audit_old_values = helpers.collect_old_values(board_member, form)

        if form.is_valid():
            board_member = form.save()
            if 'role' in form.changed_data: # change role -> change order
                _update_member_order(board_member, old_role)

            audit_data = {
                'user': request.user,
                'obj': board_member,
                'message': helpers.construct_change_message(form),
                'old_values': audit_old_values,
                'new_values': helpers.collect_new_values(form),
            }
            # this view only handle existing editorial board member, so always log changes.
            helpers.log_change(**audit_data)
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
@waffle_flag('editorialmanager')
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
            new_member.order = _get_order_for_new_members(new_member.board, new_member.role.pk, new_member.pk)
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


@login_required
@waffle_flag('editorialmanager')
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
        _update_members_order_when_delete(board_member)
        # delete member!
        board_member.delete()
        messages.success(request, _('Board Member DELETED successfully.'))
        return HttpResponseRedirect(board_url)

    return render_to_response(template_name, context, context_instance=RequestContext(request))


@login_required
@waffle_flag('editorialmanager')
@permission_required('editorialmanager.change_editorialmember', login_url=settings.AUTHZ_REDIRECT_URL)
def board_move_block(request, journal_id):
    board_url = reverse('editorial.board', args=[journal_id, ])

    if not Journal.userobjects.active().filter(pk=journal_id).exists():
        messages.error(request, _('The journal is not available for you.'))
        return HttpResponseRedirect(board_url)

    if request.method == "POST":
        # gather data and validate with a form
        data = {
            'journal_pk': request.POST.get("journal_pk", None),
            'issue_pk': request.POST.get("issue_pk", None),
            'board_pk': request.POST.get("board_pk", None),
            'role_name': request.POST.get("role_name", None),
            'role_position': request.POST.get("role_position", None),
            'direction': request.POST.get("direction", None),
        }
        form = forms.BoardMoveForm(data)

        if form.is_valid():
            _do_move_board_block(
                board_pk=data['board_pk'],
                position=data['role_position'],
                direction=data['direction'])

            messages.success(request, _('Board block moved successfully.'))
        else:
            messages.error(request, _('Board block can not be moved'))
            logger.error("Board block can not be moved. form is not valid. Errors: %s" %  form.errors)

    return HttpResponseRedirect(board_url)
