# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'game', views.GameViewSet)
router.register(r'player', views.PlayerViewSet)
router.register(r'company', views.CompanyViewSet)
router.register(r'playershare', views.PlayerShareViewSet)
router.register(r'companyshare', views.CompanyShareViewSet)

urlpatterns = [
    url(r'^transfer_money/$', views.TransferMoneyView.as_view(),
        name='transfer_money'),
    url(r'^transfer_share/$', views.TransferShareView.as_view(),
        name='transfer_share'),
    url(r'^', include(router.urls)),
]
