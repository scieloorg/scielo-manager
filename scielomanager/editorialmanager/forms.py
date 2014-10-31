#coding: utf-8

from django import forms
from . import models
from django.utils.translation import ugettext_lazy as _
from journalmanager.models import Issue, Journal


class EditorialMemberForm(forms.ModelForm):
    class Meta:
        model = models.EditorialMember
        exclude = ('board', 'order', )
        widgets = {
            'role': forms.Select(attrs={'class': 'chzn-select'}),
        }


DIRECTION_CHOICES = (
    ('up', "Up"),
    ('down', "Down"),
)


class BoardMoveForm(forms.Form):
    journal_pk = forms.IntegerField(_('journal id'))
    issue_pk = forms.IntegerField(_('issue id'))
    board_pk = forms.IntegerField(_('board id'))
    role_name = forms.CharField(_('role name'))
    role_position = forms.IntegerField(_('current role position'))
    direction = forms.ChoiceField(choices=DIRECTION_CHOICES)

    def _obj_exists(self, model_class, lookup):
        if not model_class.objects.filter(**lookup).exists():
            raise forms.ValidationError(u"Looking for a %s with pk: %s value, does not exist" % (unicode(model_class), obj_key))
        return lookup.values()[0]

    def clean_journal_pk(self):
        journal_pk = self.cleaned_data['journal_pk']
        return self._obj_exists(Journal, lookup={'pk': journal_pk})

    def clean_issue_pk(self):
        issue_pk = self.cleaned_data['issue_pk']
        return self._obj_exists(Issue, lookup={'pk': issue_pk})

    def clean_board_pk(self):
        board_pk = self.cleaned_data['board_pk']
        return self._obj_exists(models.EditorialBoard, lookup={'pk': board_pk})

    def clean_role_name(self):
        role_name = self.cleaned_data['role_name']
        return self._obj_exists(models.RoleType, lookup={'name': role_name})

    def clean(self):
        cleaned_data = super(BoardMoveForm, self).clean()
        journal_pk = cleaned_data.get("journal_pk")
        issue_pk = cleaned_data.get("issue_pk")
        board_pk = cleaned_data.get("board_pk")
        role_name = cleaned_data.get("role_name")
        role_position = cleaned_data.get("role_position")
        direction = cleaned_data.get("direction")

        # check issue and journal are related correctly
        issue = Issue.objects.get(pk=issue_pk)
        if issue.journal.pk != journal_pk:
            raise forms.ValidationError(u"Journal (pk=%s) and Issue (pk=%s) submitted are not related" % (journal_pk, issue_pk))

        # check issue and board are related correctly
        board = models.EditorialBoard.objects.get(pk=board_pk)
        members = board.editorialmember_set.all()
        if issue.pk != board.issue.pk:
            raise forms.ValidationError(u"Board (pk=%s) and Issue (pk=%s) submitted are not related" % (board_pk, issue_pk))

        # direction of move is possible?
        if members.count() > 0:
            if role_position == 1 and direction == "up": # nope nope nope, error
                raise forms.ValidationError(u"These members are at top, cannot move it upper")
            if role_position == members.count() and direction == "down": # nope nope nope, error
                raise forms.ValidationError(u"These members are at bottom, cannot move it down")

        # role name are correct
        role_names = [m.role.name for m in members]
        if role_name not in role_names:
            raise forms.ValidationError(u"Board (pk=%s) and Role (name='%s') submitted aren't related" % (board_pk, role_name))

        return cleaned_data


class RoleTypeForm(forms.ModelForm):
    class Meta:
        model = models.RoleType
