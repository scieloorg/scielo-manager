#coding: utf-8
import thriftpy
from thriftpy.rpc import make_server
from django.conf import settings

from thrift import spec


req_counter = 0


class RPCHandler(object):

    def addArticle(self, xml_string):
        global req_counter

        try:
            if req_counter == 0:
                return 'foobar'
            elif req_counter == 1:
                raise spec.DuplicationError('foobar already exists')
            else:
                raise spec.ValueError('foobar has structural errors')
        finally:
            req_counter += 1


def serve():
    server = make_server(spec.JournalManagerServices, RPCHandler(),
                          settings.THRIFT_CONFIG['HOST'],
                          settings.THRIFT_CONFIG['PORT'])

    print("serving...")
    try:
        server.serve()
    except KeyboardInterrupt:
        print("shutting down...")

