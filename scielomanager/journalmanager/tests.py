# coding: utf-8
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse

from journalmanager import tests_assets
from journalmanager.models import Collection
from journalmanager.models import Journal
from journalmanager.models import Publisher
from journalmanager.models import Sponsor
from journalmanager.models import Issue
from journalmanager.models import UserCollections
from journalmanager.models import Section

from journalmanager.forms import JournalForm

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
    Decorator that creates a sample Issue instance
    and destructs it at the end of the execution.
    """
    def decorated(self=None):
        self._create_issue()
        func(self)
        self._destroy_issue()
    return decorated

def with_sample_publisher(func):
    """
    Decorator that creates a sample Publisher instance
    and destructs it at the end of the execution.
    """
    def decorated(self=None):
        self._create_publisher()
        func(self)
        self._destroy_publisher()
    return decorated

def with_sample_sponsor(func):
    """
    Decorator that creates a sample Sponsor instance
    and destructs it at the end of the execution.
    """
    def decorated(self=None):
        self._create_sponsor()
        func(self)
        self._destroy_sponsor()
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

    def tearDown(self):
        """
        Destroying the data
        """
        for m in [Journal, Publisher, Sponsor, Issue, UserCollections, User, Section, Collection]:
            m.objects.all().delete()

    def _create_journal(self):
        sample_journal = tests_assets.get_sample_journal()
        sample_journal.creator = self.user

        sample_publisher = tests_assets.get_sample_publisher()
        sample_publisher.save()
        sample_publisher.collections = [self.collection,]
        sample_publisher.save()

        sample_sponsor = tests_assets.get_sample_sponsor()
        sample_sponsor.save()
        sample_sponsor.collections = [self.collection,]
        sample_sponsor.save()

        sample_use_license = tests_assets.get_sample_uselicense()
        sample_use_license.save()

        sample_journal.use_license = sample_use_license
        sample_journal.pub_status_changed_by = self.user
        sample_journal.save()
        sample_journal.publisher = [sample_publisher,]
        sample_journal.sponsor = [sample_sponsor,]
        sample_journal.save()
        sample_journal.collections = [self.collection,]

        sample_journal.save()

    def _destroy_journal(self):
        pass

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
        pass

    def _create_publisher(self):
        sample_publisher = tests_assets.get_sample_publisher()
        sample_publisher.save()
        sample_publisher.collections = [self.collection]
        sample_publisher.save()

    def _destroy_publisher(self):
        pass

    def _create_sponsor(self):
        sample_sponsor = tests_assets.get_sample_sponsor()
        sample_sponsor.save()
        sample_sponsor.collections = [self.collection]
        sample_sponsor.save()

    def _destroy_sponsor(self):
        pass

    @with_sample_journal
    def test_edit_journal_status(self):
        """
        View: test_edit_journal_status

        Test the feature created to change the journal Status.
        """
        from models import Journal
        from models import Section
        journal = Journal.objects.all()[0]

        # Testing access the status page.
        response = self.client.get(reverse('journal_status.edit', args=[journal.pk]))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('journal_status.edit', args=[journal.pk]), {
            'pub_status': 'deceased',
            'pub_status_reason': 'Motivo 1',
            })
        self.assertRedirects(response, reverse('journal_status.edit', args=[journal.pk]))


    def test_index(self):
        """
        Logged user verify index page
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

        self.assertTrue('user_collections' in response.context)
        self.assertEqual(response.context['user_collections'][0].collection.name, u'SciELO')

    def test_user_index(self):
        """
        Logged user verify list of users
        """
        response = self.client.get(reverse('user.index'))
        self.assertTrue('users' in response.context)
        self.assertEqual(response.context['users'].object_list[0].username, u'dummyuser')
        self.assertEqual(response.context['users'].object_list.count(), 1)

    def test_my_account(self):
        """
        Logged in user accessing his own data management dashboard
        """
        response = self.client.get(reverse('journalmanager.my_account'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset(self):
        """
        Users requesting new password by giving e-mail address

        Covered cases:
        * Validating the reset password interface
        * Given email exists
        * Given email does not exists
        """

        # Validating the reset password interface
        response = self.client.get(reverse('registration.password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u'Enter your e-mail in the form below' in response.content.decode('utf-8'))

        # Testing password recovery against a registered email
        response = self.client.post(reverse('registration.password_reset'), {
            'email': 'dev@scielo.org',
            })
        self.assertRedirects(response, reverse('registration.password_reset_done'))

        # Testing password recovery against a UNregistered email
        response = self.client.post(reverse('registration.password_reset'), {
            'email': 'juca@bala.com',
            })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u'That e-mail address doesn' in response.content.decode('utf-8'))

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


    def test_add_journal(self):
        """
        Covered cases:
        * Accessing the form
        * Submission with missing data
        * Submission with all required data
        * Edition of a existing record
        """
        #empty form
        response = self.client.get(reverse('journal.add'))
        self.assertEqual(response.status_code, 200)

        sample_publisher = tests_assets.get_sample_publisher()
        sample_publisher.collection = self.collection
        sample_publisher.save()

        sample_sponsor = tests_assets.get_sample_sponsor()
        sample_sponsor.collection = self.collection
        sample_sponsor.save()

        sample_uselicense = tests_assets.get_sample_uselicense()
        sample_uselicense.save()

        sample_language = tests_assets.get_sample_language()
        sample_language.save()

        #missing data
        response = self.client.post(reverse('journal.add'),
            tests_assets.get_sample_journal_dataform({'journal-publisher': [sample_publisher.pk],
                                                     'journal-sponsor': [sample_sponsor.pk],
                                                     'journal-collections': [self.usercollections.pk],
                                                     }))

        self.assertTrue('some errors or missing data' in response.content)

        response = self.client.post(reverse('journal.add'),
            tests_assets.get_sample_journal_dataform({'journal-publisher': [sample_publisher.pk],
                                                     'journal-sponsor': [sample_sponsor.pk],
                                                     'journal-use_license': sample_uselicense.pk,
                                                     'journal-collections': [self.usercollections.pk],
                                                     'journal-languages': [sample_language.pk],
                                                     'mission-0-language': sample_language.pk,}))

        self.assertRedirects(response, reverse('journal.index'))

        #edit journal - must be changed
        testing_journal = Journal.objects.get(title = u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)')
        response = self.client.post(reverse('journal.edit', args = (testing_journal.pk,)),
            tests_assets.get_sample_journal_dataform({'journal-title': 'Modified Title',
                                                     'journal-publisher': [sample_publisher.pk],
                                                     'journal-sponsor': [sample_sponsor.pk],
                                                     'journal-use_license': sample_uselicense.pk,
                                                     'journal-collections': [self.usercollections.pk],
                                                     'journal-languages': [sample_language.pk],
                                                     'mission-0-language': sample_language.pk, }))

        self.assertRedirects(response, reverse('journal.index'))
        modified_testing_journal = Journal.objects.get(title = 'Modified Title')
        self.assertEqual(testing_journal, modified_testing_journal)

    def test_add_publisher(self):
        #empty form
        response = self.client.get(reverse('publisher.add'))
        self.assertEqual(response.status_code, 200)

        #add publisher - must be added
        response = self.client.post(reverse('publisher.add'),
            tests_assets.get_sample_publisher_dataform({'publisher-collections': [self.usercollections.pk]}))

        self.assertRedirects(response, reverse('publisher.index'))

        #edit publisher - must be changed
        testing_publisher = Publisher.objects.get(name = u'Associação Nacional de História - ANPUH')
        response = self.client.post(reverse('publisher.edit', args = (testing_publisher.pk,)),
            tests_assets.get_sample_publisher_dataform({'publisher-name': 'Modified Title',
                                                        'publisher-collections': [self.usercollections.pk], }))

        self.assertRedirects(response, reverse('publisher.index'))
        modified_testing_publisher = Publisher.objects.get(name = 'Modified Title')
        self.assertEqual(testing_publisher, modified_testing_publisher)

    def test_add_collection(self):
        '''
        Testing edit the collections contents.

        New collections are not being included by the users. Only in Django admin module.
        '''
        testing_collection = Collection.objects.get(name = u'SciELO')

        #Calling Collection Form
        response = self.client.get(reverse('collection.edit', args = (testing_collection.pk,)))
        self.assertEqual(response.status_code, 200)

        #edit collection - must be changed
        response = self.client.post(reverse('collection.edit', args = (testing_collection.pk,)),
            tests_assets.get_sample_collection_dataform({'collection-name': 'Modified Name', }))

        self.assertRedirects(response, reverse('collection.edit', args = (testing_collection.pk,)))

        modified_testing_collection = Collection.objects.get(name = 'Modified Name')
        self.assertEqual(testing_collection, modified_testing_collection)

    def test_add_sponsor(self):
        #empty form
        response = self.client.get(reverse('sponsor.add'))
        self.assertEqual(response.status_code, 200)

        #add sponsor - must be added
        response = self.client.post(reverse('sponsor.add'),
            tests_assets.get_sample_sponsor_dataform({'sponsor-collections': [self.usercollections.pk]}))

        self.assertRedirects(response, reverse('sponsor.index'))

        #edit sponsor - must be changed
        testing_sponsor = Sponsor.objects.get(name = u'Fundação de Amparo a Pesquisa do Estado de São Paulo')
        response = self.client.post(reverse('sponsor.edit', args = (testing_sponsor.pk,)),
            tests_assets.get_sample_sponsor_dataform({'sponsor-name': 'Modified Title',
                                                        'sponsor-collections': [self.usercollections.pk], }))

        self.assertRedirects(response, reverse('sponsor.index'))
        modified_testing_sponsor = Sponsor.objects.get(name = 'Modified Title')
        self.assertEqual(testing_sponsor, modified_testing_sponsor)

    @with_sample_journal
    def test_add_section(self):
        """
        View: add_section
        """
        from models import Journal
        from models import Section
        journal = Journal.objects.all()[0]

        sample_language = tests_assets.get_sample_language()
        sample_language.save()

        journal.languages.add(sample_language)

        #empty form
        response = self.client.get(reverse('section.add', args=[journal.pk]))
        self.assertEqual(response.status_code, 200)

        #add section
        response = self.client.post(reverse('section.add', args=[journal.pk]),
            tests_assets.get_sample_section_dataform(**{
                    'journal': journal.pk,
                    'titles-0-language': sample_language.pk,
                }))
        self.assertRedirects(response, reverse('section.index', args=[journal.pk]))

        #edit section
        testing_section = Section.objects.get(sectiontitle__title='TITLES FORMSET TEST')
        previous_code = testing_section.code

        response = self.client.post(reverse('section.edit', args=[journal.pk, testing_section.pk]),
            tests_assets.get_sample_section_dataform(**{
                'titles-0-title':'Modified Original Article',
                'titles-0-language': sample_language.pk,
                'code': 'qwerty'}))

        self.assertRedirects(response, reverse('section.index', args=[journal.pk]))
        modified_section = Section.objects.get(sectiontitle__title='Modified Original Article')

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

        sample_section = tests_assets.get_sample_section()
        sample_section.journal = journal
        sample_section.save()

        sample_language = tests_assets.get_sample_language()
        sample_language.save()
        response = self.client.post(reverse('issue.add', args=[journal.pk]),
            tests_assets.get_sample_issue_dataform({'section':sample_section.pk,
                                                    'use_license': journal.use_license.pk,
                                                    'title-0-language':sample_language.pk,}))

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
        self.assertTrue('objects_journal' in response.context)
        self.assertTrue('user_collections' in response.context)

        #testing content
        self.assertEqual(u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)',
            unicode(response.context['objects_journal'].object_list[0].title))
        self.assertTrue(1, len(response.context['objects_journal'].object_list))

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
        self.assertTrue('objects_publisher' in response.context)
        self.assertTrue('user_collections' in response.context)

        #testing content
        self.assertEqual(u'Associação Nacional de História - ANPUH',
            unicode(response.context['objects_publisher'].object_list[0].name))
        self.assertTrue(1, len(response.context['objects_publisher'].object_list))

    @with_sample_journal
    def test_sponsor_index(self):
        """
        View: sponsor_index

        Tests url dispatch and values returned by the view to the template
        """
        response = self.client.get('/journal/sponsor/')

        #url dispatcher
        self.assertEqual(response.status_code, 200)

        #values passed to template
        self.assertTrue('objects_sponsor' in response.context)
        self.assertTrue('user_collections' in response.context)

        #testing content
        self.assertEqual(u'Fundação de Amparo a Pesquisa do Estado de São Paulo',
            unicode(response.context['objects_sponsor'].object_list[0].name))
        self.assertTrue(1, len(response.context['objects_sponsor'].object_list))

    @with_sample_journal
    def test_search_journal(self):
        """
        View: search_journal

        Tests url dispatch and values returned by the view to the template
        """
        response = self.client.get(reverse('journal.index') + '?q=Arquivos')

        #url dispatcher
        self.assertEqual(response.status_code, 200)

        #values passed to template
        self.assertTrue('objects_journal' in response.context)
        self.assertTrue('user_collections' in response.context)

        #testing content
        self.assertEqual(u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)', unicode(response.context['objects_journal'].object_list[0].title))
        self.assertTrue(1, len(response.context['objects_journal'].object_list))

    @with_sample_journal
    def test_search_publisher(self):
        """
        View: search_publisher

        Tests url dispatch and values returned by the view to the template
        """
        response = self.client.get(reverse('publisher.index') + '?q=Nacional')

        #url dispatcher
        self.assertEqual(response.status_code, 200)

        # #values passed to template
        self.assertTrue('objects_publisher' in response.context)
        self.assertTrue('user_collections' in response.context)

        # #testing content
        self.assertEqual(u'Associação Nacional de História - ANPUH', unicode(response.context['objects_publisher'].object_list[0].name))
        self.assertTrue(1, len(response.context['objects_publisher'].object_list))

    @with_sample_journal
    def test_search_sponsor(self):
        """
        View: search_sponsor

        Tests url dispatch and values returned by the view to the template
        """
        response = self.client.get(reverse('sponsor.index') + '?q=Amparo')

        #url dispatcher
        self.assertEqual(response.status_code, 200)

        # #values passed to template
        self.assertTrue('objects_sponsor' in response.context)
        self.assertTrue('user_collections' in response.context)

        # #testing content
        self.assertEqual(u'Fundação de Amparo a Pesquisa do Estado de São Paulo', unicode(response.context['objects_sponsor'].object_list[0].name))
        self.assertTrue(1, len(response.context['objects_sponsor'].object_list))

    @with_sample_journal
    def test_toggle_publisher_availability(self):
        pre_publisher = Publisher.objects.all()[0]
        response = self.client.get(reverse('publisher.toggle_availability', args=[pre_publisher.pk]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        pos_publisher = Publisher.objects.all()[0]

        self.assertEqual(pre_publisher, pos_publisher)
        self.assertTrue(pre_publisher.is_trashed is not pos_publisher.is_trashed)

        response = self.client.get(reverse('publisher.toggle_availability', args=[9999999]))
        self.assertEqual(response.status_code, 400)

    @with_sample_journal
    def test_toggle_sponsor_availability(self):
        pre_sponsor = Sponsor.objects.all()[0]
        response = self.client.get(reverse('sponsor.toggle_availability', args=[pre_sponsor.pk]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        pos_sponsor = Sponsor.objects.all()[0]

        self.assertEqual(pre_sponsor, pos_sponsor)
        self.assertTrue(pre_sponsor.is_trashed is not pos_sponsor.is_trashed)

        response = self.client.get(reverse('sponsor.toggle_availability', args=[9999999]))
        self.assertEqual(response.status_code, 400)

    @with_sample_issue
    def test_toggle_issue_availability(self):
        pre_issue = Issue.objects.all()[0]
        response = self.client.get(reverse('issue.toggle_availability', args=[pre_issue.pk]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        pos_issue = Issue.objects.all()[0]

        self.assertEqual(pre_issue, pos_issue)
        self.assertTrue(pre_issue.is_trashed is not pos_issue.is_trashed)

        response = self.client.get(reverse('issue.toggle_availability', args=[9999999]))
        self.assertEqual(response.status_code, 400)

    def test_toggle_user_availability(self):
        pre_user = User.objects.all()[0]
        response = self.client.get(reverse('user.toggle_availability', args=[pre_user.pk]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        pos_user = User.objects.all()[0]

        self.assertEqual(pre_user, pos_user)
        self.assertTrue(pre_user.is_active is not pos_user.is_active)

        response = self.client.get(reverse('user.toggle_availability', args=[9999999]))
        self.assertEqual(response.status_code, 400)

    @with_sample_publisher
    def test_publisher_availability_list(self):
        publisher = Publisher.objects.all()[0]

        response = self.client.get(reverse('publisher.index'))
        for pub in response.context['objects_publisher'].object_list:
            self.assertEqual(pub.is_trashed, False)

        #change atribute is_available
        publisher.is_trashed = True
        publisher.save()

        response = self.client.get(reverse('publisher.index') + '?is_available=0')
        self.assertEqual(len(response.context['objects_publisher'].object_list), 0)

    @with_sample_sponsor
    def test_sponsor_availability_list(self):
        sponsor = Sponsor.objects.all()[0]
        response = self.client.get(reverse('sponsor.index'))
        for spr in response.context['objects_sponsor'].object_list:
            self.assertEqual(spr.is_trashed, False)

        #change atribute is_available
        sponsor.is_trashed = True
        sponsor.save()

        response = self.client.get(reverse('sponsor.index') + '?is_available=0')
        self.assertEqual(len(response.context['objects_sponsor'].object_list), 0)


    @with_sample_issue
    def test_issue_availability_list(self):

        first_issue = Issue.objects.all()[0]
        response = self.client.get(reverse('issue.index', args=[first_issue.journal.pk]))

        for year, volumes in response.context['issue_grid'].items():
            for volume, issues in volumes.items():
                for issue in issues:
                    self.assertEqual(issue.is_trashed, False)

        #change atribute is_available
        first_issue.is_trashed = True
        first_issue.save()

        response = self.client.get(reverse('issue.index', args=[first_issue.journal.pk]) + '?is_available=0')

        for year, volumes in response.context['issue_grid'].items():
            for volume, issues in volumes.items():
                for issue in issues:
                    self.assertEqual(issue.is_trashed, True)

    def test_contextualized_collection_field_on_add_journal(self):
        """
        A user has a manytomany relation to Collection entities. So, when a
        user is registering a new Journal, he can only bind that Journal to
        the Collections he relates to.

        Covered cases:
        * Check if all collections presented on the form are related to the
          user.
        """
        from journalmanager.views import get_user_collections
        response = self.client.get(reverse('journal.add'))
        self.assertEqual(response.status_code, 200)

        user_collections = [collection.collection for collection in get_user_collections(self.user.pk)]

        for qset_item in response.context['add_form'].fields['collections'].queryset:
            self.assertTrue(qset_item in user_collections)

    def test_contextualized_collection_field_on_add_publisher(self):
        """
        A user has a manytomany relation to Collection entities. So, when a
        user is registering a new Publisher, he can only bind it to
        the Collections he relates to.

        Covered cases:
        * Check if all collections presented on the form are related to the
          user.
        """
        from journalmanager.views import get_user_collections
        response = self.client.get(reverse('publisher.add'))
        self.assertEqual(response.status_code, 200)

        user_collections = [collection.collection for collection in get_user_collections(self.user.pk)]

        for qset_item in response.context['add_form'].fields['collections'].queryset:
            self.assertTrue(qset_item in user_collections)


    def test_contextualized_collection_field_on_add_sponsor(self):
        """
        A user has a manytomany relation to Collection entities. So, when a
        user is registering a new Sponsor, he can only bind it to
        the Collections he relates to.

        Covered cases:
        * Check if all collections presented on the form are related to the
          user.
        """
        from journalmanager.views import get_user_collections
        response = self.client.get(reverse('sponsor.add'))
        self.assertEqual(response.status_code, 200)

        user_collections = [collection.collection for collection in get_user_collections(self.user.pk)]

        for qset_item in response.context['add_form'].fields['collections'].queryset:
            self.assertTrue(qset_item in user_collections)

    @with_sample_journal
    def test_contextualized_language_field_on_add_section(self):
        """
        A user has a manytomany relation to Collection entities. So, when a
        user is registering a new Section, he can only bind it to
        the Collections he relates to.

        Covered cases:
        * Check if all collections presented on the form are related to the
          user.
        """
        from models import Journal
        journal = Journal.objects.all()[0]

        sample_language = tests_assets.get_sample_language()
        sample_language.save()

        journal.languages.add(sample_language)

        response = self.client.get(reverse('section.add', args=[journal.pk]))
        self.assertEqual(response.status_code, 200)

        for qset_item in response.context['section_title_formset'].forms[0].fields['language'].queryset:
            self.assertTrue(qset_item in journal.languages.all())

    @with_sample_journal
    def test_journal_trash(self):
        from journalmanager.views import get_user_collections
        response = self.client.get(reverse('trash.listing'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['trashed_docs'].object_list), 0)

        journal = Journal.objects.all()[0]
        journal.is_trashed = True
        journal.save()

        response = self.client.get(reverse('trash.listing'))
        self.assertEqual(len(response.context['trashed_docs'].object_list), 1)


class JournalRestAPITest(TestCase):
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

    def tearDown(self):
        """
        Destroying the data
        """
        for m in [Journal, Publisher, Sponsor, Issue, UserCollections, User, Section, Collection]:
            m.objects.all().delete()

    def _makeOne(self):
        sample_journal = tests_assets.get_sample_journal()
        sample_journal.creator = self.user

        sample_publisher = tests_assets.get_sample_publisher()
        sample_publisher.save()
        sample_publisher.collections = [self.collection,]
        sample_publisher.save()

        sample_sponsor = tests_assets.get_sample_sponsor()
        sample_sponsor.save()
        sample_sponsor.collections = [self.collection,]
        sample_sponsor.save()

        sample_use_license = tests_assets.get_sample_uselicense()
        sample_use_license.save()

        sample_journal.use_license = sample_use_license
        sample_journal.pub_status_changed_by = self.user
        sample_journal.save()
        sample_journal.publisher = [sample_publisher,]
        sample_journal.sponsor = [sample_sponsor,]
        sample_journal.save()
        sample_journal.collections = [self.collection,]

        sample_journal.save()
        return sample_journal

    def test_journal_index(self):
        import json

        journal = self._makeOne()

        response = self.client.get(reverse('api_v1_journal.index',
            args=[self.collection.name_slug]))
        self.assertEqual(response.status_code, 200)

        response_as_py = json.loads(response.content)
        self.assertEqual(len(response_as_py), 1)

        expected_fields = ('title', 'collections','publisher', 'sponsor', 'previous_title',
        'use_license', 'languages', 'title_iso', 'short_title', 'acronym', 'scielo_issn',
        'print_issn', 'eletronic_issn', 'subject_descriptors', 'init_year', 'init_vol',
        'init_num', 'final_year', 'final_vol', 'final_num', 'frequency', 'pub_status',
        'editorial_standard', 'ctrl_vocabulary', 'pub_level', 'secs_code', 'copyrighter',
        'url_online_submission', 'url_journal', 'index_coverage', 'cover', 'other_previous_title',
    )
        for field in response_as_py[0]:
            self.assertTrue(field in expected_fields)
            if field in ('collections', 'publisher', 'sponsor', 'languages'):
                self.assertTrue(isinstance(response_as_py[0][field], list))
            elif field in ('use_license',):
                self.assertTrue(isinstance(response_as_py[0][field], dict))


    def test_journal_getone(self):
        import json

        journal = self._makeOne()

        response = self.client.get(reverse('api_v1_journal.getone',
            args=[self.collection.name_slug, journal.print_issn]))
        self.assertEqual(response.status_code, 200)

        response_as_py = json.loads(response.content)

        expected_fields = ('title', 'collections','publisher', 'sponsor', 'previous_title',
        'use_license', 'languages', 'title_iso', 'short_title', 'acronym', 'scielo_issn',
        'print_issn', 'eletronic_issn', 'subject_descriptors', 'init_year', 'init_vol',
        'init_num', 'final_year', 'final_vol', 'final_num', 'frequency', 'pub_status',
        'editorial_standard', 'ctrl_vocabulary', 'pub_level', 'secs_code', 'copyrighter',
        'url_online_submission', 'url_journal', 'index_coverage', 'cover', 'other_previous_title',
    )
        for field in response_as_py:
            self.assertTrue(field in expected_fields)
            if field in ('collections', 'publisher', 'sponsor', 'languages'):
                self.assertTrue(isinstance(response_as_py[field], list))
            elif field in ('use_license',):
                self.assertTrue(isinstance(response_as_py[field], dict))
            elif field in ('cover',):
                # instances of FileField
                if not response_as_py.get(field, None):
                    self.assertRaises(ValueError, lambda: getattr(getattr(journal, field), 'url'))
                else:
                    self.assertEqual(getattr(getattr(journal, field), 'url'), response_as_py.get(field, None))
            else:
                #check values for plain attributes
                self.assertEqual(getattr(journal, field, None), response_as_py.get(field, None))

    def test_post_data_index(self):
        response = self.client.post(reverse('api_v1_journal.index',
            args=[self.collection.name_slug]))
        self.assertEqual(response.status_code, 405)

    def test_put_data_index(self):
        response = self.client.put(reverse('api_v1_journal.index',
            args=[self.collection.name_slug]))
        self.assertEqual(response.status_code, 405)

    def test_del_data_index(self):
        response = self.client.delete(reverse('api_v1_journal.index',
            args=[self.collection.name_slug]))
        self.assertEqual(response.status_code, 405)

    def test_post_data_getone(self):
        journal = self._makeOne()
        response = self.client.post(reverse('api_v1_journal.getone',
            args=[self.collection.name_slug, journal.print_issn]))
        self.assertEqual(response.status_code, 405)

    def test_put_data_getone(self):
        journal = self._makeOne()
        response = self.client.put(reverse('api_v1_journal.getone',
            args=[self.collection.name_slug, journal.print_issn]))
        self.assertEqual(response.status_code, 405)

    def test_del_data_getone(self):
        journal = self._makeOne()
        response = self.client.delete(reverse('api_v1_journal.getone',
            args=[self.collection.name_slug, journal.print_issn]))
        self.assertEqual(response.status_code, 405)

class CollectionRestAPITest(TestCase):
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

    def tearDown(self):
        """
        Destroying the data
        """
        for m in [Journal, Publisher, Sponsor, Issue, UserCollections, User, Section, Collection]:
            m.objects.all().delete()

    def _makeOne(self):
        return self.collection

    def test_index(self):
        import json
        collection = self._makeOne()

        response = self.client.get(reverse('api_v1_collection.index'))
        self.assertEqual(response.status_code, 200)
        response_as_py = json.loads(response.content)
        self.assertEqual(len(response_as_py), 1)
        self.assertEqual(response_as_py[0]['name'], collection.name)

        expected_fields = ('name', 'name_slug', 'acronym',
            'address', 'address_number', 'address_complement',
            'city', 'state', 'country', 'zip_code', 'fax',
            'phone', 'url', 'mail',
        )

        for field in response_as_py[0]:
            self.assertTrue(field in expected_fields)
            # compare as unicode strings
            field_value = getattr(collection, field, None)
            if field_value:
                self.assertEqual(field_value.decode('utf-8'),
                    response_as_py[0].get(field, None))

    def test_post_data(self):
        response = self.client.post(reverse('api_v1_collection.index'))
        self.assertEqual(response.status_code, 405)

    def test_put_data(self):
        response = self.client.put(reverse('api_v1_collection.index'))
        self.assertEqual(response.status_code, 405)

    def test_del_data(self):
        response = self.client.delete(reverse('api_v1_collection.index'))
        self.assertEqual(response.status_code, 405)

    def test_getone(self):
        import json
        collection = self._makeOne()

        response = self.client.get(reverse('api_v1_collection.getone',
            args=[collection.name_slug]))
        self.assertEqual(response.status_code, 200)
        response_as_py = json.loads(response.content)
        self.assertEqual(response_as_py['name'], collection.name)

        expected_fields = ('name', 'name_slug', 'acronym',
            'address', 'address_number', 'address_complement',
            'city', 'state', 'country', 'zip_code', 'fax',
            'phone', 'url', 'mail',
        )

        for field in response_as_py:
            self.assertTrue(field in expected_fields)
            # compare as unicode strings
            field_value = getattr(collection, field, None)
            if field_value:
                self.assertEqual(field_value.decode('utf-8'),
                    response_as_py.get(field, None))

    def test_post_data_getone(self):
        collection = self._makeOne()

        response = self.client.post(reverse('api_v1_collection.getone',
            args=[collection.name_slug]))
        self.assertEqual(response.status_code, 405)

    def test_put_data_getone(self):
        collection = self._makeOne()

        response = self.client.put(reverse('api_v1_collection.getone',
            args=[collection.name_slug]))
        self.assertEqual(response.status_code, 405)

    def test_del_data_getone(self):
        collection = self._makeOne()

        response = self.client.delete(reverse('api_v1_collection.getone',
            args=[collection.name_slug]))
        self.assertEqual(response.status_code, 405)

class IssuesRestAPITest(TestCase):
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

    def tearDown(self):
        """
        Destroying the data
        """
        for m in [Journal, Publisher, Sponsor, Issue, UserCollections, User, Section, Collection]:
            m.objects.all().delete()

    def _makeOne(self):
        sample_journal = tests_assets.get_sample_journal()
        sample_journal.creator = self.user

        sample_publisher = tests_assets.get_sample_publisher()
        sample_publisher.save()
        sample_publisher.collections = [self.collection,]
        sample_publisher.save()

        sample_sponsor = tests_assets.get_sample_sponsor()
        sample_sponsor.save()
        sample_sponsor.collections = [self.collection,]
        sample_sponsor.save()

        sample_use_license = tests_assets.get_sample_uselicense()
        sample_use_license.save()

        sample_journal.use_license = sample_use_license
        sample_journal.pub_status_changed_by = self.user
        sample_journal.save()
        sample_journal.publisher = [sample_publisher,]
        sample_journal.sponsor = [sample_sponsor,]
        sample_journal.save()
        sample_journal.collections = [self.collection,]

        sample_journal.save()

        sample_issue = tests_assets.get_sample_issue()

        sample_issue.journal = sample_journal
        sample_issue.save()

        sample_section = tests_assets.get_sample_section()
        sample_section.journal = sample_journal
        sample_section.save()

        return sample_issue

    def test_issue_index(self):
        import json
        issue = self._makeOne()
        name_slug = issue.journal.collections.all()[0].name_slug
        response = self.client.get(reverse('api_v1_issue.index', args=[
            name_slug, issue.journal.print_issn]))
        self.assertEqual(response.status_code, 200)

        response_as_py = json.loads(response.content)
        expected_fields = ('is_marked_up', 'section', 'volume',
            'number', 'is_press_release', 'publication_start_month',
            'publication_end_month', 'publication_year', 'use_license',
            'total_documents', 'ctrl_vocabulary', 'editorial_standard',
            'label',
        )

        for field in response_as_py[0]:
            self.assertTrue(field in expected_fields)

            field_value = getattr(issue, field, None)
            if field_value:
                if field in ['is_marked_up', 'is_press_release']:
                    # boolean
                    self.assertTrue(isinstance(response_as_py[0].get(field, None),
                        bool))
                elif field in ['section',]:
                    # list
                    self.assertTrue(isinstance(response_as_py[0].get(field, None),
                        list))
                elif field in ['total_documents', 'publication_year',
                    'publication_end_month', 'publication_start_month']:
                    self.assertTrue(isinstance(response_as_py[0].get(field, None),
                        int))
                else:
                    # plain text
                    self.assertEqual(field_value.decode('utf-8'),
                        response_as_py[0].get(field, None))

    def test_post_data(self):
        issue = self._makeOne()
        name_slug = issue.journal.collections.all()[0].name_slug
        response = self.client.post(reverse('api_v1_issue.index', args=[
            name_slug, issue.journal.print_issn]))
        self.assertEqual(response.status_code, 405)

    def test_put_data(self):
        issue = self._makeOne()
        name_slug = issue.journal.collections.all()[0].name_slug
        response = self.client.put(reverse('api_v1_issue.index', args=[
            name_slug, issue.journal.print_issn]))
        self.assertEqual(response.status_code, 405)

    def test_del_data(self):
        issue = self._makeOne()
        name_slug = issue.journal.collections.all()[0].name_slug
        response = self.client.delete(reverse('api_v1_issue.index', args=[
            name_slug, issue.journal.print_issn]))
        self.assertEqual(response.status_code, 405)

    def test_issue_getone(self):
        import json
        issue = self._makeOne()
        name_slug = issue.journal.collections.all()[0].name_slug
        response = self.client.get(reverse('api_v1_issue.getone', args=[
            name_slug, issue.journal.print_issn, issue.label]))
        self.assertEqual(response.status_code, 200)

        response_as_py = json.loads(response.content)
        expected_fields = ('is_marked_up', 'section', 'volume',
            'number', 'is_press_release', 'publication_start_month',
            'publication_end_month', 'publication_year', 'use_license',
            'total_documents', 'ctrl_vocabulary', 'editorial_standard',
            'label',
        )

        for field in response_as_py:
            self.assertTrue(field in expected_fields)

            field_value = getattr(issue, field, None)
            if field_value:
                if field in ['is_marked_up', 'is_press_release']:
                    # boolean
                    self.assertTrue(isinstance(response_as_py.get(field, None),
                        bool))
                elif field in ['section',]:
                    # list
                    self.assertTrue(isinstance(response_as_py.get(field, None),
                        list))
                elif field in ['total_documents', 'publication_year',
                    'publication_end_month', 'publication_start_month']:
                    self.assertTrue(isinstance(response_as_py.get(field, None),
                        int))
                else:
                    # plain text
                    self.assertEqual(field_value.decode('utf-8'),
                        response_as_py.get(field, None))

    def test_post_data_getone(self):
        issue = self._makeOne()
        name_slug = issue.journal.collections.all()[0].name_slug
        response = self.client.post(reverse('api_v1_issue.getone',
            args=[name_slug, issue.journal.print_issn, issue.label]))
        self.assertEqual(response.status_code, 405)

    def test_put_data_getone(self):
        issue = self._makeOne()
        name_slug = issue.journal.collections.all()[0].name_slug
        response = self.client.put(reverse('api_v1_issue.getone',
            args=[name_slug, issue.journal.print_issn, issue.label]))
        self.assertEqual(response.status_code, 405)

    def test_del_data_getone(self):
        issue = self._makeOne()
        name_slug = issue.journal.collections.all()[0].name_slug
        response = self.client.delete(reverse('api_v1_issue.getone',
            args=[name_slug, issue.journal.print_issn, issue.label]))
        self.assertEqual(response.status_code, 405)

class SectionsRestAPITest(TestCase):
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

    def tearDown(self):
        """
        Destroying the data
        """
        for m in [Journal, Publisher, Sponsor, Issue, UserCollections, User, Section, Collection]:
            m.objects.all().delete()

    def _makeOne(self):
        sample_journal = tests_assets.get_sample_journal()
        sample_journal.creator = self.user

        sample_publisher = tests_assets.get_sample_publisher()
        sample_publisher.save()
        sample_publisher.collections = [self.collection,]
        sample_publisher.save()

        sample_sponsor = tests_assets.get_sample_sponsor()
        sample_sponsor.save()
        sample_sponsor.collections = [self.collection,]
        sample_sponsor.save()

        sample_use_license = tests_assets.get_sample_uselicense()
        sample_use_license.save()

        sample_journal.use_license = sample_use_license
        sample_journal.pub_status_changed_by = self.user
        sample_journal.save()
        sample_journal.publisher = [sample_publisher,]
        sample_journal.sponsor = [sample_sponsor,]
        sample_journal.save()
        sample_journal.collections = [self.collection,]

        sample_journal.save()

        sample_section = tests_assets.get_sample_section()
        sample_section.journal = sample_journal
        sample_section.save()

        return sample_journal

    def test_section_index(self):
        import json
        journal = self._makeOne()
        name_slug = journal.collections.all()[0].name_slug
        response = self.client.get(reverse('api_v1_section.index', args=[
            name_slug, journal.print_issn]))
        self.assertEqual(response.status_code, 200)

        response_as_py = json.loads(response.content)
        self.assertEqual(len(response_as_py), 1)

        expected_fields = ('sectiontitle_set', 'code',)
        for field in response_as_py[0]:
            if field in ['sectiontitle_set',]:
                self.assertTrue(isinstance(response_as_py[0][field], list))
            else:
                self.assertTrue(field in expected_fields)

    def test_post_data(self):
        journal = self._makeOne()
        name_slug = journal.collections.all()[0].name_slug
        response = self.client.post(reverse('api_v1_section.index', args=[
            name_slug, journal.print_issn]))
        self.assertEqual(response.status_code, 405)

    def test_put_data(self):
        journal = self._makeOne()
        name_slug = journal.collections.all()[0].name_slug
        response = self.client.put(reverse('api_v1_section.index', args=[
            name_slug, journal.print_issn]))
        self.assertEqual(response.status_code, 405)

    def test_del_data(self):
        journal = self._makeOne()
        name_slug = journal.collections.all()[0].name_slug
        response = self.client.delete(reverse('api_v1_section.index', args=[
            name_slug, journal.print_issn]))
        self.assertEqual(response.status_code, 405)

class LoggedOutViewsTest(TestCase):

    def test_index(self):
        """
        Logged out user try access index page
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

        self.assertTrue('SciELO Manager' in response.content)

class UserViewsTest(TestCase):

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

    def test_index(self):
        """
        Logged out user try access index page
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

        self.assertTrue('SciELO Manager' in response.content)

    def test_user_login(self):
        """
        Logged out user try login and verify session
        """
        #Login
        response = self.client.post(reverse('journalmanager.user_login'), {'username': 'dummyuser', 'password': '123', 'next':''})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('journal.index'))
        self.assertEqual(response.status_code, 200)

        #Verify the value of user session
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_user_logout(self):
        """
        Logged out user try login, logout and verify user session
        """
        #Login
        response = self.client.post(reverse('journalmanager.user_login'), {'username': 'dummyuser', 'password': '123', 'next':'/journal/?page=14'})
        self.assertRedirects(response, reverse('journal.index') + '?page=14')

        #Logout
        response = self.client.get(reverse('journalmanager.user_logout'))
        self.assertEqual(response.status_code, 200)

        self.assertTrue('SciELO Manager' in response.content)

        #Verify the value of user session
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_user_login_next(self):
        """
        Logged out user try login with next param and verify user session
        """
        #Login
        response = self.client.post(reverse('journalmanager.user_login'), {'username': 'dummyuser', 'password': '123', 'next':'/journal/?page=14'})
        self.assertRedirects(response, reverse('journal.index') + '?page=14')

        #Verify the value of user session
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_user_login_unactive(self):
        """
        Logged out user try login with is_active=False and verify user session
        """

        self.user.is_active = False
        self.user.save()

        response = self.client.post(reverse('journalmanager.user_login'), {'username': 'dummyuser', 'password': '123', 'next':''})

        #Testing content
        self.assertTrue(u'Your account is not active' in response.content.decode('utf-8'))

        self.user.is_active = True
        self.user.save()

        #Verify the value of user session
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_user_login_failed(self):
        """
        Logged out user try login with password=1234 and verify user session
        """
        response = self.client.post(reverse('journalmanager.user_login'), {'username': 'dummyuser', 'password': '1234', 'next':''})

        #Testing content
        self.assertTrue(u'Your username and password did not match' in response.content.decode('utf-8'))

        #Verify the value of user session
        self.assertFalse('_auth_user_id' in self.client.session)

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


    def test_add_user(self):
        """
        Login and Create user and verify content on database
        """
        client = Client()
        client.login(username='dummyuser', password='123')

        response = client.post(reverse('user.add'), tests_assets.get_sample_user_dataform({
                'usercollections-0-collection': self.usercollections.pk,
                'usercollections-0-is_manager': True,
                'usercollections-0-is_default': True,}))

        self.assertRedirects(response, reverse('user.index'))

        self.assertEqual(str(User.objects.all()[1].username), tests_assets.get_sample_user_dataform()['user-username'])

        self.assertQuerysetEqual(User.objects.all(), [
                "<User: dummyuser>",
                "<User: dummyuser_add>",
              ]
          )

    def test_edit_user(self):
        """
        Login user and Edit user and verify content on database
        """
        client = Client()
        client.login(username='dummyuser', password='123')

        user = User.objects.all()[0]

        response = client.get(reverse('user.edit', args=[user.pk]))
        self.assertEqual(response.context['user'], user)

        response = client.post(reverse('user.edit', args=(user.pk,)),
                tests_assets.get_sample_user_dataform({
                'user-username': 'dummyuser_edit',
                'usercollections-0-collection': self.collection.pk,
                'usercollections-0-is_manager': True,
                'usercollections-0-is_default': True,
                }))

        self.assertRedirects(response, reverse('user.index'))

        user = User.objects.all()[0]

        self.assertEqual(user.username, u'dummyuser_edit')

        self.assertQuerysetEqual(User.objects.all(), [
                "<User: dummyuser_edit>",
              ]
          )

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

class ModelBackendTest(TestCase):
    """
    Testa as especializações de metodos de backend ModelBackend
    """

    def setUp(self):
        #add a dummy user
        self.user = tests_assets.get_sample_creator()
        self.user.save()
        self.profile = tests_assets.get_sample_userprofile(user=self.user)
        self.profile.save()


    def test_authenticate(self):
        """
        test_authentication

        Covered Tests
        1. authenticating user with true username and password
        2. authenticating user with true username and wrong password
        3. authenticating user with true email and password
        4. authenticating user with true email and wrong password
        5. authenticating user with wrong username/email and password
        """
        from scielomanager.journalmanager.backends import ModelBackend

        mbkend = ModelBackend()

        auth_response = mbkend.authenticate('dummyuser','123')
        self.assertEqual(auth_response,self.user)

        auth_response = mbkend.authenticate('dummyuser','fakepasswd')
        self.assertEqual(auth_response,None)

        auth_response = mbkend.authenticate('dev@scielo.org','123')
        self.assertEqual(auth_response,self.user)

        auth_response = mbkend.authenticate('dev@scielo.org','fakepasswd')
        self.assertEqual(auth_response,None)

        auth_response = mbkend.authenticate('fakeuser','fakepasswd')
        self.assertEqual(auth_response,None)
