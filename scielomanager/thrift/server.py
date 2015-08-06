#coding: utf-8
import logging
import json

from django.db import close_connection
from celery.result import AsyncResult

from journalmanager import tasks
from thrift import spec
from scielomanager import connectors


LOGGER = logging.getLogger(__name__)
ARTICLE_ES_CLIENT = connectors.ArticleElasticsearch()


ERRNO_NS = {
        'IntegrityError': 1,
        'ValueError': 2,
}


def resource_cleanup(tocall):
    """ O Celery vaza recursos de conexão com o BD quando utiliza o ORM como
    backend de tarefas. Além disso, o próprio ORM do Django utiliza o signal
    `request_finished` para disparar a rotina `django.db.close_connection`, e
    como a interface RPC é dissociada dos ciclos convencionais de
    request/response, devemos executar essa limpeza manualmente.
    """
    def wrapper(*args, **kwargs):
        try:
            return tocall(*args, **kwargs)
        finally:
            close_connection()

    return wrapper


class RPCHandler(object):
    """Implementação do serviço `JournalManagerServices`.
    """
    @resource_cleanup
    def addArticle(self, xml_string):
        try:
            delayed_task = tasks.create_article_from_string.delay(xml_string)
            return delayed_task.id

        except Exception as exc:
            LOGGER.exception(exc)
            raise spec.ServerError()

    @resource_cleanup
    def getTaskResult(self, task_id):
        async_result = AsyncResult(task_id)
        can_forget = async_result.ready()

        try:
            try:
                result = async_result.result
                if isinstance(result, Exception):
                    result_cls_name = result.__class__.__name__
                    try:
                        errno = ERRNO_NS[result_cls_name]
                    except KeyError:
                        LOGGER.error('Undefined errno: %s', result_cls_name)
                        raise spec.ServerError()

                    value = [errno, result.message]
                else:
                    value = result

            except Exception as exc:
                LOGGER.exception(exc)
                raise spec.ServerError()

            status = getattr(spec.ResultStatus, async_result.status)
            return spec.AsyncResult(status=status, value=json.dumps(value))

        finally:
            if can_forget:
                async_result.forget()
                LOGGER.info('Forgot the result of task %s', task_id)

    def scanArticles(self, es_dsl_query):
        try:
            return ARTICLE_ES_CLIENT.scan(es_dsl_query)

        except connectors.exceptions.BadRequestError:
            raise spec.BadRequestError()

        except connectors.exceptions.TimeoutError:
            raise spec.TimeoutError()

        except Exception as exc:
            LOGGER.exception(exc)
            raise spec.ServerError()

    def getScanArticlesBatch(self, batch_id):
        try:
            next_id, batch = ARTICLE_ES_CLIENT.scroll(batch_id)

        except connectors.exceptions.BadRequestError:
            raise spec.BadRequestError()

        except connectors.exceptions.TimeoutError:
            raise spec.TimeoutError()

        except Exception as exc:
            LOGGER.exception(exc)
            raise spec.ServerError()

        articles = [spec.Article(**data) for data in batch]

        results = spec.ScanArticlesResults()
        if articles:
            results.articles = articles
        if next_id:
            results.next_batch_id = next_id

        return results

    def getInterfaceVersion(self):
        return spec.VERSION

