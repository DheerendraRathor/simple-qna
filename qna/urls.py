# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import *  # NOQA
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from ajax_select import urls as ajax_select_urls

from accounts.forms import SignupFormExtra
from forum.views import toggle_follow_user

admin.autodiscover()

urlpatterns = i18n_patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),  # NOQA
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': {'cmspages': CMSSitemap}}),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^ajax_select/', include(ajax_select_urls)),
    url(r'^accounts/signup/$', 'userena.views.signup', {'signup_form': SignupFormExtra}),
    url(r'^accounts/', include('userena.urls')),
    url(r'^toggle-follow/(?P<model_name>user)/(?P<object_id>\d+)/$', toggle_follow_user),
    url(r'^', include('followit.urls')),
    url(r'^', include('cms.urls')),

)

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',  # NOQA
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        ) + staticfiles_urlpatterns() + urlpatterns  # NOQA
