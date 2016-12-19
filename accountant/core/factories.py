# -*- coding: utf-8 -*-
import factory

from . import models

class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Game
