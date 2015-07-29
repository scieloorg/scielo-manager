# coding:utf-8
from mocker import MockerTestCase

from scielomanager.connectors.storage import ArticleElasticsearch


class ElasticsearchTests(MockerTestCase):

    def test_client_is_reused(self):
        self.assertEqual(ArticleElasticsearch().es_client,
                         ArticleElasticsearch().es_client)

