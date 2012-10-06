# coding:utf-8
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate

from scielomanager.accounts import forms


@login_required
def my_account(request):
    return render_to_response('accounts/my_account.html', {},
        context_instance=RequestContext(request))


@login_required
def password_change(request):

    if request.method == 'POST':
        form = forms.PasswordChangeForm(request.POST)
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
        form = forms.PasswordChangeForm()

    return render_to_response(
        'accounts/password_change.html',
        {'form': form},
        context_instance=RequestContext(request))
