# coding: utf-8
from django.test import TestCase
from django_factory_boy import auth
from journalmanager.models import Journal
from .modelfactories import (
    JournalFactory,
    CollectionFactory,
    RegularPressReleaseFactory,
    StatusPartyFactory,
    JournalPublicationEventsFactory,
    UserFactory
)


class SignalsTests(TestCase):

    def test_updating_journal_after_statusparty_post_save(self):
        user = UserFactory(is_active=True)
        collection = CollectionFactory.create()
        collection.add_user(user, is_manager=True)
        journal = JournalFactory(pub_status=u'inprocess')
        status1 = JournalPublicationEventsFactory.create(status=u'current', reason='porque sim!')
        status2 = JournalPublicationEventsFactory.create(status=u'deceased', reason='porque não gostei!')

        StatusPartyFactory.create(
            collection=collection,
            journal=journal,
            publication_status=status1
        )

        StatusPartyFactory.create(
            collection=collection,
            journal=journal,
            publication_status=status2
        )

        self.assertTrue(
            Journal.objects.get(pk=journal.pk).pub_status,
            u'deceased'
        )

        self.assertTrue(
            Journal.objects.get(pk=journal.pk).pub_status,
            u'porque não gostei!'
        )