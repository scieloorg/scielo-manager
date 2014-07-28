# coding:utf-8

from random import randint

from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django_factory_boy import auth

from waffle import Flag

from journalmanager.tests.modelfactories import CollectionFactory
from articletrack.tests import modelfactories
from articletrack.tests.tests_models import create_notices

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


def _extract_results_from_body(response, extract_section='pending'):
    """
    Slice the html of response.body to extract the tables with the results of
    applied filters.
    If extract_accepted:
        looks for a table with id="accepted_results"
    else:
        looks for a table with id="pending_results"
    """
    results = response.lxml.xpath('//table[@id="%s_results"]' % extract_section)
    if len(results) > 0:
        return results[0].text_content()
    else:
        return ''


class CheckinListFilterFormTests(WebTest):

    def setUp(self):
        _addWaffleFlag()
        self.user = auth.UserF(is_active=True)
        perm = _makePermission(perm='list_checkin', model='checkin')
        self.user.user_permissions.add(perm)
        self.collection = CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)
        # Producer definition:
        group_producer = auth.GroupF(name='producer')
        self.user.groups.add(group_producer)
        self.user.save()
        # QAL 1 definitions
        self.user_qal_1 = auth.UserF(is_active=True)
        group_qal_1 = auth.GroupF(name='QAL1')
        self.user_qal_1.groups.add(group_qal_1)
        self.user_qal_1.save()
        # QAL 2 definitions
        self.user_qal_2 = auth.UserF(is_active=True)
        group_qal_2 = auth.GroupF(name='QAL2')
        self.user_qal_2.groups.add(group_qal_2)
        self.user_qal_2.save()

    def tearDown(self):
        """
        Restore the default values.
        """

    def _make_N_checkins(self, start=0, end=MAX_CHOICES_QTY, checkins_status='pending'):
        checkins = []
        for x in xrange(start, end):

            new_checkin = modelfactories.CheckinFactory.create()

            # Override the issue_label to get uniques one
            new_checkin.article.issue_label = u'%s%s' % (new_checkin.article.issue_label[:-1], unicode(x))
            new_checkin.article.article_title = u'%s%s' % (new_checkin.article.article_title[:-1], unicode(x))
            new_checkin.article.save()

            # associate the self.collection with the journal to be part of the checkin list
            for journal in new_checkin.article.journals.all():
                journal.join(self.collection, self.user)

            create_notices('ok', new_checkin)  # all notices have error_level as: ok, to proceed
            if checkins_status == 'review' or checkins_status == 'rejected' or checkins_status == 'accepted':
                self.assertTrue(self.user.get_profile().can_send_checkins_to_review)
                new_checkin.send_to_review(self.user)
                # do review by QAL1
                self.assertTrue(self.user_qal_1.get_profile().can_review_l1_checkins)
                new_checkin.do_review_by_level_1(self.user_qal_1)
                # do review by QAL2
                self.assertTrue(self.user_qal_2.get_profile().can_review_l2_checkins)
                new_checkin.do_review_by_level_2(self.user_qal_2)

            if checkins_status == 'rejected':
                rejection_text = 'your checkin is bad, and you should feel bad!'
                self.assertTrue(self.user_qal_1.get_profile().can_reject_checkins)
                new_checkin.do_reject(self.user_qal_1, rejection_text)
            if checkins_status == 'accepted':
                self.assertTrue(self.user_qal_2.get_profile().can_accept_checkins)
                new_checkin.accept(self.user_qal_2)

            checkins.append(new_checkin)

        return checkins

    # PENDING FILTERS

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
        response_partial = _extract_results_from_body(response)
        context_checkins = response.context['checkins_pending'].object_list

        self.assertEqual(len(context_checkins), 1)
        self.assertEqual(target_checkin, context_checkins[0])
        self.assertTrue(u'%s' % target_checkin.package_name in response_partial)

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
        response_partial = _extract_results_from_body(response)
        context_checkins = response.context['checkins_pending'].object_list

        self.assertEqual(len(context_checkins), 1)
        self.assertEqual(target_checkin, context_checkins[0])
        self.assertTrue(u'%s' % target_checkin.article.article_title in response_partial)

    def tests_filter_pending_by_issue_label(self):
        """
        Creates various (pending) checkins and apply a filter by
        (a random existing) issue label
        """
        checkins = self._make_N_checkins()
        random_index = randint(0, len(checkins) - 1)
        target_checkin = checkins[random_index]

        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_pending']
        form['pending-issue_label'] = target_checkin.article.issue_label
        response = form.submit()
        response_partial = _extract_results_from_body(response)
        context_checkins = response.context['checkins_pending'].object_list

        self.assertEqual(len(context_checkins), 1)
        self.assertEqual(target_checkin, context_checkins[0])
        self.assertTrue(u'%s' % target_checkin.package_name in response_partial)

    # REJECTED FILTERS

    def tests_filter_reject_by_package_name(self):
        """
        Creates various (rejected) checkins and apply a filter by
        (a random existing) package name
        """
        checkins = self._make_N_checkins(checkins_status='rejected')

        random_index = randint(0, len(checkins) - 1)
        target_checkin = checkins[random_index]

        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_rejected']
        form['rejected-package_name'] = target_checkin.package_name
        response = form.submit()
        response_partial = _extract_results_from_body(response, extract_section='rejected')
        context_checkins = response.context['checkins_rejected'].object_list

        self.assertEqual(len(context_checkins), 1)
        self.assertEqual(target_checkin, context_checkins[0])
        self.assertTrue(u'%s' % target_checkin.package_name in response_partial)

    def tests_filter_rejected_by_article(self):
        """
        Creates various (rejected) checkins and apply a filter by
        (a random existing) article
        """
        checkins = self._make_N_checkins(checkins_status='rejected')
        random_index = randint(0, len(checkins) - 1)
        target_checkin = checkins[random_index]

        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_rejected']
        form.set('rejected-article', target_checkin.article.pk)
        response = form.submit()
        response_partial = _extract_results_from_body(response, extract_section='rejected')
        context_checkins = response.context['checkins_rejected'].object_list

        self.assertEqual(len(context_checkins), 1)
        self.assertEqual(target_checkin, context_checkins[0])
        self.assertTrue(u'%s' % target_checkin.article.article_title in response_partial)

    def tests_filter_rejected_by_issue_label(self):
        """
        Creates various (rejected) checkins and apply a filter by
        (a random existing) issue label
        """
        checkins = self._make_N_checkins(checkins_status='rejected')
        random_index = randint(0, len(checkins) - 1)
        target_checkin = checkins[random_index]

        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_rejected']
        form['rejected-issue_label'] = target_checkin.article.issue_label
        response = form.submit()
        response_partial = _extract_results_from_body(response, extract_section='rejected')
        context_checkins = response.context['checkins_rejected'].object_list

        self.assertEqual(len(context_checkins), 1)
        self.assertEqual(target_checkin, context_checkins[0])
        self.assertTrue(u'%s' % target_checkin.package_name in response_partial)

    # REVIEW FILTERS

    def tests_filter_review_by_package_name(self):
        """
        Creates various (review) checkins and apply a filter by
        (a random existing) package name
        """
        checkins = self._make_N_checkins(checkins_status='review')

        random_index = randint(0, len(checkins) - 1)
        target_checkin = checkins[random_index]

        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_review']
        form['review-package_name'] = target_checkin.package_name
        response = form.submit()
        response_partial = _extract_results_from_body(response, extract_section='review')
        context_checkins = response.context['checkins_review'].object_list

        self.assertEqual(len(context_checkins), 1)
        self.assertEqual(target_checkin, context_checkins[0])
        self.assertTrue(u'%s' % target_checkin.package_name in response_partial)

    def tests_filter_review_by_article(self):
        """
        Creates various (review) checkins and apply a filter by
        (a random existing) article
        """
        checkins = self._make_N_checkins(checkins_status='review')
        random_index = randint(0, len(checkins) - 1)
        target_checkin = checkins[random_index]

        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_review']
        form.set('review-article', target_checkin.article.pk)
        response = form.submit()
        response_partial = _extract_results_from_body(response, extract_section='review')
        context_checkins = response.context['checkins_review'].object_list

        self.assertEqual(len(context_checkins), 1)
        self.assertEqual(target_checkin, context_checkins[0])
        self.assertTrue(u'%s' % target_checkin.article.article_title in response_partial)

    def tests_filter_review_by_issue_label(self):
        """
        Creates various (review) checkins and apply a filter by
        (a random existing) issue label
        """
        checkins = self._make_N_checkins(checkins_status='review')
        random_index = randint(0, len(checkins) - 1)
        target_checkin = checkins[random_index]

        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_review']
        form['review-issue_label'] = target_checkin.article.issue_label
        response = form.submit()
        response_partial = _extract_results_from_body(response, extract_section='review')
        context_checkins = response.context['checkins_review'].object_list

        self.assertEqual(len(context_checkins), 1)
        self.assertEqual(target_checkin, context_checkins[0])
        self.assertTrue(u'%s' % target_checkin.package_name in response_partial)

    # ACCEPTED FILTERS

    def tests_filter_accepted_by_package_name(self):
        """
        Creates various (accepted) checkins and apply a filter by
        (a random existing) package name
        """
        checkins = self._make_N_checkins(checkins_status='accepted')

        random_index = randint(0, len(checkins) - 1)
        target_checkin = checkins[random_index]

        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_accepted']
        form['accepted-package_name'] = target_checkin.package_name
        response = form.submit()
        response_partial = _extract_results_from_body(response, extract_section='accepted')
        context_checkins = response.context['checkins_accepted'].object_list

        self.assertTrue(len(context_checkins) >= 1)
        self.assertIn(target_checkin, context_checkins)
        self.assertTrue(u'%s' % target_checkin.package_name in response_partial)

    def tests_filter_accepted_by_article(self):
        """
        Creates various (accepted) checkins and apply a filter by
        (a random existing) article
        """
        checkins = self._make_N_checkins(checkins_status='accepted')
        
        random_index = randint(0, len(checkins) - 1)
        target_checkin = checkins[random_index]

        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_accepted']
        form.set('accepted-article', target_checkin.article.pk)
        response = form.submit()
        response_partial = _extract_results_from_body(response, extract_section='accepted')
        context_checkins = response.context['checkins_accepted'].object_list

        self.assertEqual(len(context_checkins), 1)
        self.assertEqual(target_checkin, context_checkins[0])
        self.assertTrue(u'%s' % target_checkin.article.article_title in response_partial)

    def tests_filter_accepted_by_issue_label(self):
        """
        Creates various (accepted) checkins and apply a filter by
        (a random existing) issue label
        """
        checkins = self._make_N_checkins(checkins_status='accepted')
        random_index = randint(0, len(checkins) - 1)
        target_checkin = checkins[random_index]

        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_accepted']
        form['accepted-issue_label'] = target_checkin.article.issue_label
        response = form.submit()
        response_partial = _extract_results_from_body(response, extract_section='accepted')
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
        self._make_N_checkins()
        target_package_name = '9999.zip'
        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_pending']
        form['pending-package_name'] = target_package_name
        response = form.submit()
        response_partial = _extract_results_from_body(response)
        context_checkins = response.context['checkins_pending'].object_list

        self.assertEqual(len(context_checkins), 0)
        self.assertFalse(u'%s' % target_package_name in response_partial)

    def tests_filter_non_existing_pending_by_issue_label(self):
        """
        Creates various (pending) checkins and apply a filter by
        (a random existing) issue label
        """
        self._make_N_checkins()
        target_issue_label = '1999 v.99 n.9'
        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_pending']
        form['pending-issue_label'] = target_issue_label
        response = form.submit()
        response_partial = _extract_results_from_body(response)
        context_checkins = response.context['checkins_pending'].object_list

        self.assertEqual(len(context_checkins), 0)
        self.assertFalse(u'%s' % target_issue_label in response_partial)

    # Review:

    def tests_filter_non_existing_review_by_package_name(self):
        """
        Creates various (review) checkins and apply a filter by
        (a random existing) package name
        """
        self._make_N_checkins(checkins_status='review')
        target_package_name = '9999.zip'
        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_review']
        form['review-package_name'] = target_package_name
        response = form.submit()
        response_partial = _extract_results_from_body(response, extract_section='review')
        context_checkins = response.context['checkins_review'].object_list

        self.assertEqual(len(context_checkins), 0)
        self.assertFalse(u'%s' % target_package_name in response_partial)

    def tests_filter_non_existing_review_by_issue_label(self):
        """
        Creates various (review) checkins and apply a filter by
        (a random existing) issue label
        """
        self._make_N_checkins(checkins_status='review')
        target_issue_label = '1999 v.99 n.9'
        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_review']
        form['review-issue_label'] = target_issue_label
        response = form.submit()
        response_partial = _extract_results_from_body(response, extract_section='review')
        context_checkins = response.context['checkins_review'].object_list

        self.assertEqual(len(context_checkins), 0)
        self.assertFalse(u'%s' % target_issue_label in response_partial)

    # Rejected:

    def tests_filter_non_existing_rejected_by_package_name(self):
        """
        Creates various (rejected) checkins and apply a filter by
        (a random existing) package name
        """
        self._make_N_checkins(checkins_status='rejected')
        target_package_name = '9999.zip'
        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_rejected']
        form['rejected-package_name'] = target_package_name
        response = form.submit()
        response_partial = _extract_results_from_body(response, extract_section='rejected')
        context_checkins = response.context['checkins_rejected'].object_list

        self.assertEqual(len(context_checkins), 0)
        self.assertFalse(u'%s' % target_package_name in response_partial)

    def tests_filter_non_existing_rejected_by_issue_label(self):
        """
        Creates various (rejected) checkins and apply a filter by
        (a random existing) issue label
        """
        self._make_N_checkins(checkins_status='rejected')
        target_issue_label = '1999 v.99 n.9'
        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_rejected']
        form['rejected-issue_label'] = target_issue_label
        response = form.submit()
        response_partial = _extract_results_from_body(response, extract_section='rejected')
        context_checkins = response.context['checkins_rejected'].object_list

        self.assertEqual(len(context_checkins), 0)
        self.assertFalse(u'%s' % target_issue_label in response_partial)

    # accepted:

    def tests_filter_non_existing_accepted_by_package_name(self):
        """
        Creates various (accepted) checkins and apply a filter by
        (a random existing) package name
        """
        self._make_N_checkins(checkins_status='accepted')
        target_package_name = '9999.zip'
        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_accepted']
        form['accepted-package_name'] = target_package_name
        response = form.submit()
        response_partial = _extract_results_from_body(response, extract_section='accepted')
        context_checkins = response.context['checkins_accepted'].object_list

        self.assertEqual(len(context_checkins), 0)
        self.assertFalse(u'%s' % target_package_name in response_partial)

    def tests_filter_non_existing_accepted_by_issue_label(self):
        """
        Creates various (accepted) checkins and apply a filter by
        (a random existing) issue label
        """
        self._make_N_checkins(checkins_status='accepted')
        target_issue_label = '1999 v.99 n.9'
        page = self.app.get(reverse('checkin_index',), user=self.user)
        form = page.forms['filter_accepted']
        form['accepted-issue_label'] = target_issue_label
        response = form.submit()
        response_partial = _extract_results_from_body(response, extract_section='accepted')
        context_checkins = response.context['checkins_accepted'].object_list

        self.assertEqual(len(context_checkins), 0)
        self.assertFalse(u'%s' % target_issue_label in response_partial)

        self.assertEqual(len(context_checkins), 0)
        self.assertFalse(u'%s' % target_issue_label in response_partial)
