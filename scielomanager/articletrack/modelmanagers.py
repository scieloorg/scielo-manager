#coding: utf-8
from journalmanager.modelmanagers import UserObjectQuerySet, UserObjectManager, user_request_context


class CheckinQuerySet(UserObjectQuerySet):

    def all(self, get_all_collections=user_request_context.get_current_user_collections):
        return self.filter(
            journals__collection__in=get_all_collections()).distinct()

    def active(self, get_active_collection=user_request_context.get_current_user_active_collection):
        return self.filter(
            journals__collection=get_active_collection()).distinct()


class CheckinManager(UserObjectManager):

    def get_query_set(self):
        return CheckinQuerySet(self.model, using=self._db)
