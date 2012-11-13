# coding: utf-8
import factory

from maintenancewindow import models


class EventFactory(factory.Factory):
    FACTORY_FOR = models.Event

    title = u'Manutenção em servidor'
    begin_at = u'2012-11-12 14:00:00.000000'
    end_at = u'2012-11-12 14:01:00.000000'
    description = u'Troca de memória RAM'
