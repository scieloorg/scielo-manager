# coding: utf-8
import json
import socket
import urllib2
import xmlrpclib

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class SettingsMixin(object):
    def validate_settings(self, using):
        if using not in settings.API_BALAIO.keys():
            raise ImproperlyConfigured("settings.API_BALAIO don't have using == %s" % using)

        for k in ['PROTOCOL', 'HOST', 'PORT', 'PATH']:
            if k not in settings.API_BALAIO[using].keys():
                raise ImproperlyConfigured('settings.API_BALAIO (using == %s) dont have defined %s' % (using, k))
            else:
                if not settings.API_BALAIO[using][k]:
                    raise ImproperlyConfigured('settings.API_BALAIO[%s][%s] must have value' % (using, k))
                v = settings.API_BALAIO[using][k]
                if k == 'PROTOCOL' and v not in ('http', 'https'):
                    raise ImproperlyConfigured('settings.API_BALAIO[%s][%s] must be: http or https' % (using, k))
                if k == 'HOST' and v == '':
                    raise ImproperlyConfigured('settings.API_BALAIO[%s][%s] must have a valid host' % (using, k))
                if k == 'PORT' and not v.isdigit():
                    raise ImproperlyConfigured('settings.API_BALAIO[%s][%s] must have a valid port' % (using, k))
                if k == 'PATH' and (v == '' or v[0] != '/'):
                    raise ImproperlyConfigured('settings.API_BALAIO[%s][%s] must have a non-empty path and must start with /' % (using, k))
        return True


class BalaioAPI(SettingsMixin):

    def __init__(self, using='default'):
        self.using = using
        self.validate_settings(self.using)
        self.conf = settings.API_BALAIO[self.using]

    def get_hostname(self):
        return '%s://%s:%s/' % (self.conf['PROTOCOL'], self.conf['HOST'], self.conf['PORT'])

    def get_basepath(self):
        return self.conf['PATH']

    def get_fullpath(self):
        return '%s%s' % (self.get_hostname(), self.get_basepath()[1:])

    def is_up(self):
        url = self.get_hostname() + 'status/'
        try:
            response = urllib2.urlopen(url, timeout=settings.API_BALAIO_DEFAULT_TIMEOUT)
            return response.getcode() == 200
        except urllib2.URLError:
            return False

    def _response_is_json(response):
        response_headers = response.info()
        for header in response_headers:
            if header.startswith('Content-Type:') and 'json' in header:
                return True
        return False

    def _open(self, url):
        try:
            response = urllib2.urlopen(url, timeout=settings.API_BALAIO_DEFAULT_TIMEOUT)
        except urllib2.URLError as e:
            raise ValueError(e)

        if response.getcode() != 200:
            raise ValueError('Error HTTP Not 200')

        while True:
            response_chunk = response.read(settings.API_BALAIO_DEFAULT_CHUNK_SIZE)
            if response_chunk:
                yield response_chunk
            else:
                raise StopIteration()

    def _process_response_as_json(self, iterable):
        try:
            response_data = ''.join(iterable)
        except ValueError as e:
            return {'error': True, 'message': unicode(e)}
        else:
            json_response = json.loads(response_data)
            json_response['error'] = False
        return json_response

    def list_files_members_by_attempt(self, attempt_id):
        url = self.get_fullpath() + 'files/%s/' % str(attempt_id)
        response = self._open(url)
        return self._process_response_as_json(response)

    def get_file_member_by_attempt(self, attempt_id, target_name, file_member):
        url = self.get_fullpath() + 'files/%s/%s.zip/?file=%s' % (attempt_id, target_name, file_member)
        return self._open(url)

    def get_files_members_by_attempt(self, attempt_id, target_name, files_members):
        files_members = '&file='.join(files_members)
        return self.get_file_member_by_attempt(attempt_id, target_name, files_members)

    def get_full_package(self, attempt_id, target_name):
        url = self.get_fullpath() + 'files/%s/%s.zip/?full=true' % (attempt_id, target_name)
        return self._open(url)

    def get_xml_uri(self, attempt_id, target_name):
        # return self.get_fullpath() + '%s/%s/' % (attempt_id, target_name)
        # FAKE RESPONSE :: TO BE REMOVED ::
        from os import path
        target_name = 'valid.xml'
        tests_xmls_dirs = path.join(path.dirname(__file__), 'tests/xml_tests_files')
        return "file://%s" % path.join(tests_xmls_dirs, target_name)
        # END FAKE RESPONSE::::


class BalaioRPC(SettingsMixin):
    _xmlrpclib = xmlrpclib

    def __init__(self, using='default'):
        self.validate_settings(using)
        self.conf = settings.API_BALAIO[using]
        self.server_path = self._fullpath()

    def is_up(self):
        """
        Check if the RPC server is available.
        """
        try:
            return self.call('status')
        except xmlrpclib.Error:
            return False

    def get_server(self, uri):
        return self._xmlrpclib.ServerProxy(uri)

    def _fullpath(self):
        return '%s://%s:%s/%s/_rpc/' % (
            self.conf['PROTOCOL'], self.conf['HOST'].strip('/'),
            self.conf['PORT'], self.conf['PATH'].strip('/'))

    def call(self, method, args=()):
        """
        Call the remote procedure.

        ::param method: name of remote procedure
        ::param args: (optional) collection of arguments
        """
        uri = '%s/%s/' % (self.server_path.strip('/'), method)
        rpc_server = self.get_server(uri)

        return getattr(rpc_server, method)(*args)

