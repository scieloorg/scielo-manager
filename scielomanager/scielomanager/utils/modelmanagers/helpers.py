# coding:utf-8
"""
Use this module to write functional tests for the pages and
screen components, only!
"""
from django.conf import settings


class Finders(object):
    pass

finders = Finders()


def _makeUserRequestContext(user):
    """
    Constructs a class to be used by settings.USERREQUESTCONTEXT_FINDER
    bound to a user, for testing purposes.
    """
    class UserRequestContextTestFinder(object):

        def get_current_user_collections(self):
            return user.user_collection.all()

        def get_current_user_active_collection(self):
            colls = self.get_current_user_collections()
            if colls:
                return colls.get(usercollections__is_default=True)

    return UserRequestContextTestFinder


def _patch_userrequestcontextfinder_settings_setup(func):
    """
    Patch the setting USERREQUESTCONTEXT_FINDER to target a
    testing-friendly version.
    """
    def wrapper(self, **kwargs):
        func(self, **kwargs)

        # override the setting responsible for retrieving the active user context
        cls = self.__class__
        setattr(finders, cls.__name__, _makeUserRequestContext(self.user))
        self.default_USERREQUESTCONTEXT_FINDER = settings.USERREQUESTCONTEXT_FINDER
        settings.USERREQUESTCONTEXT_FINDER = 'scielomanager.scielomanager.journalmanager.test.helpers.finders.%s' % cls.__name__

    return wrapper


def _patch_userrequestcontextfinder_settings_teardown(func):
    """
    Restore the settings defaults.
    """
    def wrapper(self, **kwargs):
        func(self, **kwargs)

        attr_name = settings.USERREQUESTCONTEXT_FINDER.rsplit('.', 1)[-1]
        delattr(finders, attr_name)

        settings.USERREQUESTCONTEXT_FINDER = self.default_USERREQUESTCONTEXT_FINDER

    return wrapper


def _makeUserProfile(user):
    """
    Create a UserProfile for the ``user``
    """
    from journalmanager.models import UserProfile

    profile, created = UserProfile.objects.get_or_create(user=user)
