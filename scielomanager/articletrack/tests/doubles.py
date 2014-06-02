# -*- coding: utf-8 -*-
from os import path


DEFAULT_XML = "valid.xml"
TESTS_XMLS_DIRS = path.join(path.dirname(__file__), 'xml_tests_files')
TEXT_XML_ABS_PATH = path.join(TESTS_XMLS_DIRS, DEFAULT_XML)


class BalaioAPIDouble(object):

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
        return "file://%s" % TEXT_XML_ABS_PATH
