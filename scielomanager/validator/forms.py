# coding: utf-8

from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _


class XMLUploadForm(forms.Form):
    file = forms.FileField(label=_("File"))

    def clean_file(self):
        _file = self.cleaned_data.get('file', None)
        if _file:
            if _file.content_type not in ['text/xml', 'application/xml', ]:
                raise forms.ValidationError(_(u"This type of file is not allowed! Please select another file."))

            if _file.size > settings.VALIDATOR_MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_(u"The file's size is too large! Please select a smaller file."))

        return _file
