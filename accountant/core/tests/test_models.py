# -*- coding: utf-8 -*-
from django.db import models
from django.db.utils import IntegrityError
from django.test import TestCase
import uuid

from ..models import Game, Player, Company

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


class CompanyTests(TestCase):
    def setUp(self):
        self.game = Game()
        self.game.save()

    def test_pk_is_uuid(self):
        company = Company(game=self.game)
        company.save()
        self.assertIsInstance(company.pk, uuid.UUID)

    def test_default_name(self):
        company = Company()
        self.assertEqual(company.name, 'Company')

    def test_game_required(self):
        company = Company()
        with self.assertRaises(IntegrityError):
            company.save()

    def test_company_returns_associated_game_instance(self):
        company = Company(game=self.game)
        self.assertEqual(company.game, self.game)

    def test_game_can_access_company_list(self):
        company = Company(game=self.game)
        company.save()
        self.assertEqual(list(self.game.companies.all()), [company])

    def test_has_text_color(self):
        company = Company(text_color='blue-500')

    def test_default_text_color_is_black(self):
        company = Company(game=self.game)
        self.assertEqual(company.text_color, 'black')

    def test_has_background_color(self):
        company = Company(background_color='white')

    def test_default_background_color_is_white(self):
        company = Company(game=self.game)
        self.assertEqual(company.background_color, 'white')
