from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import loader
from django.template.context import RequestContext
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from scielomanager.journalmanager import models
from scielomanager.journalmanager.forms import *
from scielomanager.tools import get_paginated


def index(request):
    t = loader.get_template('journalmanager/home_journal.html')
    if request.user.is_authenticated():
        user_collection = request.user.userprofile_set.get().collection
    else:
        user_collection = ""
    c = RequestContext(request,{'collection':user_collection,})
    return HttpResponse(t.render(c),)

@login_required
def user_index(request):
    user_collection = request.user.userprofile_set.get().collection
    all_users = User.objects.filter(userprofile__collection=user_collection)
    users = get_paginated(all_users, request.GET.get('page', 1))

    t = loader.get_template('journalmanager/user_dashboard.html')

    c = RequestContext(request, {
                       'users': users,
                       'collection': user_collection,
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
                user_collection = request.user.userprofile_set.get().collection
                if next != '':
                    t = loader.get_template(next)
                else:
                    t = loader.get_template('journalmanager/home_journal.html')
                c = RequestContext(request, {'active': True,
                                             'collection': user_collection,})
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
        else:
            c = RequestContext(request, {'next': next,})
        return HttpResponse(t.render(c))

@login_required
def user_logout(request):
    logout(request)
    t = loader.get_template('journalmanager/home_journal.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))

@login_required
@permission_required('auth.add_user')
def add_user(request):
    user_collection = request.user.userprofile_set.get().collection
    if request.method == 'POST':
        #instance of form
        form = UserForm(request.POST)
        if form.is_valid():
            #Get the user and create a new evaluation
            user_collection = request.user.userprofile_set.get().collection
            fuser = form.save(commit=False)
            fuser.collection = user_collection
            fuser.save()
            # Saving user collection on UserProfile
            uprof = models.UserProfile();
            uprof.collection = user_collection;
            uprof.user = fuser
            uprof.save()
            return HttpResponseRedirect("/journal/user")
        else:
            add_user_form = UserForm() # An unbound form
            return render_to_response('journalmanager/add_user.html', {
                                      'add_user_form': add_user_form,
                                      'mode': 'add_user',
                                      'form': form,
                                      'user_name': request.user.pk,
                                      'collection': user_collection},
                                      context_instance=RequestContext(request))
    else:
        add_user_form = UserForm() # An unbound form
    return render_to_response('journalmanager/add_user.html', {
                              'add_user_form': add_user_form,
                              'mode': 'user_journal',
                              'user_name': request.user.pk,
                              'collection': user_collection},
                              context_instance=RequestContext(request))

@login_required
@permission_required('auth.change_user')
def edit_user(request,user_id):
    #recovering Journal Data to input form fields
    formFilled = User.objects.get(pk=user_id)
    user_collection = request.user.userprofile_set.get().collection
    if request.method == 'POST':
        form = UserForm(request.POST,instance=formFilled)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/journal/user")
        else:
            edit_user_form = UserForm(request.POST,instance=formFilled)
            return render_to_response('journalmanager/add_user.html', {
                                      'edit_user_form': edit_user_form,
                                      'mode': 'edit_user',
                                      'user_id': user_id,
                                      'user_name': request.user.pk,
                                      'collection': user_collection},
                                      context_instance=RequestContext(request))
    else:
        edit_user_form = UserForm(instance=formFilled)
    return render_to_response('journalmanager/add_user.html', {
                              'edit_user_form': edit_user_form,
                              'mode': 'edit_user',
                              'user_id': user_id,
                              'user_name': request.user.pk,
                              'collection': user_collection},
                              context_instance=RequestContext(request))

@login_required
def journal_index(request):
    user_collection = request.user.userprofile_set.get().collection
    all_journals = models.Journal.objects.available(request.GET.get('is_available', 1)).filter(collections = user_collection)

    journals = get_paginated(all_journals, request.GET.get('page', 1))

    t = loader.get_template('journalmanager/journal_dashboard.html')
    c = RequestContext(request, {
                       'journals': journals,
                       'collection': user_collection,
                       })
    return HttpResponse(t.render(c))

@login_required
def add_journal(request, journal_id = None):

    """
    Handles new and existing journals
    """
    user_collection = request.user.userprofile_set.get().collection

    if  journal_id == None:
        journal = models.Journal()
    else:
        journal = get_object_or_404(models.Journal, id = journal_id)

    JournalTitleFormSet = inlineformset_factory(models.Journal, models.JournalTitle, form=JournalTitleForm, extra=1, can_delete=True)
    JournalStudyAreaFormSet = inlineformset_factory(models.Journal, models.JournalStudyArea, form=JournalStudyAreaForm, extra=1, can_delete=True)
    JournalMissionFormSet = inlineformset_factory(models.Journal, models.JournalMission, form=JournalMissionForm, extra=1, can_delete=True)
    JournalTextLanguageFormSet = inlineformset_factory(models.Journal, models.JournalTextLanguage, extra=1, can_delete=True)
    JournalHistFormSet = inlineformset_factory(models.Journal, models.JournalHist, extra=1, can_delete=True)
    JournalIndexCoverageFormSet = inlineformset_factory(models.Journal, models.JournalIndexCoverage, extra=1, can_delete=True)

    if request.method == "POST":
        journalform = JournalForm(request.POST, instance=journal, prefix='journal')
        studyareaformset = JournalStudyAreaFormSet(request.POST, instance=journal, prefix='studyarea')
        titleformset = JournalTitleFormSet(request.POST, instance=journal, prefix='title')
        missionformset = JournalMissionFormSet(request.POST, instance=journal, prefix='mission')
        textlanguageformset = JournalTextLanguageFormSet(request.POST, instance=journal, prefix='textlanguage')
        histformset = JournalHistFormSet(request.POST, instance=journal, prefix='hist')
        indexcoverageformset = JournalIndexCoverageFormSet(request.POST, instance=journal, prefix='indexcoverage')

        if journalform.is_valid() and studyareaformset.is_valid() and titleformset.is_valid() and indexcoverageformset.is_valid() \
            and missionformset.is_valid() and textlanguageformset.is_valid() and histformset.is_valid():
            journalform.save_all(creator = request.user)
            studyareaformset.save()
            titleformset.save()
            missionformset.save()
            textlanguageformset.save()
            histformset.save()
            indexcoverageformset.save()

            return HttpResponseRedirect(reverse('journal.index'))

    else:

        journalform  = JournalForm(instance=journal, prefix='journal')
        studyareaformset = JournalStudyAreaFormSet(instance=journal, prefix='studyarea')
        titleformset = JournalTitleFormSet(instance=journal, prefix='title')
        missionformset  = JournalMissionFormSet(instance=journal, prefix='mission')
        textlanguageformset = JournalTextLanguageFormSet(instance=journal, prefix='textlanguage')
        histformset = JournalHistFormSet(instance=journal, prefix='hist')
        indexcoverageformset = JournalIndexCoverageFormSet(instance=journal, prefix='indexcoverage')

    return render_to_response('journalmanager/add_journal.html', {
                              'add_form': journalform,
                              'studyareaformset': studyareaformset,
                              'titleformset': titleformset,
                              'missionformset': missionformset,
                              'collection': user_collection,
                              'textlanguageformset': textlanguageformset,
                              'histformset': histformset,
                              'indexcoverageformset': indexcoverageformset,
                              }, context_instance = RequestContext(request))


@login_required
def toggle_journal_availability(request, journal_id):
  journal = get_object_or_404(models.Journal, pk = journal_id)
  journal.is_available = not journal.is_available
  journal.save()

  return HttpResponseRedirect(reverse('journal.index'))


@login_required
def toggle_user_availability(request, user_id):
  user = get_object_or_404(models.User, pk = user_id)
  user.is_active = not user.is_active
  user.save()

  return HttpResponseRedirect(reverse('user.index'))

@login_required
def publisher_index(request):
    user_collection = request.user.userprofile_set.get().collection
    all_publishers = models.Publisher.objects

    if all_publishers:
        all_publishers = all_publishers.available(request.GET.get('is_available', 1))
        if all_publishers:
            all_publishers = all_publishers.filter(collection = user_collection)
            if all_publishers:
                try:
                    #Get publishers where title contains the "q" value and collection equal with the user
                    all_publishers = all_publishers.filter(name__icontains = request.REQUEST['q']).order_by('name')
                except KeyError:
                    pass

    publishers = get_paginated(all_publishers, request.GET.get('page', 1))

    t = loader.get_template('journalmanager/publisher_dashboard.html')
    c = RequestContext(request, {
                       'publishers': publishers,
                       'collection': user_collection,
                       })
    return HttpResponse(t.render(c))

@login_required
def add_publisher(request, publisher_id=None):
    """
    Handles new and existing publishers
    """

    user_collection = request.user.userprofile_set.get().collection

    if request.method == 'POST':
        publisher_form_kwargs = {}

        if publisher_id is not None: #edit - preserve form-data
            filled_form = models.Publisher.objects.get(pk = publisher_id)
            publisher_form_kwargs['instance'] = filled_form

        add_form = PublisherForm(request.POST, **publisher_form_kwargs)

        if add_form.is_valid():
            add_form.save_all(collection = user_collection)
            return HttpResponseRedirect(reverse('publisher.index'))
    else:
        if publisher_id is None: #new
            add_form = PublisherForm()
        else:
            filled_form = models.Publisher.objects.get(pk = publisher_id)
            add_form = PublisherForm(instance = filled_form)

    return render_to_response('journalmanager/add_publisher.html', {
                              'add_form': add_form,
                              'user_name': request.user.pk,
                              'collection': user_collection,
                              },
                              context_instance = RequestContext(request))

@login_required
def toggle_publisher_availability(request, publisher_id):
  publisher = get_object_or_404(models.Publisher, pk = publisher_id)
  publisher.is_available = not publisher.is_available
  publisher.save()

  return HttpResponseRedirect(reverse('publisher.index'))

@login_required
def issue_index(request, journal_id):
    #FIXME: models.Journal e models.Issue ja se relacionam, avaliar
    #estas queries.
    journal = models.Journal.objects.get(pk = journal_id)
    user_collection = request.user.userprofile_set.get().collection

    all_issues = models.Issue.objects.available(request.GET.get('is_available', 1)).filter(journal = journal_id)

    issues = get_paginated(all_issues, request.GET.get('page', 1))

    t = loader.get_template('journalmanager/issue_dashboard.html')
    c = RequestContext(request, {
                       'issues': issues,
                       'journal': journal,
                       'collection': user_collection,
                       })
    return HttpResponse(t.render(c))

@login_required
def add_issue(request, journal_id, issue_id=None):
    """
    Handles new and existing issues
    """

    user_collection = request.user.userprofile_set.get().collection
    journal = get_object_or_404(models.Journal, pk=journal_id)

    if issue_id is None:
        issue = models.Issue()
    else:
        issue = models.Issue.objects.get(pk=issue_id)


    if request.method == 'POST':
        add_form = IssueForm(request.POST, journal_id=journal.pk, instance=issue)

        if add_form.is_valid():
            add_form.save_all(user_collection, journal)

            return HttpResponseRedirect(reverse('issue.index', args=[journal_id]))
    else:
        add_form = IssueForm(journal_id=journal.pk, instance=issue)

    return render_to_response('journalmanager/add_issue.html', {
                              'add_form': add_form,
                              'journal': journal,
                              'user_name': request.user.pk,
                              'collection': user_collection},
                              context_instance = RequestContext(request))

@login_required
def toggle_issue_availability(request, issue_id):
    issue = get_object_or_404(models.Issue, pk = issue_id)
    issue.is_available = not issue.is_available
    issue.save()

    return HttpResponseRedirect(reverse('issue.index', args=[issue.journal.pk]))

@login_required
def search_journal(request):
    user_collection = request.user.userprofile_set.get().collection

    #Get journals where title contains the "q" value and collection equal with the user
    journals_filter = models.Journal.objects.filter(title__icontains = request.REQUEST['q'],
                                                    collections = user_collection).order_by('title')

    #Paginated the result
    journals = get_paginated(journals_filter, request.GET.get('page', 1))

    t = loader.get_template('journalmanager/journal_search_result.html')
    c = RequestContext(request, {
                       'journals': journals,
                       'collection': user_collection,
                       'search_query_string': request.REQUEST['q'],
                       })
    return HttpResponse(t.render(c))

@login_required
def search_publisher(request):
    return publisher_index(request)

@login_required
def search_issue(request, journal_id):

    journal = models.Journal.objects.get(pk = journal_id)
    user_collection = request.user.userprofile_set.get().collection
    #Get issues where journal.id = journal_id and volume contains "q"
    selected_issues = models.Issue.objects.filter(journal = journal_id,
                                                  volume__icontains = request.REQUEST['q']).order_by('publication_date')

    #Paginated the result
    issues = get_paginated(selected_issues, request.GET.get('page', 1))

    t = loader.get_template('journalmanager/issue_dashboard.html')
    c = RequestContext(request, {
                       'issues': issues,
                       'journal': journal,
                       'collection': user_collection,
                       'search_query_string': request.REQUEST['q'],
                       })
    return HttpResponse(t.render(c))

@login_required
def section_index(request, journal_id):
    #FIXME: models.Journal e models.Issue ja se relacionam, avaliar
    #estas queries.
    journal = models.Journal.objects.get(pk = journal_id)
    user_collection = request.user.userprofile_set.get().collection

    all_sections = models.Section.objects.available(request.GET.get('is_available', 1)).filter(journal=journal_id)

    sections = get_paginated(all_sections, request.GET.get('page', 1))

    t = loader.get_template('journalmanager/section_dashboard.html')
    c = RequestContext(request, {
                       'items': sections,
                       'journal': journal,
                       'collection': user_collection,
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

    if request.method == 'POST':
        add_form = SectionForm(request.POST, instance=section)

        if add_form.is_valid():
            add_form.save_all(journal)

            return HttpResponseRedirect(reverse('section.index', args=[journal_id]))

    else:
        add_form = SectionForm(instance=section)

    return render_to_response('journalmanager/add_section.html', {
                              'add_form': add_form,
                              'user_name': request.user.pk,
                              'journal': journal,
                              },
                              context_instance = RequestContext(request))
@login_required
def center_index(request):
    user_collection = request.user.userprofile_set.get().collection
    all_centers = models.Center.objects

    if all_centers:
        all_centers = all_centers.available(request.GET.get('is_available', 1))
        if all_centers:
            all_centers = all_centers.filter(collection = user_collection)
            if all_centers:
                try:
                    #Get centers where title contains the "q" value and collection equal with the user
                    all_centers = all_centers.filter(name__icontains = request.REQUEST['q']).order_by('name')
                except KeyError:
                    pass
    centers = get_paginated(all_centers, request.GET.get('page', 1))

    t = loader.get_template('journalmanager/center_dashboard.html')
    c = RequestContext(request, {
                       'centers': centers,
                       'collection': user_collection,
                       })
    return HttpResponse(t.render(c))

@login_required
def add_center(request, center_id=None):
    """
    Handles new and existing centers
    """

    user_collection = request.user.userprofile_set.get().collection

    if request.method == 'POST':
        center_form_kwargs = {}

        if center_id is not None: #edit - preserve form-data
            filled_form = models.Center.objects.get(pk = center_id)
            center_form_kwargs['instance'] = filled_form

        add_form = CenterForm(request.POST, **center_form_kwargs)

        if add_form.is_valid():
            add_form.save_all(collection = user_collection)
            return HttpResponseRedirect(reverse('center.index'))
    else:
        if center_id is None: #new
            add_form = CenterForm()
        else:
            filled_form = models.Center.objects.get(pk = center_id)
            add_form = CenterForm(instance = filled_form)

    return render_to_response('journalmanager/add_center.html', {
                              'add_form': add_form,
                              'user_name': request.user.pk,
                              'collection': user_collection,
                              },
                              context_instance = RequestContext(request))

@login_required
def toggle_center_availability(request, center_id):
  center = get_object_or_404(models.Center, pk = center_id)
  center.is_available = not center.is_available
  center.save()

  return HttpResponseRedirect(reverse('center.index'))

@login_required
def search_center(request):
    return center_index(request)

