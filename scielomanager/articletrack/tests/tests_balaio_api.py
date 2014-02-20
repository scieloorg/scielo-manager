# -*- coding: utf-8 -*-
import unittest
import mocker
import json
import urllib2
from urllib import addinfourl
import urlparse
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from articletrack.balaio_api import BalaioAPI

class BalaioCheckSettingsTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_validate_correct_settings(self):
        b_client = BalaioAPI()
        self.assertTrue(b_client.validate_settings())

    def test_raise_using_invalid_settings(self):
        self.assertRaises(ImproperlyConfigured, BalaioAPI, using='UNEXISTENT_KEY')

    def test_api_hostname(self):
        balaio_api = BalaioAPI()
        api_hostname = balaio_api.get_hostname()
        api_protocol = settings.API_BALAIO['default']['PROTOCOL']
        api_host = settings.API_BALAIO['default']['HOST']
        api_port = settings.API_BALAIO['default']['PORT']
        api_path = settings.API_BALAIO['default']['PATH']
        api_netloc = ":".join([api_host, api_port])

        hostname_url = urlparse.urlsplit(api_hostname)
        self.assertTrue(hostname_url.scheme == api_protocol)
        self.assertTrue(hostname_url.netloc == api_netloc)
        self.assertTrue(api_path == '/api/v1/')

    def test_api_fullpath(self):
        balaio_api = BalaioAPI()
        api_fullpath_url = balaio_api.get_fullpath()
        api_protocol = settings.API_BALAIO['default']['PROTOCOL']
        api_host = settings.API_BALAIO['default']['HOST']
        api_port = settings.API_BALAIO['default']['PORT']
        api_path = settings.API_BALAIO['default']['PATH']
        api_netloc = ":".join([api_host, api_port])

        api_fullpath_url = urlparse.urlsplit(api_fullpath_url)

        self.assertTrue(api_fullpath_url.scheme == api_protocol)
        self.assertTrue(api_fullpath_url.netloc == api_netloc)
        self.assertTrue(api_fullpath_url.path == api_path)


class BalaioRequestsTests(mocker.MockerTestCase):
    
    def test_is_up(self):
        balaio_api = BalaioAPI()
        # response
        mock_response = self.mocker.mock()
        mock_response.getcode()
        self.mocker.result(200)
        
        # request
        mock_request = self.mocker.replace('urllib2')
        mock_request.urlopen("%sstatus/" % balaio_api.get_hostname(), timeout=mocker.ANY)
        self.mocker.result(mock_response)

        self.mocker.replay()
        
        self.assertTrue(balaio_api.is_up())


    def test_list_files_members_by_attempt(self):
        balaio_api = BalaioAPI()
        attempt_id = 25
        expected_json_response = {
            "xml": [
                "0034-8910-rsp-47-04-0817.xml"
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
        
        # response
        mock_response = self.mocker.mock()
        
        mock_response.getcode()
        self.mocker.result(200)

        mock_response.read(settings.API_BALAIO_DEFAULT_CHUNK_SIZE)
        self.mocker.result(json.dumps(expected_json_response))

        mock_response.read(settings.API_BALAIO_DEFAULT_CHUNK_SIZE)
        self.mocker.result('')
        
        # request
        mock_request = self.mocker.replace('urllib2')
        mock_request.urlopen('%sfiles/%s/' % (balaio_api.get_fullpath(), str(attempt_id)), timeout=mocker.ANY)
        self.mocker.result(mock_response)

        self.mocker.replay()
        
        self.assertEqual(
            balaio_api.list_files_members_by_attempt(attempt_id),
            expected_json_response
        )