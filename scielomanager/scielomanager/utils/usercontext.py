from .middlewares import threadlocal

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import memoize
from django.utils.importlib import import_module
from django.utils.datastructures import SortedDict


_finders = SortedDict()


class UserRequestContextFinder(object):
    """
    The user request context is comprised of the
    subset of records the user is authorized to access.

    Instances of this class should provide data necessary
    for the context to be built.
    """
    def get_current_user_collections(self):
        """
        Returns a queryset of all collections the current user is part.
        """
        user = threadlocal.get_current_user()
        if user:
            return user.user_collection.all()


    def get_current_user_active_collection(self):
        """
        Returns the active collection of the current user.
        """
        colls = self.get_current_user_collections()
        if colls:
            return colls.get(usercollections__is_default=True)


def get_finder():
    """
    Handles the dependency injection to get an
    UserRequestContextFinder instance.

    The DI is specified at `settings.USERREQUESTCONTEXT_FINDER`
    directive.
    """
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

