"""
Template tags and helper functions for displaying breadcrumbs in page titles
based on the current micro site.
"""
from django import template
from django.conf import settings
from microsite_configuration import microsite
from django.templatetags.static import static
from django.template.response import TemplateResponse
import third_party_auth

register = template.Library()


def page_title_breadcrumbs(*crumbs, **kwargs):
    """
    This function creates a suitable page title in the form:
    Specific | Less Specific | General | edX
    It will output the correct platform name for the request.
    Pass in a `separator` kwarg to override the default of " | "
    """
    separator = kwargs.get("separator", " | ")
    if crumbs:
        return u'{}{}{}'.format(separator.join(crumbs), separator, platform_name())
    else:
        return platform_name()


@register.simple_tag(name="page_title_breadcrumbs", takes_context=True)
def page_title_breadcrumbs_tag(context, *crumbs):
    """
    Django template that creates breadcrumbs for page titles:
    {% page_title_breadcrumbs "Specific" "Less Specific" General %}
    """
    return page_title_breadcrumbs(*crumbs)


@register.simple_tag(name="platform_name")
def platform_name():
    """
    Django template tag that outputs the current platform name:
    {% platform_name %}
    """
    return microsite.get_value('platform_name', settings.PLATFORM_NAME)


@register.simple_tag(name="favicon_path")
def favicon_path(default=getattr(settings, 'FAVICON_PATH', 'images/favicon.ico')):
    """
    Django template tag that outputs the configured favicon:
    {% favicon_path %}
    """
    return static(microsite.get_value('favicon_path', default))


@register.simple_tag(name="microsite_css_overrides_file")
def microsite_css_overrides_file():
    """
    Django template tag that outputs the css import for a:
    {% microsite_css_overrides_file %}
    """
    file_path = microsite.get_value('css_overrides_file', None)
    if file_path is not None:
        return "<link href='{}' rel='stylesheet' type='text/css'>".format(static(file_path))
    else:
        return ""


@register.simple_tag(name="third_party_auth_links", takes_context=True)
def third_party_auth_links(context):
    """
    Django template tag that outputs the third party auth links for sudo page.
    {% third_party_auth_links %}
    """
    if third_party_auth.is_enabled():
        from student.helpers import auth_pipeline_urls, get_next_url_for_login_page

        request = context['request']
        redirect_to = get_next_url_for_login_page(request)
        third_party_auth_context = {
            'pipeline_url': auth_pipeline_urls(third_party_auth.pipeline.AUTH_ENTRY_SUDO, redirect_url=redirect_to),
            'providers': third_party_auth.provider.Registry.enabled(),
        }
        response = TemplateResponse(request, 'sudo/third_party_auth_links.html', third_party_auth_context).render()

        return response.content

    return ""


@register.filter
def get_pipeline_url(pipeline_url_dict, key):
    """
    Django template filter to get dict value.
    """
    return pipeline_url_dict.get(key)
