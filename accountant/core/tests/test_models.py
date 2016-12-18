# -*- coding: utf-8 -*-
from django.db import models
from django.test import TestCase
import uuid

from ..models import Game

class GameTests(TestCase):
    def test_pk_is_uuid(self):
        game = Game()
        game.save()
        self.assertIsInstance(game.pk, uuid.UUID)
