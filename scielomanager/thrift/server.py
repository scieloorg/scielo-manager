#coding: utf-8
import logging

from thriftpy.protocol import TCyBinaryProtocolFactory
from thriftpy.transport import TCyBufferedTransportFactory
from thriftpy.rpc import make_server
from django.conf import settings
from django.db import IntegrityError, transaction

from thrift import spec
from journalmanager import services


logger = logging.getLogger(__name__)


def commit_on_success(method):
    def wrapper(*args, **kwargs):
        with transaction.commit_on_success():
            return method(*args, **kwargs)

    return wrapper


class RPCHandler(object):

    @commit_on_success
    def addArticle(self, xml_string, raw):
        try:
            return services.article.add_from_string(xml_string, raw)

        except IntegrityError as exc:
            logger.info(exc)
            raise spec.DuplicationError(message=u'Article already registered')

        except ValueError as exc:
            logger.info(exc)
            raise spec.ValueError(message=exc.message)

        except Exception as exc:
            logger.error(exc)
            raise


def serve():
    protocol = TCyBinaryProtocolFactory()
    transport = TCyBufferedTransportFactory()
    server = make_server(spec.JournalManagerServices, RPCHandler(),
                          settings.THRIFT_CONFIG['HOST'],
                          settings.THRIFT_CONFIG['PORT'],
                          proto_factory=protocol,
                          trans_factory=transport)

    logger.info('Starting Thrift RPC Server at %s:%s. Using protocol %s and transport %s.' % (
        settings.THRIFT_CONFIG['HOST'], settings.THRIFT_CONFIG['PORT'],
        protocol, transport,))

    print("Serving...")

    try:
        server.serve()
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        logger.info('Shutting down Thrift RPC Server')

