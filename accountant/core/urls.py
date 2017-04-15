# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from . import views
from . import routers

router = routers.HybridRouter()
router.register(r'game', views.GameViewSet)
router.register(r'player', views.PlayerViewSet, base_name='player')
router.register(r'company', views.CompanyViewSet)
router.register(r'playershare', views.PlayerShareViewSet)
router.register(r'companyshare', views.CompanyShareViewSet)

router.add_api_view('transfer_money', url(r'^transfer_money/$',
    views.TransferMoneyView.as_view(), name='transfer_money'))
router.add_api_view('transfer_share', url(r'^transfer_share/$',
    views.TransferShareView.as_view(), name='transfer_share'))
router.add_api_view('operate', url(r'^operate/$',
    views.OperateView.as_view(), name='operate'))
router.add_api_view('colors', url(r'^colors/$', views.ColorsView.as_view(),
    name='colors'))

urlpatterns = [
    url(r'^', include(router.urls)),
]
