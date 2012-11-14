# coding: utf-8
from django.test import TestCase
from django_factory_boy import auth
from mocker import (
    MockerTestCase,
    ANY,
    ARGS,
    KWARGS,
)

from .modelfactories import (
    IssueFactory,
    UserProfileFactory,
    SectionFactory,
    LanguageFactory,
    SectionTitleFactory,
    JournalFactory,
    CollectionFactory,
    ArticleFactory,
)


class SectionTests(TestCase):

    def test_section_not_being_used(self):
        section = SectionFactory.build()
        self.assertFalse(section.is_used())

    def test_section_bound_to_a_journal(self):
        issue = IssueFactory.create()
        section = issue.section.all()[0]

        self.assertTrue(section.is_used())

    def test_actual_code_is_the_instance_pk(self):
        section = SectionFactory.create()
        self.assertEqual(section.pk, section.actual_code)

    def test_actual_code_must_raise_attributeerror_for_unsaved_instances(self):
        section = SectionFactory.build()
        self.assertRaises(AttributeError, section.actual_code)

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


class UserProfileTests(TestCase):

    def test_gravatar_id_generation(self):
        profile = UserProfileFactory.build(email='foo@bar.org')
        expected_gravatar_id = '24191827e60cdb49a3d17fb1befe951b'

        self.assertEqual(profile.gravatar_id, expected_gravatar_id)

    def test_gravatar_url(self):
        expected_url = 'https://secure.gravatar.com/avatar/24191827e60cdb49a3d17fb1befe951b?s=18&d=mm'
        profile = UserProfileFactory.build(email='foo@bar.org')

        self.assertEqual(profile.avatar_url, expected_url)


class IssueTests(TestCase):

    def test_identification_for_suppl_volume(self):
        issue = IssueFactory.create(number='1', suppl_volume='2')
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

    def test_identification_for_suppl_number(self):
        issue = IssueFactory.create(number='1', suppl_number='2')
        expected = u'1 suppl.2'

        self.assertEqual(issue.identification, expected)

    def test_identification_for_press_release(self):
        issue = IssueFactory.create(number='1', is_press_release=True)
        expected = u'1 pr'

        self.assertEqual(issue.identification, expected)

    def test_identification_for_ahead(self):
        issue = IssueFactory.create(number='ahead')
        expected = u'ahead of print'

        self.assertEqual(issue.identification, expected)

    def test_identification_for_special(self):
        issue = IssueFactory.create(number='spe')
        expected = u'special'

        self.assertEqual(issue.identification, expected)

    def test_unicode_representation(self):
        issue = IssueFactory.create(volume='2', number='1', suppl_number='2')
        expected = u'2 (1 suppl.2)'

        self.assertEqual(unicode(issue), expected)

    def test_publication_date(self):
        issue = IssueFactory.create()
        expected = '9 / 11 - 2012'

        self.assertEqual(issue.publication_date, expected)

    def test_get_suggested_issue_order_for_first_issue(self):
        issue = IssueFactory.create(publication_year=2012, volume=2)
        self.assertEqual(issue._suggest_order(), 1)

    def test_get_suggested_issue_order_having_multiple_issues(self):
        journal = JournalFactory.create()

        for i in range(1, 6):
            issue = IssueFactory.create(volume=9,
                publication_year=2012, journal=journal)

            self.assertEqual(issue._suggest_order(), i)

    def test_get_suggested_issue_order_having_multiple_years(self):
        journal = JournalFactory.create()

        issue1 = IssueFactory.create(volume=9,
            publication_year=2012, journal=journal)
        issue2 = IssueFactory.create(volume=9,
            publication_year=2011, journal=journal)

        self.assertEqual(issue1._suggest_order(), 1)
        self.assertEqual(issue2._suggest_order(), 1)


class LanguageTests(TestCase):

    def test_the_unicode_repr_must_be_in_current_language(self):
        # todo: learn a good way to change the current language of the app
        # in order to check the unicode value translated.
        language = LanguageFactory.build(name='portuguese')
        self.assertEqual(unicode(language), u'portuguese')


class JournalTests(TestCase):

    def test_changing_publication_status(self):
        user = auth.UserF()
        journal = JournalFactory.create()
        journal.change_publication_status(status=u'deceased',
            reason=u'baz', changed_by=user)

        self.assertEqual(journal.pub_status, u'deceased')
        self.assertEqual(journal.pub_status_reason, u'baz')
        self.assertEqual(journal.pub_status_changed_by, user)

    def test_issues_grid_with_numerical_issue_numbers(self):
        journal = JournalFactory.create()
        for i in range(5):
            journal.issue_set.add(IssueFactory.create(volume=9,
                publication_year=2012))

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
            journal.issue_set.add(IssueFactory.create(volume=9,
                publication_year=2012))

        grid = journal.issues_as_grid(is_available=False)

        self.assertFalse(grid)

    def test_issues_grid_must_be_ordered_by_publication_year_desc(self):
        journal = JournalFactory.create()
        for i in range(5):
            year = 2012 - i
            journal.issue_set.add(IssueFactory.create(volume=9,
                publication_year=year))

        grid = journal.issues_as_grid()
        expected = [2012, 2011, 2010, 2009, 2008]

        self.assertEqual(grid.keys(), expected)

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

        self.assertRaises(ValueError,
            lambda: journal.reorder_issues(expected_order,
                                           volume=9,
                                           publication_year=2012))


class CollectionTests(TestCase):

    def test_collection_as_default_to_user(self):
        collection = CollectionFactory.create()
        collection.make_default_to_user(auth.UserF())

        from journalmanager import models
        collection_ = models.UserCollections.objects.get(is_default=True).collection
        self.assertEqual(collection_, collection)

    def test_collection_is_not_default_to_user(self):
        collection = CollectionFactory.create()
        user = auth.UserF()

        self.assertFalse(collection.is_default_to_user(user))

    def test_collection_is_default_to_user(self):
        user = auth.UserF()
        collection = CollectionFactory.create()
        collection.make_default_to_user(user)

        self.assertTrue(collection.is_default_to_user(user))

    def test_add_user(self):
        user = auth.UserF()
        collection = CollectionFactory.create()
        collection.add_user(user)

        from journalmanager import models
        self.assertTrue(models.UserCollections.objects.get(user=user,
            collection=collection))

    def test_remove_user(self):
        user = auth.UserF()
        collection = CollectionFactory.create()
        collection.add_user(user)

        collection.remove_user(user)

        from journalmanager import models
        self.assertRaises(models.UserCollections.DoesNotExist,
            lambda: models.UserCollections.objects.get(user=user,
                                                       collection=collection)
            )

    def test_remove_user_that_is_not_related_to_the_collection(self):
        user = auth.UserF()
        collection = CollectionFactory.create()

        collection.remove_user(user)

        from journalmanager import models
        self.assertRaises(models.UserCollections.DoesNotExist,
            lambda: models.UserCollections.objects.get(user=user,
                                                       collection=collection)
            )

    def test_collection_is_managed_by_user(self):
        user = auth.UserF()
        collection = CollectionFactory.create()
        collection.add_user(user, is_manager=True)

        self.assertTrue(collection.is_managed_by_user(user))


class CollectionManagerTests(TestCase):

    def test_get_all_by_user(self):
        user = auth.UserF()

        for i in range(5):
            if i % 2:
                CollectionFactory.create()
            else:
                col = CollectionFactory.create()
                col.add_user(user)

        from journalmanager import models
        collections = models.Collection.objects.all_by_user(user)

        self.assertEqual(collections.count(), 3)

    def test_get_default_by_user(self):
        user = auth.UserF()

        col1 = CollectionFactory.create()
        col1.make_default_to_user(user)
        col2 = CollectionFactory.create()
        col2.add_user(user)

        from journalmanager import models
        self.assertEqual(models.Collection.objects.get_default_by_user(user),
            col1)

    def test_get_default_by_user_second_collection(self):
        user = auth.UserF()

        col1 = CollectionFactory.create()
        col1.make_default_to_user(user)
        col2 = CollectionFactory.create()
        col2.make_default_to_user(user)

        from journalmanager import models
        self.assertEqual(models.Collection.objects.get_default_by_user(user),
            col2)

    def test_get_default_by_user_with_two_users(self):
        user1 = auth.UserF()
        user2 = auth.UserF()

        col1 = CollectionFactory.create()
        col1.make_default_to_user(user1)

        col2 = CollectionFactory.create()
        col2.add_user(user1)
        col2.make_default_to_user(user2)

        from journalmanager import models
        self.assertEqual(models.Collection.objects.get_default_by_user(user1),
            col1)
        self.assertEqual(models.Collection.objects.get_default_by_user(user2),
            col2)

    def test_get_first_alphabeticaly_when_default_is_not_set(self):
        user = auth.UserF()

        col1 = CollectionFactory.create()
        col1.add_user(user)
        col2 = CollectionFactory.create()
        col2.add_user(user)

        from journalmanager import models
        self.assertEqual(models.Collection.objects.get_default_by_user(user),
            col1)

    def test_get_default_by_user_must_raise_doesnotexist_if_the_user_has_no_collections(self):
        user = auth.UserF()

        col1 = CollectionFactory.create()

        from journalmanager import models
        self.assertRaises(models.Collection.DoesNotExist,
            lambda: models.Collection.objects.get_default_by_user(user))


class ArticleTests(TestCase, MockerTestCase):

    def test_basic_attribute_access(self):
        article = ArticleFactory.build()
        article.data.title = 'Some title'

        from journalmanager import mongomodels
        self.assertIsInstance(article.data, mongomodels.Article)
        self.assertEqual(article.data.title, 'Some title')

    def test_basic_attribute_save(self):
        import pymongo
        from journalmanager import mongomodels
        article_obj = self.mocker.mock(mongomodels.Article)

        article_obj()
        self.mocker.result(article_obj)

        article_obj.title = 'Some title'

        article_obj.save()
        self.mocker.result('6f1ed002ab5595859014ebf0951522d9')

        self.mocker.replay()

        article = ArticleFactory.build(article_obj=article_obj)
        article.data.title = 'Some title'
        article.save()

        self.assertEqual(article.object_id, '6f1ed002ab5595859014ebf0951522d9')
