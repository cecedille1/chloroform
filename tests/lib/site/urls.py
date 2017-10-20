# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url('^admin/', include(admin.site.urls)),
    url('^cl/', include('chloroform.urls')),
]
