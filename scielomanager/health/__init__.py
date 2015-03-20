# coding: utf-8
import datetime
import threading
import logging

import zerorpc
from django.conf import settings


logger = logging.getLogger(__name__)
BIND_ADDR = getattr(settings, 'IPC_HEALTHD_BIND_ADDR', 'tcp://0.0.0.0:11711')


def Server(health_endpoint):
    server = zerorpc.Server(health_endpoint)
    server.bind(BIND_ADDR)
    logger.info('healthd is bound to %s', BIND_ADDR)

    return server


def Client():
    client = zerorpc.Client()
    client.connect(BIND_ADDR)
    logger.info('healthd client is connected to %s', BIND_ADDR)

    return client


class CheckItem(object):
    """
    Represents an item that needs to be checked.
    """
    def __call__(self):
        """
        Performs the check step for a specific app aspect.
        """
        raise NotImplementedError()

    def structured(self):
        return {'description': self.__class__.__doc__.strip(),
                'status': self()}


class CheckList(object):
    """
    Performs a sequence of checks related to the application health.
    """
    def __init__(self, refresh=0.25):
        """
        :param refresh: (optional) refresh rate in minutes.
        """
        self.latest_report = {}

        self._check_list = []
        self._refresh_rate = datetime.timedelta(minutes=refresh)
        self._refreshed_at = None

        self._lock = threading.Lock()

    def add_check(self, check):
        """
        Add a check to the registry.

        :param check: a callable that receives nothing as argument.
        """
        assert isinstance(check, CheckItem)
        self._check_list.append(check)

    def run(self):
        """
        Run all checks sequentially and updates the object state.
        """
        self.latest_report = {check.__class__.__name__: check.structured()
                              for check in self._check_list}
        self._refreshed_at = datetime.datetime.now()

    def update(self):
        """
        Run all checks respecting the refresh rate.
        """
        with self._lock:
            if self._refreshed_at is None or (
                self._refreshed_at + self._refresh_rate <= datetime.datetime.now()):

                self.run()

    def since(self):
        """
        Total seconds since the last refresh.
        """
        try:
            return str(datetime.datetime.now() - self._refreshed_at)
        except TypeError:
            # called before run any check
            return None

