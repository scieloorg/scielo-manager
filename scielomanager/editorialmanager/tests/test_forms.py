# coding: utf-8

from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from journalmanager.tests import modelfactories

from . import modelfactories as editorial_modelfactories
from editorialmanager.models import (EditorialMember,
                                     EditorialBoard,
                                     RoleType,
                                     RoleTypeTranslation)
from audit_log.models import AuditLogEntry, ADDITION, CHANGE, DELETION
from django_countries import countries


def _makePermission(perm, model, app_label='editorialmanager'):
    """
    Retrieves a Permission according to the given model and app_label.
    """
    from django.contrib.contenttypes import models
    from django.contrib.auth import models as auth_models

    ct = models.ContentType.objects.get(model=model, app_label=app_label)
    return auth_models.Permission.objects.get(codename=perm, content_type=ct)


def _add_required_permission_to_group(group):
    # required permissions
    perm_add_editorialmember = _makePermission(perm='add_editorialmember', model='editorialmember')
    perm_change_editorialmember = _makePermission(perm='change_editorialmember', model='editorialmember')
    perm_delete_editorialmember = _makePermission(perm='delete_editorialmember', model='editorialmember')

    group.permissions.add(perm_add_editorialmember)
    group.permissions.add(perm_change_editorialmember)
    group.permissions.add(perm_delete_editorialmember)


class RestrictedJournalFormTests(WebTest):

    def setUp(self):
        # create a group 'Editors'
        group = modelfactories.GroupFactory(name="Editors")

        # create a user and set group 'Editors'
        self.user = modelfactories.UserFactory(is_active=True)
        self.user.groups.add(group)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=False)
        self.collection.make_default_to_user(self.user)

        self.journal = modelfactories.JournalFactory.create()
        self.journal.join(self.collection, self.user)

        # set the user as editor of the journal
        self.journal.editor = self.user
        self.journal.save()

    def test_editor_edit_journal_with_valid_formdata(self):
        """
        When a valid form is submited, the user is redirected to
        the journal's list and the new journal must be part
        of the list.

        In order to take this action, the user needs be part of this group:
        ``superuser`` or ``editors`` or ``librarian`` or ``trainee``
        """

        use_license = modelfactories.UseLicenseFactory.create()

        form = self.app.get(reverse('editorial.journal.edit', args=[self.journal.id, ]), user=self.user).forms['journal-form']

        form['journal-use_license'] = use_license.pk
        form['journal-publisher_name'] = 'Colégio Brasileiro de Cirurgia Digestiva'
        form['journal-publisher_country'] = 'BR'
        form['journal-publisher_state'] = 'SP'
        form['journal-publication_city'] = 'São Paulo'
        form['journal-editor_name'] = 'Colégio Brasileiro de Cirurgia Digestiva'
        form['journal-editor_address'] = 'Av. Brigadeiro Luiz Antonio, 278 - 6° - Salas 10 e 11'
        form['journal-editor_address_city'] = 'São Paulo'
        form['journal-editor_address_state'] = 'SP'
        form['journal-editor_address_zip'] = '01318-901'
        form['journal-editor_address_country'] = 'BR'
        form['journal-editor_phone1'] = '(11) 3288-8174'
        form['journal-editor_phone2'] = '(11) 3289-0741'
        form['journal-editor_email'] = 'cbcd@cbcd.org.br'
        form['journal-is_indexed_scie'] = True
        form['journal-is_indexed_ssci'] = False
        form['journal-is_indexed_aehci'] = True

        response = form.submit().follow()

        self.assertIn('Journal updated successfully.', response.body)

        self.assertIn('ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)', response.body)

        self.assertTemplateUsed(response, 'journal/journal_list.html')


class AddUserAsEditorFormTests(WebTest):

    def setUp(self):

        perm1 = _makePermission(perm='list_editor_journal', model='journal', app_label='journalmanager')
        perm2 = _makePermission(perm='change_editor', model='journal', app_label='journalmanager')

        # create a group 'Librarian'
        group = modelfactories.GroupFactory(name="Librarian")
        group.permissions.add(perm1)
        group.permissions.add(perm2)

        # create a user and set group 'Editors'
        self.user = modelfactories.UserFactory(is_active=True)
        self.user.groups.add(group)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=False)
        self.collection.make_default_to_user(self.user)

        self.journal = modelfactories.JournalFactory.create()
        self.journal.join(self.collection, self.user)

    def test_add_user_as_editor_formdata(self):
        """
        When a valid form is submited, the user is redirected to
        the editor area and journal have a new editor of the journal

        In order to take this action, the user needs be part of this group:
        ``superuser`` or ``librarian`` or ``trainee``
        """

        group = modelfactories.GroupFactory(name="Editors")

        # create a user with group 'Editors'
        user_editor = modelfactories.UserFactory(is_active=True)
        user_editor.groups.add(group)

        form = self.app.get(reverse('editor.add', args=[self.journal.id, ]), user=self.user).forms[0]

        form['editor'] = user_editor.pk

        response = form.submit().follow()

        response.mustcontain('Successfully selected %s as editor of this Journal' % user_editor.get_full_name())


class EditorialMemberFormAsEditorTests(WebTest):

    def setUp(self):
        # create a group 'Editors'
        group = modelfactories.GroupFactory(name="Editors")
        # create a user and set group 'Editors'
        self.user = modelfactories.UserFactory(is_active=True)
        self.user.groups.add(group)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=False)
        self.collection.make_default_to_user(self.user)

        self.journal = modelfactories.JournalFactory.create()
        self.journal.join(self.collection, self.user)

        # set the user as editor of the journal
        self.journal.editor = self.user

        # create an issue
        self.issue = modelfactories.IssueFactory.create()
        self.issue.journal = self.journal
        self.journal.save()
        self.issue.save()

        _add_required_permission_to_group(group)

    def tearDown(self):
        pass

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True, CELERY_ALWAYS_EAGER=True, BROKER_BACKEND='memory')
    def test_ADD_board_member_valid_POST_is_valid(self):
        """
        User of the group "Editors" successfully ADD a new board member
        """

        # with
        role = editorial_modelfactories.RoleTypeFactory.create()
        response = self.app.get(reverse("editorial.board.add", args=[self.journal.id, self.issue.id]), user=self.user)
        pre_submittion_audit_logs_count = AuditLogEntry.objects.all().count()
        # when
        member_data = {
            'role': role,
            'first_name': 'first name',
            'last_name': 'last name',
            'email': 'email@example.com',
            'institution': 'institution name',
            'link_cv': 'http://scielo.org/php/index.php',
            'state': 'SP',
            'country': 'BR',
        }
        # when
        form = response.forms['member-form']
        form.set('role',  member_data['role'].pk)
        form['first_name'] = member_data['first_name']
        form['last_name'] = member_data['last_name']
        form['email'] = member_data['email']
        form['institution'] = member_data['institution']
        form['link_cv'] = member_data['link_cv']
        form['state'] = member_data['state']
        form['country'] = member_data['country']

        response = form.submit().follow()

        # then
        self.assertIn('Board Member created successfully.', response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')

        self.assertIn(member_data['role'].name, response.body)
        self.assertIn(member_data['first_name'], response.body)
        self.assertIn(member_data['last_name'], response.body)
        self.assertIn(member_data['email'], response.body)
        self.assertIn(member_data['institution'], response.body)
        # the link_cv is not displayed in the frontend
        self.assertIn(member_data['state'], response.body)

        self.assertIn(str(dict(countries)[member_data['country']]), response.body)

        # check new member in DB
        members = EditorialMember.objects.filter(
            role=member_data['role'],
            first_name=member_data['first_name'],
            last_name=member_data['last_name'],
            email=member_data['email'],
            institution=member_data['institution'],
            link_cv=member_data['link_cv'],
            state=member_data['state'],
            country=member_data['country'],
        )
        self.assertEqual(len(members), 1)
        # check relations
        self.assertIsNotNone(self.issue.editorialboard)
        self.assertEqual(len(self.issue.editorialboard.editorialmember_set.all()), 1)
        self.assertEqual(members[0].pk, self.issue.editorialboard.editorialmember_set.all()[0].pk)

        # check audit log:
        self.assertEqual(pre_submittion_audit_logs_count, 0)
        audit_entries = AuditLogEntry.objects.all()
        self.assertEqual(audit_entries.count(), 1)
        entry = audit_entries[0]
        self.assertEqual(entry.action_flag, ADDITION)  # Flag correspond with ADDITION action
        self.assertEqual(entry.content_type.model_class(), EditorialMember)
        audited_obj = entry.get_audited_object()
        self.assertEqual(audited_obj._meta.object_name, 'EditorialMember')
        self.assertEqual(audited_obj.pk, members[0].pk)

        self.assertIn(u'Added fields:', entry.change_message)  # message starts with u'Added fields:'
        for field_name in member_data.keys():
            self.assertIn(field_name, entry.change_message)

    def test_ADD_board_member_invalid_POST_is_invalid(self):
        """
        User of the group "Editors" UNsuccessfully ADD a new board member with a invalid email
        """

        # with
        role = editorial_modelfactories.RoleTypeFactory.create()
        response = self.app.get(reverse("editorial.board.add", args=[self.journal.id, self.issue.id]), user=self.user)
        pre_submittion_audit_logs_count = AuditLogEntry.objects.all().count()
        # when
        member_data = {
            'role': role,
            'first_name': 'first name',
            'last_name': 'last name',
            'email': 'email@example.com',
            'institution': 'institution name',
            'link_cv': '@invalid_url/index.php',
            'state': 'SP',
            'country': 'BR',
        }
        # when
        form = response.forms['member-form']
        form.set('role',  member_data['role'].pk)
        form['first_name'] = member_data['first_name']
        form['last_name'] = member_data['last_name']
        form['email'] = member_data['email']
        form['institution'] = member_data['institution']
        form['link_cv'] = member_data['link_cv']
        form['state'] = member_data['state']
        form['country'] = member_data['country']

        response = form.submit()

        # check output
        self.assertTemplateUsed(response, 'board/board_member_edit_form.html')
        self.assertFalse(response.context['form'].is_valid())
        expected_errors = {'link_cv': [u'Enter a valid URL.']}
        self.assertEqual(response.context['form'].errors, expected_errors)
        self.assertIn('Check mandatory fields.', response.body)
        # expected extra context data
        expected_post_url = reverse('editorial.board.add', args=[self.journal.pk, self.issue.pk, ])
        expected_board_url = reverse('editorial.board', args=[self.journal.pk, ])
        self.assertEqual(response.context['post_url'], expected_post_url)
        self.assertEqual(response.context['board_url'], expected_board_url)

        # check relations: board created if none, but no members added
        self.assertIsNotNone(self.issue.editorialboard)
        self.assertEqual(len(self.issue.editorialboard.editorialmember_set.all()), 0)

        # check audit logs: no logs generated
        self.assertEqual(pre_submittion_audit_logs_count, 0)
        self.assertEqual(AuditLogEntry.objects.all().count(), 0)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True, CELERY_ALWAYS_EAGER=True, BROKER_BACKEND='memory')
    def test_EDIT_board_member_valid_POST_is_valid(self):
        """
        User of the group "Editors" successfully EDIT a board member
        """

        # with
        member = editorial_modelfactories.EditorialMemberFactory.create()
        member.board = EditorialBoard.objects.create(issue=self.issue)
        member.save()
        role = editorial_modelfactories.RoleTypeFactory.create()
        member_data_update = {
            'role': role,
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'nombre.apellido@fing.edu.uy',
            'institution': 'Universidad de la Republica - Facultad de Ingenieria',
            'link_cv': 'http://scielo.org.uy/',
            'state': 'Montevideo',
            'country': 'UY',
        }
        response = self.app.get(reverse("editorial.board.edit", args=[self.journal.id, member.id]), user=self.user)
        pre_submittion_audit_logs_count = AuditLogEntry.objects.all().count()

        # when
        form = response.forms['member-form']
        form.set('role',  member_data_update['role'].pk)
        form['first_name'] = member_data_update['first_name']
        form['last_name'] = member_data_update['last_name']
        form['email'] = member_data_update['email']
        form['institution'] = member_data_update['institution']
        form['link_cv'] = member_data_update['link_cv']
        form['state'] = member_data_update['state']
        form['country'] = member_data_update['country']

        response = form.submit().follow()
        # then

        # check frontend
        self.assertIn('Board Member updated successfully.', response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')
        self.assertIn(member_data_update['role'].name, response.body)
        self.assertIn(member_data_update['first_name'], response.body)
        self.assertIn(member_data_update['last_name'], response.body)
        self.assertIn(member_data_update['email'], response.body)
        self.assertIn(member_data_update['institution'], response.body)
        # the link_cv is not displayed in the frontend
        self.assertIn(member_data_update['state'], response.body)
        self.assertIn(str(dict(countries)[member_data_update['country']]), response.body)

        # check data from db
        member_from_db = EditorialMember.objects.get(pk=member.pk)
        self.assertEqual(member_from_db.role, member_data_update['role'])
        self.assertEqual(member_from_db.first_name, member_data_update['first_name'])
        self.assertEqual(member_from_db.last_name, member_data_update['last_name'])
        self.assertEqual(member_from_db.email, member_data_update['email'])
        self.assertEqual(member_from_db.institution, member_data_update['institution'])
        self.assertEqual(member_from_db.link_cv, member_data_update['link_cv'])
        self.assertEqual(member_from_db.state, member_data_update['state'])
        self.assertEqual(member_from_db.country, member_data_update['country'])

        # check relations
        self.assertIsNotNone(self.issue.editorialboard)
        self.assertEqual(len(self.issue.editorialboard.editorialmember_set.all()), 1)
        self.assertEqual(member_from_db.pk, self.issue.editorialboard.editorialmember_set.all()[0].pk)

        # check audit log:
        self.assertEqual(pre_submittion_audit_logs_count, 0)
        audit_entries = AuditLogEntry.objects.all()
        self.assertEqual(audit_entries.count(), 1)
        entry = audit_entries[0]
        self.assertEqual(entry.action_flag, CHANGE) # Flag correspond with CHANGE action
        self.assertEqual(entry.content_type.model_class(), EditorialMember)
        audited_obj = entry.get_audited_object()
        self.assertEqual(audited_obj._meta.object_name, 'EditorialMember')
        self.assertEqual(audited_obj.pk, member_from_db.pk)

        self.assertIn( u'Changed fields:', entry.change_message) # message starts with u'Changed fields:'
        for field_name in member_data_update.keys():
            self.assertIn(field_name, entry.change_message)

    def test_EDIT_board_member_invalid_POST_is_invalid(self):
        """
        User of the group "Editors" UNsuccessfully EDIT a board member with a invalid email
        """
        # with
        member = editorial_modelfactories.EditorialMemberFactory.create()
        member.board = EditorialBoard.objects.create(issue=self.issue)
        member.save()
        role = editorial_modelfactories.RoleTypeFactory.create()
        member_data_update = {
            'role': role,
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'nombre.apellido@', # invalid email
            'institution': 'Universidad de la Republica - Facultad de Ingenieria',
            'link_cv': 'http://scielo.org.uy/',
            'state': 'Montevideo',
            'country': 'UY',
        }
        response = self.app.get(reverse("editorial.board.edit", args=[self.journal.id, member.id]), user=self.user)
        pre_submittion_audit_logs_count = AuditLogEntry.objects.all().count()

        # when
        form = response.forms['member-form']
        form.set('role',  member_data_update['role'].pk)
        form['first_name'] = member_data_update['first_name']
        form['last_name'] = member_data_update['last_name']
        form['email'] = member_data_update['email']
        form['institution'] = member_data_update['institution']
        form['link_cv'] = member_data_update['link_cv']
        form['state'] = member_data_update['state']
        form['country'] = member_data_update['country']

        response = form.submit()

        # then
        # check output
        self.assertTemplateUsed(response, 'board/board_member_edit_form.html')
        self.assertFalse(response.context['form'].is_valid())
        expected_errors = {'email': [u'Enter a valid e-mail address.']}
        self.assertEqual(response.context['form'].errors, expected_errors)
        self.assertIn('Check mandatory fields.', response.body)

        # expected extra context data
        expected_post_url = reverse("editorial.board.edit", args=[self.journal.id, member.id])
        expected_board_url = reverse('editorial.board', args=[self.journal.pk, ])
        self.assertEqual(response.context['post_url'], expected_post_url)
        self.assertEqual(response.context['board_url'], expected_board_url)
        self.assertEqual(response.context['board_member'].pk, member.pk)

        # check relations: board remains the same, but no members were edited
        self.assertIsNotNone(self.issue.editorialboard)
        self.assertEqual(len(self.issue.editorialboard.editorialmember_set.all()), 1)
        member_from_db = self.issue.editorialboard.editorialmember_set.all()[0]

        self.assertEqual(member_from_db.role, member.role)
        self.assertEqual(member_from_db.first_name, member.first_name)
        self.assertEqual(member_from_db.last_name, member.last_name)
        self.assertEqual(member_from_db.email, member.email)
        self.assertEqual(member_from_db.institution, member.institution)
        self.assertEqual(member_from_db.link_cv, member.link_cv)
        self.assertEqual(member_from_db.state, member.state)
        self.assertEqual(member_from_db.country, member.country)

        # check audit logs: no logs generated
        self.assertEqual(pre_submittion_audit_logs_count, 0)
        self.assertEqual(AuditLogEntry.objects.all().count(), 0)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True, CELERY_ALWAYS_EAGER=True, BROKER_BACKEND='memory')
    def test_DELETE_board_member_valid_POST_is_valid(self):
        """
        User of the group "Editors" successfully DELETE a board member
        """
        # with
        member = editorial_modelfactories.EditorialMemberFactory.create()
        member.board = EditorialBoard.objects.create(issue=self.issue)
        member.save()
        response = self.app.get(reverse("editorial.board.delete", args=[self.journal.id, member.id]), user=self.user)
        form = response.forms['member-form']
        pre_submittion_audit_logs_count = AuditLogEntry.objects.all().count()

        # when
        response = form.submit().follow()

        # then

        # check frontend
        self.assertIn('Board Member DELETED successfully.', response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')

        # check that member was deleted from DB
        # using .filter(pk=...) to receive a [emtpy] list, and avoid DoesNotExist exception
        members_from_db = EditorialMember.objects.filter(pk=member.pk)
        self.assertNotIn(member, members_from_db)

        # check relations: board remains the same, but no members were edited
        self.assertIsNotNone(self.issue.editorialboard)
        self.assertNotIn(member, self.issue.editorialboard.editorialmember_set.all())
        self.assertEqual(len(self.issue.editorialboard.editorialmember_set.all()), 0)

        # check audit log:
        self.assertEqual(pre_submittion_audit_logs_count, 0)
        audit_entries = AuditLogEntry.objects.all()
        self.assertEqual(audit_entries.count(), 1)
        entry = audit_entries[0]
        self.assertEqual(entry.action_flag, DELETION)  # Flag correspond with DELETE action
        self.assertEqual(entry.content_type.model_class(), EditorialMember)
        audited_obj = entry.get_audited_object()
        self.assertIsNone(audited_obj)  # audited object (member) was deleted, so, no referece to it
        expected_change_msg = u'Record DELETED (%s, pk: %s): %s' % (member.pk, member._meta.verbose_name, unicode(member))
        self.assertEqual(entry.change_message, expected_change_msg)


class EditorialMemberFormAsLibrarianTests(EditorialMemberFormAsEditorTests):
    """
    Excecute the same tests that an Editors (EditorialMemberFormAsEditorTests),
    the setUp is almost the same.Only change is that the self.user is assigned
    as a member of "Librarian" group instead of "Editors" group.
    """
    def setUp(self):
        super(EditorialMemberFormAsLibrarianTests, self).setUp()
        # change user group to belong to Librarian group
        self.user.groups.clear()
        group = modelfactories.GroupFactory(name="Librarian")
        self.user.groups.add(group)
        self.user.save()

        _add_required_permission_to_group(group)

    def tearDown(self):
        super(EditorialMemberFormAsLibrarianTests, self).tearDown()


class EditorialMemberFormAsTraineeTests(EditorialMemberFormAsEditorTests):
    """
    Excecute the same tests that an Editors (EditorialMemberFormAsEditorTests),
    the setUp is almost the same. Only change is that the self.user is assigned
    as a member of "Trainee" group instead of "Editors" group.
    """
    def setUp(self):
        super(EditorialMemberFormAsTraineeTests, self).setUp()
        # change user group to belong to Trainee group
        self.user.groups.clear()
        group = modelfactories.GroupFactory(name="Trainee")
        self.user.groups.add(group)
        self.user.save()

        _add_required_permission_to_group(group)

    def tearDown(self):
        super(EditorialMemberFormAsTraineeTests, self).tearDown()


class MembersSortingOnActionTests(WebTest):

    def setUp(self):
        # create a group 'Editors'
        group = modelfactories.GroupFactory(name="Editors")
        # create a user and set group 'Editors'
        self.user = modelfactories.UserFactory(is_active=True)
        self.user.groups.add(group)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=False)
        self.collection.make_default_to_user(self.user)

        self.journal = modelfactories.JournalFactory.create()
        self.journal.join(self.collection, self.user)

        # set the user as editor of the journal
        self.journal.editor = self.user

        # create an issue
        self.issue = modelfactories.IssueFactory.create()
        self.issue.journal = self.journal
        self.journal.save()
        self.issue.save()

        _add_required_permission_to_group(group)

    # next tests DELETE one member on each role
    def test_three_roles_delete_first_member_of_three_must_keep_sequence(self):
        """
        Create 3 board members, each one with different roles: [a1(1), a2(2), a3(3), ]
        Delete the first one (order: 1), the other will remain in sequence: [a2(1), a3(2), ]
        """
        # with
        board = EditorialBoard.objects.create(issue=self.issue)

        role1 = editorial_modelfactories.RoleTypeFactory.create()
        role2 = editorial_modelfactories.RoleTypeFactory.create()
        role3 = editorial_modelfactories.RoleTypeFactory.create()
        # need to specify the correct order, otherwise will be = 1
        # usually users will use de add view, that handle the correct order
        member1 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member2 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member3 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)

        # when
        # delete member 1
        response = self.app.get(reverse("editorial.board.delete", args=[self.journal.id, member1.id]), user=self.user)
        form = response.forms['member-form']
        response = form.submit().follow()

        # then
        # check we landed in the correct place :)
        self.assertIn('Board Member DELETED successfully.', response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')

        # check the order of the board members
        self.assertEqual([m.order for m in board.editorialmember_set.all()], [1, 2])

    def test_three_roles_delete_second_member_of_three_must_keep_sequence(self):
        """
        Create 3 board members, each one with different roles. [a1(1), a2(2), a3(3), ]
        Delete the SECOND member (order: 2), the other will remain in sequence:  [a1(1), a3(2), ]
        """
        # with
        board = EditorialBoard.objects.create(issue=self.issue)

        role1 = editorial_modelfactories.RoleTypeFactory.create()
        role2 = editorial_modelfactories.RoleTypeFactory.create()
        role3 = editorial_modelfactories.RoleTypeFactory.create()
        # need to specify the correct order, otherwise will be = 1
        # usually users will use de add view, that handle the correct order
        member1 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member2 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member3 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)

        # when
        # delete member 1
        response = self.app.get(reverse("editorial.board.delete", args=[self.journal.id, member2.id]), user=self.user)
        form = response.forms['member-form']
        response = form.submit().follow()

        # then
        # check we landed in the correct place :)
        self.assertIn('Board Member DELETED successfully.', response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')

        # check the order of the board members
        self.assertEqual([m.order for m in board.editorialmember_set.all()], [1, 2])

    def test_three_roles_delete_third_member_of_three_must_keep_sequence(self):
        """
        Create 3 board members, each one with different roles. [a1(1), a2(2), a3(3), ]
        Delete the THIRD member (order: 3), the other will remain in sequence: [a1(1), a2(2),]
        """
        # with
        board = EditorialBoard.objects.create(issue=self.issue)

        role1 = editorial_modelfactories.RoleTypeFactory.create()
        role2 = editorial_modelfactories.RoleTypeFactory.create()
        role3 = editorial_modelfactories.RoleTypeFactory.create()
        # need to specify the correct order, otherwise will be = 1
        # usually users will use de add view, that handle the correct order
        member1 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member2 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member3 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)

        # when
        # delete member 1
        response = self.app.get(reverse("editorial.board.delete", args=[self.journal.id, member3.id]), user=self.user)
        form = response.forms['member-form']
        response = form.submit().follow()

        # then
        # check we landed in the correct place :)
        self.assertIn('Board Member DELETED successfully.', response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')

        # check the order of the board members
        self.assertEqual([m.order for m in board.editorialmember_set.all()], [1, 2])

    # next tests DELETE with MORE THAN one member on each role
    def test_three_roles_six_members_delete_second_member_must_keep_sequence(self):
        """
        Create 6 board members, 3 pairs with 3 different roles. [a1(1), a2(1), a3(2), a4(2), a5(3), a6(3), ]
        Delete the second member (a2, order: 1, role: 1), the other will remain in sequence: [a1(1), a3(2), a4(2), a5(3), a6(3), ]
        """
        # with
        board = EditorialBoard.objects.create(issue=self.issue)

        role1 = editorial_modelfactories.RoleTypeFactory.create()
        role2 = editorial_modelfactories.RoleTypeFactory.create()
        role3 = editorial_modelfactories.RoleTypeFactory.create()
        # need to specify the correct order, otherwise will be = 1
        # usually users will use de add view, that handle the correct order
        member1 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member2 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member3 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member4 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member5 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)
        member6 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)

        # when
        # delete member 1
        response = self.app.get(reverse("editorial.board.delete", args=[self.journal.id, member2.id]), user=self.user)
        form = response.forms['member-form']
        response = form.submit().follow()

        # then
        # check we landed in the correct place :)
        self.assertIn('Board Member DELETED successfully.', response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')

        # check the order of the board members
        self.assertEqual([m.order for m in board.editorialmember_set.all()], [1, 2, 2, 3, 3, ])

    def test_three_roles_six_members_delete_fourth_member_must_keep_sequence(self):
        """
        Create 6 board members, 3 pairs with 3 different roles. [a1(1), a2(1), a3(2), a4(2), a5(3), a6(3), ]
        Delete the fourth member (a4, order: 2, role: 2), the other will remain in sequence: [a1(1), a2(1), a3(2), a5(3), a6(3), ]
        """
        # with
        board = EditorialBoard.objects.create(issue=self.issue)

        role1 = editorial_modelfactories.RoleTypeFactory.create()
        role2 = editorial_modelfactories.RoleTypeFactory.create()
        role3 = editorial_modelfactories.RoleTypeFactory.create()
        # need to specify the correct order, otherwise will be = 1
        # usually users will use de add view, that handle the correct order
        member1 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member2 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member3 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member4 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member5 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)
        member6 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)

        # when
        # delete member 1
        response = self.app.get(reverse("editorial.board.delete", args=[self.journal.id, member4.id]), user=self.user)
        form = response.forms['member-form']
        response = form.submit().follow()

        # then
        # check we landed in the correct place :)
        self.assertIn('Board Member DELETED successfully.', response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')

        # check the order of the board members
        self.assertEqual([m.order for m in board.editorialmember_set.all()], [1, 1, 2, 3, 3, ])

    # next tests ADD one member on each role
    def test_three_roles_three_members_add_member_to_first_role_must_keep_sequence(self):
        """
        Create 3 board members, each one with different roles. (a1, a2, a3,)
        ADD a new member (AX) with the FIRST role (order: 1), then all 4 members must keep in sequence: a1(1), AX(1), a2(2), a3(3)
        """
        # with
        board = EditorialBoard.objects.create(issue=self.issue)

        role1 = editorial_modelfactories.RoleTypeFactory.create()
        role2 = editorial_modelfactories.RoleTypeFactory.create()
        role3 = editorial_modelfactories.RoleTypeFactory.create()
        # need to specify the correct order, otherwise will be = 1
        # usually users will use de add view, that handle the correct order
        member1 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member2 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member3 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)

        member_data = {
            'role': role1,
            'first_name': 'first name',
            'last_name': 'last name',
            'email': 'email@example.com',
            'institution': 'institution name',
            'link_cv': 'http://scielo.org/php/index.php',
            'state': 'SP',
            'country': 'BR',
        }
        # when
        response = self.app.get(reverse("editorial.board.add", args=[self.journal.id, self.issue.id]), user=self.user)

        form = response.forms['member-form']
        form.set('role',  member_data['role'].pk)
        form['first_name'] = member_data['first_name']
        form['last_name'] = member_data['last_name']
        form['email'] = member_data['email']
        form['institution'] = member_data['institution']
        form['link_cv'] = member_data['link_cv']
        form['state'] = member_data['state']
        form['country'] = member_data['country']

        response = form.submit().follow()
        # then
        # check we landed in the correct place :)
        self.assertIn('Board Member created successfully.', response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')
        # retrieve new member from db:
        new_member = EditorialMember.objects.get(
            role=member_data['role'],
            first_name=member_data['first_name'],
            last_name=member_data['last_name'],
            email=member_data['email'],
            institution=member_data['institution'],
            link_cv=member_data['link_cv'],
            state=member_data['state'],
            country=member_data['country'],
        )
        # check the order of the board members
        self.assertEqual([m.order for m in board.editorialmember_set.all()], [1, 1, 2, 3, ])

    def test_three_roles_three_members_add_member_to_second_role_must_keep_sequence(self):
        """
        Create 3 board members, each one with different roles. (a1, a2, a3,)
        ADD a new member (AX) with the SECOND role (order: 2), then all 4 members must keep in sequence: a1(1), a2(2), AX(2), a3(3)
        """
        # with
        board = EditorialBoard.objects.create(issue=self.issue)

        role1 = editorial_modelfactories.RoleTypeFactory.create()
        role2 = editorial_modelfactories.RoleTypeFactory.create()
        role3 = editorial_modelfactories.RoleTypeFactory.create()
        # need to specify the correct order, otherwise will be = 1
        # usually users will use de add view, that handle the correct order
        member1 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member2 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member3 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)

        member_data = {
            'role': role2,
            'first_name': 'first name',
            'last_name': 'last name',
            'email': 'email@example.com',
            'institution': 'institution name',
            'link_cv': 'http://scielo.org/php/index.php',
            'state': 'SP',
            'country': 'BR',
        }
        # when
        response = self.app.get(reverse("editorial.board.add", args=[self.journal.id, self.issue.id]), user=self.user)

        form = response.forms['member-form']
        form.set('role',  member_data['role'].pk)
        form['first_name'] = member_data['first_name']
        form['last_name'] = member_data['last_name']
        form['email'] = member_data['email']
        form['institution'] = member_data['institution']
        form['link_cv'] = member_data['link_cv']
        form['state'] = member_data['state']
        form['country'] = member_data['country']

        response = form.submit().follow()
        # then
        # check we landed in the correct place :)
        self.assertIn('Board Member created successfully.', response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')
        # retrieve new member from db:
        new_member = EditorialMember.objects.get(
            role=member_data['role'],
            first_name=member_data['first_name'],
            last_name=member_data['last_name'],
            email=member_data['email'],
            institution=member_data['institution'],
            link_cv=member_data['link_cv'],
            state=member_data['state'],
            country=member_data['country'],
        )
        # check the order of the board members
        self.assertEqual([m.order for m in board.editorialmember_set.all()], [1, 2, 2, 3, ])

    def test_three_roles_three_members_add_member_with_new_role_must_keep_sequence(self):
        """
        Create 3 board members, each one with different roles. (a1, a2, a3,)
        ADD a new member (AX) with the NEW role, then all 4 members must keep in sequence: a1(1), a2(2), a3(3), AX(4)
        """
        # with
        board = EditorialBoard.objects.create(issue=self.issue)

        role1 = editorial_modelfactories.RoleTypeFactory.create()
        role2 = editorial_modelfactories.RoleTypeFactory.create()
        role3 = editorial_modelfactories.RoleTypeFactory.create()

        new_role = editorial_modelfactories.RoleTypeFactory.create()
        # need to specify the correct order, otherwise will be = 1
        # usually users will use de add view, that handle the correct order
        member1 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member2 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member3 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)

        member_data = {
            'role': new_role,
            'first_name': 'first name',
            'last_name': 'last name',
            'email': 'email@example.com',
            'institution': 'institution name',
            'link_cv': 'http://scielo.org/php/index.php',
            'state': 'SP',
            'country': 'BR',
        }
        # when
        response = self.app.get(reverse("editorial.board.add", args=[self.journal.id, self.issue.id]), user=self.user)

        form = response.forms['member-form']
        form.set('role',  member_data['role'].pk)
        form['first_name'] = member_data['first_name']
        form['last_name'] = member_data['last_name']
        form['email'] = member_data['email']
        form['institution'] = member_data['institution']
        form['link_cv'] = member_data['link_cv']
        form['state'] = member_data['state']
        form['country'] = member_data['country']

        response = form.submit().follow()
        # then
        # check we landed in the correct place :)
        self.assertIn('Board Member created successfully.', response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')
        # retrieve new member from db:
        new_member = EditorialMember.objects.get(
            role=member_data['role'],
            first_name=member_data['first_name'],
            last_name=member_data['last_name'],
            email=member_data['email'],
            institution=member_data['institution'],
            link_cv=member_data['link_cv'],
            state=member_data['state'],
            country=member_data['country'],
        )
        # check the order of the board members
        self.assertEqual([m.order for m in board.editorialmember_set.all()], [1, 2, 3, 4, ])

    # next tests with ONLY one member on each role
    def test_three_roles_three_members_edit_1st_member_role_to_a_new_role_must_keep_sequence(self):
        """
        Create 3 board members, each one with different roles. (a1, a2, a3,)
        EDIT a member (a1) changing to a NEW role, then all members must keep in sequence: a2(1), a3(2), a1(3)
        """
        # with
        board = EditorialBoard.objects.create(issue=self.issue)

        role1 = editorial_modelfactories.RoleTypeFactory.create()
        role2 = editorial_modelfactories.RoleTypeFactory.create()
        role3 = editorial_modelfactories.RoleTypeFactory.create()

        new_role = editorial_modelfactories.RoleTypeFactory.create()
        # need to specify the correct order, otherwise will be = 1
        # usually users will use de add view, that handle the correct order
        member1 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member2 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member3 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)

        # when
        response = self.app.get(reverse("editorial.board.edit", args=[self.journal.id, member1.id]), user=self.user)
        form = response.forms['member-form']
        form.set('role',  new_role.pk)
        response = form.submit().follow()
        # check we landed in the correct place :)
        self.assertIn('Board Member updated successfully.', response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')
        # check the order of the board members
        self.assertEqual([m.order for m in board.editorialmember_set.all()], [1, 2, 3, ])

    def test_three_roles_three_members_edit_2nd_member_role_to_a_new_role_must_keep_sequence(self):
        """
        Create 3 board members, each one with different roles. (a1, a2, a3,)
        EDIT a member (a2) changing to a NEW role, then all members must keep in sequence: a1(1), a3(2), a2(3)
        """
        # with
        board = EditorialBoard.objects.create(issue=self.issue)

        role1 = editorial_modelfactories.RoleTypeFactory.create()
        role2 = editorial_modelfactories.RoleTypeFactory.create()
        role3 = editorial_modelfactories.RoleTypeFactory.create()

        new_role = editorial_modelfactories.RoleTypeFactory.create()
        # need to specify the correct order, otherwise will be = 1
        # usually users will use de add view, that handle the correct order
        member1 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member2 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member3 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)
        # when
        response = self.app.get(reverse("editorial.board.edit", args=[self.journal.id, member2.id]), user=self.user)
        form = response.forms['member-form']
        form.set('role',  new_role.pk)
        response = form.submit().follow()
        # check we landed in the correct place :)
        self.assertIn('Board Member updated successfully.', response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')
        self.assertEqual([m.order for m in board.editorialmember_set.all()], [1, 2, 3, ])

    def test_three_roles_three_members_edit_3rd_member_role_to_a_new_role_must_keep_sequence(self):
        """
        Create 3 board members, each one with different roles. (a1, a2, a3,)
        EDIT a member (a3) changing to a NEW role, then all members must keep in sequence: a1(1), a2(2), a3(3)
        """
        # with
        board = EditorialBoard.objects.create(issue=self.issue)

        role1 = editorial_modelfactories.RoleTypeFactory.create()
        role2 = editorial_modelfactories.RoleTypeFactory.create()
        role3 = editorial_modelfactories.RoleTypeFactory.create()

        new_role = editorial_modelfactories.RoleTypeFactory.create()
        # need to specify the correct order, otherwise will be = 1
        # usually users will use de add view, that handle the correct order
        member1 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member2 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member3 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)

        # when
        response = self.app.get(reverse("editorial.board.edit", args=[self.journal.id, member3.id]), user=self.user)
        form = response.forms['member-form']
        form.set('role',  new_role.pk)
        response = form.submit().follow()
        # check we landed in the correct place :)
        self.assertIn('Board Member updated successfully.', response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')
        # check the order of the board members
        self.assertEqual([m.order for m in board.editorialmember_set.all()], [1, 2, 3, ])

    def test_three_roles_three_members_edit_1st_member_role_to_the_2nd_role_must_keep_sequence(self):
        """
        Create 3 board members, each one with different roles. (a1, a2, a3,)
        EDIT a member (a1) changing to the 2nd role, then all members must keep in sequence: a2(1), a1(1), a3(2)
        """
        # with
        board = EditorialBoard.objects.create(issue=self.issue)

        role1 = editorial_modelfactories.RoleTypeFactory.create()
        role2 = editorial_modelfactories.RoleTypeFactory.create()
        role3 = editorial_modelfactories.RoleTypeFactory.create()

        # need to specify the correct order, otherwise will be = 1
        # usually users will use de add view, that handle the correct order
        member1 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member2 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member3 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)
        # when
        response = self.app.get(reverse("editorial.board.edit", args=[self.journal.id, member1.id]), user=self.user)
        form = response.forms['member-form']
        form.set('role',  role2.pk)
        response = form.submit().follow()
        # check we landed in the correct place :)
        self.assertIn('Board Member updated successfully.', response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')
        # check the order of the board members
        self.assertEqual([m.order for m in board.editorialmember_set.all()], [1, 1, 2, ])

    # next tests with MORE THAN one member on each role
    def test_three_roles_six_members_edit_1st_member_role_to_a_new_role_must_keep_sequence(self):
        """
        Create 3 board members, each one with different roles. (a1[1], a2[1], a3[2], a4[2], a5[3], a6[3])
        EDIT a member (a1) changing to a NEW role, then all members must keep in sequence: a2[1], a3[2], a4[2], a5[3], a6[3], a1[4]
        """
        # with
        board = EditorialBoard.objects.create(issue=self.issue)

        role1 = editorial_modelfactories.RoleTypeFactory.create()
        role2 = editorial_modelfactories.RoleTypeFactory.create()
        role3 = editorial_modelfactories.RoleTypeFactory.create()

        new_role = editorial_modelfactories.RoleTypeFactory.create()
        # need to specify the correct order, otherwise will be = 1
        # usually users will use de add view, that handle the correct order
        member1 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member2 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member3 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member4 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member5 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)
        member6 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)

        # when
        response = self.app.get(reverse("editorial.board.edit", args=[self.journal.id, member1.id]), user=self.user)
        form = response.forms['member-form']
        form.set('role',  new_role.pk)
        response = form.submit().follow()
        # check we landed in the correct place :)
        self.assertIn('Board Member updated successfully.', response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')
        # check the order of the board members
        self.assertEqual([m.order for m in board.editorialmember_set.all()], [1, 2, 2, 3, 3, 4, ])

    def test_three_roles_six_members_edit_2nd_member_role_to_a_new_role_must_keep_sequence(self):
        """
        Create 3 board members, each one with different roles. (a1[1], a2[1], a3[2], a4[2], a5[3], a6[3])
        EDIT a member (a2) changing to a NEW role, then all members must keep in sequence: a1[1], a3[2], a4[2], a5[3], a6[3], a2[4]
        """
        # with
        board = EditorialBoard.objects.create(issue=self.issue)

        role1 = editorial_modelfactories.RoleTypeFactory.create()
        role2 = editorial_modelfactories.RoleTypeFactory.create()
        role3 = editorial_modelfactories.RoleTypeFactory.create()

        new_role = editorial_modelfactories.RoleTypeFactory.create()
        # need to specify the correct order, otherwise will be = 1
        # usually users will use de add view, that handle the correct order
        member1 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member2 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member3 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member4 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member5 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)
        member6 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)

        # when
        response = self.app.get(reverse("editorial.board.edit", args=[self.journal.id, member2.id]), user=self.user)
        form = response.forms['member-form']
        form.set('role',  new_role.pk)
        response = form.submit().follow()
        # check we landed in the correct place :)
        self.assertIn('Board Member updated successfully.', response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')
        # check the order of the board members
        self.assertEqual([m.order for m in board.editorialmember_set.all()], [1, 2, 2, 3, 3, 4, ])

    def test_three_roles_six_members_edit_3rd_member_role_to_a_new_role_must_keep_sequence(self):
        """
        Create 3 board members, each one with different roles. (a1[1], a2[1], a3[2], a4[2], a5[3], a6[3])
        EDIT a member (a3) changing to a NEW role, then all members must keep in sequence: a1[1], a2[1], a4[2], a5[3], a6[3], a3[4]
        """
        # with
        board = EditorialBoard.objects.create(issue=self.issue)

        role1 = editorial_modelfactories.RoleTypeFactory.create()
        role2 = editorial_modelfactories.RoleTypeFactory.create()
        role3 = editorial_modelfactories.RoleTypeFactory.create()

        new_role = editorial_modelfactories.RoleTypeFactory.create()
        # need to specify the correct order, otherwise will be = 1
        # usually users will use de add view, that handle the correct order
        member1 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member2 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member3 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member4 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member5 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)
        member6 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)
        # when
        response = self.app.get(reverse("editorial.board.edit", args=[self.journal.id, member3.id]), user=self.user)
        form = response.forms['member-form']
        form.set('role',  new_role.pk)
        response = form.submit().follow()
        # check we landed in the correct place :)
        self.assertIn('Board Member updated successfully.', response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')
        # check the order of the board members
        self.assertEqual([m.order for m in board.editorialmember_set.all()], [1, 1, 2, 3, 3, 4, ])

    def test_three_roles_six_members_edit_1st_member_role_to_the_2nd_role_must_keep_sequence(self):
        """
        Create 3 board members, each one with different roles. (a1[1], a2[1], a3[2], a4[2], a5[3], a6[3])
        EDIT a member (a3) changing to a NEW role, then all members must keep in sequence: a2[1], a1[2], a3[2], a4[2], a5[3], a6[3]
        """
        # with
        board = EditorialBoard.objects.create(issue=self.issue)

        role1 = editorial_modelfactories.RoleTypeFactory.create()
        role2 = editorial_modelfactories.RoleTypeFactory.create()
        role3 = editorial_modelfactories.RoleTypeFactory.create()

        # need to specify the correct order, otherwise will be = 1
        # usually users will use de add view, that handle the correct order
        member1 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member2 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member3 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member4 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member5 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)
        member6 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)
        # when
        response = self.app.get(reverse("editorial.board.edit", args=[self.journal.id, member1.id]), user=self.user)
        form = response.forms['member-form']
        form.set('role',  role2.pk)
        response = form.submit().follow()
        # check we landed in the correct place :)
        self.assertIn('Board Member updated successfully.', response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')
        # check the order of the board members
        self.assertEqual([m.order for m in board.editorialmember_set.all()], [1, 2, 2, 2, 3, 3, ])

    # next tests MOVE UP a member (ONLY one member on each role)
    def test_three_roles_three_members_move_up_2nd_member(self):
        """
        Create 3 board members, each one with different roles. (a1[1], a2[2], a3[3],)
        MOVE UP the 2nd member (a2), then all members must keep in sequence: a2(1), a1(2), a3(3)
        """
        # with
        board = EditorialBoard.objects.create(issue=self.issue)

        role1 = editorial_modelfactories.RoleTypeFactory.create()
        role2 = editorial_modelfactories.RoleTypeFactory.create()
        role3 = editorial_modelfactories.RoleTypeFactory.create()
        # need to specify the correct order, otherwise will be = 1
        # usually users will use de add view, that handle the correct order
        member1 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member2 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member3 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)

        # when
        response = self.app.get(reverse("editorial.board", args=[self.journal.id, ]), user=self.user)
        # get the move form and indicates to move it UP!
        form = response.forms['form_move_role_%s_%s_%s' % (self.issue.pk, board.pk, member2.order)]
        form['direction'] = "up"

        response = form.submit().follow()
        # then
        # check we landed in the correct place :)
        self.assertIn('Board block moved successfully.', response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')
        # check the order of the board members
        self.assertEqual([m.order for m in board.editorialmember_set.all()], [1, 2, 3, ])

    # next tests MOVE UP a member (MORE THAN ONE member on each role)
    def test_three_roles_six_members_move_up_2nd_block_members(self):
        """
        Create 3 board members, in pairs with different roles. (a1[1], a2[1]), (a3[2], a4[2]), (a5[3], a6[3])
        MOVE UP the 2nd block members (a3, a4), then all members must keep in sequence: (a3[1], a4[1]), (a1[2], a2[2]), (a5[3], a6[3])
        """
        # with
        board = EditorialBoard.objects.create(issue=self.issue)

        role1 = editorial_modelfactories.RoleTypeFactory.create()
        role2 = editorial_modelfactories.RoleTypeFactory.create()
        role3 = editorial_modelfactories.RoleTypeFactory.create()
        # need to specify the correct order, otherwise will be = 1
        # usually users will use de add view, that handle the correct order
        member1 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member2 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member3 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member4 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member5 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)
        member6 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)
        # when
        response = self.app.get(reverse("editorial.board", args=[self.journal.id, ]), user=self.user)
        # get the move form and indicates to move it UP!
        form = response.forms['form_move_role_%s_%s_%s' % (self.issue.pk, board.pk, member3.order)]
        form['direction'] = "up"

        response = form.submit().follow()
        # then
        # check we landed in the correct place :)
        self.assertIn('Board block moved successfully.', response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')
        # check the order of the board members
        self.assertEqual([m.order for m in board.editorialmember_set.all()], [1, 1, 2, 2, 3, 3])

    # next tests MOVE DOWN a member (ONLY one member on each role)
    def test_three_roles_three_members_move_down_2nd_member(self):
        """
        Create 3 board members, each one with different roles. (a1[1], a2[2], a3[3],)
        MOVE DOWN the 2nd member (a2), then all members must keep in sequence: a1(1), a3(2), a1(3)
        """
        # with
        board = EditorialBoard.objects.create(issue=self.issue)

        role1 = editorial_modelfactories.RoleTypeFactory.create()
        role2 = editorial_modelfactories.RoleTypeFactory.create()
        role3 = editorial_modelfactories.RoleTypeFactory.create()
        # need to specify the correct order, otherwise will be = 1
        # usually users will use de add view, that handle the correct order
        member1 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member2 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member3 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)

        # when
        response = self.app.get(reverse("editorial.board", args=[self.journal.id, ]), user=self.user)
        # get the move form and indicates to move it UP!
        form = response.forms['form_move_role_%s_%s_%s' % (self.issue.pk, board.pk, member2.order)]
        form['direction'] = "down"

        response = form.submit().follow()
        # then
        # check we landed in the correct place :)
        self.assertIn('Board block moved successfully.', response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')
        # check the order of the board members
        self.assertEqual([m.order for m in board.editorialmember_set.all()], [1, 2, 3, ])

    # next tests MOVE DOWN a member (MORE THAN ONE member on each role)
    def test_three_roles_six_members_move_down_2nd_block_members(self):
        """
        Create 3 board members, in pairs with different roles. (a1[1], a2[1]), (a3[2], a4[2]), (a5[3], a6[3])
        MOVE DOWN the 2nd block members (a3, a4), then all members must keep in sequence: (a1[2], a2[2]), (a5[3], a6[3]), (a3[1], a4[1])
        """
        # with
        board = EditorialBoard.objects.create(issue=self.issue)

        role1 = editorial_modelfactories.RoleTypeFactory.create()
        role2 = editorial_modelfactories.RoleTypeFactory.create()
        role3 = editorial_modelfactories.RoleTypeFactory.create()
        # need to specify the correct order, otherwise will be = 1
        # usually users will use de add view, that handle the correct order
        member1 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member2 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member3 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member4 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member5 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)
        member6 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)
        # when
        response = self.app.get(reverse("editorial.board", args=[self.journal.id, ]), user=self.user)
        # get the move form and indicates to move it DOWN!
        form = response.forms['form_move_role_%s_%s_%s' % (self.issue.pk, board.pk, member3.order)]
        form['direction'] = "down"

        response = form.submit().follow()
        # then
        # check we landed in the correct place :)
        self.assertIn('Board block moved successfully.', response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')
        # check the order of the board members
        self.assertEqual([m.order for m in board.editorialmember_set.all()], [1, 1, 2, 2, 3, 3])

    # tests first member cant be moved UP (ONLY one member on each role)
    def test_move_up_first_block_must_raise_validation_error(self):
        """
        Create 3 board members, each one with different roles. (a1[1], a2[2], a3[3],)
        Try to MOVE UP the 1st member (a1), will raise validaton error,
        then all members must keep in sequence: a1(1), a2(2), a3(3)
        """
        # with
        board = EditorialBoard.objects.create(issue=self.issue)

        role1 = editorial_modelfactories.RoleTypeFactory.create()
        role2 = editorial_modelfactories.RoleTypeFactory.create()
        role3 = editorial_modelfactories.RoleTypeFactory.create()
        # need to specify the correct order, otherwise will be = 1
        # usually users will use de add view, that handle the correct order
        member1 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member2 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member3 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)

        # when
        response = self.app.get(reverse("editorial.board", args=[self.journal.id, ]), user=self.user)
        # get the move form and indicates to move it UP!
        form = response.forms['form_move_role_%s_%s_%s' % (self.issue.pk, board.pk, member1.order)]
        form['direction'] = "up"

        response = form.submit().follow()
        # then
        # check we landed in the correct place :)
        self.assertIn("Board block can not be moved", response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')
        # check the order of the board members
        self.assertEqual([m.order for m in board.editorialmember_set.all()], [1, 2, 3, ])

    # tests last member cant be moved DOWN (ONLY one member on each role)
    def test_move_up_last_block_must_raise_validation_error(self):
        """
        Create 3 board members, each one with different roles. (a1[1], a2[2], a3[3],)
        Try to MOVE DOWN the last member (a3), will raise validaton error,
        then all members must keep in sequence: a1(1), a2(2), a3(3)
        """
        # with
        board = EditorialBoard.objects.create(issue=self.issue)

        role1 = editorial_modelfactories.RoleTypeFactory.create()
        role2 = editorial_modelfactories.RoleTypeFactory.create()
        role3 = editorial_modelfactories.RoleTypeFactory.create()
        # need to specify the correct order, otherwise will be = 1
        # usually users will use de add view, that handle the correct order
        member1 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role1, order=1)
        member2 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role2, order=2)
        member3 = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role3, order=3)

        # when
        response = self.app.get(reverse("editorial.board", args=[self.journal.id, ]), user=self.user)
        # get the move form and indicates to move it UP!
        form = response.forms['form_move_role_%s_%s_%s' % (self.issue.pk, board.pk, member3.order)]
        form['direction'] = "down"

        response = form.submit().follow()
        # then
        # check we landed in the correct place :)
        self.assertIn("Board block can not be moved", response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')
        # check the order of the board members
        self.assertEqual([m.order for m in board.editorialmember_set.all()], [1, 2, 3, ])


class EditRoleTypeForm(WebTest):

    def setUp(self):
        # create a group 'Editors'
        group = modelfactories.GroupFactory(name="Editors")
        # create a user and set group 'Editors'
        self.user = modelfactories.UserFactory(is_active=True)
        self.user.groups.add(group)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=False)
        self.collection.make_default_to_user(self.user)

        self.journal = modelfactories.JournalFactory.create()
        self.journal.join(self.collection, self.user)

        # set the user as editor of the journal
        self.journal.editor = self.user

        # create an issue
        self.issue = modelfactories.IssueFactory.create()
        self.issue.journal = self.journal
        self.journal.save()
        self.issue.save()

    def test_ADD_ROLE_valid_POST_is_valid(self):
        """
        Users with permissions: editorialmanager.add_roletype can add new roles
        """
        # with
        perm_add_roletype = _makePermission(perm='add_roletype', model='roletype')
        self.user.user_permissions.add(perm_add_roletype)
        pre_submittion_audit_logs_count = AuditLogEntry.objects.all().count()
        # when
        response = self.app.get(reverse("editorial.role.add", args=[self.journal.id]), user=self.user)
        new_role_name = "Blaus!"
        # when
        form = response.forms['role-form']
        form['name'] = new_role_name
        response = form.submit().follow()
        # then

        # check frontend:
        self.assertIn('Role created successfully.', response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')
        # check db:
        self.assertEqual(RoleType.objects.all().count(), 1)
        new_role_from_db = RoleType.objects.all()[0]
        # check audit log
        self.assertEqual(pre_submittion_audit_logs_count, 0)
        audit_entries = AuditLogEntry.objects.all()
        self.assertEqual(audit_entries.count(), 1)
        entry = audit_entries[0]
        self.assertEqual(entry.action_flag, ADDITION)  # Flag correspond with ADD action
        self.assertEqual(entry.content_type.model_class(), RoleType)
        audited_obj = entry.get_audited_object()
        self.assertEqual(audited_obj._meta.object_name, 'RoleType')
        self.assertEqual(audited_obj.pk, new_role_from_db.pk)

    def test_ADD_ROLE_invalid_POST_is_invalid(self):
        """
        Users with permissions: editorialmanager.add_roletype can add new roles
        """
        # with
        perm_add_roletype = _makePermission(perm='add_roletype', model='roletype')
        self.user.user_permissions.add(perm_add_roletype)
        pre_submittion_audit_logs_count = AuditLogEntry.objects.all().count()
        # when
        response = self.app.get(reverse("editorial.role.add", args=[self.journal.id]), user=self.user)
        new_role_name = ""  # empty name for a mandatory field is invalid
        # when
        form = response.forms['role-form']
        form['name'] = new_role_name
        response = form.submit()
        # then
        # check output
        self.assertTemplateUsed(response, 'board/role_type_edit.html')
        self.assertFalse(response.context['form'].is_valid())
        expected_errors = {'name': [u'This field is required.']}
        self.assertEqual(response.context['form'].errors, expected_errors)
        self.assertIn('Check mandatory fields.', response.body)
        # expected extra context data
        expected_post_url = reverse('editorial.role.add', args=[self.journal.pk, ])
        expected_board_url = reverse('editorial.board', args=[self.journal.pk, ])
        self.assertEqual(response.context['post_url'], expected_post_url)
        self.assertEqual(response.context['board_url'], expected_board_url)

        # check audit logs: no logs generated
        self.assertEqual(pre_submittion_audit_logs_count, 0)
        self.assertEqual(AuditLogEntry.objects.all().count(), 0)

    def test_ADD_ROLE_that_already_exist_POST_is_invalid(self):
        """
        Role.name must be unique.
        Users with permissions: editorialmanager.add_roletype can add new roles
        """
        # with
        board = EditorialBoard.objects.create(issue=self.issue)
        role = editorial_modelfactories.RoleTypeFactory.create(name="Pickles")

        perm_add_roletype = _makePermission(perm='add_roletype', model='roletype')
        self.user.user_permissions.add(perm_add_roletype)
        pre_submittion_audit_logs_count = AuditLogEntry.objects.all().count()
        # when
        response = self.app.get(reverse("editorial.role.add", args=[self.journal.id]), user=self.user)
        # when
        form = response.forms['role-form']
        form['name'] = role.name
        response = form.submit()
        # then
        # check output
        self.assertTemplateUsed(response, 'board/role_type_edit.html')
        self.assertFalse(response.context['form'].is_valid())
        expected_errors = {'name': [u'Role type with this Role Name already exists.']}
        self.assertEqual(response.context['form'].errors, expected_errors)
        self.assertIn('Check mandatory fields.', response.body)
        # expected extra context data
        expected_post_url = reverse('editorial.role.add', args=[self.journal.pk, ])
        expected_board_url = reverse('editorial.board', args=[self.journal.pk, ])
        self.assertEqual(response.context['post_url'], expected_post_url)
        self.assertEqual(response.context['board_url'], expected_board_url)

        # check audit logs: no logs generated
        self.assertEqual(pre_submittion_audit_logs_count, 0)
        self.assertEqual(AuditLogEntry.objects.all().count(), 0)

    def test_EDIT_ROLE_valid_POST_is_valid(self):
        # with
        board = EditorialBoard.objects.create(issue=self.issue)
        role = editorial_modelfactories.RoleTypeFactory.create(name="Pickles")
        member = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role)
        # add perms
        perm_change_roletype = _makePermission(perm='change_roletype', model='roletype')
        self.user.user_permissions.add(perm_change_roletype)
        pre_submittion_audit_logs_count = AuditLogEntry.objects.all().count()
        new_role_name = "Blaus!"
        # when
        response = self.app.get(reverse("editorial.role.edit", args=[self.journal.id, role.id]), user=self.user)
        form = response.forms['role-form']
        form['name'] = new_role_name
        response = form.submit().follow()
        # then

        # check frontend:
        self.assertIn('Role updated successfully.', response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')
        # check db:
        self.assertEqual(RoleType.objects.all().count(), 1)
        role_from_db = RoleType.objects.all()[0]
        # check audit log
        self.assertEqual(pre_submittion_audit_logs_count, 0)
        audit_entries = AuditLogEntry.objects.all()
        self.assertEqual(audit_entries.count(), 1)
        entry = audit_entries[0]
        self.assertEqual(entry.action_flag, CHANGE)  # Flag correspond with ADD action
        self.assertEqual(entry.content_type.model_class(), RoleType)
        audited_obj = entry.get_audited_object()
        self.assertEqual(audited_obj._meta.object_name, 'RoleType')
        self.assertEqual(audited_obj.pk, role_from_db.pk)

    def test_EDIT_ROLE_invalid_POST_is_invalid(self):
        # with
        board = EditorialBoard.objects.create(issue=self.issue)
        role = editorial_modelfactories.RoleTypeFactory.create(name="Pickles")
        member = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role)
        # add perms
        perm_change_roletype = _makePermission(perm='change_roletype', model='roletype')
        self.user.user_permissions.add(perm_change_roletype)
        pre_submittion_audit_logs_count = AuditLogEntry.objects.all().count()
        new_role_name = ""
        # when
        response = self.app.get(reverse("editorial.role.edit", args=[self.journal.id, role.id]), user=self.user)
        form = response.forms['role-form']
        form['name'] = new_role_name
        response = form.submit()
        # then
        # check output
        self.assertTemplateUsed(response, 'board/role_type_edit.html')
        self.assertFalse(response.context['form'].is_valid())
        expected_errors = {'name': [u'This field is required.']}
        self.assertEqual(response.context['form'].errors, expected_errors)
        self.assertIn('Check mandatory fields.', response.body)
        # expected extra context data
        expected_post_url = reverse("editorial.role.edit", args=[self.journal.id, role.id])
        expected_board_url = reverse('editorial.board', args=[self.journal.pk, ])
        self.assertEqual(response.context['post_url'], expected_post_url)
        self.assertEqual(response.context['board_url'], expected_board_url)

        # check audit logs: no logs generated
        self.assertEqual(pre_submittion_audit_logs_count, 0)
        self.assertEqual(AuditLogEntry.objects.all().count(), 0)

    def test_TRANSLATE_ROLE_valid_POST_is_valid(self):
        """
        Submit a valid POST of a set of translation,
        languages: "pt", and "es", must be required
        """
        # with
        board = EditorialBoard.objects.create(issue=self.issue)
        role = editorial_modelfactories.RoleTypeFactory.create(name="The Pickles")
        l1 = modelfactories.LanguageFactory.create(iso_code='pt', name='portuguese')
        l2 = modelfactories.LanguageFactory.create(iso_code='es', name='spanish')
        l3 = modelfactories.LanguageFactory.create(iso_code='fr', name='french')

        # add perms
        perm_change_roletype = _makePermission(perm='change_roletype', model='roletype')
        self.user.user_permissions.add(perm_change_roletype)
        pre_submittion_audit_logs_count = AuditLogEntry.objects.all().count()
        data = [
            {'name': u'Os Picles', 'language': l1},
            {'name': u'Los Picles', 'language': l2},
            {'name': u'Le Piclé', 'language': l3},
        ]

        # when
        response = self.app.get(reverse("editorial.role.translate", args=[self.journal.id, role.id]), user=self.user)
        form = response.forms['role-translations-form']
        for x in xrange(0, 3):
            form['role-translations-formset-%s-name' % x] = data[x]['name']
            form.set('role-translations-formset-%s-language' % x, data[x]['language'].pk)

        response = form.submit().follow()
        # then

        # check frontend:
        self.assertIn('Role updated successfully.', response.body)
        self.assertTemplateUsed(response, 'board/board_list.html')
        # check db:
        translations = RoleTypeTranslation.objects.filter(role=role)
        self.assertEqual(translations.count(), 3)
        for x in xrange(0, 3):
            t = translations.get(language=data[x]['language'])
            self.assertEqual(t.name, data[x]['name'])

        # check audit log
        self.assertEqual(pre_submittion_audit_logs_count, 0)
        audit_entries = AuditLogEntry.objects.all()
        self.assertEqual(audit_entries.count(), 1)
        entry = audit_entries[0]
        self.assertEqual(entry.action_flag, CHANGE)  # Flag correspond with ADD action
        self.assertEqual(entry.content_type.model_class(), RoleType)
        audited_obj = entry.get_audited_object()
        self.assertEqual(audited_obj._meta.object_name, 'RoleType')
        self.assertEqual(audited_obj.pk, role.pk)

    def test_TRANSLATE_ROLE_invalid_POST_without_lang_PT_is_invalid(self):
        """
        Submit a invalid POST of a set of translation,
        languages: "pt", and "es", must be required
        """
        # with
        board = EditorialBoard.objects.create(issue=self.issue)
        role = editorial_modelfactories.RoleTypeFactory.create(name="The Pickles")
        l1 = modelfactories.LanguageFactory.create(iso_code='it', name='italian')
        l2 = modelfactories.LanguageFactory.create(iso_code='es', name='spanish')
        l3 = modelfactories.LanguageFactory.create(iso_code='fr', name='french')

        # add perms
        perm_change_roletype = _makePermission(perm='change_roletype', model='roletype')
        self.user.user_permissions.add(perm_change_roletype)
        pre_submittion_audit_logs_count = AuditLogEntry.objects.all().count()
        data = [
            {'name': u'Il Picolo', 'language': l1},
            {'name': u'Los Picles', 'language': l2},
            {'name': u'Le Piclé', 'language': l3},
        ]

        # when
        response = self.app.get(reverse("editorial.role.translate", args=[self.journal.id, role.id]), user=self.user)
        form = response.forms['role-translations-form']
        for x in xrange(0, 3):
            form['role-translations-formset-%s-name' % x] = data[x]['name']
            form.set('role-translations-formset-%s-language' % x, data[x]['language'].pk)

        response = form.submit()
        # then
        self.assertTemplateUsed(response, 'board/role_type_translate.html')
        self.assertFalse(response.context['formset'].is_valid())
        expected_errors = [u'At least Portuguese and Spanish translations are required']
        self.assertEqual(response.context['formset'].non_form_errors(), expected_errors)
        self.assertIn('Check mandatory fields.', response.body)
        # check audit log
        self.assertEqual(pre_submittion_audit_logs_count, 0)
        audit_entries = AuditLogEntry.objects.all()
        self.assertEqual(audit_entries.count(), 0)

    def test_TRANSLATE_ROLE_invalid_POST_without_lang_ES_is_invalid(self):
        """
        Submit a invalid POST of a set of translation,
        languages: "pt", and "es", must be required
        """
        # with
        board = EditorialBoard.objects.create(issue=self.issue)
        role = editorial_modelfactories.RoleTypeFactory.create(name="The Pickles")
        l1 = modelfactories.LanguageFactory.create(iso_code='pt', name='portuguese')
        l2 = modelfactories.LanguageFactory.create(iso_code='ar', name='arabic')
        l3 = modelfactories.LanguageFactory.create(iso_code='fr', name='french')

        # add perms
        perm_change_roletype = _makePermission(perm='change_roletype', model='roletype')
        self.user.user_permissions.add(perm_change_roletype)
        pre_submittion_audit_logs_count = AuditLogEntry.objects.all().count()

        data = [
            {'name': u'Os Picles', 'language': l1},
            {'name': u'Ahmet Al Picle', 'language': l2},
            {'name': u'Le Piclé', 'language': l3},
        ]

        # when
        response = self.app.get(reverse("editorial.role.translate", args=[self.journal.id, role.id]), user=self.user)
        form = response.forms['role-translations-form']
        for x in xrange(0, 3):
            form['role-translations-formset-%s-name' % x] = data[x]['name']
            form.set('role-translations-formset-%s-language' % x, data[x]['language'].pk)

        response = form.submit()
        # then
        self.assertTemplateUsed(response, 'board/role_type_translate.html')
        self.assertFalse(response.context['formset'].is_valid())
        expected_errors = [u'At least Portuguese and Spanish translations are required']
        self.assertEqual(response.context['formset'].non_form_errors(), expected_errors)
        self.assertIn('Check mandatory fields.', response.body)
        # check audit log
        self.assertEqual(pre_submittion_audit_logs_count, 0)
        audit_entries = AuditLogEntry.objects.all()
        self.assertEqual(audit_entries.count(), 0)
