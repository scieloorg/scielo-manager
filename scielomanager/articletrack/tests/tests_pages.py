# coding: utf-8
from waffle import Flag
from os import path
import mocker

from django_webtest import WebTest
from django_factory_boy import auth
from django.core.urlresolvers import reverse
from django.template import defaultfilters as filters
from django.conf import settings

from journalmanager.tests.modelfactories import UserFactory, CollectionFactory
from articletrack.tests.tests_models import create_notices
from . import modelfactories
from . import doubles


def _makePermission(perm, model, app_label='articletrack'):
    """
    Retrieves a Permission according to the given model and app_label.
    """
    from django.contrib.contenttypes import models
    from django.contrib.auth import models as auth_models

    ct = models.ContentType.objects.get(model=model,
                                        app_label=app_label)
    return auth_models.Permission.objects.get(codename=perm, content_type=ct)


class CheckinListTests(WebTest, mocker.MockerTestCase):

    def setUp(self):
        self.user = auth.UserF(is_active=True)
        self.collection = CollectionFactory.create()
        self.collection.add_user(self.user)
        self.collection.make_default_to_user(self.user)
        perm = _makePermission(perm='list_checkin', model='checkin')
        self.user.user_permissions.add(perm)

    def tearDown(self):
        """
        Restore the default values.
        """

    def _makeOne(self):
        checkin = modelfactories.CheckinFactory.create()

        # Get only the first collection and set to the user
        collection = checkin.article.journals.all()[0].collections.all()[0]
        collection.add_user(self.user, is_manager=True)
        collection.make_default_to_user(self.user)

        return checkin

    def _addWaffleFlag(self):
        Flag.objects.create(name='articletrack', authenticated=True)

    def test_status_code_checkin_list(self):
        self._addWaffleFlag()

        response = self.app.get('/arttrack/', user=self.user)

        self.assertEqual(response.status_code, 200)

    def test_status_code_checkin_list_without_waffle_flag(self):
        response = self.app.get(reverse('checkin_index'), user=self.user, expect_errors=True)

        self.assertEqual(response.status_code, 404)

    def test_checkin_list_with_itens(self):
        self._addWaffleFlag()
        checkin = self._makeOne()

        response = self.app.get(reverse('checkin_index'), user=self.user)

        response.mustcontain(checkin.article.article_title)
        self.assertIn(checkin, response.context['checkins_pending'])

    def test_status_code_checkin_history(self):
        self._addWaffleFlag()
        checkin = self._makeOne()

        response = self.app.get(reverse('checkin_history', args=[checkin.pk, ]), user=self.user)
        self.assertEqual(response.status_code, 200)

    def test_package_history_index_with_itens(self):
        self._addWaffleFlag()
        checkin = self._makeOne()

        response = self.app.get(reverse('checkin_history', args=[checkin.pk, ]), user=self.user)

        response.mustcontain(str(checkin.article.article_title))
        response.mustcontain(str(checkin.package_name))
        self.assertTrue(response.context['checkin'], checkin)

    def test_checkin_history_index_have_article_title(self):
        self._addWaffleFlag()
        checkin = self._makeOne()

        response = self.app.get(reverse('checkin_history',
                                        args=[checkin.pk, ]), user=self.user)

        response.mustcontain(checkin.article.article_title)

    def test_checkin_history_must_have_link_to_checkin_list(self):
        self._addWaffleFlag()
        checkin = self._makeOne()

        response = self.app.get(reverse('checkin_history', args=[checkin.pk]), user=self.user)
        url_to_checkin_details = reverse('notice_detail', args=[checkin.pk, ])
        url_to_checkin_index = reverse('checkin_index')
        response.mustcontain('href="%s"' % url_to_checkin_index)
        response.mustcontain('href="%s"' % url_to_checkin_details)

    def test_checkin_history_must_have_button_to_checkin_detail(self):
        self._addWaffleFlag()
        checkin = self._makeOne()

        response = self.app.get(reverse('checkin_history', args=[checkin.pk]), user=self.user)
        url_to_checkin_details = reverse('notice_detail', args=[checkin.pk])
        response.mustcontain(url_to_checkin_details)

    def test_checkin_history_must_show_all_workflowlogs(self):
        """
        test making all steps of the checkin worflow, and ensure that all logs generated,
        must be presented in the checking_history page
        """
        self._addWaffleFlag()
        checkin = self._makeOne()
        create_notices('ok', checkin)
        rejection_text = 'your checkin is bad, and you should feel bad!'

        # users
        group_producer = auth.GroupF(name='producer')
        self.user.groups.add(group_producer)
        self.user.save()
        # QAL 1 definitions
        user_qal_1 = auth.UserF(is_active=True)
        group_qal_1 = auth.GroupF(name='QAL1')
        user_qal_1.groups.add(group_qal_1)
        user_qal_1.save()
        # QAL 2 definitions
        user_qal_2 = auth.UserF(is_active=True)
        group_qal_2 = auth.GroupF(name='QAL2')
        user_qal_2.groups.add(group_qal_2)
        user_qal_2.save()

        # send to review
        checkin.send_to_review(self.user)
        # reject
        checkin.do_reject(user_qal_1, rejection_text)
        # send to pending
        checkin.send_to_pending(user_qal_2)
        # send to review
        checkin.send_to_review(self.user)

        # do review by QAL1
        self.assertTrue(checkin.can_be_reviewed)
        checkin.do_review_by_level_1(user_qal_1)

        # do review by QAL2
        self.assertTrue(checkin.can_be_reviewed)
        checkin.do_review_by_level_2(user_qal_2)

        # do accept
        self.assertTrue(checkin.can_be_accepted)
        checkin.accept(user_qal_2)

        response = self.app.get(reverse('checkin_history', args=[checkin.pk]), user=self.user)
        logs = checkin.submission_log.all()
        self.assertEqual(7, len(logs))

        for log in logs:
            creation_date_formatted = filters.date(log.created_at, settings.DATETIME_FORMAT)
            response.mustcontain(creation_date_formatted)
            response.mustcontain(log.user.get_full_name())
            response.mustcontain(log.status.title())
            response.mustcontain(log.get_status_display())
            response.mustcontain(log.description)


class CheckinDetailTests(WebTest, mocker.MockerTestCase):

    def _makeOne(self):
        notice = modelfactories.NoticeFactory.create()

        # Get only the first collection and set to the user
        collection = notice.checkin.article.journals.all()[0].collections.all()[0]
        collection.add_user(self.user, is_manager=True)

        return notice

    def _get_path_of_test_xml(self, xml_file_name):
        """
        return the abs path the xml file which name is: ``xml_file_name``
        located in: ``articletrack/tests/xml_tests_files/<xml_file_name>``
        """
        tests_xmls_dirs = path.abspath(path.join(path.dirname(__file__), 'xml_tests_files'))
        return 'file://%s' % path.join(tests_xmls_dirs, xml_file_name)

    def _addWaffleFlag(self):
        Flag.objects.create(name='articletrack', authenticated=True)

    def setUp(self):
        self.user = UserFactory(is_active=True)
        perm = _makePermission(perm='list_notice', model='notice')
        self.user.user_permissions.add(perm)

    def test_status_code_notice_list(self):
        self._addWaffleFlag()
        notice = self._makeOne()

        # to avoid making a request will replace it with a double
        balaio = self.mocker.replace('articletrack.balaio.BalaioAPI')
        balaio()
        self.mocker.result(doubles.BalaioAPIDoubleDisabled())
        self.mocker.replay()

        response = self.app.get(reverse('notice_detail',
                                        args=[notice.checkin.pk]), user=self.user)

        self.assertEqual(response.status_code, 200)

    def test_status_code_notice_list_without_waflle_flag(self):
        notice = self._makeOne()

        response = self.app.get(reverse('notice_detail', args=[notice.checkin.pk]),
                                user=self.user, expect_errors=True)

        self.assertEqual(response.status_code, 404)

    def test_notice_list_with_itens(self):
        self._addWaffleFlag()
        notice = self._makeOne()

        # to avoid making a request will replace it with a double
        balaio = self.mocker.replace('articletrack.balaio.BalaioAPI')
        balaio()
        self.mocker.result(doubles.BalaioAPIDoubleDisabled())
        self.mocker.replay()

        response = self.app.get(reverse('notice_detail',
                                        args=[notice.checkin.pk]), user=self.user)

        response.mustcontain('The reference xyz is not ok')

    def test_notice_list_must_have_link_to_checkin_list(self):
        self._addWaffleFlag()
        notice = self._makeOne()

        # to avoid making a request will replace it with a double
        balaio = self.mocker.replace('articletrack.balaio.BalaioAPI')
        balaio()
        self.mocker.result(doubles.BalaioAPIDoubleDisabled())
        self.mocker.replay()

        response = self.app.get(reverse('notice_detail',
                                        args=[notice.checkin.pk]), user=self.user)

        url_to_checkin_index = reverse('checkin_index')
        response.mustcontain('<a href="%s">' % url_to_checkin_index)

    def test_annotations_ok_if_xml_is_valid(self):
        self._addWaffleFlag()
        notice = self._makeOne()

        # MOCK/REPLACE/FAKE/PIMP MY BALAIO!!!
        target_xml = "valid.xml"
        expected_response = {
            "filename": "1415-4757-gmb-37-0210.xml",
            "uri": self._get_path_of_test_xml(target_xml)
        }

        class BalaioTest(doubles.BalaioAPIDouble):
            def get_xml_uri(self, attempt_id, target_name):
                return expected_response['uri']

        balaio = self.mocker.replace('articletrack.balaio.BalaioAPI')
        balaio()
        self.mocker.result(BalaioTest())

        # MOCK/REPLACE/FAKE/PIMP MY STYLECHECKER!!!
        XML = self.mocker.replace('packtools.stylechecker.XML')
        XML(mocker.ANY)
        self.mocker.result(doubles.StylecheckerDouble(mocker.ANY))

        self.mocker.replay()
        response = self.app.get(
            reverse('notice_detail', args=[notice.checkin.pk]),
            user=self.user)
        xml_data = response.context['xml_data']

        self.assertEqual(response.status_code, 200)
        self.assertTrue(xml_data['can_be_analyzed'][0])
        self.assertIsNone(xml_data['annotations'])
        self.assertEqual(xml_data['uri'], expected_response['uri'])
        self.assertIsNone(xml_data['validation_errors'])
        self.assertEqual(xml_data['file_name'], expected_response['filename'])

    def test_annotations_warning_if_balaio_breaks(self):
        self._addWaffleFlag()
        notice = self._makeOne()

        # MOCK/REPLACE/FAKE/PIMP MY BALAIO!!!
        target_xml = "error.xml"
        expected_response = {
            "filename": "1415-4757-gmb-37-0210.xml",
            "uri": self._get_path_of_test_xml(target_xml)
        }

        class BalaioTest(doubles.BalaioAPIDouble):
            def get_xml_uri(self, attempt_id, target_name):
                raise ValueError

        balaio = self.mocker.replace('articletrack.balaio.BalaioAPI')
        balaio()
        self.mocker.result(BalaioTest())
        self.mocker.replay()

        response = self.app.get(
            reverse('notice_detail', args=[notice.checkin.pk]),
            user=self.user)
        xml_data = response.context['xml_data']

        self.assertEqual(response.status_code, 200)
        self.assertFalse(xml_data['can_be_analyzed'][0])
        self.assertIsNone(xml_data['annotations'])
        self.assertEqual(xml_data['uri'], None)
        self.assertIsNone(xml_data['validation_errors'])
        self.assertEqual(xml_data['file_name'], expected_response['filename'])

    def test_annotations_of_error(self):
        self._addWaffleFlag()
        notice = self._makeOne()

        target_xml = "with_style_errors.xml"
        expected_response = {
            "filename": "1415-4757-gmb-37-0210.xml",
            "uri": self._get_path_of_test_xml(target_xml)
        }

        class BalaioTest(doubles.BalaioAPIDouble):
            def get_xml_uri(self, attempt_id, target_name):
                return expected_response['uri']

        balaio = self.mocker.replace('articletrack.balaio.BalaioAPI')
        balaio()
        self.mocker.result(BalaioTest())

        XML = self.mocker.replace('packtools.stylechecker.XML')
        XML(mocker.ANY)
        self.mocker.result(doubles.StylecheckerAnnotationsDouble(mocker.ANY))

        self.mocker.replay()

        response = self.app.get(
            reverse('notice_detail', args=[notice.checkin.pk]),
            user=self.user)

        xml_data = response.context['xml_data']

        self.assertEqual(response.status_code, 200)
        self.assertTrue(xml_data['can_be_analyzed'][0])
        self.assertIsNotNone(xml_data['annotations'])
        self.assertEqual(xml_data['uri'], expected_response['uri'])
        self.assertEqual(xml_data['file_name'], expected_response['filename'])
        self.assertIsNotNone(xml_data['validation_errors'])
        self.assertEqual('', xml_data['validation_errors']['error_lines'])
        self.assertEqual(1, len(xml_data['validation_errors']['results']))
        self.assertEqual(
                xml_data['validation_errors']['results'],
                [{'column': '--',
                  'line': '--',
                  'message': u"Element 'funding-group': This element is not filled-in correctly.",
                  'level': u'ERROR'}])

    def test_xml_not_found(self):
        self._addWaffleFlag()
        notice = self._makeOne()

        target_xml = "blaus.xml"
        expected_response = {
            "filename": "1415-4757-gmb-37-0210.xml",
            "uri": self._get_path_of_test_xml(target_xml)
        }

        class BalaioTest(doubles.BalaioAPIDouble):
            def get_xml_uri(self, attempt_id, target_name):
                return expected_response['uri']

        balaio = self.mocker.replace('articletrack.balaio.BalaioAPI')
        balaio()
        self.mocker.result(BalaioTest())

        XML = self.mocker.replace('packtools.stylechecker.XML')
        XML(expected_response['uri'])
        self.mocker.throw(IOError)
        self.mocker.replay()

        response = self.app.get(
            reverse('notice_detail', args=[notice.checkin.pk]),
            user=self.user)

        xml_data = response.context['xml_data']

        self.assertEqual(response.status_code, 200)
        self.assertFalse(xml_data['can_be_analyzed'][0])
        self.assertEqual(xml_data['can_be_analyzed'][1], "Error while starting Stylechecker.XML()")
        self.assertIsNone(xml_data['annotations'])
        self.assertEqual(xml_data['uri'], expected_response['uri'])
        self.assertEqual(xml_data['file_name'], expected_response['filename'])
        self.assertIsNone(xml_data['validation_errors'])

