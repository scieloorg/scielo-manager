from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms.models import inlineformset_factory
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import loader
from django.template.context import RequestContext
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from scielomanager.journalmanager.models import *
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
    users = User.objects.get_query_set().filter(userprofile__collection=user_collection)
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
    user = Institution.objects.get(id=user_id)
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
            uprof = UserProfile();
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
    journal = Journal.objects.get(id=journal_id)
    t = loader.get_template('journalmanager/show_journal.html')
    c = RequestContext(request, {
                       'journal': journal,
                       'collection': user_collection,
                       })
    return HttpResponse(t.render(c))

@login_required
def open_journal(request):
    journals = Journal.objects.all()
    t = loader.get_template('journalmanager/journal_dashboard.html')
    c = RequestContext(request, {
                       'journals': journals,
                       })
    return HttpResponse(t.render(c))

@login_required
def journal_index(request):
    user_collection = request.user.userprofile_set.get().collection
    all_journals = Journal.objects.filter(collections=user_collection)

    journals = get_paginated(all_journals, request.GET.get('page', 1))

    t = loader.get_template('journalmanager/journal_dashboard.html')
    c = RequestContext(request, {
                       'journals': journals,
                       'collection': user_collection,
                       })
    return HttpResponse(t.render(c))

# @login_required
# def add_journal(request):
#     user_collection = request.user.userprofile_set.get().collection
#     if request.method == 'POST':

#         add_form = JournalForm(request.POST)

#         if add_form.is_valid():
#             add_form.save_all(creator=request.user)
#             return HttpResponseRedirect("/journal")
#         else:
#             return render_to_response('journalmanager/add_journal.html', {
#                                       'mode': 'add_journal',
#                                       'add_form': add_form,
#                                       'user_name': request.user.pk,
#                                       'collection': user_collection},
#                                       context_instance=RequestContext(request))
#     else:
#         add_form = JournalForm()
#         return render_to_response('journalmanager/add_journal.html', {
#                               'add_form': add_form,
#                               'mode': 'add_journal',
#                               'user_name': request.user.pk,
#                               'collection': user_collection},
#                               context_instance=RequestContext(request))
@login_required
def add_journal(request, journal_id=None):
    """
    Handles new and existing journals
    """

    user_collection = request.user.userprofile_set.get().collection

    if request.method == 'POST':
        journal_form_kwargs = {}

        if journal_id is not None: #edit - preserve form-data
            filled_form = Journal.objects.get(pk=journal_id)
            journal_form_kwargs['instance'] = filled_form

        add_form = JournalForm(request.POST, **journal_form_kwargs)

        if add_form.is_valid():
            add_form.save_all(creator=request.user)
            return HttpResponseRedirect(reverse('journal.index'))
        else:
            return render_to_response('journalmanager/add_journal.html', {
                                      'add_form': add_form,
                                      'user_name': request.user.pk,
                                      'collection': user_collection,
                                      },
                                      context_instance=RequestContext(request))
    else:

        if journal_id is None: #new
            add_form = JournalForm()
        else:
            filled_form = Journal.objects.get(pk=journal_id)
            add_form = JournalForm(instance=filled_form)

        return render_to_response('journalmanager/add_journal.html', {
                                  'add_form': add_form,
                                  'user_name': request.user.pk,
                                  'collection': user_collection,
                                  },
                                  context_instance=RequestContext(request))

@login_required
def delete_journal(request, journal_id):
  Journal.objects.get(pk=journal_id).delete()
  return HttpResponseRedirect("/journal")

@login_required
def show_institution(request, institution_id):
    user_collection = request.user.userprofile_set.get().collection
    institution = Institution.objects.get(id=institution_id)
    journals = Journal.objects.filter(institution=institution_id)
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
    all_institutions = Institution.objects.filter(collection=user_collection)

    institutions = get_paginated(all_institutions, request.GET.get('page', 1))

    t = loader.get_template('journalmanager/institution_dashboard.html')
    c = RequestContext(request, {
                       'institutions': institutions,
                       'collection': user_collection,
                       })
    return HttpResponse(t.render(c))

@login_required
def add_institution(request):
    user_collection = request.user.userprofile_set.get().collection
    if request.method == 'POST':

        add_form = InstitutionForm(request.POST)

        if add_form.is_valid():
            add_form.save_all(collection=user_collection)
            return HttpResponseRedirect("/journal/institution")
        else:
            return render_to_response('journalmanager/add_institution.html', {
                                      'mode': 'add_institution',
                                      'add_form': add_form,
                                      'user_name': request.user.pk,
                                      'collection': user_collection},
                                      context_instance=RequestContext(request))
    else:
        add_form = InstitutionForm()
        return render_to_response('journalmanager/add_institution.html', {
                              'add_form': add_form,
                              'mode': 'institution_journal',
                              'user_name': request.user.pk,
                              'collection': user_collection},
                              context_instance=RequestContext(request))

@login_required
def edit_institution(request, institution_id):
    filled_form = Institution.objects.get(pk=institution_id)
    user_collection = request.user.userprofile_set.get().collection
    if request.method == 'POST':

        edit_form = InstitutionForm(request.POST, instance=filled_form)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect("/journal/institution")
        else:
            return render_to_response('journalmanager/edit_institution.html', {
                                      'edit_form': edit_form,
                                      'mode': 'edit_institution',
                                      'institution_id':institution_id,
                                      'user_name': request.user.pk,
                                      'collection': user_collection},
                                      context_instance=RequestContext(request))
    else:
        edit_form = InstitutionForm(instance=filled_form)
        return render_to_response('journalmanager/edit_institution.html', {
                              'edit_form': edit_form,
                              'mode': 'edit_institution',
                              'institution_id':institution_id,
                              'user_name': request.user.pk,
                              'collection': user_collection},
                              context_instance=RequestContext(request))

@login_required
def delete_institution(request,institution_id):
  Institution.objects.get(pk=institution_id).delete()
  return HttpResponseRedirect("/journal/institution")

@login_required
def show_issue(request, issue_id):
    issue = Issue.objects.get(id=issue_id)
    journal = issue.journal
    t = loader.get_template('journalmanager/show_issue.html')
    c = RequestContext(request, {
                       'issue': issue,
                       'journal': journal,
                       })
    return HttpResponse(t.render(c))

@login_required
def issue_index(request, journal_id):
    journal = Journal.objects.get(id=journal_id)
    user_collection = request.user.userprofile_set.get().collection

    all_issues = Issue.objects.filter(journal=journal_id)

    issues = get_paginated(all_issues, request.GET.get('page', 1))

    t = loader.get_template('journalmanager/issue_dashboard.html')
    c = RequestContext(request, {
                       'issues': issues,
                       'journal': journal,
                       'collection': user_collection,
                       })
    return HttpResponse(t.render(c))

@login_required
def add_issue(request, journal_id):
    journal = Journal.objects.get(id=journal_id)
    user_collection = request.user.userprofile_set.get().collection
    saved = False
    add_form = IssueForm()
    if request.method == 'POST':
        add_form = IssueForm(request.POST)
        if add_form.is_valid():
            issue_data = add_form.save(commit=False)
            issue_data.update_date = datetime.now
            if issue_data.creation_date == None:
                issue_data.creation_date = issue_data.update_date
            issue_data.collection = user_collection
            issue_data.journal = journal
            issue_data.save()
            saved = True
    if saved == True:
        return HttpResponseRedirect("/journal/issue/" + journal_id )
    else:
        return render_to_response('journalmanager/add_issue.html', {
                                      'mode': 'add_issue',
                                      'add_form': add_form,
                                      'journal': journal,
                                      'user_name': request.user.pk,
                                      'collection': user_collection},
                                      context_instance=RequestContext(request))

@login_required
def edit_issue(request, issue_id):
    form_filled = Issue.objects.get(pk=issue_id)
    journal = form_filled.journal
    user_collection = request.user.userprofile_set.get().collection
    saved = False
    if request.method == 'POST':
        form = IssueForm(request.POST,instance=form_filled)
        if form.is_valid():
            issue_data = form.save(commit=False)
            issue_data.update_date = datetime.now
            if issue_data.creation_date == None:
                issue_data.creation_date = issue_data.update_date
            issue_data.save()
            saved = True
        else:
            edit_form = IssueForm(request.POST,instance=form_filled)
    else:
        edit_form = IssueForm(instance=form_filled)
    if saved == True:
        return HttpResponseRedirect("/journal/issue/" + str(journal.id))
    else:
        return render_to_response('journalmanager/edit_issue.html', {
                              'edit_form': edit_form,
                              'mode': 'edit_issue',
                              'issue_id': issue_id,
                              'user_name': request.user.pk,
                              'journal_id': journal.id,
                              'journal': journal,
                              'collection': user_collection},
                              context_instance=RequestContext(request))

@login_required
def delete_issue(request, issue_id):
    issue_data = Issue.objects.get(pk=issue_id)
    journal = issue_data.journal
    user_collection = request.user.userprofile_set.get().collection
    issue_data.update_date = datetime.now
    issue_data.is_available = False
    issue_data.save()
    return HttpResponseRedirect("/journal/issue/" + str(journal.id))

@login_required
def search_journal(request):
    user_collection = request.user.userprofile_set.get().collection

    #Get journals where title contains the "q" value and collection equal with the user
    journals_filter = Journal.objects.filter(title__icontains=request.REQUEST['q'], collections=user_collection).order_by('title')

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
    institutions_filter = Institution.objects.filter(name__icontains=request.REQUEST['q'], collection=user_collection).order_by('name')

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

    journal = Journal.objects.get(id=journal_id)
    user_collection = request.user.userprofile_set.get().collection
    #Get issues where journal.id = journal_id and volume contains "q"
    selected_issues = Issue.objects.filter(journal=journal_id, volume__icontains=request.REQUEST['q']).order_by('publication_date')

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

