# coding: utf-8

from django import forms
from django.utils.translation import ugettext as _


STYLECHECKER_TYPE_CHOICES = (
	('url', _('URL')),
	('file', _('File')),
)


class StyleCheckerForm(forms.Form):
	type = forms.ChoiceField(label=_("Type"), choices=STYLECHECKER_TYPE_CHOICES, ) # widget=forms.RadioSelect
	url = forms.URLField(label=_("URL"), required=False)
	file = forms.FileField(label=_("File"), required=False)

	def clean(self):
		type = self.cleaned_data['type']
		url = self.cleaned_data.get('url', None)
		file = self.cleaned_data.get('file', None)

		if type == 'url' and not url:
			raise forms.ValidationError('if type is "URL", then "URL" field is required')
		if type == 'file' and not file:
			raise forms.ValidationError('if type is "URL", then "File" field is required')

		return self.cleaned_data