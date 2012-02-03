
from django import forms
from django.forms import ModelForm, DateField
from django.forms.extras.widgets import SelectDateWidget
from django.forms.models import inlineformset_factory
from journalmanager.models import *

class JournalForm(ModelForm):

    def save_all(self, creator):
        journal = self.save(commit=False)
        journal.creator = creator
        journal.save()
        self.save_m2m()
        return journal

    class Meta:
        model = Journal
        fields = ('title', 'short_title', 'acronym', 'institution', 'scielo_issn', 'print_issn', 'eletronic_issn',
          'subject_descriptors', 'study_area', 'init_year', 'init_vol', 'init_num', 'final_year','final_vol', 'final_num',
          'frequency', 'pub_status', 'alphabet', 'classification', 'national_code', 'editorial_standard','ctrl_vocabulary',
          'literature_type', 'treatment_level', 'pub_level', 'indexing_coverage', 'secs_code', 'use_license','copyrighter',
          'url_main_collection', 'url_online_submission', 'url_journal', 'pdf_access', 'subscription', 'notes','id_provided_by_the_center',
          'collections', 'validated', 'is_available' )

        #Overriding the default field types or widgets
        widgets = {
           'title': forms.TextInput(attrs={'class':'span12'}),
           'short_title': forms.TextInput(attrs={'class':'span8'}),
           'acronym': forms.TextInput(attrs={'class':'span2'}),
           'institution': forms.Select(attrs={'class':'xxlarge'}),
           'scielo_issn': forms.Select(attrs={'class':'span3', 'maxlength':'9'}),
           'print_issn': forms.TextInput(attrs={'class':'span3', 'maxlength':'9'}),
           'eletronic_issn': forms.TextInput(attrs={'class':'span3', 'maxlength':'9'}),
           'subject_descriptors': forms.Textarea(attrs={'class':'span10'}),
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
           'id_provided_by_the_center': forms.TextInput(attrs={'class':'span2'}),
           'editorial_standard': forms.Select(attrs={'class':'span10'}),
           'literature_type': forms.Select(attrs={'class':'span10'}),
           'copyrighter': forms.TextInput(attrs={'class':'span8'}),
        }

class InstitutionForm(ModelForm):
    class Meta:
        model = Institution
        exclude = ('collection',)

    def save_all(self, collection):
        institution = self.save(commit=False)
        institution.collection = collection
        institution.save()

class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = ('is_staff','is_superuser','last_login','date_joined','groups',
                   'user_permissions')
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class IssueForm(ModelForm):
    def save_all(self, collection, journal):
        issue = self.save(commit=False)
        issue.collection = collection
        issue.journal = journal
        issue.save()
        self.save_m2m()

        return issue

    class Meta:
        model = Issue
        exclude = ('collection', 'journal')
        widgets = {
            'publication_date': SelectDateWidget(),
            'init_year': SelectDateWidget(),
            'final_year': SelectDateWidget(),
        }
