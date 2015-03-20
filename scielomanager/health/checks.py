#coding: utf-8
import psycopg2
from django.db import connections, DatabaseError

from . import CheckItem


class PGConnection(CheckItem):
    u"""
    Conexão com o banco de dados Postgres.
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

