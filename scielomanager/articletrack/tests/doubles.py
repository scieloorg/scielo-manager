# -*- coding: utf-8 -*-
from os import path
from articletrack.balaio import BalaioAPI


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
