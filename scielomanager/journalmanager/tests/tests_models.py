# coding: utf-8
from django.test import TestCase
from mocker import MockerTestCase
from django.utils import unittest
from django_factory_boy import auth
from django.db import IntegrityError

from .modelfactories import (
    ArticleFactory,
    IssueFactory,
    UserProfileFactory,
    UserFactory,
    SectionFactory,
    LanguageFactory,
    SectionTitleFactory,
    JournalFactory,
    CollectionFactory,
    RegularPressReleaseFactory,
)

from scielomanager.utils.modelmanagers.helpers import (
    _makeUserProfile,
    _makeUserRequestContext,
)

from journalmanager import models

HASH_FOR_123 = 'sha1$93d45$5f366b56ce0444bfea0f5634c7ce8248508c9799'


class SectionTests(MockerTestCase):

    def test_section_not_being_used(self):
        section = SectionFactory.build()
        self.assertFalse(section.is_used())

    def test_section_bound_to_a_journal(self):
        issue = IssueFactory.create()
        section = issue.section.all()[0]

        self.assertTrue(section.is_used())

    def test_actual_code_is_the_instance_code(self):
        section = SectionFactory.create()
        self.assertEqual(section.code, section.actual_code)

    def test_actual_code_must_raise_attributeerror_for_unsaved_instances(self):
        section = SectionFactory.build()
        self.assertRaises(AttributeError, lambda: section.actual_code)

    def test_unicode_repr_with_only_one_language(self):
        section_title = SectionTitleFactory.create()
        expected = 'Artigos Originais'

        self.assertEqual(unicode(section_title.section), expected)

    def test_unicode_repr_with_two_languages(self):
        language = LanguageFactory.create(iso_code='en', name='english')
        section_title = SectionTitleFactory.create()
        section_title_en = SectionTitleFactory.build(
            title='Original Articles',
            language=language
        )
        section_title_en.section = section_title.section
        section_title_en.save()

        expected = 'Original Articles / Artigos Originais'

        self.assertEqual(unicode(section_title.section), expected)

    def test_add_title(self):
        section = SectionFactory.create()
        language = LanguageFactory.create(iso_code='en', name='english')
        section.add_title('Original Article', language)

        self.assertEqual(section.titles.all().count(), 1)
        self.assertEqual(section.titles.all()[0].title, 'Original Article')
        self.assertEqual(section.titles.all()[0].language, language)

    def test_suggest_code(self):
        gen = self.mocker.mock()
        gen(4)
        self.mocker.result('XYZW')
        self.mocker.replay()

        section = SectionFactory.create()
        expected_code = '{0}-{1}'.format(section.journal.acronym, 'XYZW')

        self.assertEqual(section._suggest_code(rand_generator=gen), expected_code)


class UserProfileTests(TestCase):

    def test_gravatar_id_generation(self):
        user = UserFactory(username='foo', email='foo@bar.org', password=HASH_FOR_123, is_active=True)
        profile = UserProfileFactory.build(user=user)
        expected_gravatar_id = '24191827e60cdb49a3d17fb1befe951b'

        self.assertEqual(profile.gravatar_id, expected_gravatar_id)

    def test_gravatar_url(self):
        user = UserFactory(username='foo', email='foo@bar.org', password=HASH_FOR_123, is_active=True)
        expected_url = 'https://secure.gravatar.com/avatar/24191827e60cdb49a3d17fb1befe951b?s=18&d=mm'
        profile = UserProfileFactory.build(user=user)

        self.assertEqual(profile.avatar_url, expected_url)

    def test_create_user_must_create_profile(self):
        user = UserFactory(username='foo', password=HASH_FOR_123, is_active=True)
        profile_exists = models.UserProfile.objects.filter(user=user).exists()
        self.assertTrue(profile_exists)


class IssueTests(TestCase):

    def test_identification_for_suppl_text(self):
        issue = IssueFactory.create(number='1', suppl_text='2', type='supplement')
        expected = u'1 suppl.2'

        self.assertEqual(issue.identification, expected)

    def test_identification_for_number(self):
        issue = IssueFactory.create(number='1')
        expected = u'1'

        self.assertEqual(issue.identification, expected)

    def test_identification_for_number_with_sublevels(self):
        issue = IssueFactory.create(number='1a')
        expected = u'1a'

        self.assertEqual(issue.identification, expected)

    def test_identification_for_suppl_text(self):
        issue = IssueFactory.create(number='1', suppl_text='2', type='supplement')
        expected = u'1 suppl.2'

        self.assertEqual(issue.identification, expected)

    def test_identification_for_ahead(self):
        issue = IssueFactory.create(number='ahead')
        expected = u'ahead of print'

        self.assertEqual(issue.identification, expected)

    def test_identification_for_special(self):
        issue = IssueFactory.create(number='1', spe_text='2', type='special')
        expected = u'1 spe.2'

        self.assertEqual(issue.identification, expected)

    def test_unicode_representation(self):
        issue = IssueFactory.create(volume='2', number='1', suppl_text='2', type='supplement')
        expected = u'2 (1 suppl.2)'

        self.assertEqual(unicode(issue), expected)

    def test_publication_date(self):
        issue = IssueFactory.create()
        expected = '9 / 11 - 2012'

        self.assertEqual(issue.publication_date, expected)

    def test_get_suggested_issue_order_for_first_issue(self):
        issue = IssueFactory.create(publication_year=2012, volume='2')
        self.assertEqual(issue._suggest_order(), 1)

    def test_get_suggested_issue_order_with_param_force(self):
        journal = JournalFactory.create()

        issue1 = IssueFactory.create(publication_year=2012, volume='2',
                                     journal=journal)
        issue2 = IssueFactory.create(publication_year=2012, volume='2',
                                     journal=journal)

        self.assertEqual(issue1._suggest_order(force=True), 3)
        issue1.order = issue1._suggest_order(force=True)
        issue1.save()
        self.assertEqual(issue2._suggest_order(force=True), 4)

    def test_get_suggested_issue_order_without_param_force(self):
        journal = JournalFactory.create()

        issue1 = IssueFactory.create(publication_year=2012, volume='2',
                                     journal=journal)
        issue2 = IssueFactory.create(publication_year=2012, volume='2',
                                     journal=journal)

        self.assertEqual(issue1._suggest_order(force=False), 1)
        issue1.order = issue1._suggest_order(force=False)
        issue1.save()
        self.assertEqual(issue2._suggest_order(force=False), 2)

    def test_get_suggested_issue_order_having_multiple_issues(self):
        journal = JournalFactory.create()

        for i in range(1, 6):
            issue = IssueFactory.create(volume='9',
                                        publication_year=2012, journal=journal)

            self.assertEqual(issue._suggest_order(), i)

    def test_get_suggested_issue_order_having_multiple_years(self):
        journal = JournalFactory.create()

        issue1 = IssueFactory.create(volume='9',
                                     publication_year=2012, journal=journal)
        issue2 = IssueFactory.create(volume='9',
                                     publication_year=2011, journal=journal)

        self.assertEqual(issue1._suggest_order(), 1)
        self.assertEqual(issue2._suggest_order(), 1)

    def test_get_suggested_issue_order_on_edit_without_change_publication_year_or_volume(self):
        journal = JournalFactory.create()

        issue1 = IssueFactory.create(volume='9',
                                     publication_year=2012, journal=journal)
        issue2 = IssueFactory.create(volume='9',
                                     publication_year=2012, journal=journal)

        # editing the first issue
        issue1.total_documents = 17
        issue1.save()

        self.assertTrue(issue1.order < issue2.order)

    def test_get_suggested_issue_order_on_edit_change_volume(self):
        journal = JournalFactory.create()

        issue1 = IssueFactory.create(volume='9',
                                     publication_year=2012, journal=journal)
        issue2 = IssueFactory.create(volume='9',
                                     publication_year=2012, journal=journal)
        issue3 = IssueFactory.create(volume='10',
                                     publication_year=2012, journal=journal)

        issue3.volume = '9'
        issue3.save()

        self.assertTrue(issue2.order < issue3.order)
        self.assertEqual(issue3.order, 3)

    def test_get_suggested_issue_order_on_edit_change_publication_year_and_volume(self):
        journal = JournalFactory.create()

        issue1 = IssueFactory.create(volume='9',
                                     publication_year=2012, journal=journal)
        issue2 = IssueFactory.create(volume='9',
                                     publication_year=2012, journal=journal)
        issue3 = IssueFactory.create(volume='9',
                                     publication_year=2012, journal=journal)

        issue4 = IssueFactory.create(volume='10',
                                     publication_year=2013, journal=journal)
        issue5 = IssueFactory.create(volume='10',
                                     publication_year=2013, journal=journal)
        issue6 = IssueFactory.create(volume='10',
                                     publication_year=2013, journal=journal)

        issue6.publication_year = 2012
        issue6.volume = '9'
        issue6.save()

        self.assertTrue(issue3.order < issue6.order)
        self.assertEqual(issue6.order, 4)

    def test_scielo_pid(self):
        journal = JournalFactory.create(print_issn='1234-1234',
                                        scielo_issn='print')
        issue = IssueFactory.create(publication_year=2013,
                                    order=3,
                                    journal=journal)
        expected = '1234-123420130003'

        self.assertEqual(issue.scielo_pid, expected)

    def test_get_suggested_issue_order_multiples_volumes_at_same_year(self):
        """
        Related to https://github.com/scieloorg/SciELO-Manager/issues/553
        """
        journal = JournalFactory.create()

        issue1 = IssueFactory.create(volume='9',
                                     publication_year=2012, journal=journal)
        issue2 = IssueFactory.create(volume='10',
                                     publication_year=2012, journal=journal)

        self.assertEqual(issue1._suggest_order(), 1)
        self.assertEqual(issue2._suggest_order(), 2)

    def test_get_default_use_license(self):
        from journalmanager.models import UseLicense
        issue = IssueFactory.create()
        default_use_license = UseLicense.objects.get(is_default=True)
        self.assertEqual(issue.use_license, default_use_license)


class LanguageTests(TestCase):

    def test_the_unicode_repr_must_be_in_current_language(self):
        # todo: learn a good way to change the current language of the app
        # in order to check the unicode value translated.
        language = LanguageFactory.build(name='portuguese')
        self.assertEqual(unicode(language), u'portuguese')


class JournalTests(TestCase):
    def setUp(self):
        self.user = auth.UserF(username='foo', password=HASH_FOR_123, is_active=True)
        self.collection = CollectionFactory.create()
        _makeUserProfile(self.user)

    def tearDown(self):
        """
        Restore the default values.
        """

    def test_valid_is_editors(self):
        user = auth.UserF()
        journal = JournalFactory.create()

        journal.editors.add(user)

        self.assertTrue(journal.is_editor(user))

    def test_invalid_is_editors(self):
        user = auth.UserF()
        journal = JournalFactory.create()

        self.assertFalse(journal.is_editor(user))

    def test_issues_grid_with_numerical_issue_numbers(self):
        journal = JournalFactory.create()
        for i in range(5):
            journal.issue_set.add(IssueFactory.create(volume=9, publication_year=2012))

        grid = journal.issues_as_grid()

        self.assertTrue(2012 in grid)
        self.assertTrue('9' in grid[2012])
        self.assertEqual(len(grid[2012]['9']), 5)

    def test_issues_grid_with_alphabetical_issue_numbers(self):
        journal = JournalFactory.create()
        for i in range(5):
            if i % 2:
                kwargs = {'volume': 9, 'publication_year': 2012}
            else:
                kwargs = {'volume': 9, 'publication_year': 2012, 'number': 'ahead'}

            journal.issue_set.add(IssueFactory.create(**kwargs))

        grid = journal.issues_as_grid()

        self.assertTrue(2012 in grid)
        self.assertTrue('9' in grid[2012])
        self.assertEqual(len(grid[2012]['9']), 5)

    def test_issues_grid_with_unavailable_issues(self):
        journal = JournalFactory.create()
        for i in range(5):
            journal.issue_set.add(IssueFactory.create(volume=9, publication_year=2012))

        grid = journal.issues_as_grid(is_available=False)

        self.assertFalse(grid)

    def test_issues_grid_must_be_ordered_by_publication_year_desc(self):
        journal = JournalFactory.create()
        for i in range(5):
            year = 2012 - i
            journal.issue_set.add(IssueFactory.create(volume=9, publication_year=year))

        grid = journal.issues_as_grid()
        expected = [2012, 2011, 2010, 2009, 2008]

        self.assertEqual(grid.keys(), expected)

    def test_issues_grid_must_be_ordered_by_volume_desc(self):
        journal = JournalFactory.create()

        for i in range(5):
            volume = 9 - i
            journal.issue_set.add(IssueFactory.create(volume=volume,
                                  publication_year=2012))

        grid = journal.issues_as_grid()
        expected = [u'9', u'8', u'7', u'6', u'5']

        self.assertEqual(grid.values()[0].keys(), expected)

    def test_issues_grid_must_be_ordered_dict(self):
        try:
            from collections import OrderedDict
        except ImportError:
            from ordereddict import OrderedDict

        journal = JournalFactory.create()

        grid = journal.issues_as_grid()

        self.assertIsInstance(grid, OrderedDict)

    @unittest.expectedFailure
    def test_issues_grid_must_be_ordered_by_volume_in_the_same_year(self):
        journal = JournalFactory.create()

        journal.issue_set.add(IssueFactory.create(volume='27', publication_year='2014'))

        journal.issue_set.add(IssueFactory.create(volume='10', publication_year='2014'))

        journal.issue_set.add(IssueFactory.create(volume='9', publication_year='2014'))

        journal.issue_set.add(IssueFactory.create(volume='2', publication_year='2014'))

        grid = journal.issues_as_grid()
        expected = [u'27', u'10', u'9', u'2']

        self.assertEqual(grid.values()[0].keys(), expected)

    def test_journal_has_issues_must_be_true(self):
        journal = JournalFactory.create()
        issues = []
        for i in range(5):
            year = 2012 - i
            issue = IssueFactory.create(volume=9, publication_year=year)
            journal.issue_set.add(issue)

            issues.append(issue.pk)

        self.assertTrue(journal.has_issues(issues))

    def test_journal_has_issues_must_be_false(self):
        journal = JournalFactory.create()
        issues = [666, ]
        for i in range(5):
            year = 2012 - i
            issue = IssueFactory.create(volume=9, publication_year=year)
            journal.issue_set.add(issue)

            issues.append(issue.pk)

        self.assertFalse(journal.has_issues(issues))

    def test_issues_reordering(self):
        journal = JournalFactory.create()
        issues = []
        for i in range(5):
            issue = IssueFactory.create(volume=9, publication_year=2012)
            journal.issue_set.add(issue)

            issues.append(issue.pk)

        issues[2], issues[3] = issues[3], issues[2]  # reordering
        expected_order = issues

        journal.reorder_issues(expected_order, volume=9, publication_year=2012)

        ordered_issues = [issue.pk for issue in journal.issue_set.order_by('order')]

        self.assertEqual(expected_order, ordered_issues)

    def test_issues_reordering_must_accept_pks_as_string(self):
        journal = JournalFactory.create()
        issues = []
        for i in range(5):
            issue = IssueFactory.create(volume=9, publication_year=2012)
            journal.issue_set.add(issue)

            issues.append(issue.pk)

        issues[2], issues[3] = issues[3], issues[2]  # reordering
        expected_order = [str(i_pk) for i_pk in issues]

        journal.reorder_issues(expected_order, volume=9, publication_year=2012)

        ordered_issues = [str(issue.pk) for issue in journal.issue_set.order_by('order')]

        self.assertEqual(expected_order, ordered_issues)

    def test_issues_reordering_lenght_must_match(self):
        journal = JournalFactory.create()
        issues = []
        for i in range(5):
            issue = IssueFactory.create(volume=9, publication_year=2012)
            journal.issue_set.add(issue)

            issues.append(issue.pk)

        expected_order = [1, 2, 4]

        self.assertRaises(
            ValueError,
            lambda: journal.reorder_issues(expected_order,
                                           volume=9,
                                           publication_year=2012))

    def test_scielo_pid_when_print(self):
        journal = JournalFactory.create(scielo_issn=u'print',
                                        print_issn='1234-4321',
                                        eletronic_issn='4321-1234')
        self.assertEqual(journal.scielo_pid, '1234-4321')

    def test_scielo_pid_when_electronic(self):
        journal = JournalFactory.create(scielo_issn=u'electronic',
                                        print_issn='1234-4321',
                                        eletronic_issn='4321-1234')
        self.assertEqual(journal.scielo_pid, '4321-1234')

    def test_get_default_use_license(self):
        from journalmanager.models import UseLicense
        journal = JournalFactory.create()
        default_use_license = UseLicense.objects.get(is_default=True)
        self.assertEqual(journal.use_license, default_use_license)


class CollectionTests(TestCase):
    def setUp(self):
        self.user = auth.UserF(is_active=True)
        self.collection = CollectionFactory.create()
        _makeUserProfile(self.user)

    def tearDown(self):
        """
        Restore the default values.
        """

    def test_collection_as_default_to_user(self):
        self.collection.make_default_to_user(self.user)

        collection = models.UserCollections.objects.get(is_default=True).collection
        self.assertEqual(collection, self.collection)

    def test_collection_is_not_default_to_user(self):
        collection = CollectionFactory.create()
        user = auth.UserF()
        _makeUserProfile(user)
        self.assertFalse(collection.is_default_to_user(user))

    def test_collection_is_default_to_user(self):
        self.collection.make_default_to_user(self.user)

        self.assertTrue(self.collection.is_default_to_user(self.user))

    def test_add_user(self):
        collection = CollectionFactory.create()
        collection.add_user(self.user)

        self.assertTrue(models.UserCollections.objects.get(user=self.user, collection=collection))

    def test_remove_user(self):
        self.collection.add_user(self.user)

        self.collection.remove_user(self.user)

        self.assertRaises(
            models.UserCollections.DoesNotExist,
            lambda: models.UserCollections.objects.get(user=self.user,
                                                       collection=self.collection)
            )

    def test_remove_user_that_is_not_related_to_the_collection(self):
        user = auth.UserF()
        _makeUserProfile(user)
        self.collection.remove_user(user)

        self.assertRaises(
            models.UserCollections.DoesNotExist,
            lambda: models.UserCollections.objects.get(user=user,
                                                       collection=self.collection)
            )

    def test_collection_is_managed_by_user(self):
        self.collection.add_user(self.user, is_manager=True)

        self.assertTrue(self.collection.is_managed_by_user(self.user))


class PressReleaseTests(TestCase):

    def test_add_translation(self):
        issue = IssueFactory()
        language = LanguageFactory.create(iso_code='en', name='english')
        pr = RegularPressReleaseFactory.create(issue=issue)
        pr.add_translation('Breaking news!',
                           'This issue is awesome!',
                           language)

        self.assertEqual(pr.translations.all().count(), 1)
        self.assertEqual(pr.translations.all()[0].title, 'Breaking news!')
        self.assertEqual(pr.translations.all()[0].language, language)

    def test_remove_translation(self):
        issue = IssueFactory()
        language = LanguageFactory.create(iso_code='en', name='english')
        pr = RegularPressReleaseFactory.create(issue=issue)
        pr.add_translation('Breaking news!',
                           'This issue is awesome!',
                           language)

        self.assertEqual(pr.translations.all().count(), 1)

        pr.remove_translation(language)
        self.assertEqual(pr.translations.all().count(), 0)

    def test_remove_translation_with_language_as_iso_code(self):
        issue = IssueFactory()
        language = LanguageFactory.create(iso_code='en', name='english')
        pr = RegularPressReleaseFactory.create(issue=issue)
        pr.add_translation('Breaking news!',
                           'This issue is awesome!',
                           language)

        self.assertEqual(pr.translations.all().count(), 1)

        pr.remove_translation('en')
        self.assertEqual(pr.translations.all().count(), 0)

    def test_remove_translation_with_language_as_pk(self):
        issue = IssueFactory()
        language = LanguageFactory.create(iso_code='en', name='english')
        pr = RegularPressReleaseFactory.create(issue=issue)
        pr.add_translation('Breaking news!',
                           'This issue is awesome!',
                           language)

        self.assertEqual(pr.translations.all().count(), 1)

        pr.remove_translation(language.pk)
        self.assertEqual(pr.translations.all().count(), 0)

    def test_remove_translation_fails_silently_when_translation_doesnt_exists(self):
        issue = IssueFactory()
        language = LanguageFactory.create(iso_code='en', name='english')
        pr = RegularPressReleaseFactory.create(issue=issue)
        pr.add_translation('Breaking news!',
                           'This issue is awesome!',
                           language)

        self.assertEqual(pr.translations.all().count(), 1)

        pr.remove_translation('jp')
        self.assertEqual(pr.translations.all().count(), 1)

    def test_get_trans_method_to_get_translation(self):
        from journalmanager.models import PressReleaseTranslation

        issue = IssueFactory()
        language = LanguageFactory.create(iso_code='en', name='english')
        pr = RegularPressReleaseFactory.create(issue=issue)
        pr.add_translation('Breaking news!',
                           'This issue is awesome!',
                           language)

        self.assertIsInstance(pr.get_trans('en'), PressReleaseTranslation)

    def test_raises_DoesNotExist_if_unknown_iso_code_for_get_trans(self):
        from journalmanager.models import PressReleaseTranslation

        issue = IssueFactory()
        language = LanguageFactory.create(iso_code='en', name='english')
        pr = RegularPressReleaseFactory.create(issue=issue)
        pr.add_translation('Breaking news!',
                           'This issue is awesome!',
                           language)

        self.assertRaises(PressReleaseTranslation.DoesNotExist,
                          lambda: pr.get_trans('jp'))

    def test_add_article(self):
        issue = IssueFactory()
        pr = RegularPressReleaseFactory.create(issue=issue)
        pr.add_article('S0102-311X2013000300003')

        self.assertEqual(pr.articles.all().count(), 1)

    def test_remove_article(self):
        issue = IssueFactory()
        pr = RegularPressReleaseFactory.create(issue=issue)
        pr.add_article('S0102-311X2013000300003')

        self.assertEqual(pr.articles.all().count(), 1)

        pr.remove_article('S0102-311X2013000300003')
        self.assertEqual(pr.articles.all().count(), 0)

    def test_remove_article_fails_silently_when_translation_doesnt_exists(self):
        issue = IssueFactory()
        pr = RegularPressReleaseFactory.create(issue=issue)
        pr.add_article('S0102-311X2013000300003')

        self.assertEqual(pr.articles.all().count(), 1)

        pr.remove_article('S0102-311X201300030000X')
        self.assertEqual(pr.articles.all().count(), 1)


class PressReleaseManagerTests(TestCase):

    def _makeOneElectronic(self):
        j = JournalFactory.create(scielo_issn='electronic',
                                  eletronic_issn='1234-4321')
        i = IssueFactory.create(journal=j)
        return RegularPressReleaseFactory.create(issue=i)

    def _makeOnePrint(self):
        j = JournalFactory.create(scielo_issn='electronic',
                                  eletronic_issn='1234-4321')
        i = IssueFactory.create(journal=j)
        return RegularPressReleaseFactory.create(issue=i)

    def test_by_journal_pid_when_electronic(self):
        pr = self._makeOneElectronic()
        pr2 = RegularPressReleaseFactory.create()

        from journalmanager.models import RegularPressRelease
        self.assertEqual(
            RegularPressRelease.objects.by_journal_pid(pr.issue.journal.print_issn)[0],
            pr
        )

    def test_by_journal_pid_when_print(self):
        pr = self._makeOnePrint()
        pr2 = RegularPressReleaseFactory.create()

        from journalmanager.models import RegularPressRelease
        self.assertEqual(
            RegularPressRelease.objects.by_journal_pid(pr.issue.journal.print_issn)[0],
            pr
        )

    def test_by_journal_pid_returns_an_empty_queryset_for_invalid_pid(self):
        from journalmanager.models import RegularPressRelease
        pr = RegularPressRelease.objects.by_journal_pid('INVALID')
        self.assertQuerysetEqual(pr, [])

    def test_by_issue_pid(self):
        pr = self._makeOnePrint()
        pr2 = RegularPressReleaseFactory.create()

        from journalmanager.models import RegularPressRelease

        result = RegularPressRelease.objects.by_issue_pid(pr.issue.scielo_pid)

        self.assertEqual(
            result[0],
            pr
        )
        self.assertEqual(len(result), 1)


class JournalManagerTests(TestCase):
    def test_by_issn(self):
        journal = JournalFactory.create(print_issn='2398-8734')
        journal2 = JournalFactory.create()

        self.assertEqual(
            models.Journal.objects.by_issn('2398-8734')[0],
            journal
        )


class ArticleTests(TestCase):

    def setUp(self):
        self._issue = IssueFactory.create()
        self._front = {u"title": u"Article Title"}

    def test_add_article(self):
        article = models.Article(
            issue=self._issue,
            front=self._front,
            xml_url=u'http://xml.url.com',
            pdf_url=u'http://pdf.url.com',
            images_url=u'http://img.url.com'
        )

        article.save()

        myarticle = models.Article.objects.all()
        self.assertEqual(len(myarticle), 1)

    def test_article_issue_field(self):
        article = models.Article(
            issue=self._issue,
            front=self._front,
            xml_url=u'http://xml.url.com',
            pdf_url=u'http://pdf.url.com',
            images_url=u'http://img.url.com'
        )

        article.save()

        myarticle = models.Article.objects.all()[0]
        self.assertEqual(myarticle.issue.publication_year, 2012)

    def test_article_front_field(self):
        article = models.Article(
            issue=self._issue,
            front=self._front,
            xml_url=u'http://xml.url.com',
            pdf_url=u'http://pdf.url.com',
            images_url=u'http://img.url.com'
        )

        article.save()

        myarticle = models.Article.objects.all()[0]
        self.assertEqual(myarticle.front['title'], u'Article Title')

    def test_article_xml_url_field(self):
        article = models.Article(
            issue=self._issue,
            front=self._front,
            xml_url=u'http://xml.url.com',
            pdf_url=u'http://pdf.url.com',
            images_url=u'http://img.url.com'
        )

        article.save()

        myarticle = models.Article.objects.all()[0]

        self.assertEqual(myarticle.xml_url, u'http://xml.url.com')

    def test_article_pdf_url_field(self):
        article = models.Article(
            issue=self._issue,
            front=self._front,
            xml_url=u'http://xml.url.com',
            pdf_url=u'http://pdf.url.com',
            images_url=u'http://img.url.com'
        )

        article.save()

        myarticle = models.Article.objects.all()[0]

        self.assertEqual(myarticle.pdf_url, u'http://pdf.url.com')

    def test_article_images_url_field(self):
        article = models.Article(
            issue=self._issue,
            front=self._front,
            xml_url=u'http://xml.url.com',
            pdf_url=u'http://pdf.url.com',
            images_url=u'http://img.url.com'
        )

        article.save()

        myarticle = models.Article.objects.all()[0]

        self.assertEqual(myarticle.images_url, u'http://img.url.com')

    def test_article_mandatory_issue_field(self):
        article = models.Article(
            front=self._front,
            xml_url=u'http://xml.url.com',
            pdf_url=u'http://pdf.url.com',
            images_url=u'http://img.url.com'
        )

        with self.assertRaises(IntegrityError):
            article.save()

    def test_article_mandatory_xml_url_field(self):
        article = models.Article(
            issue=self._issue,
            front=self._front,
            xml_url=None,
            pdf_url=u'http://pdf.url.com',
            images_url=u'http://img.url.com'
        )

        with self.assertRaises(IntegrityError):
            article.save()

    def test_article_mandatory_pdf_url_field(self):
        article = models.Article(
            issue=self._issue,
            front=self._front,
            xml_url=u'http://xml.url.com',
            pdf_url=None,
            images_url=u'http://img.url.com'
        )

        with self.assertRaises(IntegrityError):
            article.save()

    def test_article_mandatory_images_url_field(self):
        article = models.Article(
            issue=self._issue,
            front=self._front,
            xml_url=u'http://xml.url.com',
            pdf_url=u'http://pdf.url.com',
            images_url=None
        )

        with self.assertRaises(IntegrityError):
            article.save()

    def test_article_title_default_language_en(self):
        front = {
            'default-language': 'en',
            'title-group': {
                'en': u'Article Title',
                'pt': u'Título do Artigo',
            }
        }

        article = ArticleFactory.create(issue=self._issue, front=front)

        self.assertEqual(article.title, u'Article Title')

    def test_article_title_default_language_pt(self):
        front = {
            'default-language': 'pt',
            'title-group': {
                'en': u'Article Title',
                'pt': u'Título do Artigo',
            }
        }

        article = ArticleFactory.create(issue=self._issue, front=front)

        self.assertEqual(article.title, u'Título do Artigo')

    def test_article_title_without_data(self):
        article = ArticleFactory.create(issue=self._issue, front={})

        self.assertEqual(article.title, None)

    def test_article_title_default_language_without_data(self):
        front = {
            'title-group': {
                'en': u'Article Title',
                'pt': u'Título do Artigo',
            }
        }

        article = ArticleFactory.create(issue=self._issue, front=front)

        self.assertTrue(article.title in [u'Article Title', u'Título do Artigo'])

    def test_article_title_default_language_without_related_title_data(self):
        front = {
            'default-language': 'xx',
            'title-group': {
                'en': u'Article Title',
                'pt': u'Título do Artigo',
            }
        }

        article = ArticleFactory.create(issue=self._issue, front=front)

        self.assertTrue(article.title in [u'Article Title', u'Título do Artigo'])

    def test_aticle_titles(self):

        article = ArticleFactory.create(issue=self._issue)

        self.assertEqual(article.titles['en'], u'Article Title')
        self.assertEqual(article.titles['pt'], u'Título do Artigo')

    def test_aticle_titles_without_data(self):

        article = ArticleFactory.create(issue=self._issue, front={})

        self.assertEqual(article.titles, None)


class UseLicenseTests(TestCase):

    def test_create_license_and_set_as_default(self):
        license1 = models.UseLicense(license_code='XXX')
        license2 = models.UseLicense(license_code='YYY', is_default=False)
        license3 = models.UseLicense(license_code='ZZZ', is_default=True)

        license1.save()
        self.assertTrue(license1.is_default)

        license2.save()
        # created as not default, and already have one as default
        self.assertFalse(license2.is_default)

        license3.save()
        self.assertTrue(license3.is_default)

    def test_edit_license_and_change_default(self):
        license = models.UseLicense(license_code='XXX')

        license.save()
        self.assertTrue(license.is_default)

        license.is_default = False
        license.save()
        # no other default, so this one will be set as default (forced!)
        self.assertTrue(license.is_default)

        # create a new one as new default
        license2 = models.UseLicense(license_code='YYY', is_default=True)
        license2.save()
        self.assertTrue(license2.is_default)
        #  and then license.is_default must be False
        license = models.UseLicense.objects.get(license_code='XXX')
        self.assertFalse(license.is_default)
