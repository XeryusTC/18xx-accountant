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

    def test_can_undo_bank_transfering_money_to_player(self,
            mock_transfer_money):
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY,
            receiving_player=self.player, amount=1)
        self.game.log_cursor = entry
        self.game.save()

        utils.undo(self.game)

        self.game.refresh_from_db()
        mock_transfer_money.assert_called_once_with(receiver=self.player,
            sender=None, amount=-1)
        self.assertEqual(self.game.log_cursor, self.start_entry)

    def test_can_undo_bank_transfering_money_to_company(self,
            mock_transfer_money):
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY,
            receiving_company=self.company, amount=2)
        self.game.log_cursor = entry
        self.game.save()

        utils.undo(self.game)

        self.game.refresh_from_db()
        mock_transfer_money.assert_called_once_with(receiver=self.company,
            sender=None, amount=-2)
        self.assertEqual(self.game.log_cursor, self.start_entry)

    def test_can_undo_player_transfering_money_to_bank(self,
            mock_transfer_money):
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, acting_player=self.player,
            amount=10)
        self.game.log_cursor = entry
        self.game.save()

        utils.undo(self.game)

        self.game.refresh_from_db()
        mock_transfer_money.assert_called_once_with(receiver=None,
            sender=self.player, amount=-10)
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
        mock_transfer_money.assert_called_once_with(receiver=None,
            sender=self.company, amount=-20)
        self.assertEqual(self.game.log_cursor, self.start_entry)

    def test_can_undo_player_transfering_money_to_other_player(self,
            mock_transfer_money):
        other_player = factories.PlayerFactory(game=self.game)
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, acting_player=self.player,
            receiving_player=other_player, amount=30)
        self.game.log_cursor = entry
        self.game.save()

        utils.undo(self.game)

        self.game.refresh_from_db()
        mock_transfer_money.assert_called_once_with(receiver=other_player,
            sender=self.player, amount=-30)

    def test_can_undo_player_transfering_money_to_company(self,
            mock_transfer_money):
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, acting_player=self.player,
            receiving_company=self.company, amount=40)
        self.game.log_cursor = entry
        self.game.save()

        utils.undo(self.game)

        self.game.refresh_from_db()
        mock_transfer_money.assert_called_once_with(receiver=self.company,
            sender=self.player, amount=-40)

    def test_can_undo_company_transfering_money_to_player(self,
            mock_transfer_money):
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, acting_company=self.company,
            receiving_player=self.player, amount=50)
        self.game.log_cursor = entry
        self.game.save()

        utils.undo(self.game)

        self.game.refresh_from_db()
        mock_transfer_money.assert_called_once_with(receiver=self.player,
            sender=self.company, amount=-50)

    def test_can_undo_company_transfering_money_to_other_company(self,
            mock_transfer_money):
        other_company = factories.CompanyFactory(game=self.game)
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, acting_company=self.company,
            receiving_company=other_company, amount=60)
        self.game.log_cursor = entry
        self.game.save()

        utils.undo(self.game)

        self.game.refresh_from_db()
        mock_transfer_money.assert_called_once_with(receiver=other_company,
            sender=self.company, amount=-60)

    def test_undo_bank_transfer_money_to_player_returns_affected_instances(
            self, mock_transfer_money):
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY,
            receiving_player=self.player, amount=3)
        self.game.log_cursor = entry
        self.game.save()

        affected = utils.undo(self.game)

        self.game.refresh_from_db()
        self.player.refresh_from_db()
        self.assertNotIn('companies', affected.keys())
        self.assertEqual(affected['game'], self.game)
        self.assertEqual(affected['players'], [self.player])
        self.assertNotIn('shares', affected.keys())

    def test_undo_bank_transfer_money_to_company_returns_affected_instances(
            self, mock_transfer_money):
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY,
            receiving_company=self.company, amount=4)
        self.game.log_cursor = entry
        self.game.save()

        affected = utils.undo(self.game)

        self.game.refresh_from_db()
        self.company.refresh_from_db()
        self.assertNotIn('players', affected.keys())
        self.assertEqual(affected['game'], self.game)
        self.assertEqual(affected['companies'], [self.company])
        self.assertNotIn('shares', affected.keys())

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
        self.assertNotIn('companies', affected.keys())
        self.assertEqual(affected['game'], self.game)
        self.assertEqual(affected['players'], [self.player])
        self.assertNotIn('shares', affected.keys())

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
        self.assertNotIn('players', affected.keys())
        self.assertEqual(affected['game'], self.game)
        self.assertEqual(affected['companies'], [self.company])
        self.assertNotIn('shares', affected.keys())

    def test_undo_player_transfer_money_to_other_player_returns_affected(
            self, mock_transfer_money):
        other_player = factories.PlayerFactory(game=self.game)
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, acting_player=self.player,
            receiving_player=other_player, amount=30)
        self.game.log_cursor = entry
        self.game.save()

        affected = utils.undo(self.game)

        self.player.refresh_from_db()
        self.assertNotIn('game', affected.keys())
        self.assertNotIn('companies', affected.keys())
        self.assertCountEqual(affected['players'], [self.player, other_player])
        self.assertNotIn('shares', affected.keys())

    def test_undo_player_transfer_money_to_company_returns_affected_instances(
            self, mock_transfer_money):
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, acting_player=self.player,
            receiving_company=self.company, amount=40)
        self.game.log_cursor = entry
        self.game.save()

        affected = utils.undo(self.game)

        self.player.refresh_from_db()
        self.company.refresh_from_db()
        self.assertNotIn('game', affected.keys())
        self.assertEqual(affected['players'], [self.player])
        self.assertEqual(affected['companies'], [self.company])
        self.assertNotIn('shares', affected.keys())

    def test_undo_company_transfer_money_to_player_returns_affected_instances(
            self, mock_transfer_money):
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, acting_company=self.company,
            receiving_player=self.player, amount=50)
        self.game.log_cursor = entry
        self.game.save()

        affected = utils.undo(self.game)

        self.player.refresh_from_db()
        self.company.refresh_from_db()
        self.assertNotIn('game', affected.keys())
        self.assertEqual(affected['players'], [self.player])
        self.assertEqual(affected['companies'], [self.company])
        self.assertNotIn('shares', affected.keys())

    def test_undo_company_transfer_money_to_other_company_returns_affected(
            self, mock_transfer_money):
        other_company = factories.CompanyFactory(game=self.game)
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, acting_company=self.company,
            receiving_company=other_company, amount=60)
        self.game.log_cursor = entry
        self.game.save()

        affected = utils.undo(self.game)

        self.company.refresh_from_db()
        other_company.refresh_from_db()
        self.assertNotIn('game', affected.keys())
        self.assertNotIn('players', affected.keys())
        self.assertCountEqual(affected['companies'],
            [self.company, other_company])
        self.assertNotIn('shares', affected.keys())


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

    def test_can_redo_bank_transfering_money_to_player(self,
            mock_transfer_money):
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY,
            receiving_player=self.player, amount=1)

        utils.redo(self.game)

        self.game.refresh_from_db()
        mock_transfer_money.assert_called_once_with(sender=None,
            receiver=self.player, amount=1)
        self.assertEqual(self.game.log_cursor, entry)

    def test_can_redo_bank_transfering_money_to_company(self,
            mock_transfer_money):
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY,
            receiving_company=self.company, amount=2)

        utils.redo(self.game)

        self.game.refresh_from_db()
        mock_transfer_money.assert_called_once_with(sender=None,
            receiver=self.company, amount=2)
        self.assertEqual(self.game.log_cursor, entry)

    def test_can_redo_player_transfering_money_to_bank(self,
            mock_transfer_money):
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, acting_player=self.player,
            amount=10)

        utils.redo(self.game)

        self.game.refresh_from_db()
        mock_transfer_money.assert_called_once_with(sender=self.player,
            receiver=None, amount=10)
        self.assertEqual(self.game.log_cursor, entry)

    def test_can_redo_company_transfer_money_to_bank(self,
            mock_transfer_money):
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, acting_company=self.company,
            amount=20)

        utils.redo(self.game)

        self.game.refresh_from_db()
        mock_transfer_money.assert_called_once_with(sender=self.company,
            receiver=None, amount=20)
        self.assertEqual(self.game.log_cursor, entry)

    def test_can_redo_player_transfering_money_to_player(self,
            mock_transfer_money):
        other_player = factories.PlayerFactory(game=self.game)
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, acting_player=self.player,
            receiving_player=other_player, amount=30)

        utils.redo(self.game)

        self.game.refresh_from_db()
        mock_transfer_money.assert_called_once_with(sender=self.player,
            receiver=other_player, amount=30)
        self.assertEqual(self.game.log_cursor, entry)

    def test_can_redo_player_transfering_money_to_company(self,
            mock_transfer_money):
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, acting_player=self.player,
            receiving_company=self.company, amount=40)

        utils.redo(self.game)

        self.game.refresh_from_db()
        mock_transfer_money.assert_called_once_with(sender=self.player,
            receiver=self.company, amount=40)
        self.assertEqual(self.game.log_cursor, entry)

    def test_can_redo_company_transfering_money_to_player(self,
            mock_transfer_money):
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, acting_company=self.company,
            receiving_player=self.player, amount=50)

        utils.redo(self.game)

        self.game.refresh_from_db()
        mock_transfer_money.assert_called_once_with(sender=self.company,
            receiver=self.player, amount=50)
        self.assertEqual(self.game.log_cursor, entry)

    def test_can_redo_company_transfering_money_to_company(self,
            mock_transfer_money):
        other_company = factories.CompanyFactory(game=self.game)
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, acting_company=self.company,
            receiving_company=other_company, amount=60)

        utils.redo(self.game)

        self.game.refresh_from_db()
        mock_transfer_money.assert_called_once_with(sender=self.company,
            receiver=other_company, amount=60)
        self.assertEqual(self.game.log_cursor, entry)

    def test_redo_bank_transfer_money_to_player_returns_affected_instances(
            self, mock_transfer_money):
        models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY,
            receiving_player=self.player, amount=3)

        affected = utils.redo(self.game)

        self.game.refresh_from_db()
        self.player.refresh_from_db()
        self.assertNotIn('companies', affected.keys())
        self.assertEqual(affected['game'], self.game)
        self.assertEqual(affected['players'], [self.player])
        self.assertEqual(affected['log'], self.game.log_cursor)
        self.assertNotIn('shares', affected.keys())

    def test_redo_bank_transfer_money_to_company_returns_affected_instances(
            self, mock_transfer_money):
        models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY,
            receiving_company=self.company, amount=4)

        affected = utils.redo(self.game)

        self.game.refresh_from_db()
        self.company.refresh_from_db()
        self.assertNotIn('players', affected.keys())
        self.assertEqual(affected['game'], self.game)
        self.assertEqual(affected['companies'], [self.company])
        self.assertEqual(affected['log'], self.game.log_cursor)
        self.assertNotIn('shares', affected.keys())

    def test_redo_player_transfer_money_to_bank_returns_affected_instances(
            self, mock_transfer_money):
        models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, acting_player=self.player,
            amount=70)

        affected = utils.redo(self.game)

        self.game.refresh_from_db()
        self.player.refresh_from_db()
        self.assertNotIn('companies', affected.keys())
        self.assertEqual(affected['game'], self.game)
        self.assertEqual(affected['players'], [self.player])
        self.assertEqual(affected['log'], self.game.log_cursor)
        self.assertNotIn('shares', affected.keys())

    def test_redo_company_transfer_money_to_bank_returns_affected_instances(
            self, mock_transfer_money):
        models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, acting_company=self.company,
            amount=80)

        affected = utils.redo(self.game)

        self.game.refresh_from_db()
        self.company.refresh_from_db()
        self.assertNotIn('players', affected.keys())
        self.assertEqual(affected['game'], self.game)
        self.assertEqual(affected['companies'], [self.company])
        self.assertEqual(affected['log'], self.game.log_cursor)
        self.assertNotIn('shares', affected.keys())

    def test_redo_player_transfer_money_to_player_returns_affected_instances(
            self, mock_transfer_money):
        other_player = factories.PlayerFactory(game=self.game)
        models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, amount=90,
            acting_player=self.player, receiving_player=other_player)

        affected = utils.redo(self.game)

        self.player.refresh_from_db()
        other_player.refresh_from_db()
        self.assertNotIn('game', affected.keys())
        self.assertNotIn('companies', affected.keys())
        self.assertEqual(affected['log'], self.game.log_cursor)
        self.assertCountEqual(affected['players'], [self.player, other_player])
        self.assertNotIn('shares', affected.keys())

    def test_redo_player_transfer_money_to_company_returns_affected_instances(
            self, mock_transfer_money):
        models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, amount=90,
            acting_player=self.player, receiving_company=self.company)

        affected = utils.redo(self.game)

        self.player.refresh_from_db()
        self.company.refresh_from_db()
        self.assertNotIn('game', affected.keys())
        self.assertEqual(affected['log'], self.game.log_cursor)
        self.assertEqual(affected['players'], [self.player])
        self.assertEqual(affected['companies'], [self.company])
        self.assertNotIn('shares', affected.keys())

    def test_redo_company_transfer_money_to_player_returns_affected_instances(
            self, mock_transfer_money):
        models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, amount=90,
            acting_company=self.company, receiving_player=self.player)

        affected = utils.redo(self.game)

        self.player.refresh_from_db()
        self.company.refresh_from_db()
        self.assertNotIn('game', affected.keys())
        self.assertEqual(affected['log'], self.game.log_cursor)
        self.assertEqual(affected['players'], [self.player])
        self.assertEqual(affected['companies'], [self.company])
        self.assertNotIn('shares', affected.keys())

    def test_redo_company_transfer_money_to_company_returns_affected_instances(
            self, mock_transfer_money):
        other_company = factories.CompanyFactory(game=self.game)
        models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, amount=90,
            acting_company=self.company, receiving_company=other_company)

        affected = utils.redo(self.game)

        self.company.refresh_from_db()
        other_company.refresh_from_db()
        self.assertNotIn('game', affected.keys())
        self.assertNotIn('players', affected.keys())
        self.assertEqual(affected['log'], self.game.log_cursor)
        self.assertCountEqual(affected['companies'],
            [self.company, other_company])
        self.assertNotIn('shares', affected.keys())
