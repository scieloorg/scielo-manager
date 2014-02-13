# -*- coding: utf-8 -*-
from django.forms import ModelForm, Textarea, TextInput
from articletrack import models


class CommentMessageForm(ModelForm):
    class Meta:
        model = models.Comment
        fields = ('message',)
        widgets = {
            'message': Textarea(attrs={'class': 'span12'}),
        }


class TicketForm(ModelForm):
    class Meta:
        model = models.Ticket
        fields = ('title', 'message',)
        widgets = {
            'title': TextInput(attrs={'class': 'span12'}),
            'message': Textarea(attrs={'class': 'span12'}),
        }
