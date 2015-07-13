# coding: utf-8

import factory

from editorialmanager import models
from journalmanager.tests.modelfactories import IssueFactory, LanguageFactory


class EditorialBoardFactory(factory.Factory):
    FACTORY_FOR = models.EditorialBoard

    issue = factory.SubFactory(IssueFactory)


class RoleTypeFactory(factory.Factory):
    FACTORY_FOR = models.RoleType

    name = factory.Sequence(lambda n: "Role_%s" % n)


class RoleTypeTranslationFactory(factory.Factory):
    FACTORY_FOR = models.RoleTypeTranslation

    role = factory.SubFactory(RoleTypeFactory)
    name = factory.Sequence(lambda n: "Role_%s" % n)
    language = factory.SubFactory(LanguageFactory)


class EditorialMemberFactory(factory.Factory):
    FACTORY_FOR = models.EditorialMember

    role = factory.SubFactory(RoleTypeFactory)
    board = factory.SubFactory(EditorialBoardFactory)

    # Required fields
    first_name = factory.Sequence(lambda n: "first_name_%s" % n)
    last_name = factory.Sequence(lambda n: "last_name_%s" % n)
    email = factory.Sequence(lambda n: "email%s@example.com" % n)

    institution = factory.Sequence(lambda n: "institution_%s" % n)
    link_cv = factory.Sequence(lambda n: "http://buscatextual.cnpq.br/?id_%s" % n)
    city = factory.Sequence(lambda n: 'city_%s' % n)
    state = factory.Sequence(lambda n: 'state_%s' % n)
    country = 'BR'
    research_id = factory.Sequence(lambda n: 'A-%04d-2014' % int(n))
    orcid = factory.Sequence(lambda n: '0000-0002-4668-7157')  # por padrão um orcid válido
