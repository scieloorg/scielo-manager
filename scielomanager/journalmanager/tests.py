# coding: utf-8
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse

from scielomanager.journalmanager import tests_assets
from scielomanager.journalmanager.models import Collection
from scielomanager.journalmanager.models import Journal
from scielomanager.journalmanager.models import Publisher
from scielomanager.journalmanager.models import Issue

from scielomanager.journalmanager.forms import JournalForm

def with_sample_journal(func):
    """
    Decorator that creates a sample Journal instance
    and destructs it at the end of the execution.
    """
    def decorated(self=None):
        self._create_journal()
        func(self)
        self._destroy_journal()
    return decorated

def with_sample_issue(func):
    """
    Decorator that creates a sample Journal instance
    and destructs it at the end of the execution.
    """
    def decorated(self=None):
        self._create_issue()
        func(self)
        self._destroy_issue()
    return decorated


class LoggedInViewsTest(TestCase):
    """
    Tests views that need logged in users.

    The setUp method creates a new user and authenticates with it. If you want
    a journal to be created at the beginning and then be destructed after each
    testcase, decorate your testcase methods with ``with_sample_journal``.
    """

    def setUp(self):
        """
        Creates an authenticated session using a dummy user.
        """

        #add a dummy user
        self.user = tests_assets.get_sample_creator()
        self.collection = tests_assets.get_sample_collection()
        self.user.save()
        self.collection.save()
        self.usercollections = tests_assets.get_sample_usercollections(self.user, self.collection)
        self.usercollections.save()

        self.client = Client()
        self.client.login(username='dummyuser', password='123')

    def _create_journal(self):
        sample_journal = tests_assets.get_sample_journal()
        sample_journal.creator = self.user

        sample_publisher = tests_assets.get_sample_publisher()
        sample_publisher.collection = self.collection
        sample_publisher.save()

        sample_journal.publisher = sample_publisher
        sample_journal.save()
        sample_journal.collections = [self.collection,]

        sample_journal.save()

    def _destroy_journal(self):
        Journal.objects.get(title = u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (S\xe3o Paulo)').delete()

    def _create_issue(self):
        self._create_journal()
        sample_journal = Journal.objects.get(title = u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (S\xe3o Paulo)')
        sample_issue = tests_assets.get_sample_issue()

        sample_issue.journal = sample_journal
        sample_issue.save()

        sample_section = tests_assets.get_sample_section()
        sample_section.journal = sample_journal
        sample_section.save()

    def _destroy_issue(self):
        self._destroy_journal

    def test_add_journal(self):
        #empty form
        response = self.client.get(reverse('journal.add'))
        self.assertEqual(response.status_code, 200)

        sample_publisher = tests_assets.get_sample_publisher()
        sample_publisher.collection = self.collection
        sample_publisher.save()

        sample_uselicense = tests_assets.get_sample_uselicense()
        sample_uselicense.save()

        sample_indexdatabase = tests_assets.get_sample_index_database()
        sample_indexdatabase.save()       

        sample_center = tests_assets.get_sample_center()
        sample_center.collection = self.collection
        sample_center.save()

        response = self.client.post(reverse('journal.add'),
            tests_assets.get_sample_journal_dataform({'journal-publisher': sample_publisher.pk,
                                                     'journal-use_license': sample_uselicense.pk,
                                                     'collection-0-collection': self.usercollections.pk,
                                                     'indexcoverage-0-database': sample_indexdatabase.pk,
                                                     'journal-center': sample_center.pk, }))

        with open('/tmp/debug.html', 'w') as f:
            f.write(response.content)

        self.assertRedirects(response, reverse('journal.index'))

        #edit journal - must be changed
        testing_journal = Journal.objects.get(title = u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)')
        response = self.client.post(reverse('journal.edit', args = (testing_journal.pk,)),
            tests_assets.get_sample_journal_dataform({'journal-title': 'Modified Title',
                                                     'journal-publisher': sample_publisher.pk,
                                                     'journal-use_license': sample_uselicense.pk,
                                                     'indexcoverage-0-database': sample_indexdatabase.pk,
                                                     'collection-0-collection': self.usercollections.pk,
                                                     'journal-center': sample_center.pk, }))

        self.assertRedirects(response, reverse('journal.index'))
        modified_testing_journal = Journal.objects.get(title = 'Modified Title')
        self.assertEqual(testing_journal, modified_testing_journal)

    def test_add_publisher(self):
        #empty form
        response = self.client.get(reverse('publisher.add'))
        self.assertEqual(response.status_code, 200)

        #add publisher - must be added
        response = self.client.post(reverse('publisher.add'),
            tests_assets.get_sample_publisher_dataform({}))

        self.assertRedirects(response, reverse('publisher.index'))

        #edit publisher - must be changed
        testing_publisher = Publisher.objects.get(name = u'Associação Nacional de História - ANPUH')
        response = self.client.post(reverse('publisher.edit', args = (testing_publisher.pk,)),
            tests_assets.get_sample_publisher_dataform({'publisher-name': 'Modified Title',}))

        self.assertRedirects(response, reverse('publisher.index'))
        modified_testing_publisher = Publisher.objects.get(name = 'Modified Title')
        self.assertEqual(testing_publisher, modified_testing_publisher)

    @with_sample_journal
    def test_add_section(self):
        """
        View: add_section
        """
        from models import Journal
        from models import Section
        journal = Journal.objects.all()[0]

        #empty form
        response = self.client.get(reverse('section.add', args=[journal.pk]))
        self.assertEqual(response.status_code, 200)

        #add section
        response = self.client.post(reverse('section.add', args=[journal.pk]),
            tests_assets.get_sample_section_dataform())

        self.assertRedirects(response, reverse('section.index', args=[journal.pk]))

        #edit section
        testing_section = Section.objects.get(title='Artigo Original')
        previous_code = testing_section.code

        response = self.client.post(reverse('section.edit', args=[journal.pk, testing_section.pk]),
            tests_assets.get_sample_section_dataform(title='Modified Original Article',
                                                     code='qwerty'))

        self.assertRedirects(response, reverse('section.index', args=[journal.pk]))
        modified_section = Section.objects.get(title='Modified Original Article')

        self.assertEqual(testing_section, modified_section)
        self.assertEqual(modified_section.code, previous_code) #code must be read-only

    @with_sample_journal
    def test_add_issue(self):
        from models import Journal
        from models import Issue
        journal = Journal.objects.all()[0]

        #empty form
        response = self.client.get(reverse('issue.add', args=[journal.pk]))
        self.assertEqual(response.status_code, 200)

        #add - should work
        sample_license = tests_assets.get_sample_uselicense()
        sample_license.save()

        sample_section = tests_assets.get_sample_section()
        sample_section.journal = journal
        sample_section.save()

        response = self.client.post(reverse('issue.add', args=[journal.pk]),
            tests_assets.get_sample_issue_dataform(section=sample_section.pk,
                                                   use_license=sample_license.pk))

        self.assertRedirects(response, reverse('issue.index', args=[journal.pk]))

        #edit
        journal = Journal.objects.all()[0]

        response = self.client.get(reverse('issue.edit', args=[journal.pk, journal.issue_set.all()[0].pk]))
        self.assertEqual(response.status_code, 200)

    @with_sample_journal
    def test_journal_index(self):
        """
        View: journal_index

        Tests url dispatch and values returned by the view to the template
        """

        response = self.client.get('/journal/')

        #url dispatcher
        self.assertEqual(response.status_code, 200)

        #values passed to template
        self.assertTrue('journals' in response.context)
        self.assertTrue('user_collections' in response.context)

        #testing content
        self.assertEqual(u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)',
            unicode(response.context['journals'].object_list[0].title))
        self.assertTrue(1, len(response.context['journals'].object_list))

    @with_sample_journal
    def test_publisher_index(self):
        """
        View: publisher_index

        Tests url dispatch and values returned by the view to the template
        """
        response = self.client.get('/journal/publisher/')

        #url dispatcher
        self.assertEqual(response.status_code, 200)

        #values passed to template
        self.assertTrue('publishers' in response.context)
        self.assertTrue('user_collections' in response.context)

        #testing content
        self.assertEqual(u'Associação Nacional de História - ANPUH',
            unicode(response.context['publishers'].object_list[0].name))
        self.assertTrue(1, len(response.context['publishers'].object_list))

    @with_sample_journal
    def test_search_journal(self):
        """
        View: search_journal

        Tests url dispatch and values returned by the view to the template
        """
        response = self.client.get('/journal/search/?q=Arquivos')

        #url dispatcher
        self.assertEqual(response.status_code, 200)

        #values passed to template
        self.assertTrue('journals' in response.context)
        self.assertTrue('user_collections' in response.context)

        #testing content
        self.assertEqual(u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)', unicode(response.context['journals'].object_list[0].title))
        self.assertTrue(1, len(response.context['journals'].object_list))

    @with_sample_journal
    def test_search_publisher(self):
        """
        View: search_publisher

        Tests url dispatch and values returned by the view to the template
        """
        response = self.client.get('/journal/publisher/search/?q=Nacional')

        #url dispatcher
        self.assertEqual(response.status_code, 200)

        #values passed to template
        self.assertTrue('publishers' in response.context)
        self.assertTrue('user_collections' in response.context)

        #testing content
        self.assertEqual(u'Associação Nacional de História - ANPUH', unicode(response.context['publishers'].object_list[0].name))
        self.assertTrue(1, len(response.context['publishers'].object_list))

    @with_sample_journal
    def test_toggle_journal_availability(self):
        pre_journal = Journal.objects.all()[0]
        response = self.client.get(reverse('journal.toggle_availability', args=[pre_journal.pk]))
        pos_journal = Journal.objects.all()[0]

        self.assertEqual(pre_journal, pos_journal)
        self.assertRedirects(response, reverse('journal.index'))
        self.assertTrue(pre_journal.is_available is not pos_journal.is_available)

        response = self.client.get(reverse('journal.toggle_availability', args=[9999999]))
        self.assertEqual(response.status_code, 404)

    @with_sample_journal
    def test_toggle_publisher_availability(self):
        pre_publisher = Publisher.objects.all()[0]
        response = self.client.get(reverse('publisher.toggle_availability', args=[pre_publisher.pk]))
        pos_publisher = Publisher.objects.all()[0]

        self.assertEqual(pre_publisher, pos_publisher)
        self.assertRedirects(response, reverse('publisher.index'))
        self.assertTrue(pre_publisher.is_available is not pos_publisher.is_available)

        response = self.client.get(reverse('publisher.toggle_availability', args=[9999999]))
        self.assertEqual(response.status_code, 404)

    @with_sample_issue
    def test_toggle_issue_availability(self):
        pre_issue = Issue.objects.all()[0]
        response = self.client.get(reverse('issue.toggle_availability', args=[pre_issue.pk]))
        pos_issue = Issue.objects.all()[0]

        self.assertEqual(pre_issue, pos_issue)
        self.assertRedirects(response, reverse('issue.index', args=[pre_issue.journal.pk]))
        self.assertTrue(pre_issue.is_available is not pos_issue.is_available)

        response = self.client.get(reverse('issue.toggle_availability', args=[9999999]))
        self.assertEqual(response.status_code, 404)

    @with_sample_journal
    def test_journal_availability_list(self):

        pre_journal = Journal.objects.all()[0]
        response = self.client.get(reverse('journal.index') + '?is_available=1')
        self.assertEqual(response.context['journals'].object_list[0].is_available, True)

        #change object atribute is_available
        pre_journal.is_available = False
        pre_journal.save()

        response = self.client.get(reverse('journal.index') + '?is_available=0')
        self.assertEqual(response.context['journals'].object_list[0].is_available, False)
        self.assertEqual(len(response.context['journals'].object_list), 1)


    @with_sample_journal
    def test_publisher_availability_list(self):

        publisher = Publisher.objects.all()[0]
        response = self.client.get(reverse('publisher.index'))
        self.assertEqual(response.context['publishers'].object_list[0].is_available, True)

        #change atribute is_available
        publisher.is_available = False
        publisher.save()

        response = self.client.get(reverse('publisher.index') + '?is_available=0')
        self.assertEqual(response.context['publishers'].object_list[0].is_available, False)
        self.assertEqual(len(response.context['publishers'].object_list), 1)


    @with_sample_issue
    def test_issue_availability_list(self):

        issue = Issue.objects.all()[0]
        response = self.client.get(reverse('issue.index', args=[issue.journal.pk]))
        self.assertEqual(response.context['issues'].object_list[0].is_available, True)

        #change atribute is_available
        issue.is_available = False
        issue.save()

        response = self.client.get(reverse('issue.index', args=[issue.journal.pk]) + '?is_available=0')
        self.assertEqual(response.context['issues'].object_list[0].is_available, False)
        self.assertEqual(len(response.context['issues'].object_list), 1)

    def test_my_account(self):
        """
        Logged in user accessing his own data management dashboard
        """
        response = self.client.get(reverse('journalmanager.my_account'))
        self.assertEqual(response.status_code, 200)

    def test_password_change(self):
        """
        Logged in user changing its password

        Covered cases:
        * Correct credentials and new password
        * Correct credentials, incorrect new password confirmation
        * Incorrect credentials and correct new password
        """
        response = self.client.get(reverse('journalmanager.password_change'))
        self.assertEqual(response.status_code, 200)

        # correct credentials
        response = self.client.post(reverse('journalmanager.password_change'), {
            'password': '123',
            'new_password': '654321',
            'new_password_again': '654321',
            })
        self.assertRedirects(response, reverse('journalmanager.my_account'))

        # correct credentials, incorrect new password confirmation
        response = self.client.post(reverse('journalmanager.password_change'), {
            'password': '123',
            'new_password': '65',
            'new_password_again': '654321',
            })
        self.assertRedirects(response, reverse('journalmanager.password_change'))

        # incorrect credentials
        response = self.client.post(reverse('journalmanager.password_change'), {
            'password': '123456',
            'new_password': '654321',
            'new_password_again': '654321',
            })
        self.assertRedirects(response, reverse('journalmanager.password_change'))

class LoggedOutViewsTest(TestCase):
    def test_my_account(self):
        """
        Logged out user trying to access a user management dashboard
        """
        response = self.client.get(reverse('journalmanager.my_account'))
        self.assertRedirects(response, reverse('journalmanager.user_login') + '?next=/myaccount/')

    def test_password_change(self):
        """
        Logged out user trying to change its password
        """
        response = self.client.get(reverse('journalmanager.password_change'))
        self.assertRedirects(response, reverse('journalmanager.user_login') + '?next=/myaccount/password/')

class ToolsTest(TestCase):
    def test_paginator_factory(self):
        """
        Function: scielomanager.tools.get_paginated
        """
        from scielomanager.tools import get_paginated

        items_list = [chr(i) for i in range(97, 123)]
        page_num = 1
        items_per_page = 5

        paginated = get_paginated(items_list, page_num, items_per_page=items_per_page)

        self.assertEqual(paginated.paginator.count, 26)
        self.assertEqual(paginated.paginator.num_pages, 6)
        self.assertTrue(hasattr(paginated, 'object_list'))
        self.assertEqual(len(paginated.object_list), 5)

        del(paginated)

        # When requiring a non-existing page, the last one is retrieved
        paginated = get_paginated(items_list, 10, items_per_page=items_per_page)
        self.assertEqual(paginated.number, paginated.paginator.num_pages)

        del(paginated)

        # Testing if page parameter is integer
        paginated = get_paginated(items_list, str(1), items_per_page=items_per_page)

        self.assertEqual(paginated.paginator.count, 26)
        self.assertEqual(paginated.paginator.num_pages, 6)
        self.assertTrue(hasattr(paginated, 'object_list'))
        self.assertEqual(len(paginated.object_list), 5)

        del(paginated)

        # Testing if page parameter is a "string"
        self.assertRaises(TypeError, get_paginated, items_list, 'foo', items_per_page=items_per_page)

class ComponentsTest(TestCase):
    def test_ISSNField_validation(self):

        valid_issns = ['1678-5320','0044-5967','0102-8650','2179-975X','1413-7852','0103-2100',]
        invalid_issns = ['A123-4532','1t23-8979','0900-090900','9827-u982','8992-8u77','1111-111Y',]

        for issn in valid_issns:
            form = JournalForm({'print_issn': issn,})
            self.assertTrue(form.errors.get('print_issn') is None)
            del(form)

        for issn in invalid_issns:
            form = JournalForm({'print_issn': issn,})
            self.assertEqual(form.errors.get('print_issn')[0], u'Enter a valid ISSN.')
            del(form)
