# -*- coding: utf-8 -*-

from django.conf.urls import url

from chloroform.views import (
    ChloroformView,
    ChloroformSuccessView,
)

urlpatterns = [
    url('^$',
        ChloroformView.as_view(),
        name='default-chloroform'),
    url('^success/$',
        ChloroformSuccessView.as_view(),
        name='default-chloroform-success'),
    url('^(?P<configuration>\w+)/$',
        ChloroformView.as_view(),
        name='chloroform'),
    url('^(?P<configuration>\w+)/success/$',
        ChloroformSuccessView.as_view(),
        name='chloroform-success'),
]
