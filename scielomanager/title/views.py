from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.core.paginator import EmptyPage
from django.core.paginator import InvalidPage
from django.core.paginator import Paginator
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
from scielomanager.title.models import *
from scielomanager.title.forms import *

# Create your views here.
def index(request):
    t = loader.get_template('title/home_title.html')
    c = RequestContext(request)
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
                return HttpResponseRedirect(next)
            else:
                t = loader.get_template('title/home_title.html')
                c = RequestContext(request, {
                                   'active': True,})
                return HttpResponse(t.render(c))
        else:
            t = loader.get_template('title/home_title.html')
            c = RequestContext(request, {
                               'invalid': True, 'next': next})
            return HttpResponse(t.render(c))
    else:
        t = loader.get_template('title/home_title.html')
        if next:
            c = RequestContext(request, {'required': True, 'next': next})
        else:
            c = RequestContext(request, {'next': next})
        return HttpResponse(t.render(c))
    
def user_logout(request):
    logout(request)
    t = loader.get_template('title/home_title.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))
    
@login_required
def user_index(request):
    user_collection = request.user.userprofile_set.get().collection
    users = User.objects.get_query_set().filter(userprofile__collection=user_collection)
    t = loader.get_template('title/user_dashboard.html')
    c = RequestContext(request, {
                       'users': users,
                       'collection': user_collection,
                       })
    return HttpResponse(t.render(c))

@login_required
def title_index(request):
    user_collection = request.user.userprofile_set.get().collection
    titles = Title.objects.filter(collection=user_collection)
    t = loader.get_template('title/title_dashboard.html')
    c = RequestContext(request, {
                       'titles': titles,
                       'collection': user_collection,                       
                       })
    return HttpResponse(t.render(c))
    
@login_required
def publisher_index(request):
    user_collection = request.user.userprofile_set.get().collection
    publishers = Publisher.objects.filter(collection=user_collection)
    t = loader.get_template('title/publisher_dashboard.html')
    c = RequestContext(request, {
                       'publishers': publishers,
                       })
    return HttpResponse(t.render(c))

@login_required
def show_title(request,title_id):
    user_collection = request.user.userprofile_set.get().collection   
    title = Title.objects.get(id=title_id)
    t = loader.get_template('title/show_title.html')
    c = RequestContext(request, {
                       'title': title,
                       'collection': user_collection,                       
                       })
    return HttpResponse(t.render(c))
   
@login_required
def add_publisher(request):
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

            return HttpResponseRedirect("/title/user")
        else:
             
            add_user_form = UserForm() # An unbound form
            
            return render_to_response('title/add_user.html', {
                                      'add_user_form': add_user_form,
                                      'type': type,
                                      'mode': 'add_user',
                                      'form': form,
                                      'user_name': request.user.pk},
                                      context_instance=RequestContext(request))
    else:
        #recovering Evaluation Data to input form fields
        add_user_form = UserForm() # An unbound form
    return render_to_response('title/add_user.html', {
                              'add_user_form': add_user_form,
                              'type': type,
                              'mode': 'user_title',
                              'user_name': request.user.pk},
                              context_instance=RequestContext(request))
    
@login_required
def add_user(request):
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

            return HttpResponseRedirect("/title/user")
        else:
             
            add_user_form = UserForm() # An unbound form
            
            return render_to_response('title/add_user.html', {
                                      'add_user_form': add_user_form,
                                      'type': type,
                                      'mode': 'add_user',
                                      'form': form,
                                      'user_name': request.user.pk},
                                      context_instance=RequestContext(request))
    else:
        #recovering Evaluation Data to input form fields
        add_user_form = UserForm() # An unbound form
    return render_to_response('title/add_user.html', {
                              'add_user_form': add_user_form,
                              'type': type,
                              'mode': 'user_title',
                              'user_name': request.user.pk},
                              context_instance=RequestContext(request))
    
@login_required
def add_title(request):
    if request.method == 'POST':
        #instance of form
        form = TitleForm(request.POST)
        if form.is_valid():
            #Get the user and create a new evaluation

            user_collection = Collection.objects.get(manager=request.user)
            ftitle = form.save(commit=False)
            ftitle.creator = request.user
            ftitle.collection = user_collection
            ftitle.save()

            title = Title()
            return HttpResponseRedirect("/title")
        else:
             
            add_title_form = TitleForm() # An unbound form
            
            return render_to_response('title/add_title.html', {
                                      'add_title_form': add_title_form,
                                      'type': type,
                                      'mode': 'add_title',
                                      'form': form,
                                      'user_name': request.user.pk},
                                      context_instance=RequestContext(request))
    else:
        #recovering Evaluation Data to input form fields
        add_title_form = TitleForm() # An unbound form
    return render_to_response('title/add_title.html', {
                              'add_title_form': add_title_form,
                              'type': type,
                              'mode': 'add_title',
                              'user_name': request.user.pk},
                              context_instance=RequestContext(request))

@login_required
def open_title(request):
    titles = Title.objects.all()
    t = loader.get_template('title/title_dashboard.html')
    c = RequestContext(request, {
                       'titles': titles,
                       })
    return HttpResponse(t.render(c))