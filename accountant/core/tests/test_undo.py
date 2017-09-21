# -*- coding: utf-8 -*-
from django.test import TestCase
from unittest import mock

from .. import factories
from .. import models
from .. import utils

@mock.patch.object(utils, 'transfer_money')
class UndoTransferMoneyTests(TestCase):
    def setUp(self):
        self.game = factories.GameFactory(cash=1000)
        self.start_entry = models.LogEntry.objects.create(game=self.game,
            text='New game')
        self.game.log_cursor = self.start_entry
        self.game.save()
        self.player = factories.PlayerFactory(game=self.game)
        self.company = factories.CompanyFactory(game=self.game)

    def test_can_undo_player_transfering_money_to_bank(self,
            mock_transfer_money):
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, acting_player=self.player,
            amount=10)
        self.game.log_cursor = entry
        self.game.save()

        utils.undo(self.game)

        self.game.refresh_from_db()
        mock_transfer_money.assert_called_once_with(None, self.player, 10)
        self.assertEqual(self.game.log_cursor, self.start_entry)

    def test_can_undo_company_transfering_money_to_bank(self,
            mock_transfer_money):
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, acting_company=self.company,
            amount=20)
        self.game.log_cursor = entry
        self.game.save()

        utils.undo(self.game)

        self.game.refresh_from_db()
        mock_transfer_money.assert_called_once_with(None, self.company, 20)
        self.assertEqual(self.game.log_cursor, self.start_entry)

    def test_undo_player_transfer_money_to_bank_returns_affected_instances(
            self, mock_transfer_money):
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, acting_player=self.player,
            amount=10)
        self.game.log_cursor = entry
        self.game.save()

        affected = utils.undo(self.game)

        self.game.refresh_from_db()
        self.player.refresh_from_db()
        self.assertEqual(affected['game'], self.game)
        self.assertEqual(affected['players'], [self.player])

    def test_undo_company_transfer_money_to_bank_returns_affected_instances(
            self, mock_transfer_money):
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, acting_company=self.company,
            amount=20)
        self.game.log_cursor = entry
        self.game.save()

        affected = utils.undo(self.game)

        self.game.refresh_from_db()
        self.company.refresh_from_db()
        self.assertEqual(affected['game'], self.game)
        self.assertEqual(affected['companies'], [self.company])


@mock.patch.object(utils, 'transfer_money')
class RedoTransferMoneyTests(TestCase):
    def setUp(self):
        self.game = factories.GameFactory(cash=1000)
        self.start_entry = models.LogEntry.objects.create(game=self.game,
            text='New game')
        self.game.log_cursor = self.start_entry
        self.game.save()
        self.player = factories.PlayerFactory(game=self.game)
        self.company = factories.CompanyFactory(game=self.game)

    def test_can_redo_player_transfering_money_to_bank(self,
            mock_transfer_money):
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, acting_player=self.player,
            amount=10)

        utils.redo(self.game)

        self.game.refresh_from_db()
        mock_transfer_money.assert_called_once_with(self.player, None, 10)
        self.assertEqual(self.game.log_cursor, entry)

    def test_can_redo_company_transfer_money_to_bank(self,
            mock_transfer_money):
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, acting_company=self.company,
            amount=10)

        utils.redo(self.game)

        self.game.refresh_from_db()
        mock_transfer_money.assert_called_once_with(self.company, None, 10)
        self.assertEqual(self.game.log_cursor, entry)

    def test_redo_player_transfer_money_to_bank_returns_affected_instances(
            self, mock_transfer_money):
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, acting_player=self.player,
            amount=20)

        affected = utils.redo(self.game)

        self.game.refresh_from_db()
        self.player.refresh_from_db()
        self.assertEqual(affected['game'], self.game)
        self.assertEqual(affected['players'], [self.player])
        self.assertEqual(affected['log'], self.game.log_cursor)

    def test_redo_company_transfer_money_to_bank_returns_affected_instances(
            self, mock_transfer_money):
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, acting_company=self.company,
            amount=20)

        affected = utils.redo(self.game)

        self.game.refresh_from_db()
        self.company.refresh_from_db()
        self.assertEqual(affected['game'], self.game)
        self.assertEqual(affected['companies'], [self.company])
        self.assertEqual(affected['log'], self.game.log_cursor)
