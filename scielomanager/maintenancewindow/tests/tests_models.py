# coding: utf-8
from django.test import TestCase

from .modelfactories import (
    EventFactory,
)


class SectionTests(TestCase):

    def test_on_maintenace_out_of_range(self):
        """
        Testing if a given date is out of the period of the available events.
        """
        event = EventFactory.create(
            begin_at=u'2012-11-12 14:00:00.000000',
            end_at=u'2012-11-12 14:01:00.000000'
        )
        self.assertFalse(event.on_maintenance(
            date=u'2012-11-11 14:00:00.000000')
        )

    def test_on_maintenace_in_range(self):
        """
        Testing if a given date is in the period of an available event.
        """
        event = EventFactory.create(
            begin_at=u'2012-11-12 14:00:00.000000',
            end_at=u'2012-11-12 14:02:00.000000'
            )

        self.assertTrue(event.on_maintenance(
            date=u'2012-11-12 14:01:00.000000')
        )
