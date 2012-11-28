# coding: utf8

from wtforms import (
    fields,
    form
)


class AbstractForm(form.Form):
    language = fields.SelectField('Language', choices=[('pt', 'Portuguese')])
    abstract = fields.TextField('Abstract')


class DatesForm(form.Form):
    thesis = fields.DateField()
    conference = fields.DateField()
    publication = fields.DateField()
    revision = fields.DateField()


class PagesForm(form.Form):
    first = fields.IntegerField()
    last = fields.IntegerField()


class AffiliationForm(form.Form):
    name = fields.TextField('Name')
    divisions = fields.FieldList(fields.TextField(),
                                 min_entries=1)


class AnalyticalAuthorForm(form.Form):
    firstname = fields.TextField('Firstname')
    lastname = fields.TextField('Lastname')
    role = fields.SelectField('Role', choices=[('coord', 'Coordinator')])
    affiliations = fields.FieldList(fields.FormField(AffiliationForm),
                                    min_entries=1)


class CorporateAuthorForm(form.Form):
    institution_name = fields.TextField('Name')
    divisions = fields.FieldList(fields.TextField(),
                                 min_entries=1)


class TitleForm(form.Form):
    language = fields.SelectField('Language', choices=[('pt', 'Portuguese')])
    title = fields.TextField('Title')


class ArticleForm(form.Form):
    analytical_authors = fields.FieldList(fields.FormField(AnalyticalAuthorForm),
                                          min_entries=1)
    corporate_authors = fields.FieldList(fields.FormField(CorporateAuthorForm),
                                         min_entries=1)
    titles = fields.FieldList(fields.FormField(TitleForm), min_entries=1)
    pages = fields.FormField(PagesForm)
    language = fields.SelectField('Language', choices=[('pt', 'Portuguese')])
    dates = fields.FormField(DatesForm)
    publication_city = fields.TextField('City of publication')
    publication_state = fields.TextField('State of publication')
    publication_country = fields.TextField('Country of publication')
    doctopic = fields.TextField('Doctopic')
    abstracts = fields.FieldList(fields.FormField(AbstractForm), min_entries=1)
    created_at = fields.DateField()
    bibliographic_standard = fields.TextField('Bibliographic standard')
    sponsor = fields.TextField()
    type_literature = fields.TextField('Type of literature')
    pid = fields.TextField('PID')
