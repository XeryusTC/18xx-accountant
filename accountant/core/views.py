# -*- coding: utf-8 -*-
from rest_framework import viewsets

from .models import Game
from .serializers import GameSerializer

class GameViewSet(viewsets.ModelViewSet):
    """
    This viewset provides the default methods and an additional 'create'
    view.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
