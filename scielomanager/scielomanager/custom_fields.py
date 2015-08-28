# -*- coding: utf-8 -*-
import io

from django.db import models
from django.db.models.fields import TextField
from django.forms import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from lxml import etree


class ContentTypeRestrictedFileField(models.FileField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types.
            Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file size allowed for upload.
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 5242880
            100MB 104857600
            250MB - 214958080
            500MB - 429916160

    http://stackoverflow.com/a/9016664/1503
    """

    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types", None)
        self.max_upload_size = kwargs.pop("max_upload_size", None)

        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)
        file = data.file
        try:
            content_type = file.content_type
            if content_type in self.content_types:
                if file._size > self.max_upload_size:
                    raise forms.ValidationError(
                        _('Please keep file size under {maxsize}. Current file size {filesize}'.format(
                            maxsize=filesizeformat(self.max_upload_size),
                            filesize=filesizeformat(file._size)
                        ))
                    )
            else:
                raise forms.ValidationError(_('File type not supported.'))
        except AttributeError as e:
            pass

        return data


class XMLSPS(object):
    def __init__(self, xml_root_string):
        if isinstance(xml_root_string, str):
            xml_string = xml_root_string
        elif isinstance(xml_root_string, unicode):
            xml_string = xml_root_string.encode('utf-8')
        else:
            raise TypeError('xml must be str or unicode')

        self.root_etree = etree.parse(io.BytesIO(xml_string))

    def __repr__(self):
        return etree.tostring(self.root_etree, encoding='utf-8', xml_declaration=True)

    def __getattr__(self, name):
        return getattr(self.root_etree, name)


class XMLSPSField(TextField):
    description = 'A xml sps field'

    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if not value:
            return None
        elif isinstance(value, XMLSPS):
            return value
        else:
            return XMLSPS(value)

    def get_prep_value(self, value):
        return str(value)


from south.modelsinspector import add_introspection_rules
add_introspection_rules([],[
        "^scielomanager\.custom_fields\.ContentTypeRestrictedFileField",
        "^scielomanager\.custom_fields\.XMLSPSField",
    ])
