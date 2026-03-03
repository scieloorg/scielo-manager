# coding: utf-8
import factory

from maintenancewindow import models


class EventFactory(factory.Factory):
    FACTORY_FOR = models.Event

    title = 'Manutenção em servidor'
    begin_at = '2012-11-12 14:00:00.000000'
    end_at = '2012-11-12 14:01:00.000000'
    description = 'Troca de memória RAM'
