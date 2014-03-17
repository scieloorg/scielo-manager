# coding: utf-8
import socket
import xmlrpclib
from django.conf import settings

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
            _return = True
        except socket.error:
            # socket error which mean that services is unavailable
            _return = False

        return _return

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
