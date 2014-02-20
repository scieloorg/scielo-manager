# -*- coding: utf-8 -*-
import urllib2
import json
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
        return True

    def get_hostname(self):
        return '%s://%s:%s/' % (self.conf['PROTOCOL'], self.conf['HOST'], self.conf['PORT'])


    def get_fullpath(self):
        return '%s://%s:%s%s' % (self.conf['PROTOCOL'], self.conf['HOST'], self.conf['PORT'], self.conf['PATH'])


    def is_up(self):
        url = self.get_hostname() + 'status/'
        try:
            response = urllib2.urlopen(url, timeout=settings.API_BALAIO_DEFAULT_TIMEOUT)
            return response.getcode() == 200
        except Exception:
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
