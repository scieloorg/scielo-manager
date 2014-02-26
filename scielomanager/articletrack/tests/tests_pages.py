#coding: utf-8
from waffle import Flag
from django_webtest import WebTest
from django_factory_boy import auth
from django.core.urlresolvers import reverse

from . import modelfactories
from scielomanager.utils.modelmanagers.helpers import (
    _makeUserRequestContext,
    _patch_userrequestcontextfinder_settings_setup,
    _patch_userrequestcontextfinder_settings_teardown
    )


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


    @_patch_userrequestcontextfinder_settings_setup
    def setUp(self):
        self.user = auth.UserF(is_active=True)
        perm = _makePermission(perm='list_checkin', model='checkin')
        self.user.user_permissions.add(perm)


    @_patch_userrequestcontextfinder_settings_teardown
    def tearDown(self):
        """
        Restore the default values.
        """

    def _makeOne(self):
        checkin = modelfactories.CheckinFactory.create()

        #Get only the first collection and set to the user
        collection = checkin.article.journals.all()[0].collection
        collection.add_user(self.user, is_manager=True, is_default=True)

        return checkin

    def _addWaffleFlag(self):
        Flag.objects.create(name='articletrack', authenticated=True)


    def test_status_code_checkin_list(self):
        self._addWaffleFlag()

        response = self.app.get('/arttrack/', user=self.user)

        self.assertEqual(response.status_code, 200)

    def test_status_code_checkin_list_without_waffle_flag(self):
        response = self.app.get('/arttrack/', user=self.user, expect_errors=True)

        self.assertEqual(response.status_code, 404)

    def test_checkin_list_with_itens(self):
        self._addWaffleFlag()
        self._makeOne()

        response = self.app.get('/arttrack/', user=self.user)

        response.mustcontain('Journal of the Brazilian Chemical Society')

    def test_status_code_package_history(self):
        self._addWaffleFlag()
        checkin = self._makeOne()

        response = self.app.get(reverse('checkin_history',
            args=[checkin.article.pk]), user=self.user)

        self.assertEqual(response.status_code, 200)

    def test_package_history_index_with_itens(self):
        self._addWaffleFlag()
        checkin = self._makeOne()

        response = self.app.get(reverse('checkin_history',
            args=[checkin.article.pk]), user=self.user)

        response.mustcontain('20132404.zip')

    def test_package_history_index_have_article_title(self):
        self._addWaffleFlag()
        checkin = self._makeOne()

        response = self.app.get(reverse('checkin_history',
            args=[checkin.article.pk]), user=self.user)

        response.mustcontain('An azafluorenone alkaloid and a megastigmane from ...')

    def test_package_history_must_have_link_to_checkin_history(self):
        self._addWaffleFlag()
        checkin = self._makeOne()

        response = self.app.get(reverse('checkin_history',
            args=[checkin.article.pk]), user=self.user)

        #response.mustcontain('<a href="/arttrack/">List of check ins</a>')
        response.mustcontain('<a class="btn" href="/arttrack/"><i class="icon-arrow-left"></i> List of check ins</a>')

    def test_package_history_must_have_button_to_detail(self):
        self._addWaffleFlag()
        checkin = self._makeOne()

        response = self.app.get("/arttrack/package/%s/" % checkin.article.pk, user=self.user)

        response.mustcontain('href="/arttrack/notice/%s/"' % checkin.id)

    def test_package_history_can_create_tickets(self):
        self._addWaffleFlag()
        checkin = self._makeOne()

        response = self.app.get(reverse('checkin_history',
            args=[checkin.article.pk]), user=self.user)

        response.mustcontain(reverse('ticket_add', args=[checkin.pk]))

class NoticeListTests(WebTest):

    def _makeOne(self):
        notice = modelfactories.NoticeFactory.create()

        #Get only the first collection and set to the user
        collection = notice.checkin.article.journals.all()[0].collection
        collection.add_user(self.user, is_manager=True, is_default=True)

        return notice

    def _addWaffleFlag(self):
        Flag.objects.create(name='articletrack', authenticated=True)

    def setUp(self):
        self.user = auth.UserF(is_active=True)
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

        response = self.app.get(reverse('notice_detail',
            args=[notice.checkin.pk]), user=self.user, expect_errors=True)

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

        #response.mustcontain('<a href="/arttrack/">List of check ins</a>')
        response.mustcontain('<a href="/arttrack/"><i class="icon-chevron-left"></i> List of Articles in submission</a>')

