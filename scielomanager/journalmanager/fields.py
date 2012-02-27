# coding: utf-8
import re
from django import forms
from django.utils.translation import ugettext_lazy as _


class ISSNField(forms.CharField): 
    default_error_messages = {
        'invalid': _('Enter a valid ISSN.')
    }

    regex = r'[0-9]{4}-[0-9]{3}[0-9X]{1}$'

    def clean(self, value):

        if value is not u'' and value is not None:
          result = re.match(self.regex, value)

          if result is None:
              raise forms.ValidationError(self.error_messages['invalid'])

        return value 