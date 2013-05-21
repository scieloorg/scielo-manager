# coding: utf-8
import threading

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import memoize
from django.utils.importlib import import_module
from django.utils.datastructures import SortedDict


th_localstore = threading.local()
_finders = SortedDict()

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


class UserRequestContextFinder(object):

    def get_current_user_collections(self):
        user = get_current_user()
        if user:
            return user.user_collection.all()


    def get_current_user_active_collection(self):
        colls = self.get_current_user_collections()
        if colls:
            return colls.get(usercollections__is_default=True)


def get_finder():
    finder_path = settings.USERREQUESTCONTEXT_FINDER
    return new_finder(finder_path)


def _get_finder(import_path):
    """
    Imports the staticfiles finder class described by import_path, where
    import_path is the full Python path to the class.
    """
    module, attr = import_path.rsplit('.', 1)
    try:
        mod = import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured('Error importing module %s: "%s"' %
                                   (module, e))
    try:
        Finder = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a "%s" '
                                   'class.' % (module, attr))
    return Finder()
new_finder = memoize(_get_finder, _finders, 1)

