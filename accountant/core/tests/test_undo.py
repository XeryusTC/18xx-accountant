# -*- coding: utf-8 -*-
from django.test import TestCase
from unittest import mock

from .. import factories
from .. import models
from .. import utils

class UndoTransferMoneyTests(TestCase):
    def setUp(self):
        self.game = factories.GameFactory(cash=1000)
        self.start_entry = models.LogEntry.objects.create(game=self.game,
            text='New game')
        self.game.log_cursor = self.start_entry
        self.game.save()

    @mock.patch.object(utils, 'transfer_money')
    def test_can_undo_player_transfering_money_to_bank(self,
            mock_transfer_money):
        player = factories.PlayerFactory(game=self.game, cash=0)
        entry = models.LogEntry.objects.create(
            game=self.game,
            action=models.LogEntry.TRANSFER_MONEY,
            acting_player=player,
            amount=10)
        self.game.log_cursor = entry
        self.game.save()

        utils.undo(self.game)

        self.game.refresh_from_db()
        mock_transfer_money.assert_called_once_with(None, player, 10)
        self.assertEqual(self.game.log_cursor, self.start_entry)

    @mock.patch.object(utils, 'transfer_money')
    def test_undo_player_transfer_money_to_bank_returns_affected_instances(
            self, mock_transfer_money):
        player = factories.PlayerFactory(game=self.game, cash=0)
        entry = models.LogEntry.objects.create(
            game=self.game,
            action=models.LogEntry.TRANSFER_MONEY,
            acting_player=player,
            amount=10)
        self.game.log_cursor = entry
        self.game.save()

        affected = utils.undo(self.game)

        self.game.refresh_from_db()
        player.refresh_from_db()
        self.assertEqual(affected['game'], self.game)
        self.assertEqual(affected['players'], [player])


class RedoTransferMoneyTests(TestCase):
    def setUp(self):
        self.game = factories.GameFactory(cash=1000)
        self.start_entry = models.LogEntry.objects.create(game=self.game,
            text='New game')
        self.game.log_cursor = self.start_entry
        self.game.save()

    @mock.patch.object(utils, 'transfer_money')
    def test_can_redo_player_transfering_money_to_bank(self,
            mock_transfer_money):
        player = factories.PlayerFactory(game=self.game, cash=0)
        entry = models.LogEntry.objects.create(
            game=self.game,
            action=models.LogEntry.TRANSFER_MONEY,
            acting_player=player,
            amount=10)

        utils.redo(self.game)

        self.game.refresh_from_db()
        mock_transfer_money.assert_called_once_with(player, None, 10)
        self.assertEqual(self.game.log_cursor, entry)

    @mock.patch.object(utils, 'transfer_money')
    def test_redo_player_transfer_money_to_bank_returns_affected_instances(
            self, mock_transfer_money):
        player = factories.PlayerFactory(game=self.game, cash=0)
        entry = models.LogEntry.objects.create(
            game=self.game,
            action=models.LogEntry.TRANSFER_MONEY,
            acting_player=player,
            amount=20)

        affected = utils.redo(self.game)

        self.game.refresh_from_db()
        player.refresh_from_db()
        self.assertEqual(affected['game'], self.game)
        self.assertEqual(affected['players'], [player])
        self.assertEqual(affected['log'], self.game.log_cursor)
