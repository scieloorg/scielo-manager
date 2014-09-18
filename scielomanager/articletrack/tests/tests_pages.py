# coding: utf-8
from waffle import Flag
from os import path
import mocker
import lxml

from django_webtest import WebTest
from django_factory_boy import auth
from django.core.urlresolvers import reverse
from django.template import defaultfilters as filters
from django.conf import settings

from journalmanager.tests.modelfactories import UserFactory, CollectionFactory
from articletrack.tests.tests_models import create_notices
from . import modelfactories
from . import doubles
from validator.tests import doubles as packtools_double


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
        # with
        self._addWaffleFlag()
        notice = self._makeOne()

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

        XMLValidator = self.mocker.replace('packtools.stylechecker.XMLValidator')
        XMLValidator(mocker.ANY)
        self.mocker.result(packtools_double.XMLValidatorDouble(mocker.ANY))

        self.mocker.replay()
        # when
        response = self.app.get(
            reverse('notice_detail', args=[notice.checkin.pk]),
            user=self.user)
        # then
        xml_data = response.context['xml_data']
        self.assertEqual(response.status_code, 200)
        self.assertTrue(xml_data['can_be_analyzed'][0])
        self.assertIsNone(response.context['results'])
        self.assertIsNone(response.context['xml_exception'])
        self.assertEqual(xml_data['uri'], expected_response['uri'])
        self.assertEqual(xml_data['file_name'], expected_response['filename'])

    def test_annotations_warning_if_balaio_breaks(self):
        self._addWaffleFlag()
        notice = self._makeOne()

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
        # check "could not be analyzed" message
        self.assertFalse(xml_data['can_be_analyzed'][0])
        self.assertEqual(
            xml_data['can_be_analyzed'][1],
            'Could not obtain the XML with this file name %s' % expected_response['filename']
        )

        self.assertEqual(xml_data['uri'], None)
        self.assertEqual(xml_data['file_name'], expected_response['filename'])
        from validator.tests.tests_pages import PACKTOOLS_VERSION
        self.assertEqual(response.context['packtools_version'], PACKTOOLS_VERSION)

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

        XMLValidator = self.mocker.replace('packtools.stylechecker.XMLValidator')
        XMLValidator(mocker.ANY)
        self.mocker.result(packtools_double.XMLValidatorAnnotationsDouble(mocker.ANY))
        lxml_tostring = self.mocker.replace('lxml.etree.tostring')
        lxml_tostring(mocker.ANY, mocker.KWARGS)
        self.mocker.result("some annotations in xml string")

        self.mocker.replay()

        response = self.app.get(
            reverse('notice_detail', args=[notice.checkin.pk]),
            user=self.user)

        xml_data = response.context['xml_data']

        self.assertEqual(response.status_code, 200)
        self.assertTrue(xml_data['can_be_analyzed'][0])
        self.assertEqual(xml_data['uri'], expected_response['uri'])
        self.assertEqual(xml_data['file_name'], expected_response['filename'])
        results = response.context['results']
        self.assertIsNotNone(results)
        self.assertIsNotNone(results['annotations'])
        validation_errors = results['validation_errors']
        self.assertIsNotNone(validation_errors)
        self.assertEqual(1, len(validation_errors))

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

        XMLValidator = self.mocker.replace('packtools.stylechecker.XMLValidator')
        XMLValidator(expected_response['uri'])
        self.mocker.throw(IOError)
        self.mocker.replay()

        response = self.app.get(
            reverse('notice_detail', args=[notice.checkin.pk]),
            user=self.user)

        xml_data = response.context['xml_data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(xml_data['uri'], expected_response['uri'])
        self.assertEqual(xml_data['file_name'], expected_response['filename'])
        self.assertTrue(xml_data['can_be_analyzed'][0])
        # previous version display a IOError exception custom messsage
        expected_results = None
        expected_xml_exception = ''

        self.assertEqual(response.context['results'], expected_results)
        self.assertEqual(response.context['xml_exception'], expected_xml_exception)

    def test_annotations_of_syntax_error(self):
        self._addWaffleFlag()
        notice = self._makeOne()

        target_xml = "with_syntax_error.xml"
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

        syntax_error_data = {
            'message': u'Premature end of data in tag xml line 1, line 1, column 6',
            'line': 1,
            'column': 6,
            'code': 77,
        }

        XMLValidator = self.mocker.replace('packtools.stylechecker.XMLValidator')
        XMLValidator(expected_response['uri'])
        self.mocker.throw(
            lxml.etree.XMLSyntaxError(
                syntax_error_data['message'],
                syntax_error_data['code'],
                syntax_error_data['line'],
                syntax_error_data['column'],
            )
        )

        self.mocker.replay()

        response = self.app.get(
            reverse('notice_detail', args=[notice.checkin.pk]),
            user=self.user)

        xml_data = response.context['xml_data']

        self.assertEqual(response.status_code, 200)
        self.assertTrue(xml_data['can_be_analyzed'][0])
        self.assertEqual(xml_data['uri'], expected_response['uri'])
        self.assertEqual(xml_data['file_name'], expected_response['filename'])

        results = response.context['results']
        xml_exception = response.context['xml_exception']
        self.assertIsNone(results)
        self.assertIsNotNone(xml_exception)
        self.assertEqual(xml_exception, syntax_error_data['message'])



class CheckinWorkflowTests(WebTest, mocker.MockerTestCase):

    def _mock_balaio_disabled(self):
        # to avoid making a request will replace it with a double
        balaio = self.mocker.replace('articletrack.balaio.BalaioAPI')
        balaio()
        self.mocker.result(doubles.BalaioAPIDoubleDisabled())
        self.mocker.replay()

    def _makeOne(self):
        checkin = modelfactories.CheckinFactory.create()

        # # Get only the first collection and set to the user
        collection = checkin.article.journals.all()[0].collections.all()[0]
        collection.add_user(self.user, is_manager=True)
        collection.make_default_to_user(self.user)

        collection.add_user(self.user_qal_1, is_manager=True)
        collection.make_default_to_user(self.user_qal_1)

        collection.add_user(self.user_qal_2, is_manager=True)
        collection.make_default_to_user(self.user_qal_2)

        return checkin

    def _addWaffleFlag(self):
        Flag.objects.create(name='articletrack', authenticated=True)

    def setUp(self):
        self.user = auth.UserF(is_active=True)
        self.collection = CollectionFactory.create()

        # checkin list permission
        list_checkin_perm = _makePermission(perm='list_checkin', model='checkin')
        # notices_detail view, requires this permission too
        list_notice_perm = _makePermission(perm='list_notice', model='notice')

        # users-groups-permissions
        self.group_producer = auth.GroupF(name='producer')
        self.user.groups.add(self.group_producer)
        self.user.save()

        self.user.user_permissions.add(list_notice_perm)
        self.user.user_permissions.add(list_checkin_perm)
        # QAL 1 definitions
        self.user_qal_1 = auth.UserF(is_active=True)
        self.group_qal_1 = auth.GroupF(name='QAL1')
        self.user_qal_1.groups.add(self.group_qal_1)
        self.user_qal_1.save()

        self.user_qal_1.user_permissions.add(list_notice_perm)
        self.user_qal_1.user_permissions.add(list_checkin_perm)
        # QAL 2 definitions
        self.user_qal_2 = auth.UserF(is_active=True)
        self.group_qal_2 = auth.GroupF(name='QAL2')
        self.user_qal_2.groups.add(self.group_qal_2)
        self.user_qal_2.save()

        self.user_qal_2.user_permissions.add(list_notice_perm)
        self.user_qal_2.user_permissions.add(list_checkin_perm)

        # add user, user_qal1 and user_qal2 to default collection
        self.collection.add_user(self.user)
        self.collection.make_default_to_user(self.user)
        # add qal1 user to collection
        self.collection.add_user(self.user_qal_1)
        self.collection.make_default_to_user(self.user_qal_1)
        # add qal2 user to collection
        self.collection.add_user(self.user_qal_2)
        self.collection.make_default_to_user(self.user_qal_2)

    def tearDown(self):
        """
        Restore the default values.
        """

    def test_checkin_send_to_review(self):
        """ Create a checkin and call the view: checkin_send_to_review """
        self._addWaffleFlag()
        checkin = self._makeOne()
        create_notices('ok', checkin)

        # mock balaio for request checkin files
        self._mock_balaio_disabled()

        response = self.app.get(reverse('checkin_send_to_review', args=[checkin.pk, ]), user=self.user)
        response = response.follow() #  "checkin_send_to_review" redirects to: "notice_detail"

        self.assertEqual(response.status_code, 200)

        expected_message = 'Checkin was SENT TO REVIEW succesfully.'
        self.assertIn(expected_message, response.body)

        response_checkin = response.context['checkin']
        self.assertTrue(response_checkin.status, 'review')
        # is not reviewed yet
        self.assertFalse(response_checkin.is_level1_reviewed)
        self.assertFalse(response_checkin.is_level2_reviewed)
        self.assertFalse(response_checkin.is_full_reviewed)
        self.assertFalse(response_checkin.can_be_send_to_review)
        self.assertFalse(response_checkin.is_accepted)
        # can be rejected or reviewed
        self.assertTrue(response_checkin.can_be_rejected)
        self.assertTrue(response_checkin.can_be_reviewed)

    def test_checkin_reject(self):
        """ Create a checkin and call the view: checkin_reject """
        self._addWaffleFlag()
        checkin = self._makeOne()
        create_notices('ok', checkin)
        rejection_text = 'your checkin is bad, and you should feel bad!'
        # send to review
        checkin.send_to_review(self.user)

        form = self.app.get(
            reverse('checkin_reject', args=[checkin.pk, ]),
            user=self.user).follow().forms['checkin_reject_form']
        form['rejected_cause'] = rejection_text
        response = form.submit()
        response = response.follow() #  "checkin_reject" redirects to: "notice_detail"

        self.assertEqual(response.status_code, 200)

        expected_message = 'Checkin REJECTED succesfully.'
        self.assertIn(expected_message, response.body)

        response_checkin = response.context['checkin']
        self.assertTrue(response_checkin.status, 'rejected')

        self.assertFalse(response_checkin.is_level1_reviewed)
        self.assertFalse(response_checkin.is_level2_reviewed)
        self.assertFalse(response_checkin.is_full_reviewed)
        self.assertFalse(response_checkin.can_be_send_to_review)
        self.assertFalse(response_checkin.is_accepted)
        # can't be rejected or reviewed
        self.assertFalse(response_checkin.can_be_rejected)
        self.assertFalse(response_checkin.can_be_reviewed)
        # can be sent to pending
        self.assertTrue(response_checkin.can_be_send_to_pending)

    def test_checkin_send_to_pending(self):
        """ Create a checkin and call the view: checkin_send_to_pending """
        self._addWaffleFlag()
        checkin = self._makeOne()
        create_notices('ok', checkin)
        rejection_text = 'your checkin is bad, and you should feel bad!'

        # send to review
        checkin.send_to_review(self.user)
        # reject
        checkin.do_reject(self.user_qal_1, rejection_text)

        # mock balaio for request checkin files
        self._mock_balaio_disabled()

        response = self.app.get(reverse('checkin_send_to_pending', args=[checkin.pk, ]), user=self.user)
        response = response.follow() #  "checkin_send_to_pending" redirects to: "notice_detail"

        self.assertEqual(response.status_code, 200)

        expected_message = 'Checkin was SENT TO PENDING succesfully.'
        self.assertIn(expected_message, response.body)

        response_checkin = response.context['checkin']
        self.assertTrue(response_checkin.status, 'pending')
        # is not reviewed or rejected or accepted yet
        self.assertFalse(response_checkin.is_level1_reviewed)
        self.assertFalse(response_checkin.is_level2_reviewed)
        self.assertFalse(response_checkin.is_full_reviewed)
        self.assertFalse(response_checkin.is_rejected)
        self.assertFalse(response_checkin.is_accepted)
        # can't be sent to pending again
        self.assertFalse(response_checkin.can_be_send_to_pending)
        # but can be send to review
        self.assertTrue(response_checkin.can_be_send_to_review)

    def test_checkin_review_level1(self):
        """ Create a checkin and call the view: checkin_review(level=1) """
        self._addWaffleFlag()
        checkin = self._makeOne()
        create_notices('ok', checkin)
        # send to review
        checkin.send_to_review(self.user)

        # mock balaio for request checkin files
        self._mock_balaio_disabled()

        # do review by QAL1
        response = self.app.get(reverse('checkin_review', args=[checkin.pk, 1]), user=self.user_qal_1)
        response = response.follow() #  "checkin_review" redirects to: "notice_detail"

        self.assertEqual(response.status_code, 200)

        expected_message = 'Checkin REVIEWED succesfully.'
        self.assertIn(expected_message, response.body)

        response_checkin = response.context['checkin']
        self.assertTrue(response_checkin.status, 'review')
        # is only reviewed at level 1
        self.assertTrue(response_checkin.is_level1_reviewed)
        self.assertFalse(response_checkin.is_level2_reviewed)
        self.assertFalse(response_checkin.is_full_reviewed)
        self.assertFalse(response_checkin.can_be_send_to_review)
        self.assertFalse(response_checkin.is_accepted)
        # can be rejected and reviewed too
        self.assertTrue(response_checkin.can_be_rejected)
        self.assertTrue(response_checkin.can_be_reviewed)

    def test_checkin_review_level2(self):
        """ Create a checkin and call the view: checkin_review(level=2) """
        self._addWaffleFlag()
        checkin = self._makeOne()
        create_notices('ok', checkin)
        # send to review
        checkin.send_to_review(self.user)
        # do review by QAL1
        self.assertTrue(checkin.can_be_reviewed)
        checkin.do_review_by_level_1(self.user_qal_1)

        # mock balaio for request checkin files
        self._mock_balaio_disabled()

        # do review by user_qal2
        response = self.app.get(reverse('checkin_review', args=[checkin.pk, 2]), user=self.user_qal_2)

        # if ok, will try automatically to call checkin_accept
        self.assertEqual(response.status_code, 302)
        expected_location = reverse('checkin_accept', args=[checkin.pk, ])
        self.assertTrue(response.location.endswith(expected_location))

        # if ok, will try automatically to call checkin_send_to_checkout
        response = response.follow()
        expected_location = reverse('checkin_send_to_checkout', args=[checkin.pk, ])
        self.assertTrue(response.location.endswith(expected_location))

        # if ok, will try automatically to call notice_detail
        response = response.follow()
        expected_location = reverse('notice_detail', args=[checkin.pk, ])
        self.assertTrue(response.location.endswith(expected_location))

        # finally get response and check status
        response = response.follow()
        self.assertEqual(response.status_code, 200)

        expected_message = 'Checkin REVIEWED succesfully.'
        self.assertIn(expected_message, response.body)

        expected_message = 'Checkin ACCEPTED succesfully.'
        self.assertIn(expected_message, response.body)

        expected_message = "Checkin will proceed to checkout soon!"
        self.assertIn(expected_message, response.body)

        response_checkin = response.context['checkin']
        # is reviewed at level 1, level 2, accepted and scheduled to checkout
        # normally the final status now is: checkout_scheduled.
        # 'cause "review l2" -[ redirect to ]-> "accepted"  -[ redirect to ]-> "scheduled to checkout"
        self.assertTrue(response_checkin.is_level1_reviewed)
        self.assertTrue(response_checkin.is_level2_reviewed)
        self.assertFalse(response_checkin.is_accepted)
        self.assertTrue(response_checkin.is_scheduled_to_checkout)
        self.assertEqual(response_checkin.status, 'checkout_scheduled')
        # can't be rejected, reviewed, or send_to_review, or send_to_pending
        self.assertFalse(response_checkin.can_be_send_to_review)
        self.assertFalse(response_checkin.can_be_send_to_pending)
        self.assertFalse(response_checkin.can_be_rejected)
        self.assertFalse(response_checkin.can_be_reviewed)

    def test_checkin_accept(self):
        """ Create a checkin and call the view: checkin_accept """
        self._addWaffleFlag()
        checkin = self._makeOne()
        create_notices('ok', checkin)
        # send to review
        checkin.send_to_review(self.user)

        # do review by QAL1
        self.assertTrue(checkin.can_be_reviewed)
        checkin.do_review_by_level_1(self.user_qal_1)

        # do review by QAL2
        self.assertTrue(checkin.can_be_reviewed)
        checkin.do_review_by_level_2(self.user_qal_2)

        # mock balaio for request checkin files
        self._mock_balaio_disabled()

        # do accept with QAL2
        response = self.app.get(reverse('checkin_accept', args=[checkin.pk, ]), user=self.user_qal_2)
        # if ok, will try automatically to call checkin_send_to_checkout
        expected_location = reverse('checkin_send_to_checkout', args=[checkin.pk, ])
        self.assertTrue(response.location.endswith(expected_location))

        # if ok, will try automatically to call notice_detail
        response = response.follow()
        expected_location = reverse('notice_detail', args=[checkin.pk, ])
        self.assertTrue(response.location.endswith(expected_location))

        # finally get response and check status
        response = response.follow()
        self.assertEqual(response.status_code, 200)

        expected_message = 'Checkin ACCEPTED succesfully.'
        self.assertIn(expected_message, response.body)

        expected_message = "Checkin will proceed to checkout soon!"
        self.assertIn(expected_message, response.body)

        response_checkin = response.context['checkin']
        # is reviewed at level 1, level 2, accepted and scheduled to checkout
        # normally the final status now is: checkout_scheduled.
        # 'cause "review l2" -[ redirect to ]-> "accepted"  -[ redirect to ]-> "scheduled to checkout"
        self.assertTrue(response_checkin.is_level1_reviewed)
        self.assertTrue(response_checkin.is_level2_reviewed)
        self.assertFalse(response_checkin.is_accepted)
        self.assertTrue(response_checkin.is_scheduled_to_checkout)
        self.assertEqual(response_checkin.status, 'checkout_scheduled')
        # can't be rejected, reviewed, or send_to_review, or send_to_pending
        self.assertFalse(response_checkin.can_be_send_to_review)
        self.assertFalse(response_checkin.can_be_send_to_pending)
        self.assertFalse(response_checkin.can_be_rejected)
        self.assertFalse(response_checkin.can_be_reviewed)

    def test_checkin_send_to_checkout(self):
        """
        Create a checkin and call the view: checkin_send_to_checkout.
        """
        self._addWaffleFlag()
        checkin = self._makeOne()
        create_notices('ok', checkin)

        # send to review
        checkin.send_to_review(self.user)

        # do review by QAL1
        self.assertTrue(checkin.can_be_reviewed)
        checkin.do_review_by_level_1(self.user_qal_1)

        # do review by QAL2
        self.assertTrue(checkin.can_be_reviewed)
        checkin.do_review_by_level_2(self.user_qal_2)

        # do accept
        self.assertTrue(checkin.can_be_accepted)
        checkin.accept(self.user_qal_2)

        # mock balaio for request checkin files
        self._mock_balaio_disabled()

        # try to do send to checkout:
        response = self.app.get(reverse('checkin_send_to_checkout', args=[checkin.pk, ]), user=self.user_qal_2)

        # if ok, will try automatically to call notice_detail
        expected_location = reverse('notice_detail', args=[checkin.pk, ])
        self.assertTrue(response.location.endswith(expected_location))

        # finally get response and check status
        response = response.follow()
        self.assertEqual(response.status_code, 200)

        expected_message = "Checkin will proceed to checkout soon!"
        self.assertIn(expected_message, response.body)

        response_checkin = response.context['checkin']
        # is reviewed at level 1, level 2, accepted and scheduled to checkout
        # normally the final status now is: checkout_scheduled.
        # 'cause "review l2" -[ redirect to ]-> "accepted"  -[ redirect to ]-> "scheduled to checkout"
        self.assertTrue(response_checkin.is_level1_reviewed)
        self.assertTrue(response_checkin.is_level2_reviewed)
        self.assertFalse(response_checkin.is_accepted)
        self.assertTrue(response_checkin.is_scheduled_to_checkout)
        self.assertEqual(response_checkin.status, 'checkout_scheduled')
        # can't be rejected, reviewed, or send_to_review, or send_to_pending
        self.assertFalse(response_checkin.can_be_send_to_review)
        self.assertFalse(response_checkin.can_be_send_to_pending)
        self.assertFalse(response_checkin.can_be_rejected)
        self.assertFalse(response_checkin.can_be_reviewed)
