# -*- coding: utf-8 -*-
from rest_framework import viewsets

from . import models, serializers

class GameViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the default methods and an additional 'create'
    view.
    """
    queryset = models.Game.objects.all()
    serializer_class = serializers.GameSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = models.Player.objects.all()
    serializer_class = serializers.PlayerSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer
