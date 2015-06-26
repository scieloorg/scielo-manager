# coding: utf-8
from optparse import make_option

from thriftpywrap import make_server, _PROTO_FACTORY, _TRANS_FACTORY
from django.core.management.base import BaseCommand

from thrift import spec
from thrift.server import RPCHandler


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--fd', action='store', type=int, dest='fd'),
        make_option('--host', action='store', type=str, dest='host'),
        make_option('--port', action='store', type=int, dest='port'),
    )

    def handle(self, *args, **kwargs):
        if kwargs.get('fd') and kwargs.get('host'):
            raise ValueError('--fd and --host are mutually exclusive')

        server = make_server(spec.JournalManagerServices,
                             RPCHandler(),
                             fd=kwargs['fd'],
                             host=kwargs['host'],
                             port=kwargs['port'],
                             proto_factory=_PROTO_FACTORY(),
                             trans_factory=_TRANS_FACTORY())

        try:
            server.serve()
        finally:
            server.trans.close()

