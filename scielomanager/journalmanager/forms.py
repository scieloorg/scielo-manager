# coding: utf-8
from django import forms
from django.forms import ModelForm, DateField
from django.forms.extras.widgets import SelectDateWidget
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from journalmanager import models
from scielo_extensions import formfields as fields

class JournalForm(ModelForm):

    print_issn = fields.ISSNField(max_length=9, required=False)
    eletronic_issn = fields.ISSNField(max_length=9, required=False)
    collections = forms.ModelMultipleChoiceField(models.Collection.objects.none(),
        widget=forms.SelectMultiple(attrs={'title': _('Select one or more collections')}),
        required=True)

    def __init__(self, *args, **kwargs):
        """
        Collection field queryset is overridden to display only
        collections related to a user.

        ``collections_qset`` should not be passed to the superclass
        ``__init__`` method.
        """
        collections_qset = kwargs.pop('collections_qset', None)
        super(JournalForm, self).__init__(*args, **kwargs)

        if collections_qset is not None:
            self.fields['collections'].queryset = models.Collection.objects.filter(pk__in = (collection.collection.pk for collection in collections_qset))


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
           'title': forms.TextInput(attrs={'class':'span9'}),
           'previous_title': forms.Select(attrs={'class':'span9'}),
           'short_title': forms.TextInput(attrs={'class':'span8'}),
           'acronym': forms.TextInput(attrs={'class':'span2'}),
           'publisher': forms.Select(attrs={'class':'span8'}),
           'scielo_issn': forms.Select(attrs={'class':'span3'}),
           'subject_descriptors': forms.Textarea(attrs={'class':'span9'}),
           'init_year': SelectDateWidget(),
           'init_vol': forms.TextInput(attrs={'class':'span1'}),
           'init_num': forms.TextInput(attrs={'class':'span1'}),
           'final_year': SelectDateWidget(),
           'final_vol': forms.TextInput(attrs={'class':'span1'}),
           'final_num': forms.TextInput(attrs={'class':'span1'}),
           'url_main_collection': forms.TextInput(attrs={'class':'span9'}),
           'url_online_submission': forms.TextInput(attrs={'class':'span9'}),
           'url_journal': forms.TextInput(attrs={'class':'span9'}),
           'notes': forms.Textarea(attrs={'class':'span9'}),
           'editorial_standard': forms.Select(attrs={'class':'span3'}),
           'literature_type': forms.Select(attrs={'class':'span8'}),
           'copyrighter': forms.TextInput(attrs={'class':'span8'}),
        }

class PublisherForm(ModelForm):
    class Meta:
        model = models.Publisher


class UserForm(ModelForm):
    class Meta:
        model = models.User
        exclude = ('is_staff','is_superuser','last_login','date_joined',
                   'user_permissions', 'email')
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class PasswordChangeForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'span3'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'span3'}))
    new_password_again = forms.CharField(widget=forms.PasswordInput(attrs={'class':'span3'}))

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


    def save_all(self, journal):
        issue = self.save(commit=False)
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

class PublisherCollectionsForm(ModelForm):
    class Meta:
      model = models.Publisher
      widgets = {
        'collection':forms.Select(attrs={'class':'span10', 'rows':'3'}),
      }

class CenterCollectionsForm(ModelForm):
    class Meta:
      model = models.Center
      widgets = {
        'collection':forms.Select(attrs={'class':'span10', 'rows':'3'}),
      }

class UserCollectionsForm(ModelForm):
    class Meta:
      model = models.UserCollections
      widgets = {
        'collection':forms.Select(attrs={'class':'span10', 'rows':'3'}),
      }

# class JournalCollectionsForm(ModelForm):
#     collection = forms.ModelChoiceField(models.JournalCollections.objects.none(), required=True)

#     def __init__(self, *args, **kwargs):
#         """
#         Collection field queryset is overridden to display only
#         collections related to a user.

#         ``collections_qset`` should not be passed to the superclass
#         ``__init__`` method.
#         """
#         collections_qset = kwargs.pop('collections_qset', None)
#         super(JournalCollectionsForm, self).__init__(*args, **kwargs)

#         if collections_qset is not None:
#             self.fields['collection'].queryset = models.Collection.objects.filter(pk__in = (collection.collection.pk for collection in collections_qset))


#     class Meta:
#       model = models.JournalCollections
#       widgets = {
#         'collection':forms.Select(attrs={'class':'span10', 'rows':'3'}),
#       }


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
        'description':forms.Textarea(attrs={'class':'span6', 'rows':'3'}),
      }

class JournalTitleForm(ModelForm):
    class Meta:
      model = models.JournalTitle
      widgets = {
        'title': forms.TextInput(attrs={'class':'span6  '}),
      }

class CenterForm(ModelForm):
    class Meta:
        model = models.Center
        exclude = ('collection',)