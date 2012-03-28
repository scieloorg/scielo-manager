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
from scielomanager.journalmanager.models import Center

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

def with_sample_center(func):
    """
    Decorator that creates a sample Journal instance
    and destructs it at the end of the execution.
    """
    def decorated(self=None):
        self._create_center()
        func(self)
        self._destroy_center()
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

    def _create_center(self):

        sample_center = tests_assets.get_sample_center()
        sample_center.collection = self.collection
        sample_center.save()

    def _destroy_center(self):
        Center.objects.get(name = u'Associação Nacional de História - ANPUH').delete()

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

        sample_uselicense = tests_assets.get_sample_uselicense()
        sample_uselicense.save()

        sample_indexdatabase = tests_assets.get_sample_index_database()
        sample_indexdatabase.save()

        sample_center = tests_assets.get_sample_center()
        sample_center.collection = self.collection
        sample_center.save()

        sample_language = tests_assets.get_sample_language()
        sample_language.save()

        #missing data
        response = self.client.post(reverse('journal.add'),
            tests_assets.get_sample_journal_dataform({'journal-publisher': sample_publisher.pk,
                                                     'journal-collections': [self.usercollections.pk],
                                                     'indexcoverage-0-database': sample_indexdatabase.pk,}))
        self.assertTrue('some errors or missing data' in response.content)


        response = self.client.post(reverse('journal.add'),
            tests_assets.get_sample_journal_dataform({'journal-publisher': sample_publisher.pk,
                                                     'journal-use_license': sample_uselicense.pk,
                                                     'journal-collections': [self.usercollections.pk],
                                                     'indexcoverage-0-database': sample_indexdatabase.pk,
                                                     'journal-center': sample_center.pk,
                                                     'journal-languages': [sample_language.pk], }))

        self.assertRedirects(response, reverse('journal.index'))

        #edit journal - must be changed
        testing_journal = Journal.objects.get(title = u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)')
        response = self.client.post(reverse('journal.edit', args = (testing_journal.pk,)),
            tests_assets.get_sample_journal_dataform({'journal-title': 'Modified Title',
                                                     'journal-publisher': sample_publisher.pk,
                                                     'journal-use_license': sample_uselicense.pk,
                                                     'indexcoverage-0-database': sample_indexdatabase.pk,
                                                     'journal-collections': [self.usercollections.pk],
                                                     'journal-center': sample_center.pk,
                                                     'journal-languages': [sample_language.pk], }))

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

    def test_add_center(self):

        #empty form
        response = self.client.get(reverse('center.add'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('center.add'),
            tests_assets.get_sample_center_dataform({
                'center-collections': [self.usercollections.pk]
                }))

        self.assertRedirects(response, reverse('center.index'))

        response = self.client.get(reverse('center.edit', args=[Center.objects.all()[0].pk]))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('center.edit', args=[Center.objects.all()[0].pk]),
            tests_assets.get_sample_center_dataform({
                'center-name': u'Associação Nacional de História - ANPUH - modified',
                'center-collections': [self.usercollections.pk]
                }))

        self.assertRedirects(response, reverse('center.index'))

        self.assertQuerysetEqual(Center.objects.all(), [
                "<Center: Associação Nacional de História - ANPUH - modified>",
              ]
          )

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

    @with_sample_center
    def test_center_index(self):
        """
        Logged user verify list of centers
        """
        response = self.client.get(reverse('center.index'))
        self.assertTrue('objects_center' in response.context)

        self.assertEqual(response.context['objects_center'].object_list[0].name, u'Associação Nacional de História - ANPUH')
        self.assertEqual(response.context['objects_center'].object_list.count(), 1)


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

    @with_sample_center
    def test_search_center(self):
        """
        View: search_center

        Tests url dispatch and values returned by the view to the template
        """
        response = self.client.get(reverse('center.index') + '?q=Associação')

        #url dispatcher
        self.assertEqual(response.status_code, 200)

        #values passed to template
        self.assertTrue('objects_center' in response.context)

        #testing content
        self.assertEqual(u'Associação Nacional de História - ANPUH', unicode(response.context['objects_center'].object_list[0].name))
        self.assertTrue(1, len(response.context['objects_center'].object_list))

    @with_sample_journal
    def test_toggle_journal_availability(self):
        pre_journal = Journal.objects.all()[0]
        response = self.client.get(reverse('journal.toggle_availability', args=[pre_journal.pk]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        pos_journal = Journal.objects.all()[0]

        self.assertEqual(pre_journal, pos_journal)
        self.assertTrue(pre_journal.is_available is not pos_journal.is_available)

        response = self.client.get(reverse('journal.toggle_availability', args=[9999999]))
        self.assertEqual(response.status_code, 400)

    @with_sample_journal
    def test_toggle_publisher_availability(self):
        pre_publisher = Publisher.objects.all()[0]
        response = self.client.get(reverse('publisher.toggle_availability', args=[pre_publisher.pk]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        pos_publisher = Publisher.objects.all()[0]

        self.assertEqual(pre_publisher, pos_publisher)
        self.assertTrue(pre_publisher.is_available is not pos_publisher.is_available)

        response = self.client.get(reverse('publisher.toggle_availability', args=[9999999]))
        self.assertEqual(response.status_code, 400)

    @with_sample_issue
    def test_toggle_issue_availability(self):
        pre_issue = Issue.objects.all()[0]
        response = self.client.get(reverse('issue.toggle_availability', args=[pre_issue.pk]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        pos_issue = Issue.objects.all()[0]

        self.assertEqual(pre_issue, pos_issue)
        self.assertTrue(pre_issue.is_available is not pos_issue.is_available)

        response = self.client.get(reverse('issue.toggle_availability', args=[9999999]))
        self.assertEqual(response.status_code, 400)

    @with_sample_center
    def test_toggle_center_availability(self):
        pre_center = Center.objects.all()[0]
        response = self.client.get(reverse('center.toggle_availability', args=[pre_center.pk]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        pos_center = Center.objects.all()[0]

        self.assertEqual(pre_center, pos_center)
        self.assertTrue(pre_center.is_available is not pos_center.is_available)

        response = self.client.get(reverse('center.toggle_availability', args=[9999999]))
        self.assertEqual(response.status_code, 400)

    def test_toggle_user_availability(self):
        pre_user = User.objects.all()[0]
        response = self.client.get(reverse('user.toggle_availability', args=[pre_user.pk]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        pos_user = User.objects.all()[0]

        self.assertEqual(pre_user, pos_user)
        self.assertTrue(pre_user.is_active is not pos_user.is_active)

        response = self.client.get(reverse('user.toggle_availability', args=[9999999]))
        self.assertEqual(response.status_code, 400)

    @with_sample_journal
    def test_journal_availability_list(self):

        pre_journal = Journal.objects.all()[0]
        response = self.client.get(reverse('journal.index') + '?is_available=1')
        self.assertEqual(response.context['objects_journal'].object_list[0].is_available, True)

        #change object atribute is_available
        pre_journal.is_available = False
        pre_journal.save()

        response = self.client.get(reverse('journal.index') + '?is_available=0')
        self.assertEqual(response.context['objects_journal'].object_list[0].is_available, False)
        self.assertEqual(len(response.context['objects_journal'].object_list), 1)


    @with_sample_journal
    def test_publisher_availability_list(self):

        publisher = Publisher.objects.all()[0]
        response = self.client.get(reverse('publisher.index'))
        self.assertEqual(response.context['objects_publisher'].object_list[0].is_available, True)

        #change atribute is_available
        publisher.is_available = False
        publisher.save()

        response = self.client.get(reverse('publisher.index') + '?is_available=0')
        self.assertEqual(response.context['objects_publisher'].object_list[0].is_available, False)
        self.assertEqual(len(response.context['objects_publisher'].object_list), 1)

    @with_sample_journal
    def test_bulk_action_availability(self):
        journal = Journal.objects.all()[0]

        response = self.client.get(reverse('journal.index'))
        self.assertEqual(response.context['objects_journal'].object_list[0].is_available, True)

        self.client.post(reverse('journal.bulk_action', args=['is_available', '0']), {'action': journal.id})

        response = self.client.get(reverse('journal.index'))
        self.assertEqual(response.context['objects_journal'].object_list[0].is_available, False)

    @with_sample_issue
    def test_issue_availability_list(self):

        issue = Issue.objects.all()[0]
        response = self.client.get(reverse('issue.index', args=[issue.journal.pk]))
        self.assertEqual(response.context['objects_issue'].object_list[0].is_available, True)

        #change atribute is_available
        issue.is_available = False
        issue.save()

        response = self.client.get(reverse('issue.index', args=[issue.journal.pk]) + '?is_available=0')
        self.assertEqual(response.context['objects_issue'].object_list[0].is_available, False)
        self.assertEqual(len(response.context['objects_issue'].object_list), 1)


    def test_add_user(self):
        """
        Create user and verify content on database
        """
        response = self.client.post(reverse('user.add'), tests_assets.get_sample_user_dataform({
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
        Edit user and verify content on database
        """
        user = User.objects.all()[0]

        response = self.client.get(reverse('user.edit', args=[user.pk]))
        self.assertEqual(response.context['user'], user)

        response = self.client.post(reverse('user.edit', args=(user.pk,)),
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

    def test_contextualized_collection_field_on_add_center(self):
        """
        A user has a manytomany relation to Collection entities. So, when a
        user is registering a new Center, he can only bind it to
        the Collections he relates to.

        Covered cases:
        * Check if all collections presented on the form are related to the
          user.
        """
        from journalmanager.views import get_user_collections
        response = self.client.get(reverse('center.add'))
        self.assertEqual(response.status_code, 200)

        user_collections = [collection.collection for collection in get_user_collections(self.user.pk)]

        for qset_item in response.context['add_form'].fields['collections'].queryset:
            self.assertTrue(qset_item in user_collections)

class LoggedOutViewsTest(TestCase):

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
