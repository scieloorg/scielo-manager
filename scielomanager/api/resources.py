# coding: utf-8
from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie import fields

from journalmanager.models import Journal


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        excludes = [
            'email',
            'password',
            'is_active',
            'is_staff',
            'is_superuser',
        ]

class JournalResource(ModelResource):
    missions = fields.CharField(readonly=True)

    class Meta:
        queryset = Journal.objects.all()
        resource_name = 'journals'

    def dehydrate_missions(self, bundle):
        return [(mission.language.iso_code, mission.description)
            for mission in bundle.obj.missions.all()]

