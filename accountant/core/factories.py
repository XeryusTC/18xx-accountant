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
    game = factory.SubFactory(GameFactory)


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Company

    name = factory.Sequence(lambda n: 'C%d' % n)
    game = factory.SubFactory(GameFactory)


class PlayerShareFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PlayerShare

    owner = factory.SubFactory(PlayerFactory)
    company = factory.SubFactory(CompanyFactory)


class CompanyShareFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CompanyShare

    owner = factory.SubFactory(CompanyFactory)
    company = factory.SubFactory(CompanyFactory)


class LogEntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.LogEntry

    text = factory.Sequence(lambda n: 'Log entry %d' % n)
    game = factory.SubFactory(GameFactory)
