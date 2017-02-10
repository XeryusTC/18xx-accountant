# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', views.MainPageView.as_view(), name='main'),
    url(r'^game/(?P<uuid>[^/]+)/$', views.GameView.as_view(), name='game'),
    url(r'^game/(?P<uuid>[^/]+)/add-player/$', views.AddPlayerView.as_view(),
        name='add_player'),
    url(r'^game/(?P<uuid>[^/]+)/add-company/$', views.AddCompanyView.as_view(),
        name='add_company'),
]
