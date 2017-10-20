# -*- coding: utf-8 -*-

from django.conf.urls import url, include

urlpatterns = [
    url('^cl/', include('chloroform.urls')),
]
