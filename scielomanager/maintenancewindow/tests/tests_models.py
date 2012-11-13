# coding: utf-8
from django.test import TestCase

from .modelfactories import (
    EventFactory,
)


class SectionTests(TestCase):

    def test_on_maintenace(self):
        """
        Testing if a given date is out of the period of the available events.
        """
        event = EventFactory.create(
            is_blocking_users=True
        )
        self.assertTrue(event.on_maintenance())

    def test_not_on_maintenace(self):
        """
        Testing if a given date is in the period of an available event.
        """
        event = EventFactory.create(
            is_blocking_users=False
        )

        self.assertFalse(event.on_maintenance())

    def test_scheduled_events_unavailable(self):

        event = EventFactory.create(
            end_at=u'2012-11-12',
        )

        # Once no date was given, the call for open_events is assuming the current date.
        self.assertTrue(len(event.scheduled_events()) == 0)

    def test_scheduled_events_available(self):

        event = EventFactory.create(
            end_at=u'2012-11-12',
        )

        self.assertTrue(len(event.scheduled_events(actual_date="2012-11-11")) > 0)
