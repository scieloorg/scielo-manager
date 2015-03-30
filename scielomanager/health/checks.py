#coding: utf-8
import psycopg2
from django.db import connections, DatabaseError
from django.conf import settings
import logging
import memcache

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


class MemcachedConnection(CheckItem):
    """
    Connection with the Memcached backend
    """

    def __init__(self):
        try:
            self.memcache_installed = 'memcached' in settings.CACHES['default']['BACKEND']
        except KeyError:
            self.memcache_installed = False

    def __call__(self):
        """
        Send a command ``stats`` and read the first line of the response.
        """
        if self.memcache_installed:
            cache_backend_location = settings.CACHES['default']['LOCATION']
            mc = memcache.Client([cache_backend_location], debug=1)
            server = mc.servers[0]
            try:
                server.connect()
                server.send_cmd('stats')
            except AttributeError:
                logger.error("can't connect to memcached")
                return False
            else:
                response = server.readline()
                server.close_socket()
                logger.debug("server response: ", response)
                return (response is not None) and (response != "")
        else:
            logger.error("memcached not configured as a default cache or default location is wrong")
            return None

