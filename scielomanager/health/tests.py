# coding: utf-8
from django.test import TestCase
import mocker

import health


class CheckItem(TestCase):
    def test_call_must_be_implemented(self):
        class CheckIt(health.CheckItem):
            pass

        check = CheckIt()
        self.assertRaises(NotImplementedError, check)


class CheckListTests(mocker.MockerTestCase):

    def test_refresh_in_minutes(self):
        import datetime
        check_list = health.CheckList(refresh=2)
        self.assertEqual(datetime.timedelta(minutes=2),
            check_list._refresh_rate)

    def test_latest_refresh_date_starts_as_None(self):
        check_list = health.CheckList(refresh=2)
        self.assertIsNone(check_list._refreshed_at)


    def test_add_check(self):
        check_list = health.CheckList(refresh=2)
        self.assertEqual(len(check_list._check_list), 0)

        class CheckIt(health.CheckItem):
            def __call__(self):
                return True

        check_list.add_check(CheckIt())
        self.assertEqual(len(check_list._check_list), 1)

    def test_run(self):

        class CheckIt(health.CheckItem):
            """There be dragons"""
            def __call__(self):
                return True

        check_list = health.CheckList(refresh=2)
        check = CheckIt()
        check_list.add_check(check)
        check_list.run()

        self.assertEqual(check_list.latest_report,
            {'CheckIt': {'status': True, 'description': 'There be dragons'}})

    def test_since(self):
        """
        The elapsed time since the last refresh.
        """
        import datetime
        dt1 = datetime.datetime(2013, 12, 15, 10, 10, 10)
        dt2 = datetime.datetime(2013, 12, 15, 10, 11, 10)

        check_list = health.CheckList(refresh=1)
        check_list._refreshed_at = dt1

        mock_datetime = self.mocker.replace(datetime)
        mock_datetime.datetime.now()
        self.mocker.result(dt2)
        self.mocker.replay()

        self.assertEqual(check_list.since(), '0:01:00')

