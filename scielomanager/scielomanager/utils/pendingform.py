# coding: utf-8
try:
    from hashlib import md5
except:
    from md5 import new as md5

from django.http import QueryDict

from journalmanager import models as journalmanager_models


class PendingPostData(object):

    def __init__(self, data):
        """
        data is the request.POST QueryDict.
        """
        self.data = data

    def hash_data(self):
        content = ','.join('%s:%s' % (k.encode('utf-8'), v.encode('utf-8')) for k, v in self.data.items())
        return md5(content).hexdigest()

    def pend(self, view_name, user):

        form_hash = self.hash_data()

        pended_form = journalmanager_models.PendedForm.objects.get_or_create(view_name=view_name,
            form_hash=form_hash, user=user)[0]

        for name, values in self.data.lists():
            for value in values:
                pended_form.data.get_or_create(name=name, value=value)

        if self.data.get('form_hash', None) and self.data['form_hash'] != 'None':
            journalmanager_models.PendedForm.objects.get(form_hash=self.data['form_hash']).delete()

        return form_hash

    @classmethod
    def resume(self, form_hash):
        form = journalmanager_models.PendedForm.objects.get(form_hash=form_hash)

        post_dict = QueryDict('', mutable=True)
        for d in form.data.all():
            i = post_dict.setlistdefault(d.name, [])
            i.append(d.value)

        return post_dict
