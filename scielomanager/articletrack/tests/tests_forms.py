# coding:utf-8

import os
import unittest
from random import randint

from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django_factory_boy import auth
from django.test import TestCase

from waffle import Flag

from journalmanager.tests.modelfactories import CollectionFactory
from articletrack.tests import modelfactories
from articletrack import forms
from articletrack import models
from scielomanager.utils.modelmanagers.helpers import (
    _patch_userrequestcontextfinder_settings_setup,
    _patch_userrequestcontextfinder_settings_teardown,
    )


MAX_CHOICES_QTY = 10


def _makePermission(perm, model, app_label='articletrack'):
    """
    Retrieves a Permission according to the given model and app_label.
    """
    from django.contrib.contenttypes import models
    from django.contrib.auth import models as auth_models

    ct = models.ContentType.objects.get(model=model,
                                        app_label=app_label)
    return auth_models.Permission.objects.get(codename=perm, content_type=ct)


def _addWaffleFlag():
    Flag.objects.create(name='articletrack', authenticated=True)


def _extract_results_from_body(response_body, extract_accepted=False):
    """
    Simplest way to extract a substring of the  response_body's HTML
    If extract_accepted:
        looks for a table with 'id="accepted_results"' until  the next </table>
    else:
        looks for a table with 'id="pending_results"' until the next </table>

    """
    pending_table_start = response_body.find('<table id="pending_results"')
    pending_table_end = response_body.find('</table>')
    pending_table_html = response_body[pending_table_start:pending_table_end]

    if extract_accepted:
        html_partial = response_body[pending_table_end + 10:]
        accepted_table_start = html_partial.find('<table id="accepted_results"')
        accepted_table_end = html_partial.find('</table>')
        accepted_table = html_partial[accepted_table_start:accepted_table_end]
        return accepted_table
    return pending_table_html


class CheckinListFilterFormTests(WebTest):

    @_patch_userrequestcontextfinder_settings_setup
    def setUp(self):
        _addWaffleFlag()
        self.user = auth.UserF(is_active=True)
        perm = _makePermission(perm='list_checkin', model='checkin')
        self.user.user_permissions.add(perm)
        self.collection = CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)
        self.collection.make_default_to_user(self.user)

    @_patch_userrequestcontextfinder_settings_teardown
    def tearDown(self):
        """
        Restore the default values.
        """

    def _make_N_checkins(self, start=0, end=MAX_CHOICES_QTY, checkins_accepted=False):
        checkins = []
        for x in xrange(start, end):

            # I want to get unique package_name
            package_name = u'201404%s.zip' % x
            new_checkin = modelfactories.CheckinFactory.create(package_name=package_name)

            # Override the issue_label to get uniques one
            new_checkin.article.issue_label = u'%s%s' % (new_checkin.article.issue_label[:-1], unicode(x))
            new_checkin.article.save()

            # associate the self.collection with the journal to be part of the checkin list
            for journal in new_checkin.article.journals.all():
                journal.collection = self.collection
                journal.save()

            if checkins_accepted:
                new_checkin.accept(self.user)
            checkins.append(new_checkin)

        return checkins

    def tests_filter_pending_by_package_name(self):
        """
        Creates various (pending) checkins and apply a filter by
        (a random existing) package name
        """
        checkins = self._make_N_checkins()

        random_index = randint(0, len(checkins) - 1)
        target_checkin = checkins[random_index]

        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_pending']
        form['pending-package_name'] = target_checkin.package_name
        response = form.submit()
        response_partial = _extract_results_from_body(response.body)
        context_checkins = response.context['checkins_pending'].object_list

        self.assertEqual(len(context_checkins), 1)
        self.assertEqual(target_checkin, context_checkins[0])
        self.assertTrue(u'%s' % target_checkin.package_name in response_partial)

    def tests_filter_pending_by_journal_title(self):
        """
        Creates various (pending) checkins and apply a filter by
        (a random existing) journal title
        """
        checkins = self._make_N_checkins()
        random_index = randint(0, len(checkins) - 1)
        target_checkin = checkins[random_index]

        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_pending']
        form['pending-journal_title'] = target_checkin.article.pk
        response = form.submit()
        response_partial = _extract_results_from_body(response.body)
        context_checkins = response.context['checkins_pending'].object_list

        self.assertEqual(len(context_checkins), 1)
        self.assertEqual(target_checkin, context_checkins[0])
        self.assertTrue(u'%s' % target_checkin.article.journal_title in response_partial)

    def tests_filter_pending_by_article(self):
        """
        Creates various (pending) checkins and apply a filter by
        (a random existing) article
        """
        checkins = self._make_N_checkins()
        random_index = randint(0, len(checkins) - 1)
        target_checkin = checkins[random_index]

        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_pending']
        form['pending-article'] = target_checkin.article.pk
        response = form.submit()
        response_partial = _extract_results_from_body(response.body)
        context_checkins = response.context['checkins_pending'].object_list

        self.assertEqual(len(context_checkins), 1)
        self.assertEqual(target_checkin, context_checkins[0])
        self.assertTrue(u'%s' % target_checkin.article.article_title in response_partial)

    def tests_filter_accepted_by_issue_label(self):
        """
        Creates various (pending) checkins and apply a filter by
        (a random existing) issue label
        """
        checkins = self._make_N_checkins(checkins_accepted=True)
        random_index = randint(0, len(checkins) - 1)
        target_checkin = checkins[random_index]

        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_accepted']
        form['accepted-issue_label'] = target_checkin.article.issue_label
        response = form.submit()
        response_partial = _extract_results_from_body(response.body)
        context_checkins = response.context['checkins_pending'].object_list

        self.assertEqual(len(context_checkins), 1)
        self.assertEqual(target_checkin, context_checkins[0])
        self.assertTrue(u'%s' % target_checkin.package_name in response_partial)

    def tests_filter_accepted_by_package_name(self):
        """
        Creates various (accepted) checkins and apply a filter by
        (a random existing) package name
        """
        checkins = self._make_N_checkins(checkins_accepted=True)

        random_index = randint(0, len(checkins) - 1)
        target_checkin = checkins[random_index]

        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_accepted']
        form['accepted-package_name'] = target_checkin.package_name
        response = form.submit()
        response_partial = _extract_results_from_body(response.body, extract_accepted=True)
        context_checkins = response.context['checkins_accepted'].object_list

        self.assertTrue(len(context_checkins) >= 1)
        self.assertIn(target_checkin, context_checkins)
        self.assertTrue(u'%s' % target_checkin.package_name in response_partial)

    def tests_filter_accepted_by_journal_title(self):
        """
        Creates various (accepted) checkins and apply a filter by
        (a random existing) journal title
        """
        checkins = self._make_N_checkins(checkins_accepted=True)
        random_index = randint(0, len(checkins) - 1)
        target_checkin = checkins[random_index]

        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_accepted']
        form['accepted-journal_title'] = target_checkin.article.pk
        response = form.submit()
        response_partial = _extract_results_from_body(response.body, extract_accepted=True)
        context_checkins = response.context['checkins_accepted'].object_list

        self.assertEqual(len(context_checkins), 1)
        self.assertEqual(target_checkin, context_checkins[0])
        self.assertTrue(u'%s' % target_checkin.article.journal_title in response_partial)

    def tests_filter_accepted_by_article(self):
        """
        Creates various (accepted) checkins and apply a filter by
        (a random existing) article
        """
        checkins = self._make_N_checkins(checkins_accepted=True)
        random_index = randint(0, len(checkins) - 1)
        target_checkin = checkins[random_index]

        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_accepted']
        form['accepted-article'] = target_checkin.article.pk
        response = form.submit()
        response_partial = _extract_results_from_body(response.body, extract_accepted=True)
        context_checkins = response.context['checkins_accepted'].object_list

        self.assertEqual(len(context_checkins), 1)
        self.assertEqual(target_checkin, context_checkins[0])
        self.assertTrue(u'%s' % target_checkin.article.article_title in response_partial)

    def tests_filter_accepted_by_issue_label(self):
        """
        Creates various (accepted) checkins and apply a filter by
        (a random existing) issue label
        """
        checkins = self._make_N_checkins(checkins_accepted=True)
        random_index = randint(0, len(checkins) - 1)
        target_checkin = checkins[random_index]

        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_accepted']
        form['accepted-issue_label'] = target_checkin.article.issue_label
        response = form.submit()
        response_partial = _extract_results_from_body(response.body, extract_accepted=True)
        context_checkins = response.context['checkins_accepted'].object_list

        self.assertEqual(len(context_checkins), 1)
        self.assertEqual(target_checkin, context_checkins[0])
        self.assertTrue(u'%s' % target_checkin.package_name in response_partial)

    # Tests filtering with non-existent checkins

    # Pendings:

    def tests_filter_non_existing_pending_by_package_name(self):
        """
        Creates various (pending) checkins and apply a filter by
        (a random existing) package name
        """
        checkins = self._make_N_checkins()
        target_package_name = '9999.zip'
        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_pending']
        form['pending-package_name'] = target_package_name
        response = form.submit()
        response_partial = _extract_results_from_body(response.body)
        context_checkins = response.context['checkins_pending'].object_list

        self.assertEqual(len(context_checkins), 0)
        self.assertFalse(u'%s' % target_package_name in response_partial)

    def tests_filter_non_existing_pending_by_issue_label(self):
        """
        Creates various (pending) checkins and apply a filter by
        (a random existing) issue label
        """
        checkins = self._make_N_checkins()
        target_issue_label = '1999 v.99 n.9'
        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_pending']
        form['pending-issue_label'] = target_issue_label
        response = form.submit()
        response_partial = _extract_results_from_body(response.body)
        context_checkins = response.context['checkins_pending'].object_list

    # accepted:

    def tests_filter_non_existing_accepted_by_package_name(self):
        """
        Creates various (accepted) checkins and apply a filter by
        (a random existing) package name
        """
        checkins = self._make_N_checkins()
        target_package_name = '9999.zip'
        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_accepted']
        form['accepted-package_name'] = target_package_name
        response = form.submit()
        response_partial = _extract_results_from_body(response.body)
        context_checkins = response.context['checkins_accepted'].object_list

        self.assertEqual(len(context_checkins), 0)
        self.assertFalse(u'%s' % target_package_name in response_partial)

    def tests_filter_non_existing_accepted_by_issue_label(self):
        """
        Creates various (accepted) checkins and apply a filter by
        (a random existing) issue label
        """
        checkins = self._make_N_checkins()
        target_issue_label = '1999 v.99 n.9'
        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_accepted']
        form['accepted-issue_label'] = target_issue_label
        response = form.submit()
        response_partial = _extract_results_from_body(response.body)
        context_checkins = response.context['checkins_accepted'].object_list

        self.assertEqual(len(context_checkins), 0)
        self.assertFalse(u'%s' % target_issue_label in response_partial)

        self.assertEqual(len(context_checkins), 0)
        self.assertFalse(u'%s' % target_issue_label in response_partial)