from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _


register = template.Library()


def user_collections_dashboard(collections, user):
    html = ''

    for collection in collections:
        is_default = collection.is_default_to_user(user)

        classname = u'dropdown active' if is_default else u'dropdown'
        name = collection.name
        edit_url = reverse('collection.edit', args=[collection.pk])
        edit_label = _('Edit')

        activation_label = _('Activate')
        activation_url = reverse('usercollection.toggle_active',
            args=[user.pk, collection.pk])

        if not is_default:
            activation_snippet = u"""
            <li id="activate-{lowercase_name}">
                <a href="{activation_url}">
                  <i class="icon-ok-circle"></i> {activation_label}
                </a>
            </li>
            """.format(activation_url=activation_url,
                       activation_label=activation_label,
                       lowercase_name=name.lower()).strip()
        else:
            activation_snippet = u"""
            <li class="disabled" id="activate-{lowercase_name}">
                <i class="icon-ok-circle"></i> {activation_label}
            </li>
            """.format(activation_url=activation_url,
                       activation_label=activation_label,
                       lowercase_name=name.lower()).strip()

        if collection.is_managed_by_user(user):
            html_edit = u"""<li id="edit-{lowercase_name}">
                              <a href="{edit_url}">
                                <i class="icon-edit"></i> {edit_label}
                              </a>
                            </li>""".format(edit_url=edit_url,
                                            edit_label=edit_label,
                                            lowercase_name=name.lower()
                                            ).strip()
        else:
            html_edit = u"""<li class="disabled" id="edit-{lowercase_name}">
                              <i class="icon-edit"></i> {edit_label}
                            </li>""".format(edit_url=edit_url,
                                            edit_label=edit_label,
                                            lowercase_name=name.lower(),
                                            ).strip()


        html_snippet = u"""
        <li id="{lowercase_name}" class="{classname}">
          <a class="dropdown-toggle" data-toggle="dropdown" href="#">
            {name}
            <b class="caret"></b>
          </a>
          <ul class="dropdown-menu">
            {html_edit}
            {activation_snippet}
          </ul>
        </li>
    """.format(classname=classname,
               name=name,
               activation_snippet=activation_snippet,
               lowercase_name=name.lower(),
               html_edit=html_edit
        ).strip()

        html += html_snippet

    return html

register.simple_tag(user_collections_dashboard)
