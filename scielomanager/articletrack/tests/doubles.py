# -*- coding: utf-8 -*-
from os import path
from articletrack.balaio import BalaioAPI, BalaioRPC
from django.conf import settings
from urllib2 import urlopen
from packtools import stylechecker


def make_expected_generator(file_uri):
    # function to return a generator with the expected result
    response = urlopen(file_uri, timeout=settings.API_BALAIO_DEFAULT_TIMEOUT)
    while True:
        response_chunk = response.read(settings.API_BALAIO_DEFAULT_CHUNK_SIZE)
        if response_chunk:
            yield response_chunk
        else:
            raise StopIteration()


class BalaioAPIDouble(BalaioAPI):

    def is_up(self):
        return True

    def list_files_members_by_attempt(self, attempt_id):
        return {
            "xml": [
                "1415-4757-gmb-37-0210.xml"
            ],
            "pdf": [
                "0034-8910-rsp-47-04-0817.pdf",
                "en_0034-8910-rsp-47-04-0817.pdf"
            ],
            "tif": [
                "0034-8910-rsp-47-04-0817-gf01.tif"
            ],
            'error': False
        }

    def get_xml_uri(self, attempt_id, target_name):
        tests_xmls_dirs = path.abspath(path.join(path.dirname(__file__), 'xml_tests_files'))
        return "file://%s" % path.join(tests_xmls_dirs, "valid.xml")


class BalaioAPIDoubleDisabled(BalaioAPI):
    def is_up(self):
        return False

    def list_files_members_by_attempt(self, attempt_id):
        raise ValueError


class BalaioRPCDouble(BalaioRPC):

    def is_up(self):
        return True

    def call(self, method, args=()):
        return None


# packtools.stylechecker double


class StylecheckerDouble(stylechecker.XML):
    def __init__(self, file):
        pass

    def validate(self):
        return (True, None)

    def validate_style(self):
        return (True, None)

    def annotate_errors(self):
        return None


class StylecheckerAnnotationsDouble(StylecheckerDouble):
    def __str__(self):
        return "some annotations in xml string"

    def validate(self):
        return (True, None)

    def validate_style(self):
        class Error(object):
            line = None
            column = None
            message = u"Element 'funding-group': This element is not filled-in correctly."
            level_name = u'ERROR'
        return (False, [Error(), ])
