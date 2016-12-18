# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'game', views.GameViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
