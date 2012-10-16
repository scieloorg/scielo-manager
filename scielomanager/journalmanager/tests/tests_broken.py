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
                for issue in issues['numbers']:
                    self.assertEqual(issue.is_trashed, False)

        #change atribute is_available
        first_issue.is_trashed = True
        first_issue.save()

        response = self.client.get(reverse('issue.index', args=[first_issue.journal.pk]) + '?is_available=0')

        for year, volumes in response.context['issue_grid'].items():
            for volume, issues in volumes.items():
                for issue in issues['numbers']:
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
        from journalmanager.models import get_user_collections
        response = self.client.get(reverse('journal.add'))
        self.assertEqual(response.status_code, 200)

        user_collections = [collection.collection for collection in get_user_collections(self.user.pk)]

        for qset_item in response.context['add_form'].fields['collection'].queryset:
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
        from journalmanager.models import get_user_collections
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
        from journalmanager.models import Journal
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
        response = self.client.get(reverse('trash.listing'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['trashed_docs'].object_list), 0)

        journal = Journal.objects.all()[0]
        journal.is_trashed = True
        journal.save()

        response = self.client.get(reverse('trash.listing'))
        self.assertEqual(len(response.context['trashed_docs'].object_list), 1)



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

        auth_response = mbkend.authenticate('dummyuser', '123')
        self.assertEqual(auth_response, self.user)

        auth_response = mbkend.authenticate('dummyuser', 'fakepasswd')
        self.assertEqual(auth_response, None)

        auth_response = mbkend.authenticate('dev@scielo.org', '123')
        self.assertEqual(auth_response, self.user)

        auth_response = mbkend.authenticate('dev@scielo.org', 'fakepasswd')
        self.assertEqual(auth_response, None)

        auth_response = mbkend.authenticate('fakeuser', 'fakepasswd')
        self.assertEqual(auth_response, None)
