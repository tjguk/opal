"""
Core OPAL URlconfs
"""
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from opal.utils import camelcase_to_underscore
from opal import views
from opal.core import api, subrecords
from opal.forms import ChangePasswordForm

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view()),

    url(r'^accounts/login/$', views.check_password_reset, name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/change-password/?$', 'django.contrib.auth.views.password_change',
        {'post_change_redirect': '/', 'password_change_form': ChangePasswordForm},
        name='change-password'),
    url(r'^accounts/templates/account_detail.html',
        views.AccountDetailTemplateView.as_view()),
    url(r'^accounts/banned', views.BannedView.as_view(), name='banned'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^episode/(?P<pk>\d+)/actions/copyto/(?P<category>[a-zA-Z_\-]+)/?$',
        views.EpisodeCopyToCategoryView.as_view()),

    # Template vires
    url(r'^templates/patient_list.html/(?P<slug>[0-9a-z_\-]+)/?$', views.PatientListTemplateView.as_view(), name="patient_list_template_view"),

    url(r'^templates/patient_detail.html$',
        views.PatientDetailTemplateView.as_view(), name="patient_detail"),
    url(r'^templates/episode_detail.html/(?P<pk>\d+)/?$',
        views.EpisodeDetailTemplateView.as_view(), name="episode_detail"),

    url(r'^templates/modals/undischarge.html/?$',
        views.UndischargeTemplateView.as_view(),
        name="undischarge_tempate_view"
        ),
    url(r'^templates/modals/hospital_number.html/?$',
        views.HospitalNumberTemplateView.as_view()),
    url(r'^templates/modals/reopen_episode.html/?$',
        views.ReopenEpisodeTemplateView.as_view()),
    url(r'^templates/modals/discharge_episode.html/?$',
        views.DischargeEpisodeTemplateView.as_view()),
    url(r'^templates/modals/copy_to_category.html/?$',
        views.CopyToCategoryTemplateView.as_view()),

    url(r'^templates/modals/delete_item_confirmation.html/?$',
        views.DeleteItemConfirmationView.as_view()),

    # New Public facing API urls
    url(r'api/v0.1/', include(api.router.urls)),
    url(r'^templates/record/(?P<model>[a-z_\-]+).html$',
        views.RecordTemplateView.as_view(), name="record_view"),
    url(r'^templates/forms/(?P<model>[a-z_\-]+).html/?$',
        views.FormTemplateView.as_view(), name="form_view"),
    url(r'^design-patterns/$', TemplateView.as_view(template_name='design_patterns.html'),
        name='design_patterns'),

)


# Generated subrecord template views
for subrecord_model in subrecords.subrecords():
    sub_url = subrecord_model.get_api_name()
    url_name = "{}_modal".format(sub_url)
    urlpatterns += patterns(
        '',
        url(r'^templates/modals/%s.html/?$' % sub_url,
            views.ModalTemplateView.as_view(),
            {'model': subrecord_model},
            name=url_name
        ),
        url(r'^templates/modals/%s.html/(?P<list>[0-9a-z_\-]+/?)$' % sub_url,
            views.ModalTemplateView.as_view(),
            {'model': subrecord_model},
            name=url_name
        ),
    )


urlpatterns += staticfiles_urlpatterns()

from opal.core import plugins

for plugin in plugins.plugins():
    urlpatterns += plugin.urls

urlpatterns += patterns(
    '',
    url(
        r'templates/(?P<template_name>[0-9a-z_/]+.html)',
        views.RawTemplateView.as_view(),
        name="raw_template_view"
    )
)
