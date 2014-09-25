# coding: utf-8
import datetime
import json
import logging
import lxml

from waffle.decorators import waffle_flag
from django.conf import settings
from django.template.loader import render_to_string
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth.decorators import permission_required
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest
from django.template.defaultfilters import slugify
from django.contrib.sites.models import get_current_site

from scielomanager.tools import get_paginated, get_referer_view
from scielomanager import tasks
from . import models
from .forms import CommentMessageForm, TicketForm, CheckinListFilterForm, CheckinRejectForm
from .balaio import BalaioAPI, BalaioRPC
from validator import utils as stylechecker_utils
from .utils import checkin_send_email_by_action, ticket_send_mail_by_action, comment_send_mail_by_action

AUTHZ_REDIRECT_URL = '/accounts/unauthorized/'
MSG_FORM_SAVED = _('Saved.')
MSG_FORM_SAVED_PARTIALLY = _('Saved partially. You can continue to fill in this form later.')
MSG_FORM_MISSING = _('There are some errors or missing data.')
MSG_DELETE_PENDED = _('The pended form has been deleted.')


logger = logging.getLogger(__name__)


def verify_if_user_can_do(action):
    """
    Decorator that check if user.get_profile().can_do(``action``)
    Pre: Exist a request.user with profile
    Post: If can not, will return a message to the user, else: proceed calling the view function:
    something like: def checkin_xxxx(request, checkin_id).
    """
    def decorator(f):
        def decorated(*args, **kwargs):
            request = args[0]
            checkin_id = kwargs['checkin_id']
            user_can, error = request.user.get_profile().can_do(action)
            if user_can:
                return f(*args, **kwargs)
            else:
                messages.error(request, error)
                return HttpResponseRedirect(reverse('notice_detail', args=[checkin_id, ]))

        return decorated
    return decorator


@waffle_flag('articletrack')
@permission_required('articletrack.list_checkin', login_url=AUTHZ_REDIRECT_URL)
def checkin_index(request):

    def filter_queryset_by_form_fields(queryset, form):
        """
        Shortcut function to filter the queryset in both filter-forms: pending and accepted listings
        And assume that both forms have the same fields, because is allways a CheckinListFilterForm
        with different prefix.
        Returns: a filtered queryset.
        """
        if form.is_valid():
            package_name = form.cleaned_data.get('package_name', None)
            article = form.cleaned_data.get('article', None)
            issue_label = form.cleaned_data.get('issue_label', None)

            if package_name:
                queryset = queryset.filter(package_name__icontains=package_name)
            if article:
                queryset = queryset.filter(article=article)
            if issue_label:
                queryset = queryset.filter(article__issue_label__icontains=issue_label)

        return queryset

    pending_filter_form = CheckinListFilterForm(request.GET, prefix="pending")
    rejected_filter_form = CheckinListFilterForm(request.GET, prefix="rejected")
    review_filter_form = CheckinListFilterForm(request.GET, prefix="review")
    accepted_filter_form = CheckinListFilterForm(request.GET, prefix="accepted")

    # get records from db
    checkins_pending = models.Checkin.userobjects.active().pending()
    checkins_rejected = models.Checkin.userobjects.active().rejected()
    checkins_review = models.Checkin.userobjects.active().review()
    checkins_accepted = models.Checkin.userobjects.active().accepted()

    # apply filters from form fields
    checkins_pending = filter_queryset_by_form_fields(checkins_pending, pending_filter_form)
    checkins_rejected = filter_queryset_by_form_fields(checkins_rejected, rejected_filter_form)
    checkins_review = filter_queryset_by_form_fields(checkins_review, review_filter_form)
    checkins_accepted = filter_queryset_by_form_fields(checkins_accepted, accepted_filter_form)

    # paginate resutls
    objects_pending = get_paginated(checkins_pending, request.GET.get('pending_page', 1))
    objects_rejected = get_paginated(checkins_rejected, request.GET.get('rejected_page', 1))
    objects_review = get_paginated(checkins_review, request.GET.get('review_page', 1))
    objects_accepted = get_paginated(checkins_accepted, request.GET.get('accepted_page', 1))

    prefered_tab = 'pending'
    if request.method == "GET" and request.GET.keys() and len(request.GET.keys()) > 0:
        # get the prefix of first querystring parameter (something like: accepted-article), and get that prefix as a prefered tab
        prefered_tab = request.GET.keys()[0].split('-')[0]  # keys are lilke: "prefix-fieldname"
        if prefered_tab not in ['pending', 'rejected', 'review', 'accepted']:
            # maybe the user put something strange in the address bar
            prefered_tab = 'pending'

    return render_to_response(
        'articletrack/checkin_list.html',
        {
            'checkins_pending': objects_pending,
            'checkins_rejected': objects_rejected,
            'checkins_review': objects_review,
            'checkins_accepted': objects_accepted,
            'pending_filter_form': pending_filter_form,
            'rejected_filter_form': rejected_filter_form,
            'review_filter_form': review_filter_form,
            'accepted_filter_form': accepted_filter_form,
            'prefered_tab': prefered_tab,
        },
        context_instance=RequestContext(request)
    )


@waffle_flag('articletrack')
@permission_required('articletrack.list_checkin', login_url=AUTHZ_REDIRECT_URL)
@verify_if_user_can_do('reject')
def checkin_reject(request, checkin_id):
    """
    Excecute checkin.do_reject, obtains the rejection text from the form filled by user.
    """

    checkin = get_object_or_404(models.Checkin.userobjects.active(), pk=checkin_id)

    if checkin.can_be_rejected:
        if request.method == 'POST':
            form = CheckinRejectForm(request.POST)
            if form.is_valid():
                rejected_cause = form.cleaned_data['rejected_cause']
                try:
                    checkin.do_reject(request.user, rejected_cause)
                    messages.success(request, _("Checkin REJECTED succesfully."))
                except ValueError as e:
                    logger.error("ValueError when trying to REJECT the Checkin: (pk: %s). Traceback: %s" % (checkin.pk, e))
                    msg = _("Something went wrong when trying to REJECT this Checkin, please try again later.")
                    messages.error(request, msg)
                    return HttpResponseRedirect(reverse('notice_detail', args=[checkin_id, ]))

                # Send e-mail only exists submitted_by attribute
                checkin_send_email_by_action(checkin, "checkin_reject")

            else:
                form_errors = u", ".join([u"%s %s" % (field, error[0]) for field, error in form.errors.items()])
                error_msg = "%s %s" % (MSG_FORM_MISSING, form_errors)
                messages.error(request, error_msg)
    else:
        error_msg = _("This checkin doesn't comply the requirements to be rejected")
        messages.error(request, error_msg)
    return HttpResponseRedirect(reverse('notice_detail', args=[checkin_id, ]))


@waffle_flag('articletrack')
@permission_required('articletrack.list_checkin', login_url=AUTHZ_REDIRECT_URL)
def checkin_review(request, checkin_id, level):
    """
    Excecute checkin.[do_review_by_level_1|do_review_by_level_2] (depends on ``level`` args),
    and if checkin.can_be_accepted, proceed to accept the checkin (redirect to ``checkin_accept``).
    """
    if level not in ['1','2']:
        msg = _("Trying to REVIEW the checkin, but parameters are wrong")
        messages.error(request, msg)
        return HttpResponseRedirect(reverse('notice_detail', args=[checkin_id, ]))
    else:
        user_can, error = request.user.get_profile().can_do('review_l%s' % level)
        if not user_can:
            messages.error(request, error)
            return HttpResponseRedirect(reverse('notice_detail', args=[checkin_id, ]))

    checkin = get_object_or_404(models.Checkin.userobjects.active(), pk=checkin_id)

    if checkin.can_be_reviewed:
        try:
            if level == '1':
                checkin.do_review_by_level_1(request.user)
            else: # level = '2'
                checkin.do_review_by_level_2(request.user)

            messages.success(request, _("Checkin REVIEWED succesfully."))
        except ValueError as e:
            logger.error("ValueError when trying to REVIEW the Checkin: (pk: %s). Traceback: %s" % (checkin.pk, e))
            msg = _("Something went wrong when trying to REVIEW this Checkin, please try again later.")
            messages.error(request, msg)
            return HttpResponseRedirect(reverse('notice_detail', args=[checkin_id, ]))

        # Send e-mail only if has "submitted_by" attribute
        checkin_send_email_by_action(checkin, "checkin_review")

        if checkin.can_be_accepted:
            return HttpResponseRedirect(reverse('checkin_accept', args=[checkin_id, ]))

    else:
        error_msg = _("This checkin doesn't comply the requirements to be reviewed")
        messages.error(request, error_msg)

    return HttpResponseRedirect(reverse('notice_detail', args=[checkin_id, ]))


@waffle_flag('articletrack')
@permission_required('articletrack.list_checkin', login_url=AUTHZ_REDIRECT_URL)
@verify_if_user_can_do('accept')
def checkin_accept(request, checkin_id):
    """
    Excecute checkin.accept, if checkin can be accepted and Balaio RPC API
    is up, try to proceed to checkout.
    """

    checkin = get_object_or_404(models.Checkin.userobjects.active(), pk=checkin_id)

    if checkin.can_be_accepted:

        try:
            checkin.accept(request.user)
            messages.success(request, _("Checkin ACCEPTED succesfully."))
            # Send e-mail only if has "submitted_by" attribute
        except ValueError as e:
            logger.error("ValueError when trying to ACCEPT the Checkin: (pk: %s). Traceback: %s" % (checkin.pk, e))
            msg = _("Something went wrong when trying to ACCEPT this Checkin, please try again later.")
            messages.error(request, msg)
            return HttpResponseRedirect(reverse('notice_detail', args=[checkin_id, ]))

        # Send e-mail only if has "submitted_by" attribute
        checkin_send_email_by_action(checkin, "checkin_accept")

        # Proceed to Checkout
        if checkin.can_be_scheduled_to_checkout:
            return HttpResponseRedirect(reverse('checkin_send_to_checkout', args=[checkin_id, ]))
    else:
        error_msg = _("This checkin doesn't comply the requirements to be accepted")
        messages.error(request, error_msg)
    return HttpResponseRedirect(reverse('notice_detail', args=[checkin_id, ]))


@waffle_flag('articletrack')
@permission_required('articletrack.list_checkin', login_url=AUTHZ_REDIRECT_URL)
@verify_if_user_can_do('send_to_pending')
def checkin_send_to_pending(request, checkin_id):
    """
    Excecute checkin.send_to_pending, if checkin can be send to pending
    """
    checkin = get_object_or_404(models.Checkin.userobjects.active(), pk=checkin_id)
    if checkin.can_be_send_to_pending:
        try:
            checkin.send_to_pending(request.user)
            messages.success(request, _("Checkin was SENT TO PENDING succesfully."))
        except ValueError as e:
            logger.error("ValueError when trying to SEND TO PENDING the Checkin: (pk: %s). Traceback: %s" % (checkin.pk, e))
            msg = _("Something went wrong when trying to SEND TO PENDING this Checkin, please try again later.")
            messages.error(request, msg)
            return HttpResponseRedirect(reverse('notice_detail', args=[checkin_id, ]))

        # Send e-mail only if has "submitted_by" attribute
        checkin_send_email_by_action(checkin, "checkin_send_to_pending")

    else:
        error_msg = _("This checkin doesn't comply the requirements to be sent to pending")
        messages.error(request, error_msg)
    return HttpResponseRedirect(reverse('notice_detail', args=[checkin_id, ]))


@waffle_flag('articletrack')
@permission_required('articletrack.list_checkin', login_url=AUTHZ_REDIRECT_URL)
@verify_if_user_can_do('send_to_review')
def checkin_send_to_review(request, checkin_id):
    """
    Excecute checkin.send_to_review, if checkin can be send to review
    """

    checkin = get_object_or_404(models.Checkin.userobjects.active(), pk=checkin_id)

    if checkin.can_be_send_to_review:
        try:
            checkin.send_to_review(request.user)
            messages.success(request, _("Checkin was SENT TO REVIEW succesfully."))
        except ValueError as e:
            logger.error("ValueError when trying to SEND TO REVIEW the Checkin: (pk: %s). Traceback: %s" % (checkin.pk, e))
            msg = _("Something went wrong when trying to SEND TO REVIEW this Checkin, please try again later.")
            messages.error(request, msg)
            return HttpResponseRedirect(reverse('notice_detail', args=[checkin_id, ]))

        # Send e-mail only if has "submitted_by" attribute
        checkin_send_email_by_action(checkin, "checkin_send_to_review")

    else:
        error_msg = _("This checkin doesn't comply the requirements to be sent to review")
        messages.error(request, error_msg)
    return HttpResponseRedirect(reverse('notice_detail', args=[checkin_id, ]))


@waffle_flag('articletrack')
@permission_required('articletrack.list_checkin', login_url=AUTHZ_REDIRECT_URL)
@verify_if_user_can_do('send_to_checkout')
def checkin_send_to_checkout(request, checkin_id):
    """
    Excecute checkin.send_to_checkout, if checkin can be send to checkout
    This action will set checkin.status ==  'checkout_scheduled' and then will be
    processed by a scheduled backgroud task. No more user's actions are required.
    """

    checkin = get_object_or_404(models.Checkin.userobjects.active(), pk=checkin_id)

    if checkin.can_be_scheduled_to_checkout:
        checkin.do_schedule_to_checkout(request.user)
        messages.success(request, _("Checkin will proceed to checkout soon!"))

        # Send e-mail only if has "submitted_by" attribute
        checkin_send_email_by_action(checkin, "checkin_send_to_checkout")

    else:
        error_msg = _("This checkin doesn't comply the requirements to be scheduled to checkout")
        messages.error(request, error_msg)

    return HttpResponseRedirect(reverse('notice_detail', args=[checkin_id, ]))


@waffle_flag('articletrack')
@permission_required('articletrack.list_checkin', login_url=AUTHZ_REDIRECT_URL)
def checkin_history(request, checkin_id):
    checkin = get_object_or_404(models.Checkin.userobjects.active(), pk=checkin_id)

    return render_to_response(
        'articletrack/checkin_history.html',
        {
            'checkin': checkin,
        },
        context_instance=RequestContext(request)
    )


@waffle_flag('articletrack')
@permission_required('articletrack.list_notice', login_url=AUTHZ_REDIRECT_URL)
def notice_detail(request, checkin_id):

    checkin = get_object_or_404(models.Checkin.userobjects.active(), pk=checkin_id)
    notices = checkin.notices.exclude(status__istartswith="serv_")
    tickets = checkin.article.tickets.all()
    opened_tickets = tickets.filter(finished_at__isnull=True)
    closed_tickets = tickets.filter(finished_at__isnull=False)

    profile = request.user.get_profile()
    have_actions_to_do = any(
        [
            profile.can_reject_checkins and checkin.can_be_rejected,
            profile.can_send_checkins_to_pending and checkin.can_be_send_to_pending,
            profile.can_send_checkins_to_review and checkin.can_be_send_to_review,
            profile.can_review_l1_checkins and checkin.can_be_reviewed,
            profile.can_review_l2_checkins and checkin.can_be_reviewed,
            profile.can_accept_checkins and checkin.can_be_accepted,
            profile.can_send_checkins_to_checkout and checkin.can_be_scheduled_to_checkout,
        ]
    )

    zip_filename = "%s_%s" % (datetime.date.today().isoformat(), slugify(checkin.article.article_title))
    reject_form = CheckinRejectForm()
    context = {
        'notices': notices,
        'checkin': checkin,
        'opened_tickets': opened_tickets,
        'closed_tickets': closed_tickets,
        'zip_filename': zip_filename,
        'reject_form': reject_form,
        'have_actions_to_do': have_actions_to_do,
        'packtools_version': stylechecker_utils.PACKTOOLS_VERSION,
    }

    balaio = BalaioAPI()
    files_list = []
    xml_data = {
        'file_name': None,
        'uri': None,
        'can_be_analyzed': (False, ''),
    }

    try:

        files = balaio.list_files_members_by_attempt(checkin.attempt_ref)
        if files and not files['error']:
            del files['error']
            for file_extension in files.keys():
                files_list += [{'ext': file_extension, 'name': f} for f in files[file_extension]]

            xml_data['file_name'] = files['xml'][0]  # assume only ONE xml per package
            xml_data['can_be_analyzed'] = (True, '')
        else:
            xml_data['can_be_analyzed'] = (False, "The package's files could not requested")


    except ValueError as e:
        # Service Unavailable
        logger.error('ValueError while requesting: list_files_members_by_attempt(%s) for checkin.pk == %s. Traceback: %s' % (checkin.attempt_ref, checkin.pk, e))
        xml_data['can_be_analyzed'] = (False, "The package's files could not requested")

    # get stylechecker annotations
    if xml_data['can_be_analyzed'][0]:
        try:
            xml_data['uri'] = balaio.get_xml_uri(checkin.attempt_ref, xml_data['file_name']) if xml_data['file_name'] else None
        except ValueError as e:
            # Service Unavailable
            logger.error('ValueError while requesting: get_xml_uri(%s, %s) for checkin.pk == %s. Traceback: %s' % (checkin.attempt_ref, xml_data['file_name'], checkin.pk, e))
            xml_data['can_be_analyzed'] = (False, 'Could not obtain the XML with this file name %s' % xml_data['file_name'])
        else:
            if bool(xml_data['uri']):
                xml_data['can_be_analyzed'] = (True, "")
            else:
                xml_data['can_be_analyzed'] = (False, "XML's URI is invalid (%s)" % xml_data['uri'])

    if xml_data['can_be_analyzed'][0]:
        results, exc = stylechecker_utils.analyze_xml(xml_data['uri'])
        context['results'] = results
        context['xml_exception'] = getattr(exc, 'message', None)

    context['files'] = files_list
    context['xml_data'] = xml_data

    return render_to_response(
        'articletrack/notice_detail.html',
        context,
        context_instance=RequestContext(request)
    )


@waffle_flag('articletrack')
@permission_required('articletrack.list_ticket', login_url=AUTHZ_REDIRECT_URL)
def ticket_list(request):

    tickets = models.Ticket.userobjects.active()
    objects = get_paginated(tickets, request.GET.get('page', 1))

    return render_to_response(
        'articletrack/ticket_list.html',
        {
            'tickets': objects,
        },
        context_instance=RequestContext(request)
    )


@waffle_flag('articletrack')
@permission_required('articletrack.list_ticket', login_url=AUTHZ_REDIRECT_URL)
def ticket_detail(request, ticket_id, template_name='articletrack/ticket_detail.html'):

    ticket = get_object_or_404(models.Ticket.userobjects.active(), pk=ticket_id)
    comment_form = CommentMessageForm()
    context = {
        'ticket': ticket,
        'form': comment_form,
    }

    if request.method == "POST":

        comment_form = CommentMessageForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.ticket = ticket
            comment.save()

            comment_send_mail_by_action(comment, "comment_created")

            messages.info(request, MSG_FORM_SAVED)
            return render_to_response(
                template_name,
                context,
                context_instance=RequestContext(request)
            )
        else:
            context['form'] = comment_form

    return render_to_response(
        template_name,
        context,
        context_instance=RequestContext(request)
    )


@waffle_flag('articletrack')
@permission_required('articletrack.change_ticket', login_url=AUTHZ_REDIRECT_URL)
def ticket_close(request, ticket_id):

    ticket = get_object_or_404(models.Ticket.userobjects.active(), pk=ticket_id)
    if not ticket.is_open:
        messages.info(request, _("Ticket are already closed"))
        return HttpResponseRedirect(reverse('ticket_detail', args=[ticket.id]))

    ticket.finished_at = datetime.datetime.now()
    ticket.save()

    ticket_send_mail_by_action(ticket, "ticket_close")

    messages.info(request, MSG_FORM_SAVED)

    referer = get_referer_view(request)
    return HttpResponseRedirect(referer)


@waffle_flag('articletrack')
@permission_required('articletrack.add_ticket', login_url=AUTHZ_REDIRECT_URL)
def ticket_add(request, checkin_id, template_name='articletrack/ticket_add.html'):

    checkin = get_object_or_404(models.Checkin.userobjects.active(), pk=checkin_id)
    ticket_form = TicketForm()
    context = {
        'checkin': checkin,
        'form': ticket_form,
    }

    if request.method == "POST":

        ticket_form = TicketForm(request.POST)

        if ticket_form.is_valid():

            ticket = ticket_form.save(commit=False)
            ticket.author = request.user
            ticket.article = checkin.article
            ticket.save()

            ticket_send_mail_by_action(ticket, "ticket_add")

            messages.success(request, MSG_FORM_SAVED)
            return HttpResponseRedirect(reverse('ticket_detail', args=[ticket.id, ]))
        else:
            context['form'] = ticket_form

    return render_to_response(
        template_name,
        context,
        context_instance=RequestContext(request)
    )


@waffle_flag('articletrack')
@permission_required('articletrack.change_ticket', login_url=AUTHZ_REDIRECT_URL)
def ticket_edit(request, ticket_id, template_name='articletrack/ticket_edit.html'):

    ticket = get_object_or_404(models.Ticket.userobjects.active(), pk=ticket_id)

    if not ticket.is_open:
        messages.info(request, _("Closed ticket can't be edited"))
        return HttpResponseRedirect(reverse('ticket_detail', args=[ticket.pk]))

    ticket_form = TicketForm(instance=ticket)
    context = {
        'form': ticket_form,
        'ticket': ticket,
    }

    if request.method == "POST":

        ticket_form = TicketForm(request.POST, instance=ticket)

        if ticket_form.is_valid():

            ticket = ticket_form.save()

            ticket_send_mail_by_action(ticket, "ticket_edit")

            messages.success(request, MSG_FORM_SAVED)
            return HttpResponseRedirect(reverse('ticket_detail', args=[ticket.pk]))
        else:
            context['form'] = ticket_form

    return render_to_response(
        template_name,
        context,
        context_instance=RequestContext(request)
    )


@waffle_flag('articletrack')
@permission_required('articletrack.change_ticket', login_url=AUTHZ_REDIRECT_URL)
def comment_edit(request, comment_id, template_name='articletrack/comment_edit.html'):

    comment = get_object_or_404(models.Comment.userobjects.active(), pk=comment_id)

    if not comment.ticket.is_open:
        messages.info(request, _("Can't edit a comment of a closed ticket"))
        return HttpResponseRedirect(reverse('ticket_detail', args=[comment.ticket.pk]))

    comment_form = CommentMessageForm(instance=comment)
    context = {
        'form': comment_form,
        'comment': comment,
    }

    if request.method == "POST":

        comment_form = CommentMessageForm(request.POST, instance=comment)
        if comment_form.is_valid():
            comment = comment_form.save()

            comment_send_mail_by_action(comment, "comment_edit")

            messages.info(request, MSG_FORM_SAVED)
            return HttpResponseRedirect(reverse('ticket_detail', args=[comment.ticket.pk]))
        else:
            context['form'] = comment_form

    return render_to_response(
        template_name,
        context,
        context_instance=RequestContext(request)
    )


# BALAIO API


@waffle_flag('articletrack')
@permission_required('articletrack.list_ticket', login_url=AUTHZ_REDIRECT_URL)
def get_balaio_api_is_up(request):

    balaio = BalaioAPI()
    is_up = balaio.is_up()
    context = {
        'is_up': is_up,
    }

    if request.is_ajax():
        json_response = json.dumps(context)
        return HttpResponse(json_response, content_type='application/json; charset=UTF-8')
    else:
        raise Http404


@waffle_flag('articletrack')
@permission_required('articletrack.list_ticket', login_url=AUTHZ_REDIRECT_URL)
def get_balaio_api_full_package(request, attempt_id, target_name):
    balaio = BalaioAPI()
    try:
        balaio_response = balaio.get_full_package(attempt_id, target_name)
    except ValueError:
        return HttpResponse(status_code=503)
    else:
        view_response = HttpResponse(balaio_response, content_type='application/zip')
        view_response['Content-Disposition'] = 'attachment; filename="%s.ZIP"' % target_name
        return view_response


@waffle_flag('articletrack')
@permission_required('articletrack.list_ticket', login_url=AUTHZ_REDIRECT_URL)
def get_balaio_api_files_members(request, attempt_id, target_name):
    balaio = BalaioAPI()

    qs_files = request.GET.getlist('file')
    if qs_files:
        try:
            balaio_response = balaio.get_files_members_by_attempt(attempt_id, target_name, qs_files)
        except ValueError:
            return HttpResponse(status_code=503)
        else:
            view_response = HttpResponse(balaio_response, content_type='application/zip')
            view_response['Content-Disposition'] = 'attachment; filename="%s.ZIP"' % target_name
            return view_response
    else:
        return HttpResponseBadRequest()
