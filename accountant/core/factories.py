# -*- coding: utf-8 -*-
import factory

from . import models

class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Game


class PlayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Player

    name = factory.Sequence(lambda n: 'Player %d' % n)


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Company

    name = factory.Sequence(lambda n: 'C%d' % n)


class PlayerShareFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PlayerShare
