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
from django.contrib.auth.decorators import permission_required

from journalmanager.models import Journal, JournalMission
from journalmanager.forms import RestrictedJournalForm, JournalMissionForm


@permission_required('journalmanager.list_editor_journal', login_url=settings.AUTHZ_REDIRECT_URL)
def index(request):
    return render_to_response('journal/journal_list.html', {},
        context_instance=RequestContext(request))


@permission_required('journalmanager.list_editor_journal', login_url=settings.AUTHZ_REDIRECT_URL)
def journal_detail(request):
    return render_to_response('journal/journal_detail.html', {},
        context_instance=RequestContext(request))


@permission_required('journalmanager.list_editor_journal', login_url=settings.AUTHZ_REDIRECT_URL)
def edit_journal(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)

    if journal_id is None:
        journal = Journal()
    else:
        journal = get_object_or_404(Journal, id=journal_id)

    JournalMissionFormSet = inlineformset_factory(Journal, JournalMission, form=JournalMissionForm, extra=1, can_delete=True)

    if request.method == "POST":
        journalform = RestrictedJournalForm(request.POST, request.FILES, instance=journal, prefix='journal')
        missionformset = JournalMissionFormSet(request.POST, instance=journal, prefix='mission')

        if journalform.is_valid() and missionformset.is_valid():
            journal = journalform.save()
            missionformset.save()

            messages.info(request, _('Journal updated successfully.'))

            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, _('Check mandatory fields.'))

    else:
        journalform = RestrictedJournalForm(instance=journal, prefix='journal')
        missionformset = JournalMissionFormSet(instance=journal, prefix='mission')

    return render_to_response('journal/edit_journal.html', {
                              'add_form': journalform,
                              'missionformset': missionformset,
                              }, context_instance=RequestContext(request))


@permission_required('journalmanager.list_editor_journal', login_url=settings.AUTHZ_REDIRECT_URL)
def board(request):
    return render_to_response('board/board_list.html', {},
        context_instance=RequestContext(request))
