#coding: utf-8
import logging

from celery.result import AsyncResult

from thrift import spec, tasks


logger = logging.getLogger(__name__)


class RPCHandler(object):
    """Implementação do serviço `JournalManagerServices`.
    """
    def addArticle(self, xml_string, raw):
        try:
            delayed_task = tasks.add_article.delay(xml_string, raw)
            return delayed_task.id

        except Exception as exc:
            logger.exception(exc)
            raise spec.ServerError(message='Something bad happened')

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
            return spec.AsyncResult(status=status, value=value)

        finally:
            if can_forget:
                async_result.forget()
                logger.info('Forgot the result of task %s', task_id)

