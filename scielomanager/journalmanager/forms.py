# coding: utf-8
import re
from django import forms
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from django.core.files.images import get_image_dimensions
from django.contrib.auth.models import Group
from django.core.exceptions import NON_FIELD_ERRORS

from journalmanager import models
from journalmanager import choices
from scielo_extensions import formfields as fields
from django.conf import settings


class UserCollectionContext(ModelForm):
    """
    Inherit from this base class if you have a ``collections`` attribute
    that needs to be contextualized with user collections.
    """

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
        super(UserCollectionContext, self).__init__(*args, **kwargs)

        if collections_qset is not None:
            self.fields['collections'].queryset = models.Collection.objects.filter(
                pk__in=(collection.collection.pk for collection in collections_qset))


class JournalForm(ModelForm):
    print_issn = fields.ISSNField(max_length=9, required=False)
    eletronic_issn = fields.ISSNField(max_length=9, required=False)
    languages = forms.ModelMultipleChoiceField(models.Language.objects.all(),
        widget=forms.SelectMultiple(attrs={'title': _('Select one or more languages')}),
        required=True)
    abstract_keyword_languages = forms.ModelMultipleChoiceField(models.Language.objects.all(),
        widget=forms.SelectMultiple(attrs={'title': _('Select one or more languages')}),
        required=True)
    sponsor = forms.ModelMultipleChoiceField(models.Sponsor.objects.all(),
        widget=forms.SelectMultiple(attrs={'title': _('Select one or more sponsors')}),
        required=True)
    subject_categories = forms.ModelMultipleChoiceField(models.SubjectCategory.objects.all(),
        widget=forms.SelectMultiple(attrs={'title': _('Select one or more categories')}),
        required=False)
    study_areas = forms.ModelMultipleChoiceField(models.StudyArea.objects.all(),
        widget=forms.SelectMultiple(attrs={'title': _('Select one or more study area')}),
        required=False)
    regex = re.compile(r'^(1|2)\d{3}$')
    collection = forms.ModelChoiceField(models.Collection.objects.none(),
        required=True)

    def __init__(self, *args, **kwargs):
        collections_qset = kwargs.pop('collections_qset', None)
        super(JournalForm, self).__init__(*args, **kwargs)

        if collections_qset is not None:
            self.fields['collection'].queryset = models.Collection.objects.filter(
                pk__in=(collection.collection.pk for collection in collections_qset))

    def save_all(self, creator):
        journal = self.save(commit=False)
        journal.creator = creator

        if not journal.pub_status_changed_by_id:
            journal.pub_status_changed_by = creator

        journal.save()
        self.save_m2m()
        return journal

    def clean(self):
        cleaned_data = self.cleaned_data
        print_issn = cleaned_data.get("print_issn")
        eletronic_issn = cleaned_data.get("eletronic_issn")

        if not (print_issn or eletronic_issn):
            msg = u'Eletronic ISSN or Print ISSN must be filled.'
            self._errors['scielo_issn'] = self.error_class([msg])

        return cleaned_data

    def clean_acronym(self):
        return self.cleaned_data["acronym"].lower()

    def clean_init_year(self):

        if self.cleaned_data["init_year"]:
            result = self.regex.match(self.cleaned_data["init_year"])

            if result is None:
                raise forms.ValidationError(u'Invalid Date')

        return self.cleaned_data["init_year"]

    def clean_final_year(self):

        if self.cleaned_data["final_year"]:
            result = self.regex.match(self.cleaned_data["final_year"])

            if result is None:
                raise forms.ValidationError(u'Invalid Date')

        return self.cleaned_data["final_year"]

    def clean_cover(self):

        if self.cleaned_data['cover']:

            if not self.cleaned_data['cover'].name:
                if not self.cleaned_data['cover'].content_type in settings.IMAGE_CONTENT_TYPE:
                    raise forms.ValidationError(u'File type is not supported')

            if self.cleaned_data['cover'].size > settings.IMAGE_SIZE:
                raise forms.ValidationError(u'File size not allowed')

            w, h = get_image_dimensions(self.cleaned_data['cover'])

            if w != settings.IMAGE_DIMENSIONS['width_cover']:
                raise forms.ValidationError("The image is %ipx pixel wide. It's supposed to be %spx" % (w, settings.IMAGE_DIMENSIONS['width_cover']))
            if h != settings.IMAGE_DIMENSIONS['height_cover']:
                raise forms.ValidationError("The image is %ipx pixel high. It's supposed to be %spx" % (h, settings.IMAGE_DIMENSIONS['height_cover']))

        return self.cleaned_data['cover']

    def clean_logo(self):

        if self.cleaned_data['logo']:

            if not self.cleaned_data['logo'].name:
                if not self.cleaned_data['logo'].content_type in settings.IMAGE_CONTENT_TYPE:
                    raise forms.ValidationError(u'File type is not supported')

            if self.cleaned_data['logo'].size > settings.IMAGE_SIZE:
                raise forms.ValidationError(u'File size not allowed')

            w, h = get_image_dimensions(self.cleaned_data['logo'])

            if w != settings.IMAGE_DIMENSIONS['width_logo']:
                raise forms.ValidationError("The image is %ipx pixel wide. It's supposed to be %spx" % (w, settings.IMAGE_DIMENSIONS['width_logo']))
            if h != settings.IMAGE_DIMENSIONS['height_logo']:
                raise forms.ValidationError("The image is %ipx pixel high. It's supposed to be %spx" % (h, settings.IMAGE_DIMENSIONS['height_logo']))

        return self.cleaned_data['logo']

    class Meta:

        model = models.Journal
        exclude = ('pub_status', 'pub_status_changed_by')
        #Overriding the default field types or widgets
        widgets = {
           'title': forms.TextInput(attrs={'class': 'span9'}),
           'title_iso': forms.TextInput(attrs={'class': 'span9'}),
           'short_title': forms.TextInput(attrs={'class': 'span9'}),
           'previous_title': forms.Select(attrs={'class': 'span9'}),
           'acronym': forms.TextInput(attrs={'class': 'span2'}),
           'scielo_issn': forms.Select(attrs={'class': 'span3'}),
           'subject_descriptors': forms.Textarea(attrs={'class': 'span9'}),
           'init_year': forms.TextInput(attrs={'class': 'datepicker', 'id': 'datepicker0'}),
           'init_vol': forms.TextInput(attrs={'class': 'span2'}),
           'init_num': forms.TextInput(attrs={'class': 'span2'}),
           'final_year': forms.TextInput(attrs={'class': 'datepicker', 'id': 'datepicker1'}),
           'final_vol': forms.TextInput(attrs={'class': 'span2'}),
           'final_num': forms.TextInput(attrs={'class': 'span2'}),
           'url_main_collection': forms.TextInput(attrs={'class': 'span9'}),
           'url_online_submission': forms.TextInput(attrs={'class': 'span9'}),
           'url_journal': forms.TextInput(attrs={'class': 'span9'}),
           'notes': forms.Textarea(attrs={'class': 'span9'}),
           'editorial_standard': forms.Select(attrs={'class': 'span3'}),
           'copyrighter': forms.TextInput(attrs={'class': 'span8'}),
           'index_coverage': forms.Textarea(attrs={'class': 'span9'}),
           'other_previous_title': forms.TextInput(attrs={'class': 'span9'}),
           'editor_address': forms.TextInput(attrs={'class': 'span9'}),
           'publisher_name': forms.TextInput(attrs={'class': 'span9'}),
        }


class CollectionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CollectionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.Collection
        exclude = ('collection', )


class SponsorForm(UserCollectionContext):

    def __init__(self, *args, **kwargs):
        super(SponsorForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.Sponsor
        exclude = ('acronym', 'country', 'state', 'city', 'address_number', 'address_complement',
            'zip_code', 'phone', 'fax', 'cel')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'span6'}),
            'complement': forms.Textarea(attrs={'class': 'span6'}),
            'address': forms.Textarea(attrs={'class': 'span6'}),
            'email': forms.TextInput(attrs={'class': 'span6'}),
        }


class LoginForm(forms.Form):
        username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-xlarge focused span4', 'placeholder': _('Username or email')}))
        password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-xlarge focused span4', 'placeholder': _('Password')}))


class UserForm(ModelForm):
    groups = forms.ModelMultipleChoiceField(Group.objects.all(),
        widget=forms.SelectMultiple(attrs={'title': _('Select one or more groups')}),
        required=False)

    class Meta:
        model = models.User
        exclude = ('is_staff', 'is_superuser', 'last_login', 'date_joined',
                   'user_permissions', 'email', 'password', 'is_active')

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        #user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()
            self.save_m2m()
        return user


class EventJournalForm(forms.Form):
    pub_status = forms.ChoiceField(widget=forms.Select, choices=choices.JOURNAL_PUBLICATION_STATUS)
    pub_status_reason = forms.CharField(widget=forms.Textarea)


class IssueForm(ModelForm):
    section = forms.ModelMultipleChoiceField(models.Section.objects.none(),
         widget=forms.SelectMultiple(attrs={'title': _('Select one or more section')}),
         required=False)

    widgets = {
        'section': forms.Select(attrs={'class': 'span3'}),
    }

    def __init__(self, *args, **kwargs):
        """
        Section field queryset is overridden to display only
        sections related to a given journal.

        ``journal_id`` should not be passed to the superclass
        ``__init__`` method.
        """
        self.journal_id = kwargs.pop('journal_id', None)
        super(IssueForm, self).__init__(*args, **kwargs)
        if self.journal_id is not None:
            self.fields['section'].queryset = models.Section.objects.filter(journal=self.journal_id)

    def save_all(self, journal):
        issue = self.save(commit=False)
        issue.journal = journal
        issue.save()
        self.save_m2m()

        return issue

    def clean(self):
        volume = self.cleaned_data.get('volume')
        number = self.cleaned_data.get('number')
        publication_year = self.cleaned_data.get('publication_year')

        if volume or number:
            issue = models.Issue.objects.filter(number=number, volume=volume,\
                publication_year=publication_year, journal=self.journal_id)

            if issue:
                if self.instance.id != issue[0].id:
                    raise forms.ValidationError({NON_FIELD_ERRORS:\
                        _('Issue with this Year and (Volume or Number) already exists for this Journal.')})
        else:
            raise forms.ValidationError(_('You must complete at least one of two fields volume or number.'))

        return self.cleaned_data

    class Meta:
        model = models.Issue
        exclude = ('collection', 'journal', 'created', 'updated')
        widgets = {
            'publication_date': forms.TextInput(attrs={'class': 'datepicker', 'id': 'datepicker'}),
        }


class SectionTitleForm(ModelForm):

    def __init__(self, *args, **kwargs):
        """
        Section field queryset is overridden to display only
        sections related to a given journal.

        ``journal_id`` should not be passed to the superclass
        ``__init__`` method.
        """
        self.journal = kwargs.pop('journal', None)
        super(SectionTitleForm, self).__init__(*args, **kwargs)
        if self.journal:
            self.fields['language'].queryset = models.Language.objects.filter(journal__pk=self.journal.pk)

    def clean(self):
        if not self.instance.id and 'title' in self.cleaned_data and 'language' in self.cleaned_data:
            title = self.cleaned_data['title']
            language = self.cleaned_data['language']

            if models.Section.objects.filter(titles__title__iexact=title, \
                titles__language=language, journal=self.journal).exists():

                raise forms.ValidationError({NON_FIELD_ERRORS:\
                    _('This section title already exists for this Journal.')})

        return self.cleaned_data

    class Meta:
        model = models.SectionTitle
        fields = ('title', 'language',)


class SectionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(SectionForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.fields['legacy_code'].widget.attrs['readonly'] = True

    def clean_code(self):
        return self.instance.legacy_code

    def save_all(self, journal):
        section = self.save(commit=False)
        section.journal = journal
        section.save()

        return section

    class Meta:
        model = models.Section
        exclude = ('journal', 'code')


class UserCollectionsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        """
        Collection field queryset is overridden to display only
        collections managed by the given user.

        ``user`` should not be passed to the superclass
        ``__init__`` method.
        """
        self._user = kwargs.pop('user', None)
        super(UserCollectionsForm, self).__init__(*args, **kwargs)
        if self._user:
            self.fields['collection'].queryset = models.Collection.objects.get_managed_by_user(self._user)

    class Meta:
        model = models.UserCollections
        exclude = ('is_default', )
        widgets = {
            'collection': forms.Select(attrs={'class': 'span8'}),
        }


class JournalStudyAreaForm(ModelForm):
    class Meta:
        model = models.JournalStudyArea
        widgets = {
            'studyarea': forms.TextInput(attrs={'class': 'span10'}),
        }


class JournalMissionForm(ModelForm):
    class Meta:
        model = models.JournalMission
        widgets = {
            'description': forms.Textarea(attrs={'class': 'span6', 'rows': '3'}),
        }


class JournalTitleForm(ModelForm):
    class Meta:
        model = models.JournalTitle
        widgets = {
            'title': forms.TextInput(attrs={'class': 'span6'}),
        }


class IssueTitleForm(ModelForm):
    class Meta:
        model = models.IssueTitle
        widgets = {
            'title': forms.TextInput(attrs={'class': 'span6'}),
        }


## Formsets ##
class FirstFieldRequiredFormSet(BaseInlineFormSet):
    """
    Formset class that makes the first item required.

    Usage: ABCFormSet = inlineformset_factory(models.Wrappee, models.Wrapped,
        extra=1, formset=FirstFieldRequiredFormSet)
    """
    def __init__(self, *args, **kwargs):
        super(FirstFieldRequiredFormSet, self).__init__(*args, **kwargs)
        self.forms[0].empty_permitted = False
