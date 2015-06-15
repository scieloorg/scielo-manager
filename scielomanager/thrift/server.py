#coding: utf-8
import logging
import json

from django.db import close_connection
from celery.result import AsyncResult

from journalmanager import tasks
from thrift import spec


logger = logging.getLogger(__name__)


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
            logger.exception(exc)
            raise spec.ServerError(message='Something bad happened')

    @resource_cleanup
    def getTaskResult(self, task_id):
        async_result = AsyncResult(task_id)
        can_forget = async_result.ready()

        try:
            try:
                result = async_result.result
                if isinstance(result, Exception):
                    value = result.message
                else:
                    value = result

            except Exception as exc:
                logger.exception(exc)
                raise spec.ServerError()

            status = getattr(spec.ResultStatus, async_result.status)
            return spec.AsyncResult(status=status, value=json.dumps(value))

        finally:
            if can_forget:
                async_result.forget()
                logger.info('Forgot the result of task %s', task_id)

