from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _


register = template.Library()


def user_collections_dashboard(collections, user):
    html = ''

    for collection in collections:
        is_default = collection.is_default_to_user(user)

        classname = 'dropdown active' if is_default else 'dropdown'
        name = collection.name
        edit_url = reverse('collection.edit', args=[collection.pk])
        edit_label = _('Edit')

        if not is_default:
            activation_url = reverse('usercollection.toggle_active',
                args=[user.pk, collection.pk])
            activation_label = _('Activate')

            activation_snippet = """
            <li>
                <a href="{activation_url}">
                  <i class="icon-ok-circle"></i> {activation_label}
                </a>
            </li>
            """.format(activation_url=activation_url,
                       activation_label=activation_label).strip()
        else:
            activation_snippet = ''

        html_snippet = """
        <li class="{classname}">
          <a class="dropdown-toggle" data-toggle="dropdown" href="#">
            {name}
            <b class="caret"></b>
          </a>
          <ul class="dropdown-menu">
            <li>
              <a href="{edit_url}">
                <i class="icon-edit"></i> {edit_label}
              </a>
            </li>
            {activation_snippet}
          </ul>
        </li>
    """.format(classname=classname,
               name=name,
               edit_url=edit_url,
               edit_label=edit_label,
               activation_snippet=activation_snippet,
        ).strip()

        html += html_snippet

    return html

register.simple_tag(user_collections_dashboard)
