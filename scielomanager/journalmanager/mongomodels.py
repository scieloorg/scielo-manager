# coding:utf-8
from urlparse import urlparse

from django.conf import settings
import pymongo


class MongoManager(object):

    def __init__(self):
        """
        Connects to MongoDB and makes self.db available to the instance.
        """
        db_url = urlparse(getattr(settings, 'MONGO_URI',
            r'mongodb://localhost:27017/journalmanager'))
        self._conn = pymongo.Connection(host=db_url.hostname,
                                        port=db_url.port)
        self.db = self._conn[db_url.path[1:]]
        if db_url.username and db_url.password:
            self.db.authenticate(db_url.username, db_url.password)
