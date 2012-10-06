# coding: utf-8
from django import forms


class PasswordChangeForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'span3'}))
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'span3'}))
    new_password_again = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'span3'}))
