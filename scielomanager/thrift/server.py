#coding: utf-8
import logging
import functools

from django.db import IntegrityError, transaction

from thrift import spec
from journalmanager import services


logger = logging.getLogger(__name__)


def commit_on_success(method):
    """Envolve um método em um contexto transacional.
    """
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        with transaction.commit_on_success():
            return method(*args, **kwargs)

    return wrapper


class RPCHandler(object):
    """Implementação do serviço `JournalManagerServices`.
    """
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

