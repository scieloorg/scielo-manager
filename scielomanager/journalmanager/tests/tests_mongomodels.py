# coding: utf-8
from django.test import TestCase
import pymongo
from mocker import (
    MockerTestCase,
    ANY,
    KWARGS,
)


class MongoManagerTest(TestCase, MockerTestCase):

    def _makeOne(self, *args, **kwargs):
        from journalmanager.mongomodels import MongoManager
        return MongoManager(*args, **kwargs)

    def test_make_db_available_on_instantiation(self):
        mongo_driver = self.mocker.mock()
        mongo_conn = self.mocker.mock()
        mongo_db = self.mocker.mock(pymongo.database.Database)

        mongo_driver.Connection(host=ANY, port=ANY)
        self.mocker.result(mongo_conn)

        mongo_conn[ANY]
        self.mocker.result(mongo_db)

        mongo_db.authenticate(ANY, ANY)
        self.mocker.result(None)

        self.mocker.replay()

        mongo_uri = r'mongodb://user:pass@localhost:27017/journalmanager'
        mm = self._makeOne(mongodb_driver=mongo_driver, mongo_uri=mongo_uri)

        self.assertIsInstance(mm.db, pymongo.database.Database)

    def test_expose_pymongo_find_method(self):
        mongo_driver = self.mocker.mock()
        mongo_conn = self.mocker.mock()
        mongo_db = self.mocker.mock(pymongo.database.Database)
        mongo_col = self.mocker.mock()

        mongo_driver.Connection(host=ANY, port=ANY)
        self.mocker.result(mongo_conn)

        mongo_conn[ANY]
        self.mocker.result(mongo_db)

        mongo_db.authenticate(ANY, ANY)
        self.mocker.result(None)

        mongo_db['articles']
        self.mocker.result(mongo_col)

        mongo_col.find()
        self.mocker.result({})

        self.mocker.replay()

        mongo_uri = r'mongodb://user:pass@localhost:27017/journalmanager'
        mm = self._makeOne(mongodb_driver=mongo_driver,
                           mongo_uri=mongo_uri,
                           mongo_collection='articles')

        self.assertEqual(mm.find(), {})


class ArticleModelTest(TestCase, MockerTestCase):

    def _makeOne(self, *args, **kwargs):
        from journalmanager.mongomodels import Article
        return Article(*args, **kwargs)

    def test_simple_attr_access(self):
        mongo_driver = self.mocker.mock()
        mongo_conn = self.mocker.mock()
        mongo_db = self.mocker.mock(pymongo.database.Database)

        mongo_driver.Connection(host=ANY, port=ANY)
        self.mocker.result(mongo_conn)

        mongo_conn[ANY]
        self.mocker.result(mongo_db)

        mongo_db.authenticate(ANY, ANY)
        self.mocker.result(None)

        self.mocker.replay()

        article_microdata = {
            'title': 'Micronucleated lymphocytes in parents of lalala children'
        }

        mongo_uri = r'mongodb://user:pass@localhost:27017/journalmanager'
        a = self._makeOne(mongodb_driver=mongo_driver,
                          mongo_uri=mongo_uri,
                          **article_microdata)

        self.assertEqual(a.title,
            'Micronucleated lymphocytes in parents of lalala children')
