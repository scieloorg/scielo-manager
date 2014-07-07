# coding: utf-8
from scielomanager.utils import usercontext
from scielomanager.utils.modelmanagers import UserObjectQuerySet, UserObjectManager

user_request_context = usercontext.get_finder()


# CHECKIN

class CheckinQuerySet(UserObjectQuerySet):

    def all(self, get_all_collections=user_request_context.get_current_user_collections):
        return self.filter(
            article__journals__collections__in=get_all_collections()).distinct()

    def active(self, get_active_collection=user_request_context.get_current_user_active_collection):
        return self.filter(
            article__journals__collections=get_active_collection()
            ).exclude(status='expired').distinct()

    def accepted(self):
        return self.filter(status='accepted')

    def pending(self):
        return self.filter(status='pending')

    def rejected(self):
        return self.filter(status='rejected')

    def review(self):
        return self.filter(status='review')

    def expired(self):
        return self.filter(status='expired')


class CheckinManager(UserObjectManager):

    def get_query_set(self):
        return CheckinQuerySet(self.model, using=self._db)


# ARTICLE

class ArticleQuerySet(UserObjectQuerySet):
    def all(self, get_all_collections=user_request_context.get_current_user_collections):
        return self.filter(
            journals__collections__in=get_all_collections()).distinct()

    def active(self, get_active_collection=user_request_context.get_current_user_active_collection):
        return self.filter(
            journals__collections=get_active_collection()).distinct()


class ArticleManager(UserObjectManager):
    def get_query_set(self):
        return ArticleQuerySet(self.model, using=self._db)

# TICKET

class TicketQuerySet(UserObjectQuerySet):
    def all(self, get_all_collections=user_request_context.get_current_user_collections):
        return self.filter(
            article__journals__collections__in=get_all_collections()).distinct()

    def active(self, get_active_collection=user_request_context.get_current_user_active_collection):
        return self.filter(
            article__journals__collections=get_active_collection()).distinct()


class TicketManager(UserObjectManager):
    def get_query_set(self):
        return TicketQuerySet(self.model, using=self._db)


# COMMENT

class CommentQuerySet(UserObjectQuerySet):
    def all(self, get_all_collections=user_request_context.get_current_user_collections):
        return self.filter(
            ticket__article__journals__collections__in=get_all_collections()).distinct()

    def active(self, get_active_collection=user_request_context.get_current_user_active_collection):
        return self.filter(
            ticket__article__journals__collections=get_active_collection()).distinct()


class CommentManager(UserObjectManager):
    def get_query_set(self):
        return CommentQuerySet(self.model, using=self._db)

