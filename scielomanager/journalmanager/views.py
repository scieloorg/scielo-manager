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
from django.db.models import Q

from scielomanager.journalmanager import models
from scielomanager.journalmanager.forms import *
from scielomanager.tools import get_paginated

def get_user_collections(user_id):

    user_collections = User.objects.get(pk=user_id).usercollections_set.all()

    return user_collections        

def index(request):
    t = loader.get_template('journalmanager/home_journal.html')
    if request.user.is_authenticated():
        collections = get_user_collections(request.user.id)
        user_collections = collections['all'] 
    else:
        user_collections = ""

    c = RequestContext(request,{'user_collections':user_collections,})
    return HttpResponse(t.render(c),)

@login_required
def user_index(request):
    
    
    user_collections = get_user_collections(request.user.id)
    user_collections_managed = user_collections.filter(is_manager=True)

    # Filtering users manager by the administrator
    all_users = models.User.objects.filter(usercollections__collection__in =
        ( collection.collection.pk for collection in user_collections_managed )).distinct('username')

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
                    t = loader.get_template(next)
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
def add_user(request, user_id=None):
    """
    Handles new and existing users
    """

    if  user_id == None:
        user = models.User()
    else:
        user = get_object_or_404(models.User, id = user_id)

    # Getting Collections from the logged user.
    user_collections = get_user_collections(request.user.id)

    UserCollectionsFormSet = inlineformset_factory(models.User, models.UserCollections, 
        form=UserCollectionsForm, extra=1, can_delete=True)

    if request.method == 'POST':
        usercollectionsformset = UserCollectionsFormSet(request.POST, instance=user, prefix='usercollections',)
        user_form_kwargs = {}

        if user_id is not None: #edit - preserve form-data    
            filled_form = user
            user_form_kwargs['instance'] = filled_form

        add_form = UserForm(request.POST, **user_form_kwargs)

        if add_form.is_valid() and usercollectionsformset.is_valid():
            user_saved = add_form.save()
            usercollectionsformset.save()     

            return HttpResponseRedirect(reverse('user.index'))
    else:
        if user_id is None: #new
            add_form = UserForm() # An unbound form
            usercollectionsformset = UserCollectionsFormSet(instance=user, prefix='usercollections')
        else:
            filled_form = models.User.objects.get(pk = user_id)
            add_form = UserForm(instance = filled_form)
            usercollectionsformset = UserCollectionsFormSet(instance=user, prefix='usercollections')

    return render_to_response('journalmanager/add_user.html', {
                              'add_form': add_form,
                              'mode': 'user_journal',
                              'user_name': request.user.pk,
                              'user_collections': user_collections,
                              'usercollectionsformset': usercollectionsformset},
                              context_instance=RequestContext(request))

@login_required
def journal_index(request):
    user_collections = get_user_collections(request.user.id)
    default_collections = user_collections.filter(is_default=True)

    all_journals = models.Journal.objects.available(request.GET.get('is_available', 1))

    journals = get_paginated(all_journals, request.GET.get('page', 1))

    t = loader.get_template('journalmanager/journal_dashboard.html')
    c = RequestContext(request, {
                       'journals': journals,
                       'user_collections': user_collections,
                       })
    return HttpResponse(t.render(c))

@login_required
def add_journal(request, journal_id = None):
    """
    Handles new and existing journals
    """
    user_collections = get_user_collections(request.user.id)

    if  journal_id == None:
        journal = models.Journal()
    else:
        journal = get_object_or_404(models.Journal, id = journal_id)

    JournalTitleFormSet = inlineformset_factory(models.Journal, models.JournalTitle, form=JournalTitleForm, extra=1, can_delete=True)
    JournalStudyAreaFormSet = inlineformset_factory(models.Journal, models.JournalStudyArea, form=JournalStudyAreaForm, extra=1, can_delete=True)
    JournalMissionFormSet = inlineformset_factory(models.Journal, models.JournalMission, form=JournalMissionForm, extra=1, can_delete=True)
    JournalTextLanguageFormSet = inlineformset_factory(models.Journal, models.JournalTextLanguage, extra=1, can_delete=True)
    JournalHistFormSet = inlineformset_factory(models.Journal, models.JournalHist, extra=1, can_delete=True)
    JournalCollectionsFormSet = inlineformset_factory(models.Journal, models.JournalCollections, extra=1, can_delete=True)
    JournalIndexCoverageFormSet = inlineformset_factory(models.Journal, models.JournalIndexCoverage, extra=1, can_delete=True)

    if request.method == "POST":
        journalform = JournalForm(request.POST, instance=journal, prefix='journal')
        studyareaformset = JournalStudyAreaFormSet(request.POST, instance=journal, prefix='studyarea')
        titleformset = JournalTitleFormSet(request.POST, instance=journal, prefix='title')
        missionformset = JournalMissionFormSet(request.POST, instance=journal, prefix='mission')
        textlanguageformset = JournalTextLanguageFormSet(request.POST, instance=journal, prefix='textlanguage')
        histformset = JournalHistFormSet(request.POST, instance=journal, prefix='hist')
        collectionsformset = JournalCollectionsFormSet(request.POST, instance=journal, prefix='collection')
        indexcoverageformset = JournalIndexCoverageFormSet(request.POST, instance=journal, prefix='indexcoverage')

        if journalform.is_valid() and studyareaformset.is_valid() and titleformset.is_valid() and indexcoverageformset.is_valid() and collectionsformset.is_valid() \
            and missionformset.is_valid() and textlanguageformset.is_valid() and histformset.is_valid():
            journalform.save_all(creator = request.user)
            studyareaformset.save()
            titleformset.save()
            missionformset.save()
            textlanguageformset.save()
            histformset.save()
            collectionsformset.save()
            indexcoverageformset.save()

            return HttpResponseRedirect(reverse('journal.index'))

    else:
        journalform  = JournalForm(instance=journal, prefix='journal')
        studyareaformset = JournalStudyAreaFormSet(instance=journal, prefix='studyarea')
        titleformset = JournalTitleFormSet(instance=journal, prefix='title')
        missionformset  = JournalMissionFormSet(instance=journal, prefix='mission')
        textlanguageformset = JournalTextLanguageFormSet(instance=journal, prefix='textlanguage')
        histformset = JournalHistFormSet(instance=journal, prefix='hist')
        collectionsformset = JournalCollectionsFormSet(instance=journal, prefix='collection')
        indexcoverageformset = JournalIndexCoverageFormSet(instance=journal, prefix='indexcoverage')

    return render_to_response('journalmanager/add_journal.html', {
                              'add_form': journalform,
                              'collectionsformset': collectionsformset,
                              'studyareaformset': studyareaformset,
                              'titleformset': titleformset,
                              'missionformset': missionformset,
                              'user_collections': user_collections,
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
def institution_index(request):
    user_collections = get_user_collections(request.user.id)
    default_collections = user_collections.filter(is_default = True)
    #all_institutions = models.Institution.objects.available(request.GET.get('is_available', 1)).filter(institutioncollections_set__collection__in = ( collection.collection.pk for collection in default_collections ))
    all_institutions = models.Institution.objects.available(request.GET.get('is_available', 1))
    institutions = get_paginated(all_institutions, request.GET.get('page', 1))

    t = loader.get_template('journalmanager/institution_dashboard.html')
    c = RequestContext(request, {
                       'institutions': institutions,
                       'user_collections': user_collections,
                       })
    return HttpResponse(t.render(c))

@login_required
def add_institution(request, institution_id=None):
    """
    Handles new and existing institutions
    """
    if  institution_id == None:
        institution = models.Institution()
    else:
        institution = get_object_or_404(models.Institution, id = institution_id)

    user_collections = get_user_collections(request.user.id)

    InstitutionCollectionsFormSet = inlineformset_factory(models.Institution, models.InstitutionCollections, 
        form=InstitutionCollectionsForm, extra=1, can_delete=True)

    if request.method == 'POST':
        institution_form_kwargs = {}
        institutioncollectionsformset = InstitutionCollectionsFormSet(request.POST, 
            instance=institution, prefix='institutioncollections',)

        if institution_id is not None: #edit - preserve form-data
            filled_form = institution
            institution_form_kwargs['instance'] = filled_form

        add_form = InstitutionForm(request.POST, **institution_form_kwargs)

        if add_form.is_valid() and institutioncollectionsformset.is_valid():
            add_form.save()
            institutioncollectionsformset.save()  
            return HttpResponseRedirect(reverse('institution.index'))

    else:
        if institution_id is None: #new
            add_form = InstitutionForm()
            institutioncollectionsformset = InstitutionCollectionsFormSet(instance=institution, 
                prefix='institutioncollections')
        else:
            filled_form = models.Institution.objects.get(pk = institution_id)
            add_form = InstitutionForm(instance = filled_form)
            institutioncollectionsformset = InstitutionCollectionsFormSet(instance=institution, 
                prefix='institutioncollections')

    return render_to_response('journalmanager/add_institution.html', {
                              'add_form': add_form,
                              'user_name': request.user.pk,
                              'user_collections': user_collections,
                              'institutioncollectionsformset': institutioncollectionsformset},
                              context_instance = RequestContext(request))

@login_required
def toggle_institution_availability(request, institution_id):
  institution = get_object_or_404(models.Institution, pk = institution_id)
  institution.is_available = not institution.is_available
  institution.save()

  return HttpResponseRedirect(reverse('institution.index'))

@login_required
def issue_index(request, journal_id):
    #FIXME: models.Journal e models.Issue ja se relacionam, avaliar
    #estas queries.
    journal = models.Journal.objects.get(pk = journal_id)

    user_collections = get_user_collections(request.user.id)

    all_issues = models.Issue.objects.available(request.GET.get('is_available', 1)).filter(journal = journal_id)

    issues = get_paginated(all_issues, request.GET.get('page', 1))

    t = loader.get_template('journalmanager/issue_dashboard.html')
    c = RequestContext(request, {
                       'issues': issues,
                       'journal': journal,
                       'user_collections': user_collections,
                       })
    return HttpResponse(t.render(c))

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
            add_form.save_all(user_collection, journal)

            return HttpResponseRedirect(reverse('issue.index', args=[journal_id]))
    else:
        add_form = IssueForm(journal_id=journal.pk, instance=issue)

    return render_to_response('journalmanager/add_issue.html', {
                              'add_form': add_form,
                              'journal': journal,
                              'user_name': request.user.pk,
                              'user_collections': user_collections},
                              context_instance = RequestContext(request))

@login_required
def toggle_issue_availability(request, issue_id):
    issue = get_object_or_404(models.Issue, pk = issue_id)
    issue.is_available = not issue.is_available
    issue.save()

    return HttpResponseRedirect(reverse('issue.index', args=[issue.journal.pk]))

@login_required
def search_journal(request):
    user_collections = get_user_collections(request.user.id)
    default_collections = user_collections.filter(is_default=True)

    #Get journals where title contains the "q" value and collection equal with the user
    journals_filter = models.Journal.objects.filter(title__icontains = request.REQUEST['q'],
                                                    collection__in = ( collection.collection.pk for collection in default_collections )).order_by('title')

    #Paginated the result
    journals = get_paginated(journals_filter, request.GET.get('page', 1))

    t = loader.get_template('journalmanager/journal_search_result.html')
    c = RequestContext(request, {
                       'journals': journals,
                       'user_collections': user_collections,
                       'search_query_string': request.REQUEST['q'],
                       })
    return HttpResponse(t.render(c))

@login_required
def search_institution(request):
    user_collections = get_user_collections(request.user.id)
    default_collections = user_collections.filter(is_default=True)

    #Get institutions where title contains the "q" value and collection equal with the user
    institutions_filter = models.Institution.objects.filter(name__icontains = request.REQUEST['q'],
                                                            collection__in = ( collection.collection.pk for collection in default_collections )).order_by('name')

    #Paginated the result
    institutions = get_paginated(institutions_filter, request.GET.get('page', 1))

    t = loader.get_template('journalmanager/institution_search_result.html')
    c = RequestContext(request, {
                       'institutions': institutions,
                       'user_collections': user_collections,
                       'search_query_string': request.REQUEST['q'],
                       })
    return HttpResponse(t.render(c))

@login_required
def search_issue(request, journal_id):

    journal = models.Journal.objects.get(pk = journal_id)
    user_collections = get_user_collections(request.user.id)

    #Get issues where journal.id = journal_id and volume contains "q"
    selected_issues = models.Issue.objects.filter(journal = journal_id,
                                                  volume__icontains = request.REQUEST['q']).order_by('publication_date')

    #Paginated the result
    issues = get_paginated(selected_issues, request.GET.get('page', 1))

    t = loader.get_template('journalmanager/issue_dashboard.html')
    c = RequestContext(request, {
                       'issues': issues,
                       'journal': journal,
                       'user_collection': user_collections,
                       'search_query_string': request.REQUEST['q'],
                       })
    return HttpResponse(t.render(c))

@login_required
def section_index(request, journal_id):
    #FIXME: models.Journal e models.Issue ja se relacionam, avaliar
    #estas queries.
    journal = models.Journal.objects.get(pk = journal_id)
    user_collections = get_user_collections(request.user.id)

    all_sections = models.Section.objects.available(request.GET.get('is_available', 1)).filter(journal=journal_id)

    sections = get_paginated(all_sections, request.GET.get('page', 1))

    t = loader.get_template('journalmanager/section_dashboard.html')
    c = RequestContext(request, {
                       'items': sections,
                       'journal': journal,
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
    user_collections = get_user_collections(request.user.id)
    default_collections = user_collections.filter(is_default=True)

    all_centers = models.Center.objects
    if all_centers:
        all_centers = all_centers.filter(collection__in = ( collection.collection.pk for collection in default_collections ))

    centers = get_paginated(all_centers, request.GET.get('page', 1))

    t = loader.get_template('journalmanager/center_dashboard.html')
    c = RequestContext(request, {
                       'centers': centers,
                       'user_collections': user_collections,
                       })
    return HttpResponse(t.render(c))

@login_required
def add_center(request, center_id=None):
    """
    Handles new and existing centers
    """
    user_collections = get_user_collections(request.user.id)

    if request.method == 'POST':
        center_form_kwargs = {}

        if center_id is not None: #edit - preserve form-data
            filled_form = models.Center.objects.get(pk = center_id)
            center_form_kwargs['instance'] = filled_form

        add_form = CenterForm(request.POST, **center_form_kwargs)

        if add_form.is_valid():
            add_form.save_all(collection = user_collections)
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
                              'user_collections': user_collections,
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
    user_collections = get_user_collections(request.user.id)

    #Get centers where title contains the "q" value and collection equal with the user
    center_filter = models.Center.objects.filter(name__icontains = request.REQUEST['q'],
                                                            collection__in = ( collection.collection.pk for collection in default_collections )).order_by('name')

    #Paginated the result
    centers = get_paginated(center_filter, request.GET.get('page', 1))

    t = loader.get_template('journalmanager/center_dashboard.html')
    c = RequestContext(request, {
                       'centers': centers,
                       'user_collections': user_collections,
                       'search_query_string': request.REQUEST['q'],
                       })
    return HttpResponse(t.render(c))

