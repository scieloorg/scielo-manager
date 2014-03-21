# coding: utf-8
import json
import socket
import urllib2
import xmlrpclib

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

class BalaioAPI(object):


    def __init__(self, using='default'):
        self.using = using
        self.validate_settings()
        self.conf =  settings.API_BALAIO[self.using]


    def validate_settings(self):
        if not self.using in settings.API_BALAIO.keys():
            raise ImproperlyConfigured("settings.API_BALAIO don't have using == %s" % self.using)

        for k in ['PROTOCOL', 'HOST', 'PORT', 'PATH']:
            if k not in settings.API_BALAIO[self.using].keys():
                raise ImproperlyConfigured('settings.API_BALAIO (using == %s) dont have defined %s' % (self.using, k))
            else:
                if not settings.API_BALAIO[self.using][k]:
                    raise ImproperlyConfigured('settings.API_BALAIO[%s][%s] must have value' % (self.using, k))
                v = settings.API_BALAIO[self.using][k]
                if k == 'PROTOCOL' and v not in ('http', 'https'):
                    raise ImproperlyConfigured('settings.API_BALAIO[%s][%s] must be: http or https' % (self.using, k))
                if k == 'HOST' and v == '':
                    raise ImproperlyConfigured('settings.API_BALAIO[%s][%s] must have a valid host' % (self.using, k))
                if k == 'PORT' and not v.isdigit():
                    raise ImproperlyConfigured('settings.API_BALAIO[%s][%s] must have a valid port' % (self.using, k))
                if k == 'PATH' and (v == '' or v[0] != '/'):
                    raise ImproperlyConfigured('settings.API_BALAIO[%s][%s] must have a non-empty path and must start with /' % (self.using, k))
        return True


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


class BalaioRPC(object):

    def __init__(self, using='default'):
        self.conf =  settings.API_BALAIO[using]

    def connection_status(self):
        """
        Verify the xmlrpc connection
        """
        s = xmlrpclib.ServerProxy(self.get_fullpath() + '_rpc/status/')

        try:
            s.status()
            return True
        except socket.error:
            # socket error which mean that services is unavailable
            return False

    def make_connection(self, uri):
        return xmlrpclib.ServerProxy(uri)

    def get_hostname(self):
        return '%s://%s:%s/' % (self.conf['PROTOCOL'], self.conf['HOST'], self.conf['PORT'])

    def get_basepath(self):
        return self.conf['PATH']

    def get_fullpath(self):
        return '%s%s' % (self.get_hostname(), self.get_basepath()[1:])

    def send_request(self, path_info, method, *params):
        """
        Method responsable to send request to XML-RPC ServerProxy
        ::param path_info: specifies a path to be interpreted in RPC server
        ::param method: name of remote RCP method
        ::param *params: params tho the RPC method
        """
        uri = self.get_fullpath() + path_info

        conn = self.make_connection(uri)

        return getattr(conn, method)(*params)
