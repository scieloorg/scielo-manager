#coding: utf-8
import logging
import uuid

import psycopg2
from django.db import connections, DatabaseError
from django.conf import settings
from django.core.cache import cache

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


class CachingBackend(CheckItem):
    """
    Connection with the caching backend
    """
    def __call__(self):
        key = uuid.uuid4().hex

        try:
            ret_code = cache.add(key, '\x01', timeout=1)
            return bool(ret_code)
        finally:
            cache.delete(key)

