#coding: utf-8
import logging
import json
import datetime

from django.db import close_connection
from celery.result import AsyncResult

from journalmanager import tasks
from thrift import spec
from scielomanager import connectors
from journalmanager.models import Journal, Issue, Collection
from editorialmanager.models import EditorialBoard
from django.core.exceptions import ObjectDoesNotExist

LOGGER = logging.getLogger(__name__)
ARTICLE_ES_CLIENT = connectors.ArticleElasticsearch()

TODAY = datetime.datetime.now().isoformat()[:10]
LIMIT = 100

ERRNO_NS = {
        'IntegrityError': 1,
        'ValueError': 2,
}


def resource_cleanup(tocall):
    """ O Celery vaza recursos de conexão com o BD quando utiliza o ORM como
    backend de tarefas. Além disso, o próprio ORM do Django utiliza o signal
    `request_finished` para disparar a rotina `django.db.close_connection`, e
    como a interface RPC é dissociada dos ciclos convencionais de
    request/response, devemos executar essa limpeza manualmente.
    """
    def wrapper(*args, **kwargs):
        try:
            return tocall(*args, **kwargs)
        finally:
            close_connection()

    return wrapper


def article_from_es(data):
    """
    Get an instance of `spec.Article` from Elasticsearch datastructure.
    """

    article = spec.Article(abbrev_journal_title=data.get('abbrev_journal_title'),
            epub=data.get('epub'), ppub=data.get('ppub'), volume=data.get('volume'),
            issue=data.get('issue'), year=data.get('year'), doi=data.get('doi'),
            pid=data.get('pid'), aid=data.get('aid'), head_subject=data.get('head_subject'),
            article_type=data.get('article_type'), version=data.get('version'),
            is_aop=data.get('is_aop'), source=data.get('source'),
            timestamp=data.get('timestamp'))

    article.links_to = [spec.RelatedArticle(aid=rel.get('aid'), type=rel.get('type'))
                        for rel in data.get('links_to', [])]

    article.referrers = [spec.RelatedArticle(aid=rel.get('aid'), type=rel.get('type'))
                         for rel in data.get('referrers', [])]

    return article


def journal_mission_from_model(data):

    journal_mission = spec.JournalMission(
        language=data.language.iso_code,
        description=data.description

    )

    return journal_mission


def use_license_from_model(data):

    use_license = spec.UseLicense(
        license_code=data.license_code,
        reference_url=data.reference_url,
        disclaimer=data.disclaimer,
        is_default=data.is_default

    )

    return use_license


def collection_from_model(data):
    """
    Get an instance of `spec.Collection` from models.collection instance.
    """

    try:
        journals = data.journal_set.all()
    except ObjectDoesNotExist:
        journals = []

    collection = spec.Collection(
        id=data.pk,
        name=data.name,
        name_slug=data.name_slug,
        url=data.url,
        acronym=data.acronym,
        country=data.country,
        state=data.state,
        city=data.city,
        address=data.address,
        address_number=data.address_number,
        address_complement=data.address_complement,
        zip_code=data.zip_code,
        phone=data.phone,
        fax=data.fax,
        email=data.email,
        journals=[i.pk for i in journals]
    )

    return collection


def journal_from_model(data):
    """
    Get an instance of `spec.Journal` from models.journal instance.
    """

    journal = spec.Journal(
        id=data.pk,
        title=data.title,
        title_iso=data.title_iso,
        short_title=data.short_title,
        medline_title=data.medline_title,
        medline_code=data.medline_code,
        twitter_user=data.twitter_user,
        study_areas=[i.study_area for i in data.study_areas.all()],
        subject_categories=[i.term for i in data.subject_categories.all()],
        use_license=use_license_from_model(data.use_license),
        created=data.created.isoformat(),
        updated=data.updated.isoformat(),
        acronym=data.acronym,
        scielo_issn=data.scielo_pid,
        print_issn=data.print_issn,
        electronic_issn=data.eletronic_issn,
        frequency=data.frequency,
        copyrighter=data.copyrighter,
        url_online_submission=data.url_online_submission,
        url_journal=data.url_journal,
        notes=data.notes,
        is_trashed=data.is_trashed,
        is_indexed_scie=data.is_indexed_scie,
        is_indexed_ssci=data.is_indexed_ssci,
        is_indexed_aehci=data.is_indexed_aehci,
        missions=[journal_mission_from_model(i) for i in data.missions.all()],
        issues=[i.pk for i in data.issue_set.all()]
    )

    return journal


def issue_title_from_model(data):

    issue_title = spec.IssueTitle(
        language=data.language.iso_code,
        title=data.title
    )

    return issue_title


def editorial_board_member_from_model(data):
    """
    Get an instance of `spec.EditorialBoardMember` from
    models.editorial_members instance.
    """

    editorial_board_member = spec.EditorialBoardMember(
        first_name=data.first_name,
        last_name=data.last_name,
        city=data.city,
        country=data.country.code,
        state=data.state,
        email=data.email,
        research_id=data.research_id,
        orcid=data.orcid,
        link_cv=data.link_cv,
        role=data.role.name,
        order=data.order,
        institution=data.institution
    )

    return editorial_board_member


def issue_from_model(data):
    """
    Get an instance of `spec.Issue` from models.issue instance.
    """

    try:
        eb = data.editorialboard.editorialmember_set.all()
    except ObjectDoesNotExist:
        eb = []

    try:
        it = data.issuetitle_set.all()
    except ObjectDoesNotExist:
        it = []

    issue = spec.Issue(
        id=data.pk,
        journal=journal_from_model(data.journal),
        volume=data.volume,
        number=data.number,
        created=data.created.isoformat(),
        updated=data.updated.isoformat(),
        publication_start_month=data.publication_start_month,
        publication_end_month=data.publication_end_month,
        publication_year=data.publication_year,
        publication_date=str(data.publication_date),
        use_license=use_license_from_model(data.use_license),
        label=data.label,
        order=data.order,
        type=data.type,
        suppl_text=data.suppl_text,
        spe_text=data.spe_text,
        identification=data.identification,
        issue_title=[issue_title_from_model(i) for i in it],
        articles=[i.aid for i in data.articles.all()],
        editorial_board=[editorial_board_member_from_model(i) for i in eb]
    )

    return issue


class RPCHandler(object):
    """Implementação do serviço `JournalManagerServices`.
    """
    @resource_cleanup
    def addArticle(self, xml_string, overwrite):
        try:
            delayed_task = tasks.create_article_from_string.delay(
                    xml_string, overwrite_if_exists=overwrite)
            return delayed_task.id

        except Exception as exc:
            LOGGER.exception(exc)
            raise spec.ServerError()

    @resource_cleanup
    def getTaskResult(self, task_id):
        async_result = AsyncResult(task_id)
        can_forget = async_result.ready()

        try:
            try:
                result = async_result.result
                if isinstance(result, Exception):
                    result_cls_name = result.__class__.__name__
                    try:
                        errno = ERRNO_NS[result_cls_name]
                    except KeyError:
                        LOGGER.error('Undefined errno: %s', result_cls_name)
                        raise spec.ServerError()

                    value = [errno, result.message]
                else:
                    value = result

            except Exception as exc:
                LOGGER.exception(exc)
                raise spec.ServerError()

            status = getattr(spec.ResultStatus, async_result.status)
            return spec.AsyncResult(status=status, value=json.dumps(value))

        finally:
            if can_forget:
                async_result.forget()
                LOGGER.info('Forgot the result of task %s', task_id)

    def scanArticles(self, es_dsl_query):
        try:
            return ARTICLE_ES_CLIENT.scan(es_dsl_query)

        except connectors.exceptions.BadRequestError:
            raise spec.BadRequestError()

        except connectors.exceptions.TimeoutError:
            raise spec.TimeoutError()

        except Exception as exc:
            LOGGER.exception(exc)
            raise spec.ServerError()

    def getScanArticlesBatch(self, batch_id):
        try:
            next_id, batch = ARTICLE_ES_CLIENT.scroll(batch_id)

        except connectors.exceptions.BadRequestError:
            raise spec.BadRequestError()

        except connectors.exceptions.TimeoutError:
            raise spec.TimeoutError()

        except Exception as exc:
            LOGGER.exception(exc)
            raise spec.ServerError()

        articles = [article_from_es(data) for data in batch]

        results = spec.ScanArticlesResults()
        if articles:
            results.articles = articles
        if next_id:
            results.next_batch_id = next_id

        return results

    def getInterfaceVersion(self):
        return spec.VERSION

    @resource_cleanup
    def addArticleAsset(self, aid, filename, content, meta):
        try:
            delayed_task = tasks.create_articleasset_from_bytes.delay(
                    aid, filename, content, meta.owner, meta.use_license)
            return delayed_task.id

        except Exception as exc:
            LOGGER.exception(exc)
            raise spec.ServerError()

    def getJournal(self, journal_id):

        try:
            data = Journal.objects.get(pk=journal_id)
            return journal_from_model(data)
        except Journal.DoesNotExist:
            raise spec.DoesNotExist()
        except Exception as exc:
            LOGGER.ServerError(exc)
            raise spec.Server()

    def getIssue(self, issue_id):

        try:
            data = Issue.objects.get(pk=issue_id)
            return issue_from_model(data)
        except Issue.DoesNotExist:
            raise spec.DoesNotExist()
        except Exception as exc:
            LOGGER.ServerError(exc)
            raise spec.Server()

    def getCollection(self, collection_id):

        try:
            data = Collection.objects.get(pk=collection_id)
            return collection_from_model(data)
        except Collection.DoesNotExist:
            raise spec.DoesNotExist()
        except Exception as exc:
            LOGGER.ServerError(exc)
            raise spec.Server()

    def getJournals(self, collection_id, from_date, until_date, limit, offset):
        query = {}
        limit = limit or LIMIT
        offset = offset or 0

        if from_date or until_date:
            from_date = from_date or '0001-01-01'
            until_date = until_date or TODAY
            query = {
                "created__range": [from_date, until_date]
            }

        if collection_id:
            query['collections__pk'] = collection_id

        try:
            data = [journal_from_model(i) for i in Journal.objects.filter(**query)[offset:offset+limit]]
        except Exception as exc:
            LOGGER.ServerError(exc)
            raise spec.Server()

        return data

    def getIssues(self, journal_id, from_date, until_date, limit, offset):
        query = {}
        limit = limit or LIMIT
        offset = offset or 0

        if from_date or until_date:
            from_date = from_date or '0001-01-01'
            until_date = until_date or TODAY
            query = {
                "created__range": [from_date, until_date]
            }

        if journal_id:
            query['journal__pk'] = journal_id

        try:
            data = [issue_from_model(i) for i in Issue.objects.filter(**query)[offset:offset+limit]]
        except Exception as exc:
            LOGGER.ServerError(exc)
            raise spec.Server()

        return data

    def getCollections(self, from_date, until_date, limit, offset):
        query = {}
        limit = limit or LIMIT
        offset = offset or 0

        if from_date or until_date:
            from_date = from_date or '0001-01-01'
            until_date = until_date or TODAY
            query = {
                "created__range": [from_date, until_date]
            }

        try:
            data = [collection_from_model(i) for i in Collection.objects.filter(**query)[offset:offset+limit]]
        except Exception as exc:
            LOGGER.ServerError(exc)
            raise spec.Server()

        return data