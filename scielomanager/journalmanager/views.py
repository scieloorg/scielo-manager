import json
import urllib
from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import loader
from django.template.context import RequestContext
from django.utils.translation import ugettext as _
from django.utils.functional import curry

from scielomanager.journalmanager import models
from scielomanager.journalmanager.forms import *
from scielomanager.tools import get_paginated


MSG_FORM_SAVED = _('Saved.')
MSG_FORM_MISSING = _('There are some errors or missing data.')

def get_user_collections(user_id):

    user_collections = User.objects.get(pk=user_id).usercollections_set.all()

    return user_collections

def index(request):
    t = loader.get_template('journalmanager/home_journal.html')
    if request.user.is_authenticated():
        user_collections = get_user_collections(request.user.id)
    else:
        user_collections = ""

    c = RequestContext(request,{'user_collections':user_collections,})
    return HttpResponse(t.render(c))

@login_required
def generic_index_search(request, model, journal_id = None):
    """
    Generic list and search
    """
    user_collections = get_user_collections(request.user.id)
    default_collections = user_collections.filter(is_default=True)

    if journal_id:
        journal = models.Journal.objects.get(pk=journal_id)
        objects_all = model.objects.available(request.GET.get('is_available')).filter(journal=journal_id)
    else:
        journal = None
        objects_all = model.objects.available(request.GET.get('is_available'))

    if request.GET.get('q'):
        if model is models.Publisher:
            objects_all = model.objects.available(request.GET.get('is_available')).filter(name__icontains = request.REQUEST['q']).order_by('name')

        if model is models.Journal:
            objects_all = model.objects.available(request.GET.get('is_available')).filter(title__icontains = request.REQUEST['q']).order_by('title')

        if model is models.Center:
            objects_all = model.objects.available(request.GET.get('is_available')).filter(name__icontains = request.REQUEST['q']).order_by('name')

    if objects_all.count() == 0:
        messages.error(request, _('Your search did not match any documents.'))

    objects = get_paginated(objects_all, request.GET.get('page', 1))

    template = loader.get_template('journalmanager/%s_dashboard.html' % model.__name__.lower())

    context = RequestContext(request, {
                       'objects_%s' %  model.__name__.lower(): objects,
                       'journal': journal,
                       'user_collections': user_collections,
                       })
    return HttpResponse(template.render(context))

@login_required
def generic_toggle_availability(request, object_id, model):

  if request.is_ajax():

    model = get_object_or_404(model, pk = object_id)
    model.is_available = not model.is_available
    model.save()

    response_data = json.dumps({
      "result": str(model.is_available),
      "object_id": model.id
      })

    #ajax response json
    return HttpResponse(response_data, mimetype="application/json")
  else:
    #bad request
    return HttpResponse(status=400)

@login_required
def generic_bulk_action(request, model, action_name, value = None):

    if request.method == 'POST':
        items = request.POST.getlist('action')
        for item in items:
            model = get_object_or_404(model, pk = item)
            if action_name == 'is_available':
                model.is_available = int(value)
                model.save()

    return HttpResponseRedirect(reverse('journal.index') + '?' + urllib.urlencode(request.GET))

@login_required
def user_index(request):

    user_collections = get_user_collections(request.user.id)
    user_collections_managed = user_collections.filter(is_manager=True)

    # Filtering users manager by the administrator
    all_users = models.User.objects.filter(usercollections__collection__in = ( collection.collection.pk for collection in user_collections_managed )).distinct('username')
    users = get_paginated(all_users, request.GET.get('page', 1))

    t = loader.get_template('journalmanager/user_dashboard.html')

    c = RequestContext(request, {
                       'users': users,
                       'user_collections': user_collections,
                       })
    return HttpResponse(t.render(c))

def user_login(request):

    next = request.GET.get('next', None)

    if request.method == 'POST':
        next = request.POST['next']
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                user_collections = get_user_collections(request.user.id)

                if next != '':
                    return HttpResponseRedirect(next)
                else:
                    t = loader.get_template('journalmanager/home_journal.html')
                c = RequestContext(request, {'active': True,
                                             'user_collections': user_collections,})
                return HttpResponse(t.render(c))
            else: #Login Success User inactive
                t = loader.get_template('journalmanager/home_journal.html')
                c = RequestContext(request, {'active': True,})
                return HttpResponse(t.render(c))
        else: #Login Failed
            t = loader.get_template('journalmanager/home_journal.html')
            c = RequestContext(request, {
                               'invalid': True, 'next': next,})
            return HttpResponse(t.render(c))
    else:
        t = loader.get_template('journalmanager/home_journal.html')
        if next:
            c = RequestContext(request, {'required': True, 'next': next,})
        return HttpResponse(t.render(c))

@login_required
def user_logout(request):
    logout(request)
    t = loader.get_template('journalmanager/home_journal.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))

@login_required
@permission_required('auth.add_user')
def add_user(request, user_id=None):
    """
    Handles new and existing users
    """
    if  user_id == None:
        user = User()
    else:
        user = get_object_or_404(User, id = user_id)

    # Getting Collections from the logged user.
    user_collections = get_user_collections(request.user.id)

    UserProfileFormSet = inlineformset_factory(User, models.UserProfile, )
    UserCollectionsFormSet = inlineformset_factory(User, models.UserCollections,
        form=UserCollectionsForm, extra=1, can_delete=True)

    if request.method == 'POST':
        userform = UserForm(request.POST, instance=user, prefix='user')
        userprofileformset = UserProfileFormSet(request.POST, instance=user, prefix='userprofile',)
        usercollectionsformset = UserCollectionsFormSet(request.POST, instance=user, prefix='usercollections',)

        if userform.is_valid() and userprofileformset.is_valid() and usercollectionsformset.is_valid():
            userform.save()
            userprofileformset.save()
            usercollectionsformset.save()

            messages.info(request, MSG_FORM_SAVED)
            return HttpResponseRedirect(reverse('user.index'))
        else:
            messages.error(request, MSG_FORM_MISSING)
    else:
        userform  = UserForm(instance=user, prefix='user')
        userprofileformset = UserProfileFormSet(instance=user, prefix='userprofile',)
        usercollectionsformset = UserCollectionsFormSet(instance=user, prefix='usercollections',)

    return render_to_response('journalmanager/add_user.html', {
                              'add_form': userform,
                              'mode': 'user_journal',
                              'user_name': request.user.pk,
                              'user_collections': user_collections,
                              'usercollectionsformset': usercollectionsformset,
                              'userprofileformset': userprofileformset
                              },
                              context_instance=RequestContext(request))

@login_required
def add_journal(request, journal_id = None):
    """
    Handles new and existing journals
    """

    user_collections = get_user_collections(request.user.id)

    if  journal_id is None:
        journal = models.Journal()
    else:
        journal = get_object_or_404(models.Journal, id = journal_id)

    JournalTitleFormSet = inlineformset_factory(models.Journal, models.JournalTitle, form=JournalTitleForm, extra=1, can_delete=True)
    JournalStudyAreaFormSet = inlineformset_factory(models.Journal, models.JournalStudyArea, form=JournalStudyAreaForm, extra=1, can_delete=True)
    JournalMissionFormSet = inlineformset_factory(models.Journal, models.JournalMission, form=JournalMissionForm, extra=1, can_delete=True)
    JournalHistFormSet = inlineformset_factory(models.Journal, models.JournalHist, extra=1, can_delete=True)
    JournalIndexCoverageFormSet = inlineformset_factory(models.Journal, models.JournalIndexCoverage, extra=1, can_delete=True)

    if request.method == "POST":

        journalform = JournalForm(request.POST, instance=journal, prefix='journal', collections_qset=user_collections)
        studyareaformset = JournalStudyAreaFormSet(request.POST, instance=journal, prefix='studyarea')
        titleformset = JournalTitleFormSet(request.POST, instance=journal, prefix='title')
        missionformset = JournalMissionFormSet(request.POST, instance=journal, prefix='mission')
        histformset = JournalHistFormSet(request.POST, instance=journal, prefix='hist')
        indexcoverageformset = JournalIndexCoverageFormSet(request.POST, instance=journal, prefix='indexcoverage')

        if journalform.is_valid() and studyareaformset.is_valid() and titleformset.is_valid() and indexcoverageformset.is_valid() \
            and missionformset.is_valid() and histformset.is_valid():
            journalform.save_all(creator = request.user)
            studyareaformset.save()
            titleformset.save()
            missionformset.save()
            histformset.save()
            indexcoverageformset.save()
            messages.info(request, MSG_FORM_SAVED)

            return HttpResponseRedirect(reverse('journal.index'))
        else:
            messages.error(request, MSG_FORM_MISSING)

    else:
        journalform  = JournalForm(instance=journal, prefix='journal', collections_qset=user_collections)
        studyareaformset = JournalStudyAreaFormSet(instance=journal, prefix='studyarea')
        titleformset = JournalTitleFormSet(instance=journal, prefix='title')
        missionformset  = JournalMissionFormSet(instance=journal, prefix='mission')
        histformset = JournalHistFormSet(instance=journal, prefix='hist')
        indexcoverageformset = JournalIndexCoverageFormSet(instance=journal, prefix='indexcoverage')

    return render_to_response('journalmanager/add_journal.html', {
                              'add_form': journalform,
                              'studyareaformset': studyareaformset,
                              'titleformset': titleformset,
                              'missionformset': missionformset,
                              'user_collections': user_collections,
                              'histformset': histformset,
                              'indexcoverageformset': indexcoverageformset,
                              }, context_instance = RequestContext(request))

@login_required
def add_publisher(request, publisher_id=None):
    """
    Handles new and existing publishers
    """

    if  publisher_id is None:
        publisher = models.Publisher()
    else:
        publisher = get_object_or_404(models.Publisher, id = publisher_id)

    user_collections = get_user_collections(request.user.id)

    if request.method == "POST":
        publisherform = PublisherForm(request.POST, instance=publisher, prefix='publisher',
            collections_qset=user_collections)

        if publisherform.is_valid():
            publisherform.save()
            messages.info(request, MSG_FORM_SAVED)
            return HttpResponseRedirect(reverse('publisher.index'))
        else:
            messages.error(request, MSG_FORM_MISSING)
    else:
        publisherform  = PublisherForm(instance=publisher, prefix='publisher',
            collections_qset=user_collections)

    return render_to_response('journalmanager/add_publisher.html', {
                              'add_form': publisherform,
                              'user_name': request.user.pk,
                              'user_collections': user_collections,
                              },
                              context_instance = RequestContext(request))


@login_required
def add_issue(request, journal_id, issue_id=None):
    """
    Handles new and existing issues
    """

    user_collections = get_user_collections(request.user.id)
    journal = get_object_or_404(models.Journal, pk=journal_id)

    if issue_id is None:
        issue = models.Issue()
    else:
        issue = models.Issue.objects.get(pk=issue_id)


    if request.method == 'POST':
        add_form = IssueForm(request.POST, journal_id=journal.pk, instance=issue)

        if add_form.is_valid():
            add_form.save_all(journal)
            messages.info(request, MSG_FORM_SAVED)
            return HttpResponseRedirect(reverse('issue.index', args=[journal_id]))
        else:
            messages.error(request, MSG_FORM_MISSING)
    else:
        add_form = IssueForm(journal_id=journal.pk, instance=issue)

    return render_to_response('journalmanager/add_issue.html', {
                              'add_form': add_form,
                              'journal': journal,
                              'user_name': request.user.pk,
                              'user_collections': user_collections},
                              context_instance = RequestContext(request))

@login_required
def publisher_index(request):
    user_collections = get_user_collections(request.user.id)
    default_collections = user_collections.filter(is_default = True)

    all_publishers = models.Publisher.objects.available(request.GET.get('is_available', 1))
    publishers = get_paginated(all_publishers, request.GET.get('page', 1))

    t = loader.get_template('journalmanager/publisher_dashboard.html')
    c = RequestContext(request, {
                       'objects_publisher': publishers,
                       'user_collections': user_collections,
                       })
    return HttpResponse(t.render(c))

@login_required
def add_section(request, journal_id, section_id=None):
    """
    Handles new and existing sections
    """

    if section_id is None:
        section = models.Section()
    else:
        section = get_object_or_404(models.Section, pk=section_id)

    journal = get_object_or_404(models.Journal, pk=journal_id)
    SectionTitleFormSet = inlineformset_factory(models.Section, models.SectionTitle, form=SectionTitleForm, extra=1, can_delete=True)
    SectionTitleFormSet.form = staticmethod(curry(SectionTitleForm, journal=journal))

    if request.method == 'POST':
        add_form = SectionForm(request.POST, instance=section)
        section_title_formset = SectionTitleFormSet(request.POST, instance=section, prefix='titles')
        if add_form.is_valid() and section_title_formset.is_valid():
            add_form.save_all(journal)
            section_title_formset.save()
            messages.info(request, MSG_FORM_SAVED)
            return HttpResponseRedirect(reverse('section.index', args=[journal_id]))
        else:
            messages.error(request, MSG_FORM_MISSING)

    else:
        add_form = SectionForm(instance=section)
        section_title_formset = SectionTitleFormSet(instance=section, prefix='titles')

    return render_to_response('journalmanager/add_section.html', {
                              'add_form': add_form,
                              'section_title_formset': section_title_formset,
                              'user_name': request.user.pk,
                              'journal': journal,
                              },
                              context_instance = RequestContext(request))

@login_required
def add_center(request, center_id=None):
    """
    Handles new and existing centers
    """
    if  center_id == None:
        center = models.Center()
    else:
        center = get_object_or_404(models.Center, id = center_id)

    user_collections = get_user_collections(request.user.id)

    if request.method == 'POST':
        centerform = CenterForm(request.POST, instance=center, prefix='center',
            collections_qset=user_collections)

        if centerform.is_valid():
            centerform.save()
            messages.info(request, MSG_FORM_SAVED)
            return HttpResponseRedirect(reverse('center.index'))
        else:
            messages.error(request, MSG_FORM_MISSING)

    else:
        centerform  = CenterForm(instance=center, prefix='center', collections_qset=user_collections)

    return render_to_response('journalmanager/add_center.html', {
                              'add_form': centerform,
                              'user_name': request.user.pk,
                              'user_collections': user_collections,
                              },
                              context_instance = RequestContext(request))


@login_required
def center_index(request):
    user_collections = get_user_collections(request.user.id)
    default_collections = user_collections.filter(is_default = True)

    all_centers = models.Center.objects.available(request.GET.get('is_available', 1))
    centers = get_paginated(all_centers, request.GET.get('page', 1))

    t = loader.get_template('journalmanager/center_dashboard.html')
    c = RequestContext(request, {
                       'objects_center': centers,
                       'user_collections': user_collections,
                       })
    return HttpResponse(t.render(c))


@login_required
def toggle_user_availability(request, user_id):

  if request.is_ajax():

    user = get_object_or_404(models.User, pk = user_id)
    user.is_active = not user.is_active
    user.save()

    response_data = json.dumps({
      "result": str(user.is_active),
      "object_id": user.id
      })

    #ajax response json
    return HttpResponse(response_data, mimetype="application/json")
  else:
    #bad request
    return HttpResponse(status=400)

@login_required
def my_account(request):
    t = loader.get_template('journalmanager/my_account.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))

@login_required
def password_change(request):

    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            if cleaned_data['new_password'] != cleaned_data['new_password_again']:
                messages.error(request, _('Your new password and new password confirmation must match.'))
                return HttpResponseRedirect(reverse('journalmanager.password_change'))

            auth_user = authenticate(username=request.user.username,
                                     password=cleaned_data['password'])
            if auth_user:
                auth_user.set_password(cleaned_data['new_password'])
                auth_user.save()
            else:
                messages.error(request, _('Your current password does not match. Please try again.'))
                return HttpResponseRedirect(reverse('journalmanager.password_change'))

            messages.info(request, _('Your new password has been set.'))
            return HttpResponseRedirect(reverse('journalmanager.my_account'))
    else:
        form = PasswordChangeForm()

    return render_to_response(
        'journalmanager/password_change.html',
        {'form': form},
        context_instance = RequestContext(request))
