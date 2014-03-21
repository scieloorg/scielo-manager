# -*- coding: utf-8 -*-
import unittest
import json
import urlparse

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import mocker

from articletrack.balaio import BalaioAPI, BalaioRPC, SettingsMixin


class BalaioCheckSettingsTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_validate_correct_settings(self):
        b_client = BalaioAPI()
        self.assertTrue(b_client.validate_settings('default'))

    def test_raise_using_invalid_settings(self):
        self.assertRaises(ImproperlyConfigured, BalaioAPI, using='UNEXISTENT_KEY')

    def test_api_hostname(self):
        balaio_api = BalaioAPI()
        api_hostname = balaio_api.get_hostname()
        hostname_url = urlparse.urlsplit(api_hostname)

        api_settings_protocol = settings.API_BALAIO['default']['PROTOCOL']
        api_settings_host = settings.API_BALAIO['default']['HOST']
        api_settings_port = settings.API_BALAIO['default']['PORT']
        api_settings_netloc = ":".join([api_settings_host, api_settings_port])

        self.assertTrue(hostname_url.scheme == api_settings_protocol)
        self.assertTrue(hostname_url.netloc == api_settings_netloc)

    def test_api_basepath(self):
        balaio_api = BalaioAPI()
        api_basepath = balaio_api.get_basepath()

        api_settings_path = settings.API_BALAIO['default']['PATH']
        self.assertTrue(api_basepath == api_settings_path)

    def test_api_fullpath(self):
        balaio_api = BalaioAPI()
        api_fullpath_url = balaio_api.get_fullpath()
        api_fullpath_url = urlparse.urlsplit(api_fullpath_url)

        api_settings_protocol = settings.API_BALAIO['default']['PROTOCOL']
        api_settings_host = settings.API_BALAIO['default']['HOST']
        api_settings_port = settings.API_BALAIO['default']['PORT']
        api_settings_netloc = ":".join([api_settings_host, api_settings_port])
        api_settings_path = settings.API_BALAIO['default']['PATH']


        self.assertTrue(api_fullpath_url.scheme == api_settings_protocol)
        self.assertTrue(api_fullpath_url.netloc == api_settings_netloc)
        self.assertTrue(api_fullpath_url.path == api_settings_path)


class BalaioRPCCheckSettingsTests(unittest.TestCase):

    def test_validate_correct_settings(self):
        b_client = BalaioRPC()
        self.assertTrue(b_client.validate_settings('default'))

    def test_raise_using_invalid_settings(self):
        self.assertRaises(ImproperlyConfigured, BalaioAPI, using='UNEXISTENT_KEY')

    def test_api_fullpath(self):
        balaio_api = BalaioRPC()
        api_fullpath_url = balaio_api._fullpath()
        api_fullpath_url = urlparse.urlsplit(api_fullpath_url)

        api_settings_protocol = settings.API_BALAIO['default']['PROTOCOL']
        api_settings_host = settings.API_BALAIO['default']['HOST']
        api_settings_port = settings.API_BALAIO['default']['PORT']
        api_settings_netloc = ":".join([api_settings_host, api_settings_port])
        api_settings_path = settings.API_BALAIO['default']['PATH']

        self.assertTrue(api_fullpath_url.scheme == api_settings_protocol)
        self.assertTrue(api_fullpath_url.netloc == api_settings_netloc)
        self.assertTrue(api_fullpath_url.path == '/' + api_settings_path.strip('/') + '/_rpc/')


class SettingsMixinTests(unittest.TestCase):

    def test_validate_correct_settings(self):
        self.assertTrue(SettingsMixin().validate_settings('default'))

    def test_validate_incorrect_settings(self):
        self.assertRaises(ImproperlyConfigured,
            lambda: SettingsMixin().validate_settings('nonexisting'))


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

    def test_list_files_unexistent_attempt_raise_error(self):
        balaio_api = BalaioAPI()
        invalid_attempt_id = 0
        expected_json_response = {'message': u'Error HTTP Not 200', 'error': True}

        # response
        mock_response = self.mocker.mock()

        mock_response.getcode()
        self.mocker.result(404)

        # request
        mock_request = self.mocker.replace('urllib2')
        mock_request.urlopen('%sfiles/%s/' % (balaio_api.get_fullpath(), str(invalid_attempt_id)), timeout=mocker.ANY)
        self.mocker.result(mock_response)

        self.mocker.replay()

        self.assertEqual(
            balaio_api.list_files_members_by_attempt(invalid_attempt_id),
            expected_json_response
        )


class BalaioAPIRequestsTests(mocker.MockerTestCase):
    def test_valid_remote_call_without_args(self):
        client = BalaioRPC(using='default')

        mock_serverproxy = self.mocker.mock()
        mock_serverproxy.foo()
        self.mocker.result('bar')

        mock_client = self.mocker.patch(client)
        mock_client.server_path
        self.mocker.result('http://domain.com:8086/api/v1/_rpc/')

        mock_client._xmlrpclib.ServerProxy('http://domain.com:8086/api/v1/_rpc/foo/')
        self.mocker.result(mock_serverproxy)

        self.mocker.replay()

        self.assertEqual(client.call('foo'), 'bar')

    def test_valid_remote_call_with_args(self):
        client = BalaioRPC(using='default')

        mock_serverproxy = self.mocker.mock()
        mock_serverproxy.foo('bla')
        self.mocker.result('bar')

        mock_client = self.mocker.patch(client)
        mock_client.server_path
        self.mocker.result('http://domain.com:8086/api/v1/_rpc/')

        mock_client._xmlrpclib.ServerProxy('http://domain.com:8086/api/v1/_rpc/foo/')
        self.mocker.result(mock_serverproxy)

        self.mocker.replay()

        self.assertEqual(client.call('foo', ['bla']), 'bar')

    def test_is_up_when_server_returns_True(self):
        client = BalaioRPC(using='default')

        mock_client = self.mocker.patch(client)
        mock_client.call('status')
        self.mocker.result(True)

        self.mocker.replay()

        self.assertTrue(client.is_up())

    def test_is_up_when_server_returns_False(self):
        client = BalaioRPC(using='default')

        mock_client = self.mocker.patch(client)
        mock_client.call('status')
        self.mocker.result(False)

        self.mocker.replay()

        self.assertFalse(client.is_up())

    def test_is_up_when_connection_blows(self):
        import xmlrpclib
        client = BalaioRPC(using='default')

        mock_client = self.mocker.patch(client)
        mock_client.call('status')
        self.mocker.throw(xmlrpclib.ProtocolError('url', 'headers', '1', 'errmsg'))

        self.mocker.replay()

        self.assertFalse(client.is_up())

    def test_is_up_when_rpc_is_faulty(self):
        import xmlrpclib
        client = BalaioRPC(using='default')

        mock_client = self.mocker.patch(client)
        mock_client.call('status')
        self.mocker.throw(xmlrpclib.Fault('1', 'fault_str'))

        self.mocker.replay()

        self.assertFalse(client.is_up())

