# coding: utf-8
import threading

#
# Hey, make sure you are not messing with
# `_request` attribute of the threadlocal
# scope!
#
th_localstore = threading.local()


class ThreadLocalMiddleware(object):
    """
    Makes the request object visible system-wide in a thread local
    basis.
    """
    def process_request(self, request):
        th_localstore._request = request

    def process_response(self, request, response):
        th_localstore._request = None
        return response

    def process_exception(self, request, exception):
        th_localstore._request = None


def get_current_request():
    """
    Get a reference to the current request object.
    """
    return getattr(th_localstore, '_request', None)


def get_current_user():
    """
    Get a reference to the current user. This is a shortcut
    to ``get_current_request().user``.
    """
    req = get_current_request()

    if req:
        return getattr(req, 'user', None)
