#coding: utf-8

from django import forms
from django.forms import ModelForm
from . import models


class EditorialMemberForm(ModelForm):
    class Meta:
        model = models.EditorialMember
        exclude = ('board', )
        widgets = {
            'role': forms.Select(attrs={'class': 'chzn-select'}),
        }
