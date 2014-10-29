# -*- coding: utf-8 -*-
from django.utils import simplejson as json
from django.utils.translation import ugettext as _
from django.utils.text import get_text_list
from django.utils.encoding import force_unicode
from django.db import models
from django.db.models.query import QuerySet
from django.db.models.fields.files import FieldFile
from django.contrib.contenttypes.models import ContentType
from django.forms import model_to_dict
from django.core import serializers
from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile
from audit_log.models import AuditLogEntry, CHANGE, ADDITION, DELETION
from django.conf import settings


ALWAYS_EXCLUDED_FIELDS = ('password', 'password1', 'password2', 'DELETE', )


def get_auditable_fields(form):
    """
    Return a list of fields name, keeping away some fields such as password or sensible data.

    * if form has a Meta attribute: is_auditable == False, then return an empty list,
        otherwise: the form is considered as an auditable form.
    * if form has a Meta attribute: auditable_fields, then those fields are considered
        otherwise: all changed fields of the form are considered.
    * if form has a Meta attribute: no_auditable_fields, then those fields are excluded
        otherwise: all changed fields of the form are considered.
    * Always the fields listed in ALWAYS_EXCLUDED_FIELDS, are excluded from result.
    """
    is_auditable = getattr(form._meta.model._meta, 'is_auditable', True)
    if is_auditable and form.changed_data:
        auditable_fields = set(form.changed_data)
        explicit_auditable_fields = set(getattr(form._meta, 'auditable_fields', None) or auditable_fields)
        explicit_non_auditable_fields = set(getattr(form._meta, 'no_auditable_fields', []))
        explicit_non_auditable_fields.union(set(ALWAYS_EXCLUDED_FIELDS))
        result = auditable_fields.intersection(explicit_auditable_fields).difference(explicit_non_auditable_fields)
        return list(result)
    else:
        return []


def field_serializer(field_value):
    """
    return the field value ready to be serialized.
    depending of the field type:
        QuerySet, foreign key, file field, image field, etc
    """
    if hasattr(field_value,'get_query_set') or isinstance(field_value, QuerySet):
        # probably is a m2m field, so lets get it with serializer
        field_value = [model_to_dict(m) for m in field_value.all()]
    elif isinstance(field_value, models.Model):
        # is a foreign key, so lets get it with model_to_dict
        field_value = model_to_dict(field_value)
        for k,v in field_value.iteritems():
            field_value[k] = field_serializer(v)
    elif isinstance(field_value, InMemoryUploadedFile) or isinstance(field_value, TemporaryUploadedFile):
        try:
            # new files/images uploaded does not have a path or url already
            field_value = {
                'name': getattr(field_value, 'name',''),
                'size': getattr(field_value, 'size',''),
                'content_type': getattr(field_value, 'content_type',''),
                'charset': getattr(field_value, 'charset',''),
                'encoding': getattr(field_value, 'encoding',''),
            }
        except AttributeError:
            field_value = force_unicode(field_value)
    elif hasattr(field_value,'path') or isinstance(field_value, FieldFile):
        # the field is an image or file. so lets get the file's 'path'
        try:
            field_value = {
                'url': getattr(field_value, 'url',''),
                'path': getattr(field_value, 'path',''),
                'size': getattr(field_value, 'size',''),
                'content_type': getattr(field_value, 'content_type',''),
                'charset': getattr(field_value, 'charset',''),
                'name': getattr(field_value, 'name',''),
                'encoding': getattr(field_value, 'encoding',''),
            }
            if field_value['path']:
                field_value['path'] = field_value['path'].split(settings.MEDIA_ROOT)[1]
        except ValueError:
            # possible the file field is empty (or deleted)
            field_value = force_unicode(field_value)
    else:
        field_value = force_unicode(field_value)
    return field_value


def collect_old_values(obj, form=None, formsets=None, as_json_string=False):
    """
    Collect the "pre save" data into a JSON-compatible structure.
    returns something like this:
    {
        'form_data': {
            *** for each form field edited AND auditable ***
            '<field name 1>': <new field 1 value>,
            '<field name 2>': <new field 2 value>,
            ...
        },
        formsets_data: [
            *** for each formset ***
            {
                'related_name': '<object related model name>',
                'related_objects': [
                    {
                        'pk': related_object.pk,
                        'model': 'app_name.model_name',
                        'fields': {
                            '<field name X>': <new field value X>,
                            '<field name Y>': <new field value Y>,
                            '<field name Z>': <new field value Z>,
                            ...
                        },
                    },
                    ...
                ]
            },
            ...
        ]
    }
    """

    result = {
        "form_data": {},
        "formsets_data": [],
    }
    # request the object from DB, to get the object as persisted in DB
    unsaved_object = obj.__class__.objects.get(pk=obj.pk)

    if form:
        for field_name in get_auditable_fields(form):
            field_value = getattr(unsaved_object, field_name)
            result["form_data"][field_name] = field_serializer(field_value)

    if formsets:
        model_related_objects = {}
        for formset in formsets:
            accessor_name = formset.rel_name
            related_objects = getattr(unsaved_object, accessor_name).all()
            model_related_objects[accessor_name] = related_objects

        for related_name, related_objects in model_related_objects.iteritems():
            result_formset_data = {
                "related_name": related_name,
                "related_objects": [ model_to_dict(r_obj) for r_obj in related_objects]
            }
            result["formsets_data"].append(result_formset_data)

    if as_json_string:
        return json.dumps(result)
    else:
        return result


def collect_new_values(form=None, formsets=None, as_json_string=False):
    """
    Collect the "post save" data into a JSON-compatible structure.
    returns something like this:
    {
        'form_data': {
            '<field name 1>': <new field 1 value>,
            '<field name 2>': <new field 2 value>,
            ...
        },
        formsets_data: [
            # for each formset:
            {
                'added':[
                    {
                        'object_verbose_name': '<object verbose name>',
                        'object_unicode': '<object unicode>',
                        '<field name 1>': <new field 1 value>,
                        '<field name 2>': <new field 2 value>,
                    },
                    ...
                ],
                'changed': [
                    {
                        'object_verbose_name': '<object verbose name>',
                        'object_unicode': '<object unicode>',
                        '<field name X>': <new field X value>,
                        '<field name Y>': <new field Y value>,
                        '<field name Z>': <new field Z value>,
                    },
                    ...
                ],
                'deleted': [
                    {
                        'object_verbose_name': '<object verbose name>',
                        'object_unicode': '<object unicode>',
                    },
                    ...
                ]
            },
            ...
        ]
    }
    """
    result = {
        "form_data": {},
        "formsets_data": [],
    }
    if form:
        for field_name in get_auditable_fields(form):
            field_value = form.cleaned_data[field_name]
            result["form_data"][field_name] = field_serializer(field_serializer(field_value))

    if formsets:
        for formset in formsets:
            formset_data = {
                'added': [],
                'changed': [],
                'deleted': [],
            }
            added_data = []
            # formset NEW objects
            for added_object in formset.new_objects:
                object_values = {
                    'object_verbose_name': force_unicode(added_object._meta.verbose_name),
                    'object_unicode': force_unicode(added_object),
                    'fields': {}
                }
                for field in added_object._meta.local_fields:
                    field_name = field.get_attname()
                    field_value = getattr(added_object, field_name)
                    object_values['fields'][field_name] = field_serializer(field_value)

                added_data.append(object_values)
            formset_data['added'] = added_data

            changed_data = []
            # formset CHANGED objects
            for changed_object, changed_fields in formset.changed_objects:
                object_values = {
                    'object_verbose_name': force_unicode(changed_object._meta.verbose_name),
                    'object_unicode': force_unicode(changed_object),
                    'fields': {}
                }
                for field_name in changed_fields:
                    field_value = getattr(changed_object, field_name)
                    object_values['fields'][field_name] = field_serializer(field_value)

                changed_data.append(object_values)
            formset_data['changed'] = changed_data

            deleted_data = []
            # formset DELETED objects
            for deleted_object in formset.deleted_objects:
                object_values = {
                    'object_verbose_name': force_unicode(deleted_object._meta.verbose_name),
                    'object_unicode': force_unicode(deleted_object),
                }
                deleted_data.append(object_values)
            formset_data['deleted'] = deleted_data

            # save formset data in the results, if any
            if any([added_data, changed_data, deleted_data]):
                result["formsets_data"].append(formset_data)

    if as_json_string:
        return json.dumps(result)
    else:
        return result


def construct_message_from_formset(formsets):
    message = []

    for formset in formsets:
        for added_object in formset.new_objects:
            message.append(_(u'Added %(name)s "%(object)s".')
                                  % {'name': force_unicode(added_object._meta.verbose_name),
                                     'object': force_unicode(added_object)})
        for changed_object, changed_fields in formset.changed_objects:
            message.append(_(u'Changed %(list)s for %(name)s "%(object)s".')
                                  % {'list': get_text_list(changed_fields, _('and')),
                                     'name': force_unicode(changed_object._meta.verbose_name),
                                     'object': force_unicode(changed_object)})
        for deleted_object in formset.deleted_objects:
            message.append(_(u'Deleted %(name)s "%(object)s".')
                                  % {'name': force_unicode(deleted_object._meta.verbose_name),
                                     'object': force_unicode(deleted_object)})
    return message


def construct_change_message(form=None, formsets=None):
    """
    Construct a description text message with a brief explanation of the changes.
    """
    message = []
    if form and form.changed_data:
        message.append(_(u'Changed fields: %s.') % get_text_list(form.changed_data, _('and')))

    if formsets:
        message.extend(construct_message_from_formset(formsets))

    message = u'\n'.join(message)
    return message or _(u'No fields changed.')


def construct_create_message(form=None, formsets=None):
    """
    Construct a "created record" data into a message from a new object.
    """
    message = [u'%s' % force_unicode(field) for field in form.cleaned_data if form]

    if formsets:
        message.extend(construct_message_from_formset(formsets))

    message = u'Added fields:\n' + u'\n'.join(message)
    return message or _(u'No fields added.')


def construct_delete_message(obj):
    return u"Record DELETED (%s, pk: %s): %s" % (
                obj.pk,
                force_unicode(obj._meta.verbose_name),
                force_unicode(obj)
            )


def _do_log(user, obj, action_flag, change_message, old_values='', new_values=''):
    AuditLogEntry.objects.log_action(
        user_id=user.pk,
        content_type_id=ContentType.objects.get_for_model(obj).pk,
        object_id=obj.pk,
        object_repr=force_unicode(obj),
        action_flag=action_flag,
        change_message=change_message,
        old_values=old_values,
        new_values=new_values
    )


def log_delete(user, obj, message):
    """
    Log that obj has been deleted.
    """
    _do_log(user, obj, DELETION, message)


def log_change(user, obj, message, old_values, new_values):
    """
    Log that obj has been changed.
    """
    _do_log(user, obj, CHANGE, message, old_values, new_values)


def log_create(user, obj, message, old_values, new_values):
    """
    Log that obj has been created.
    """
    _do_log(user, obj, ADDITION, message, old_values, new_values)
