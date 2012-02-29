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
def show_user(request,user_id):
    user_collection = request.user.userprofile_set.get().collection
    user = models.Institution.objects.get(id=user_id)
    t = loader.get_template('journalmanager/show_user.html')
    c = RequestContext(request, {
                       'user': user,
                       'collection': user_collection,
                       })
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
            return render_to_response('journalmanager/edit_user.html', {
                                      'edit_user_form': edit_user_form,
                                      'mode': 'edit_user',
                                      'user_id': user_id,
                                      'user_name': request.user.pk,
                                      'collection': user_collection},
                                      context_instance=RequestContext(request))
    else:
        edit_user_form = UserForm(instance=formFilled)
    return render_to_response('journalmanager/edit_user.html', {
                              'edit_user_form': edit_user_form,
                              'mode': 'edit_user',
                              'user_id': user_id,
                              'user_name': request.user.pk,
                              'collection': user_collection},
                              context_instance=RequestContext(request))

@login_required
def show_journal(request, journal_id):
    user_collection = request.user.userprofile_set.get().collection
    journal = models.Journal.objects.get(pk = journal_id)
    t = loader.get_template('journalmanager/show_journal.html')
    c = RequestContext(request, {
                       'journal': journal,
                       'collection': user_collection,
                       })
    return HttpResponse(t.render(c))

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

    JournalStudyAreaFormSet = inlineformset_factory(models.Journal, models.JournalStudyArea, form=JournalStudyAreaForm, extra=1, can_delete=True)
    JournalTitleFormSet = inlineformset_factory(models.Journal, models.JournalTitle, form=JournalTitleForm, extra=1, can_delete=True)
    JournalMissionFormSet = inlineformset_factory(models.Journal, models.JournalMission, form=JournalMissionForm, extra=1, can_delete=True)
    JournalTextLanguageFormSet = inlineformset_factory(models.Journal, models.JournalTextLanguage, extra=1, can_delete=True)
    JournalAbstrLanguageFormSet = inlineformset_factory(models.Journal, models.JournalAbstrLanguage, extra=1, can_delete=True)
    JournalHistFormSet = inlineformset_factory(models.Journal, models.JournalHist, extra=1, can_delete=True)

    if request.method == "POST":
        journalform = JournalForm(request.POST, instance=journal, prefix='journal')
        studyareaformset = JournalStudyAreaFormSet(request.POST, instance=journal, prefix='studyarea')
        titleformset = JournalTitleFormSet(request.POST, instance=journal, prefix='title')
        missionformset = JournalMissionFormSet(request.POST, instance=journal, prefix='mission')
        textlanguageformset = JournalTextLanguageFormSet(request.POST, instance=journal, prefix='textlanguage')
        abstrlanguageformset = JournalAbstrLanguageFormSet(request.POST, instance=journal, prefix='abstrlanguage')
        histformset = JournalHistFormSet(request.POST, instance=journal, prefix='hist')

        if journalform.is_valid() and studyareaformset.is_valid() and titleformset.is_valid() and missionformset.is_valid() and textlanguageformset.is_valid() and histformset.is_valid():
            journalform.save_all(creator = request.user)
            studyareaformset.save()
            titleformset.save()
            missionformset.save()
            textlanguageformset.save()
            abstrlanguageformset.save()
            histformset.save()

            return HttpResponseRedirect(reverse('journal.index'))

    else:

        journalform  = JournalForm(instance=journal, prefix='journal')
        studyareaformset = JournalStudyAreaFormSet(instance=journal, prefix='studyarea')
        titleformset = JournalTitleFormSet(instance=journal, prefix='title')
        missionformset  = JournalMissionFormSet(instance=journal, prefix='mission')
        textlanguageformset = JournalTextLanguageFormSet(instance=journal, prefix='textlanguage')
        abstrlanguageformset = JournalAbstrLanguageFormSet(instance=journal, prefix='abstrlanguage')
        histformset = JournalHistFormSet(instance=journal, prefix='hist')

    return render_to_response('journalmanager/add_journal.html', {
                              'add_form': journalform,
                              'studyareaformset': studyareaformset,
                              'titleformset': titleformset,
                              'missionformset': missionformset,
                              'collection': user_collection,
                              'textlanguageformset': textlanguageformset,
                              'histformset': histformset,
                              'abstrlanguageformset': abstrlanguageformset,
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
def show_institution(request, institution_id):
    #FIXME: models.Intitutions e models.Journals ja se relacionam, avaliar
    #estas queries.
    user_collection = request.user.userprofile_set.get().collection
    institution = models.Institution.objects.get(pk = institution_id)
    journals = models.Journal.objects.filter(institution = institution_id)
    t = loader.get_template('journalmanager/show_institution.html')
    c = RequestContext(request, {
                       'institution': institution,
                       'journals': journals,
                       'collection': user_collection,
                       })
    return HttpResponse(t.render(c))

@login_required
def institution_index(request):
    user_collection = request.user.userprofile_set.get().collection
    all_institutions = models.Institution.objects.available(request.GET.get('is_available', 1)).filter(collection = user_collection)

    institutions = get_paginated(all_institutions, request.GET.get('page', 1))

    t = loader.get_template('journalmanager/institution_dashboard.html')
    c = RequestContext(request, {
                       'institutions': institutions,
                       'collection': user_collection,
                       })
    return HttpResponse(t.render(c))

@login_required
def add_institution(request, institution_id=None):
    """
    Handles new and existing institutions
    """

    user_collection = request.user.userprofile_set.get().collection

    if request.method == 'POST':
        institution_form_kwargs = {}

        if institution_id is not None: #edit - preserve form-data
            filled_form = models.Institution.objects.get(pk = institution_id)
            institution_form_kwargs['instance'] = filled_form

        add_form = InstitutionForm(request.POST, **institution_form_kwargs)

        if add_form.is_valid():
            add_form.save_all(collection = user_collection)
            return HttpResponseRedirect(reverse('institution.index'))
    else:
        if institution_id is None: #new
            add_form = InstitutionForm()
        else:
            filled_form = models.Institution.objects.get(pk = institution_id)
            add_form = InstitutionForm(instance = filled_form)

    return render_to_response('journalmanager/add_institution.html', {
                              'add_form': add_form,
                              'user_name': request.user.pk,
                              'collection': user_collection,
                              },
                              context_instance = RequestContext(request))

@login_required
def toggle_institution_availability(request, institution_id):
  institution = get_object_or_404(models.Institution, pk = institution_id)
  institution.is_available = not institution.is_available
  institution.save()

  return HttpResponseRedirect(reverse('institution.index'))

@login_required
def show_issue(request, issue_id):
    issue = models.Issue.objects.get(pk = issue_id)
    journal = issue.journal
    t = loader.get_template('journalmanager/show_issue.html')
    c = RequestContext(request, {
                       'issue': issue,
                       'journal': journal,
                       })
    return HttpResponse(t.render(c))

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
    journal = models.Journal.objects.get(pk = journal_id)

    if request.method == 'POST':
        issue_form_kwargs = {}

        if issue_id is not None: #edit - preserve form-data
            filled_form = models.Issue.objects.get(pk = issue_id)
            issue_form_kwargs['instance'] = filled_form

        add_form = IssueForm(request.POST, **issue_form_kwargs)

        if add_form.is_valid():
            if issue_id is not None:
                add_form.save()
            else:
                add_form.save_all(user_collection, journal)

            return HttpResponseRedirect(reverse('issue.index', args=[journal_id]))
    else:
        if issue_id is None: #new
            add_form = IssueForm()
        else:
            filled_form = models.Issue.objects.get(pk = issue_id)
            add_form = IssueForm(instance = filled_form)

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
def search_institution(request):
    user_collection = request.user.userprofile_set.get().collection

    #Get institutions where title contains the "q" value and collection equal with the user
    institutions_filter = models.Institution.objects.filter(name__icontains = request.REQUEST['q'],
                                                            collection = user_collection).order_by('name')

    #Paginated the result
    institutions = get_paginated(institutions_filter, request.GET.get('page', 1))

    t = loader.get_template('journalmanager/institution_search_result.html')
    c = RequestContext(request, {
                       'institutions': institutions,
                       'collection': user_collection,
                       'search_query_string': request.REQUEST['q'],
                       })
    return HttpResponse(t.render(c))

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
        all_centers = all_centers.filter(collection = user_collection)

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
    user_collection = request.user.userprofile_set.get().collection

    #Get centers where title contains the "q" value and collection equal with the user
    center_filter = models.Center.objects.filter(name__icontains = request.REQUEST['q'],
                                                            collection = user_collection).order_by('name')

    #Paginated the result
    centers = get_paginated(center_filter, request.GET.get('page', 1))

    t = loader.get_template('journalmanager/center_dashboard.html')
    c = RequestContext(request, {
                       'centers': centers,
                       'collection': user_collection,
                       'search_query_string': request.REQUEST['q'],
                       })
    return HttpResponse(t.render(c))

