# -*- coding: utf-8 -*-
from django.db import models
from django.db.utils import IntegrityError
from django.test import TestCase
import uuid

from ..models import Game, Player

class GameTests(TestCase):
    def test_pk_is_uuid(self):
        game = Game()
        game.save()
        self.assertIsInstance(game.pk, uuid.UUID)


class PlayerTests(TestCase):
    def setUp(self):
        self.game = Game()
        self.game.save()

    def test_pk_is_uuid(self):
        player = Player(game=self.game)
        player.save()
        self.assertIsInstance(player.pk, uuid.UUID)

    def test_default_name(self):
        player = Player()
        self.assertEqual(player.name, 'Player')

    def test_game_required(self):
        player = Player()
        with self.assertRaises(IntegrityError):
            player.save()

    def test_player_returns_associated_game_instance(self):
        player = Player(game=self.game)
        self.assertEqual(player.game, self.game)

    def test_game_can_access_player_list(self):
        player = Player(game=self.game)
        player.save()
        self.assertEqual(list(self.game.players.all()), [player])
