# coding: utf-8
from waffle import Flag
from django_webtest import WebTest
from django_factory_boy import auth
from django.core.urlresolvers import reverse
from django.template import defaultfilters as filters
from django.conf import settings

from . import modelfactories
from journalmanager.tests.modelfactories import UserFactory, CollectionFactory


def _makePermission(perm, model, app_label='articletrack'):
    """
    Retrieves a Permission according to the given model and app_label.
    """
    from django.contrib.contenttypes import models
    from django.contrib.auth import models as auth_models

    ct = models.ContentType.objects.get(model=model,
                                        app_label=app_label)
    return auth_models.Permission.objects.get(codename=perm, content_type=ct)


class CheckinListTests(WebTest):

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
        rejection_text = 'your checkin is bad, and you should feel bad!'

        # send to review
        checkin.send_to_review(self.user)
        # reject
        checkin.do_reject(self.user, rejection_text)
        # send to pending
        checkin.send_to_pending(self.user)
        # send to review
        checkin.send_to_review(self.user)
        # do review
        checkin.do_review(self.user)
        # do accept
        checkin.accept(self.user)

        response = self.app.get(reverse('checkin_history', args=[checkin.pk]), user=self.user)
        logs = checkin.checkin_worflow_logs.all()
        self.assertEqual(6, len(logs))

        for log in logs:
            creation_date_formatted = filters.date(log.created_at, settings.DATETIME_FORMAT)
            response.mustcontain(creation_date_formatted)
            response.mustcontain(log.user.get_full_name())
            response.mustcontain(log.status.title())
            response.mustcontain(log.get_status_display())
            response.mustcontain(log.description)


class NoticeListTests(WebTest):

    def _makeOne(self):
        notice = modelfactories.NoticeFactory.create()

        # Get only the first collection and set to the user
        collection = notice.checkin.article.journals.all()[0].collections.all()[0]
        collection.add_user(self.user, is_manager=True)

        return notice

    def _addWaffleFlag(self):
        Flag.objects.create(name='articletrack', authenticated=True)

    def setUp(self):
        self.user = UserFactory(is_active=True)
        perm = _makePermission(perm='list_notice', model='notice')
        self.user.user_permissions.add(perm)

    def test_status_code_notice_list(self):
        self._addWaffleFlag()
        notice = self._makeOne()

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

        response = self.app.get(reverse('notice_detail',
                                        args=[notice.checkin.pk]), user=self.user)

        response.mustcontain('The reference xyz is not ok')

    def test_notice_list_must_have_link_to_checkin_list(self):
        self._addWaffleFlag()
        notice = self._makeOne()

        response = self.app.get(reverse('notice_detail',
                                        args=[notice.checkin.pk]), user=self.user)

        # response.mustcontain('<a href="/arttrack/">List of check ins</a>')
        url_to_checkin_index = reverse('checkin_index')
        response.mustcontain('<a href="%s">' % url_to_checkin_index)
