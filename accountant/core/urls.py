# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from . import views
from . import routers

router = routers.HybridRouter()
router.register(r'game', views.GameViewSet)
router.register(r'player', views.PlayerViewSet, base_name='player')
router.register(r'company', views.CompanyViewSet, base_name='company')
router.register(r'playershare', views.PlayerShareViewSet,
    base_name='playershare')
router.register(r'companyshare', views.CompanyShareViewSet,
    base_name='companyshare')
router.register(r'logentry', views.LogEntryViewSet, base_name='logentry')

router.add_api_view('transfer_money', url(r'^transfer_money/$',
    views.TransferMoneyView.as_view(), name='transfer_money'))
router.add_api_view('transfer_share', url(r'^transfer_share/$',
    views.TransferShareView.as_view(), name='transfer_share'))
router.add_api_view('operate', url(r'^operate/$',
    views.OperateView.as_view(), name='operate'))
router.add_api_view('colors', url(r'^colors/$', views.ColorsView.as_view(),
    name='colors'))
router.add_api_view('undo', url(r'^undo/$', views.UndoRedoView.as_view(),
    name='undo'))

urlpatterns = [
    url(r'^', include(router.urls)),
]
