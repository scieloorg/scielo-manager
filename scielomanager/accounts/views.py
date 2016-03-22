# coding:utf-8
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate
from django.conf import settings
from journalmanager.forms import UserProfileForm

from . import forms


@login_required
def my_account(request):
    profile_form = UserProfileForm(instance=request.user.get_profile())
    password_form = forms.PasswordChangeForm()
    # password_form faz post na view: password_change, então não deve ser tratado aqui
    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, instance=request.user.get_profile())
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, _(u'Saved successfully'))
        else:
            messages.error(request, _(u'There are some errors or missing data.'))

    my_collecttions = [{'name': c.name, 'is_manager': c.is_managed_by_user(request.user)} for c in request.user.user_collection.all()]

    context = {
        'profile_form': profile_form,
        'password_form': password_form,
        'my_collecttions': my_collecttions,
    }
    return render_to_response('accounts/my_account.html', context,
        context_instance=RequestContext(request))


@login_required
def password_change(request):

    if request.method == 'POST':
        form = forms.PasswordChangeForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            if cleaned_data['new_password'] != cleaned_data['new_password_again']:
                messages.error(request, _(u'Your new password and new password confirmation must match.'))
                return HttpResponseRedirect(reverse('journalmanager.password_change'))

            auth_user = authenticate(username=request.user.username,
                                     password=cleaned_data['password'])
            if auth_user:
                auth_user.set_password(cleaned_data['new_password'])
                auth_user.save()
            else:
                messages.error(request, _(u'Your current password does not match. Please try again.'))
                return HttpResponseRedirect(reverse('journalmanager.password_change'))

            messages.info(request, _(u'Your new password has been set.'))
            return HttpResponseRedirect(reverse('journalmanager.my_account'))
    else:
        form = forms.PasswordChangeForm()

    return render_to_response(
        'accounts/password_change.html',
        {'form': form},
        context_instance=RequestContext(request))


def unauthorized(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(settings.LOGIN_URL)

    next = request.GET.get('next', None)

    return render_to_response('accounts/unauthorized.html',
        {'next': next}, context_instance=RequestContext(request))
