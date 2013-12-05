# coding: utf-8
from django import forms
from django.core.exceptions import ValidationError

from journalmanager import models as jm_models


class BlidModelChoiceField(forms.ModelChoiceField):
    def to_python(self, value):
        try:
            issue_pk = int(value)
        except ValueError:
            raise ValidationError(self.error_messages['invalid_choice'])
        try:
            return jm_models.Issue.objects.get(pk=issue_pk)
        except jm_models.Issue.DoesNotExist:
            raise ValidationError(self.error_messages['invalid_choice'])


class MarkupFilesForm(forms.Form):
    journal = forms.ModelChoiceField(queryset=jm_models.Journal.objects.none())
    issue = BlidModelChoiceField(queryset=jm_models.Issue.objects.none())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MarkupFilesForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['journal'].queryset = jm_models.Journal.objects.all_by_user(user)
