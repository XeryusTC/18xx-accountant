# -*- coding: utf-8 -*-
from django.test import TestCase

from .. import factories
from .. import utils

class TransferMoneyTests(TestCase):
    def setUp(self):
        self.game = factories.GameFactory(cash=100)
        self.player = factories.PlayerFactory(game=self.game, cash=10)
        self.company = factories.CompanyFactory(game=self.game, cash=10)

    def test_can_transfer_cash_from_bank_to_player(self):
        utils.transfer_money(None, self.player, 10)
        self.assertEqual(self.game.cash, 90)
        self.assertEqual(self.player.cash, 20)

    def test_can_transfer_cash_from_bank_to_company(self):
        utils.transfer_money(None, self.company, 10)
        self.assertEqual(self.game.cash, 90)
        self.assertEqual(self.company.cash, 20)

    def test_can_transfer_cash_from_player_to_bank(self):
        utils.transfer_money(self.player, None, 10)
        self.assertEqual(self.game.cash, 110)
        self.assertEqual(self.player.cash, 0)

    def test_can_transfer_cash_from_player_to_company(self):
        utils.transfer_money(self.player, self.company, 10)
        self.assertEqual(self.player.cash, 0)
        self.assertEqual(self.company.cash, 20)

    def test_can_transfer_cash_from_company_to_bank(self):
        utils.transfer_money(self.company, None, 10)
        self.assertEqual(self.game.cash, 110)
        self.assertEqual(self.company.cash, 0)

    def test_can_transfer_cash_from_company_to_player(self):
        utils.transfer_money(self.company, self.player, 10)
        self.assertEqual(self.player.cash, 20)
        self.assertEqual(self.company.cash, 0)

    def test_raises_SameEntityError_when_receiver_sender_are_the_bank(self):
        with self.assertRaises(utils.SameEntityError):
            utils.transfer_money(None, None, 0)

    def test_raises_SameEntityError_when_receiver_sender_are_the_same(self):
        with self.assertRaises(utils.SameEntityError):
            utils.transfer_money(self.player, self.player, 0)
