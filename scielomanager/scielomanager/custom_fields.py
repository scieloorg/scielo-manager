# -*- coding: utf-8 -*-
import io

from django.db import models
from django.db.models.fields import TextField
from django.forms import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _
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
    def __init__(self, data):
        if isinstance(data, str):
            xml_bytes = data.encode("utf-8")
        elif isinstance(data, bytes):
            xml_bytes = data
        else:
            raise TypeError("xml must be str or bytes")

        self.root_etree = etree.parse(io.BytesIO(xml_bytes))

    def __repr__(self):
        return '<%s xml_etree=%s>' % (self.__class__.__name__,
                repr(self.root_etree))

    def __str__(self):
        xml_bytes = etree.tostring(
            self.root_etree,
            encoding="utf-8",
            xml_declaration=True,
        )
        return xml_bytes.decode("utf-8")

    def __getattr__(self, name):
        return getattr(self.root_etree, name)


class XMLSPSField(TextField):
    description = 'A xml sps field'

    def to_python(self, value):
        if isinstance(value, XMLSPS):
            return value
        elif bool(value) is False:
            return None

        return XMLSPS(value)

    def get_prep_value(self, value):
        return str(value)
