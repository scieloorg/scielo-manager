# coding: utf-8
import logging
import uuid

import psycopg2
from django.db import connections, DatabaseError
from celery import current_app
from kombu import Connection

from . import CheckItem


logger = logging.getLogger(__name__)


class PGConnection(CheckItem):
    """
    Connection with the data backend
    """
    working_status = (
            psycopg2.extensions.STATUS_READY,
            psycopg2.extensions.STATUS_BEGIN,
            psycopg2.extensions.STATUS_IN_TRANSACTION,
            psycopg2.extensions.STATUS_PREPARED,
    )

    def __init__(self):
        self.must_fail = False

        for conn in connections.all():
            try:
                # Executa uma query, mesmo que inválida, apenas para
                # forçar a comunicação com o backend
                conn.cursor().execute('SELECT')
            except DatabaseError:
                # Erro esperado por conta da query inválida
                pass
            except psycopg2.OperationalError as e:
                self.must_fail = True

    def __call__(self):
        """
        Try to list table names just to reach the db.
        """
        if self.must_fail:
            return False

        for conn in connections.all():
            try:
                if conn.connection.status not in self.working_status:
                    return False
            except AttributeError as e:
                return None
        else:
            return True


class CeleryConnection(CheckItem):
    """
    Connection with celery backend.
    """
    def __init__(self):
        self.broker_url = current_app.conf.BROKER_URL

    def __call__(self):
        """
        If backend is "django://" will return None
        Else: return if is connected or not
        """
        if self.broker_url == 'django://':
            return None
        else:
            try:
                ping_response = current_app.control.ping(timeout=1)[0]
                ping_key = ping_response.keys()[0]
                status = ping_response[ping_key]['ok'] == u'pong'
            except Exception as exc:
                logger.exception(exc)
                status = False
            return status


class RabbitConnection(CheckItem):
    """
    Connection with RabbitMQ server.
    """
    def __init__(self):
        self.broker_url = current_app.conf.BROKER_URL

    def __call__(self):
        """
        Broker URL must start with "amqp://" else return None
        Return True if can establish connection or not.
        """
        if self.broker_url.startswith("amqp://"):
            try:
                connection = Connection(self.broker_url, connection_timeout=1)
                try:
                    connection.connect()
                    status = connection.connected
                finally:
                    connection.release()
            except Exception as exc:
                logger.exception(exc)
                status = False
            return status
        else:
            return None
