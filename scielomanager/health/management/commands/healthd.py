# coding: utf-8
import logging

from django.core.management.base import BaseCommand

import health
from health import checks


logger = logging.getLogger(__name__)


def get_checklist():
    checklist = health.CheckList()
    checklist.add_check(checks.PGConnection())
    checklist.add_check(checks.CeleryConnection())
    checklist.add_check(checks.RabbitConnection())

    return checklist


class HealthEndpoint(object):
    def __init__(self, checklist):
        self.checklist = checklist

    def __latest_report(self):
        self.checklist.update()
        return self.checklist.latest_report

    def overall_status(self):
        """ O estado de saúde de todos os pontos de integração monitorados.
        """
        return self.__latest_report()

    def status(self, integration):
        """ O estado de saúde de um único ponto de integração.
        """
        try:
            return self.overall_status()[integration]
        except KeyError as e:
            logger.exception(e)
            raise ValueError('Invalid integration point "%s"' % integration)

    def elapsed_time(self):
        """ Total de segundos desde a última verificação.
        """
        return self.checklist.since()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        checklist = get_checklist()

        server = health.Server(HealthEndpoint(checklist))
        try:
            logger.info('healthd will start to accept incomming connections now')
            server.run()
        except KeyboardInterrupt:
            logger.info('healthd is shutting down')

