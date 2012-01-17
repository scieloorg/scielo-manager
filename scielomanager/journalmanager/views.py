from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
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

# Create your views here.
def index(request):
    t = loader.get_template('journalmanager/home_journal.html')
    if request.user.is_authenticated():
        user_collection = request.user.userprofile_set.get().collection
    else:
        user_collection = ""
    c = RequestContext(request,{'collection':user_collection,})
    return HttpResponse(t.render(c),)

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
def user_index(request):
    user_collection = request.user.userprofile_set.get().collection
    users = User.objects.get_query_set().filter(userprofile__collection=user_collection)
    t = loader.get_template('journalmanager/user_dashboard.html')
    c = RequestContext(request, {
                       'users': users,
                       'collection': user_collection,
                       })
    return HttpResponse(t.render(c))

@login_required
def journal_index(request):
    user_collection = request.user.userprofile_set.get().collection
    all_journals = Journal.objects.filter(collection=user_collection)

    journals = get_paginated(all_journals, request.GET.get('page', 1))

    t = loader.get_template('journalmanager/journal_dashboard.html')
    c = RequestContext(request, {
                       'journals': journals,
                       'collection': user_collection,
                       })
    return HttpResponse(t.render(c))

@login_required
def institution_index(request):
    user_collection = request.user.userprofile_set.get().collection
    institution = Institution.objects.filter(collection=user_collection)
    t = loader.get_template('journalmanager/institution_dashboard.html')
    c = RequestContext(request, {
                       'institutions': institution,
                       'collection': user_collection,
                       })
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
def show_journal(request,journal_id):
    user_collection = request.user.userprofile_set.get().collection
    journal = Journal.objects.get(id=journal_id)
    t = loader.get_template('journalmanager/show_journal.html')
    c = RequestContext(request, {
                       'journal': journal,
                       'collection': user_collection,
                       })
    return HttpResponse(t.render(c))

@login_required
def show_institution(request,institution_id):
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
                                      'type': type,
                                      'mode': 'add_user',
                                      'form': form,
                                      'user_name': request.user.pk,
                                      'collection': user_collection},
                                      context_instance=RequestContext(request))
    else:
        #recovering Evaluation Data to input form fields
        add_user_form = UserForm() # An unbound form
    return render_to_response('journalmanager/add_user.html', {
                              'add_user_form': add_user_form,
                              'type': type,
                              'mode': 'user_journal',
                              'user_name': request.user.pk,
                              'collection': user_collection},
                              context_instance=RequestContext(request))

@login_required
def add_journal(request):
    user_collection = request.user.userprofile_set.get().collection
    if request.method == 'POST':
        #instance of form
        form = JournalForm(request.POST)
        if form.is_valid():
            #Get the user and create a new evaluation
            user_collection = Collection.objects.get(manager=request.user)
            fjournal = form.save(commit=False)
            fjournal.creator = request.user
            fjournal.collection = user_collection
            fjournal.save()
            journal = Journal()
            return HttpResponseRedirect("/journal")
        else:
            add_journal_form = JournalForm() # An unbound form
            return render_to_response('journalmanager/add_journal.html', {
                                      'add_journal_form': add_journal_form,
                                      'type': type,
                                      'mode': 'add_journal',
                                      'form': form,
                                      'user_name': request.user.pk,
                                      'collection': user_collection},
                                      context_instance=RequestContext(request))
    else:
        #recovering Evaluation Data to input form fields
        add_journal_form = JournalForm() # An unbound form
    return render_to_response('journalmanager/add_journal.html', {
                              'add_journal_form': add_journal_form,
                              'type': type,
                              'mode': 'add_journal',
                              'user_name': request.user.pk,
                              'collection': user_collection},
                              context_instance=RequestContext(request))

@login_required
def add_institution(request):
    user_collection = request.user.userprofile_set.get().collection
    if request.method == 'POST':
        #instance of form
        form = InstitutionForm(request.POST)
        if form.is_valid():
            #Get the user and create a new evaluation
            user_collection = request.user.userprofile_set.get().collection
            finstitution = form.save(commit=False)
            finstitution.collection = user_collection
            finstitution.save()
            return HttpResponseRedirect("/journal/institution")
        else:
            add_institution_form = UserForm() # An unbound form
            return render_to_response('journalmanager/add_institution.html', {
                                      'add_institution_form': add_institution_form,
                                      'type': type,
                                      'mode': 'add_institution',
                                      'form': form,
                                      'user_name': request.user.pk,
                                      'collection': user_collection},
                                      context_instance=RequestContext(request))
    else:
        #recovering Evaluation Data to input form fields
        add_institution_form = InstitutionForm() # An unbound form
    return render_to_response('journalmanager/add_institution.html', {
                              'add_institution_form': add_institution_form,
                              'type': type,
                              'mode': 'institution_journal',
                              'user_name': request.user.pk,
                              'collection': user_collection},
                              context_instance=RequestContext(request))

@login_required
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
                                      'type': type,
                                      'mode': 'edit_user',
                                      'user_id': user_id,
                                      'user_name': request.user.pk,
                                      'collection': user_collection},
                                      context_instance=RequestContext(request))
    else:
        edit_user_form = UserForm(instance=formFilled)
    return render_to_response('journalmanager/edit_user.html', {
                              'edit_user_form': edit_user_form,
                              'type': type,
                              'mode': 'edit_user',
                              'user_id': user_id,
                              'user_name': request.user.pk,
                              'collection': user_collection},
                              context_instance=RequestContext(request))

@login_required
def edit_journal(request,journal_id):
    #recovering Journal Data to input form fields
    formFilled = Journal.objects.get(pk=journal_id)
    user_collection = request.user.userprofile_set.get().collection
    if request.method == 'POST':
        form = JournalForm(request.POST,instance=formFilled)
        if form.is_valid():
            fjournal = form.save(commit=False)
            fjournal.creator = request.user
            fjournal.save()
            journal = Journal()
            return HttpResponseRedirect("/journal")
        else:
            edit_journal_form = JournalForm(request.POST,instance=formFilled)
            return render_to_response('journalmanager/edit_journal.html', {
                                      'edit_journal_form': edit_journal_form,
                                      'type': type,
                                      'mode': 'edit_journal',
                                      'journal_id': journal_id,
                                      'user_name': request.user.pk,
                                      'collection': user_collection},
                                      context_instance=RequestContext(request))
    else:
        edit_journal_form = JournalForm(instance=formFilled)
    return render_to_response('journalmanager/edit_journal.html', {
                              'edit_journal_form': edit_journal_form,
                              'type': type,
                              'mode': 'edit_journal',
                              'journal_id': journal_id,
                              'user_name': request.user.pk,
                              'collection': user_collection},
                              context_instance=RequestContext(request))

@login_required
def delete_journal(request,journal_id):
  Journal.objects.get(pk=journal_id).delete()
  return HttpResponseRedirect("/journal")

@login_required
def edit_institution(request,institution_id):
    #recovering Institution Data to input form fields
    formFilled = Institution.objects.get(pk=institution_id)
    user_collection = request.user.userprofile_set.get().collection
    if request.method == 'POST':
        form = InstitutionForm(request.POST,instance=formFilled)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/journal/institution")
        else:
            edit_institution_form = UserForm(request.POST,instance=formFilled)
            return render_to_response('journalmanager/edit_institution.html', {
                                      'edit_institution_form': edit_institution_form,
                                      'type': type,
                                      'mode': 'edit_institution',
                                      'institution_id':institution_id,
                                      'user_name': request.user.pk,
                                      'collection': user_collection},
                                      context_instance=RequestContext(request))
    else:
        edit_institution_form = InstitutionForm(instance=formFilled)
    return render_to_response('journalmanager/edit_institution.html', {
                              'edit_institution_form': edit_institution_form,
                              'type': type,
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
def open_journal(request):
    journals = Journal.objects.all()
    t = loader.get_template('journalmanager/journal_dashboard.html')
    c = RequestContext(request, {
                       'journals': journals,
                       })
    return HttpResponse(t.render(c))