import datetime
import json
import logging

from waffle.decorators import waffle_flag
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest
from django.template.defaultfilters import slugify

from scielomanager.tools import get_paginated, get_referer_view
from . import models
from .forms import CommentMessageForm, TicketForm
from .balaio import BalaioAPI, BalaioRPC


AUTHZ_REDIRECT_URL = '/accounts/unauthorized/'
MSG_FORM_SAVED = _('Saved.')
MSG_FORM_SAVED_PARTIALLY = _('Saved partially. You can continue to fill in this form later.')
MSG_FORM_MISSING = _('There are some errors or missing data.')
MSG_DELETE_PENDED = _('The pended form has been deleted.')


logger = logging.getLogger(__name__)


@waffle_flag('articletrack')
@permission_required('articletrack.list_checkin', login_url=AUTHZ_REDIRECT_URL)
def checkin_index(request):

    checkins = models.Checkin.userobjects.active()

    objects_pending = get_paginated(checkins.pending(), request.GET.get('pending_page', 1))
    objects_accepted = get_paginated(checkins.accepted(), request.GET.get('accepted_page', 1))

    return render_to_response(
        'articletrack/checkin_list.html',
        {
            'checkins_pending': objects_pending,
            'checkins_accepted': objects_accepted,
        },
        context_instance=RequestContext(request)
    )


@waffle_flag('articletrack')
@permission_required('articletrack.list_checkin', login_url=AUTHZ_REDIRECT_URL)
def checkin_history(request, article_id):

    article = get_object_or_404(models.Article.userobjects.active().select_related('checkins'),
        pk=article_id)

    objects = get_paginated(article.checkins.all(), request.GET.get('page', 1))

    return render_to_response(
        'articletrack/history.html',
        {
            'checkins': objects,
            'first_article': article,
        },
        context_instance=RequestContext(request)
    )


@waffle_flag('articletrack')
@permission_required('articletrack.list_notice', login_url=AUTHZ_REDIRECT_URL)
def notice_detail(request, checkin_id):

    checkin = get_object_or_404(models.Checkin.userobjects.active(), pk=checkin_id)
    notices = checkin.notices.all()

    objects = get_paginated(notices, request.GET.get('page', 1))

    tickets = checkin.article.tickets.all()
    opened_tickets = tickets.filter(finished_at__isnull=True)
    closed_tickets = tickets.filter(finished_at__isnull=False)

    zip_filename =  "%s_%s"% (datetime.date.today().isoformat(), slugify(checkin.article.article_title))

    context = {
        'notices': objects,
        'checkin': checkin,
        'opened_tickets': opened_tickets,
        'closed_tickets': closed_tickets,
        'zip_filename': zip_filename,
    }

    balaio = BalaioAPI()
    files_list = []

    try:

        files = balaio.list_files_members_by_attempt(checkin.attempt_ref)
        if files and not files['error']:
            del files['error']
            for file_extension in files.keys():
                files_list += [{'ext': file_extension, 'name': f} for f in files[file_extension]]

    except ValueError:
        pass # Service Unavailable

    context['files'] = files_list

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

            messages.info(request, MSG_FORM_SAVED)
            return HttpResponseRedirect(reverse('ticket_detail', args=[ticket.id]))
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

            messages.info(request, MSG_FORM_SAVED)
            return HttpResponseRedirect(reverse('ticket_detail', args=[ticket.pk]))
        else:
            context['form'] = ticket_form

    return render_to_response(
        template_name,
        context,
        context_instance=RequestContext(request)
    )


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


@waffle_flag('articletrack')
@login_required
def ajx_set_attempt_proceed_to_checkout(request, attempt_id, checkin_id):
    """
    View function responsible for mark an attempt to checkout process
    """
    if not request.is_ajax():
        return HttpResponse(status=400)

    rpc_client = BalaioRPC()
    rpc_response = rpc_client.call('proceed_to_checkout', [attempt_id,])

    #if the response is True, the checkin must be marked as accepted
    if rpc_response:
        checkin = get_object_or_404(models.Checkin.userobjects.active(), pk=checkin_id)
        try:
            checkin.accept(request.user)
        except ValueError as e:
            logger.info('Could not mark %s as accepted. Traceback: %s' % (checkin, e))
            rpc_response = False

    return HttpResponse(json.dumps(rpc_response), mimetype="application/json")


@waffle_flag('articletrack')
@login_required
def ajx_verify_status_rpc(request):
    """
    View function responsible to check the XML-RPC status
    """
    if not request.is_ajax():
        return HttpResponse(status=400)

    rpc_client = BalaioRPC()
    return HttpResponse(json.dumps({'rpc_status': rpc_client.is_up()}),
        mimetype="application/json")

