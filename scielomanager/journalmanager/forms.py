# coding: utf-8
from django import forms
from django.forms import ModelForm, DateField
from django.forms.extras.widgets import SelectDateWidget
from django.forms.models import inlineformset_factory

from journalmanager import models
from journalmanager import fields

class JournalForm(ModelForm):

    print_issn = fields.ISSNField(max_length=9, required=False)
    eletronic_issn = fields.ISSNField(max_length=9, required=False)

    def save_all(self, creator):
        journal = self.save(commit=False)
        journal.creator = creator
        journal.save()
        self.save_m2m()
        return journal

    class Meta:

        model = models.Journal

        #Overriding the default field types or widgets
        widgets = {
           'title': forms.TextInput(attrs={'class':'span10'}),
           'previous_title': forms.Select(attrs={'class':'span10'}),
           'short_title': forms.TextInput(attrs={'class':'span8'}),
           'acronym': forms.TextInput(attrs={'class':'span2'}),
           'institution': forms.Select(attrs={'class':'span8'}),
           'scielo_issn': forms.Select(attrs={'class':'span3'}),
           'subject_descriptors': forms.Textarea(attrs={'class':'span12'}),
           'init_year': SelectDateWidget(),
           'init_vol': forms.TextInput(attrs={'class':'span1'}),
           'init_num': forms.TextInput(attrs={'class':'span1'}),
           'final_year': SelectDateWidget(),
           'final_vol': forms.TextInput(attrs={'class':'span1'}),
           'final_num': forms.TextInput(attrs={'class':'span1'}),
           'url_main_collection': forms.TextInput(attrs={'class':'span8'}),
           'url_online_submission': forms.TextInput(attrs={'class':'span8'}),
           'url_journal': forms.TextInput(attrs={'class':'span8'}),
           'notes': forms.Textarea(attrs={'class':'span10'}),
           'editorial_standard': forms.Select(attrs={'class':'span3'}),
           'literature_type': forms.Select(attrs={'class':'span10'}),
           'copyrighter': forms.TextInput(attrs={'class':'span8'}),
        }

class InstitutionForm(ModelForm):
    class Meta:
        model = models.Institution
        exclude = ('collection',)

    def save_all(self, collection):
        institution = self.save(commit=False)
        institution.collection = collection
        institution.save()

class UserForm(ModelForm):
    class Meta:
        model = models.User
        exclude = ('is_staff','is_superuser','last_login','date_joined','groups',
                   'user_permissions')
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class IssueForm(ModelForm):
    section = forms.ModelMultipleChoiceField(models.Section.objects.none(), required=True)

    widgets = {
        'section': forms.Select(attrs={'class':'span3'}),
    }

    def __init__(self, *args, **kwargs):
        """
        Section field queryset is overridden to display only
        sections related to a given journal.

        ``journal_id`` should not be passed to the superclass
        ``__init__`` method.
        """
        journal_id = kwargs.pop('journal_id', None)
        super(IssueForm, self).__init__(*args, **kwargs)
        if journal_id is not None:
            self.fields['section'].queryset = models.Section.objects.filter(journal=journal_id)


    def save_all(self, collection, journal):
        issue = self.save(commit=False)
        issue.collection = collection
        issue.journal = journal
        issue.save()
        self.save_m2m()

        return issue

    class Meta:
        model = models.Issue
        exclude = ('collection', 'journal', 'created', 'updated')
        widgets = {
            'publication_date': SelectDateWidget(),
            'init_year': SelectDateWidget(),
            'final_year': SelectDateWidget(),
        }

class SectionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SectionForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.fields['code'].widget.attrs['readonly'] = True

    def clean_code(self):
        return self.instance.code

    def save_all(self, journal):
        section = self.save(commit=False)
        section.journal = journal
        section.save()

        return section

    class Meta:
      model = models.Section

class InstitutionCollectionsForm(ModelForm):
    class Meta:
      model = models.Institution
      widgets = { 
        'collection':forms.Select(attrs={'class':'span10', 'rows':'3'}), 
      }

class UserCollectionsForm(ModelForm):
    class Meta:
      model = models.UserCollections
      widgets = { 
        'collection':forms.Select(attrs={'class':'span10', 'rows':'3'}), 
      }

class JournalStudyAreaForm(ModelForm):
    class Meta:
      model = models.JournalStudyArea
      widgets = {
        'studyarea':forms.TextInput(attrs={'class':'span10', 'rows':'3'}), 
      }

class JournalMissionForm(ModelForm):
    class Meta:
      model = models.JournalMission
      widgets = {
        'description':forms.Textarea(attrs={'class':'span10', 'rows':'3'}),
      }

class JournalTitleForm(ModelForm):
    class Meta:
      model = models.JournalTitle
      widgets = {
        'title': forms.TextInput(attrs={'class':'span11'}),
      }



class CenterForm(ModelForm):
    class Meta:
        model = models.Center
        exclude = ('collection',)

    def save_all(self, collection):
        center = self.save(commit=False)
        center.collection = collection
        center.save()
