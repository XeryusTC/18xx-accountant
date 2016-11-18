# -*- coding: utf-8 -*-
from django.conf.urls import url

from game import views

urlpatterns = [
    url('^$', views.HomepageView.as_view(), name='start'),
]
