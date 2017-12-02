# -*- coding: utf-8 -*-
from django.test import TestCase
from unittest import mock

from .. import factories
from .. import models
from .. import utils

@mock.patch.object(utils, 'buy_share')
class UndoTransferShareTests(TestCase):
    def setUp(self):
        self.game = factories.GameFactory(cash=1000)
        self.start_entry = models.LogEntry.objects.create(game=self.game,
            text='New game')
        self.game.log_cursor = self.start_entry
        self.game.save()
        self.player, self.other_player = factories.PlayerFactory.create_batch(
            game=self.game, size=2)
        self.buy_company = factories.CompanyFactory(game=self.game)
        self.share_company = factories.CompanyFactory(game=self.game)
        self.source_company = factories.CompanyFactory(game=self.game)
        self.player_share = factories.PlayerShareFactory(owner=self.player,
            company=self.share_company, shares=0)
        self.other_player_share = factories.PlayerShareFactory(
            owner=self.other_player, company=self.share_company, shares=0)
        self.company_share = factories.CompanyShareFactory(
            owner=self.buy_company, company=self.share_company, shares=0)
        self.source_company_share = factories.CompanyShareFactory(
            owner=self.source_company, company=self.share_company, shares=0)

    def create_entry(self, **kwargs):
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_SHARE, company=self.share_company,
            **kwargs)
        self.game.log_cursor = entry
        self.game.save()

    def test_can_undo_player_buying_share_from_ipo(self, mock_buy_share):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='ipo', price=1, shares=9)
        utils.undo(self.game)
        mock_buy_share.assert_called_once_with(self.player, self.share_company,
            utils.Share.IPO, 1, -9)

    def test_can_undo_player_buying_share_from_bank(self, mock_buy_share):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='bank', price=2, shares=8)
        utils.undo(self.game)
        mock_buy_share.assert_called_once_with(self.player, self.share_company,
            utils.Share.BANK, 2, -8)

    def test_can_undo_player_buying_share_from_company(self, mock_buy_share):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='company', company_source=self.buy_company, price=3,
            shares=7)
        utils.undo(self.game)
        mock_buy_share.assert_called_once_with(self.player, self.share_company,
            self.buy_company, 3, -7)

    def test_can_undo_player_buying_share_from_player(self, mock_buy_share):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='player', player_source=self.other_player, price=4,
            shares=6)
        utils.undo(self.game)
        mock_buy_share.assert_called_once_with(self.player, self.share_company,
            self.other_player, 4, -6)

    def test_can_undo_company_buying_share_from_ipo(self, mock_buy_share):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='ipo', price=5, shares=5)
        utils.undo(self.game)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.share_company, utils.Share.IPO, 5, -5)

    def test_can_undo_company_buying_share_from_bank(self, mock_buy_share):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='bank', price=6, shares=4)
        utils.undo(self.game)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.share_company, utils.Share.BANK, 6, -4)

    def test_can_undo_company_buying_share_from_company(self, mock_buy_share):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='company', company_source=self.source_company, price=7,
            shares=3)
        utils.undo(self.game)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.share_company, self.source_company, 7, -3)

    def test_can_undo_company_buying_share_from_player(self, mock_buy_share):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='player', player_source=self.player, price=8, shares=2)
        utils.undo(self.game)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.share_company, self.player, 8, -2)

    def test_can_undo_player_selling_shares_to_ipo(self, mock_buy_share):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='ipo', price=9, shares=-1)
        utils.undo(self.game)
        mock_buy_share.assert_called_once_with(self.player, self.share_company,
            utils.Share.IPO, 9, 1)

    def test_can_undo_player_selling_shares_to_bank(self, mock_buy_share):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='bank', price=10, shares=-3)
        utils.undo(self.game)
        mock_buy_share.assert_called_once_with(self.player, self.share_company,
            utils.Share.BANK, 10, 3)

    def test_can_undo_player_selling_shares_to_company(self, mock_buy_share):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='company', company_source=self.buy_company, price=11,
            shares=-3)
        utils.undo(self.game)
        mock_buy_share.assert_called_once_with(self.player, self.share_company,
            self.buy_company, 11, 3)

    def test_can_undo_player_selling_shares_to_player(self, mock_buy_share):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='player', player_source=self.other_player, price=12,
            shares=-5)
        utils.undo(self.game)
        mock_buy_share.assert_called_once_with(self.player, self.share_company,
            self.other_player, 12, 5)

    def test_can_undo_company_selling_shares_to_ipo(self, mock_buy_share):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='ipo', price=13, shares=-2)
        utils.undo(self.game)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.share_company, utils.Share.IPO, 13, 2)

    def test_can_undo_company_selling_shares_to_bank(self, mock_buy_share):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='bank', price=14, shares=-4)
        utils.undo(self.game)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.share_company, utils.Share.BANK, 14, 4)

    def test_can_undo_company_selling_shares_to_company(self, mock_buy_share):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='company', company_source=self.source_company, price=15,
            shares=-6)
        utils.undo(self.game)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.share_company, self.source_company, 15, 6)

    def test_can_undo_company_selling_shares_to_player(self, mock_buy_share):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='player', player_source=self.player, price=16,
            shares=-8)
        utils.undo(self.game)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.share_company, self.player, 16, 8)

    def test_undo_player_buying_share_from_ipo_returns_affected(self, mock):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='ipo', price=17, shares=1)
        affected = utils.undo(self.game)
        self.assertEqual(affected['game'], self.game)
        self.assertEqual(affected['players'], [self.player])
        self.assertEqual(affected['shares'], [self.player_share])
        self.assertEqual(affected['companies'], [self.share_company])

    def test_undo_player_buying_share_from_bank_returns_affected(self, mock):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='bank', price=18, shares=2)
        affected = utils.undo(self.game)
        self.assertEqual(affected['game'], self.game)
        self.assertEqual(affected['players'], [self.player])
        self.assertEqual(affected['shares'], [self.player_share])
        self.assertEqual(affected['companies'], [self.share_company])

    def test_undo_player_buying_share_from_company_returns_affected(self,
            mock):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='company', company_source=self.buy_company, price=19,
            shares=3)
        affected = utils.undo(self.game)
        self.assertNotIn('game', affected.keys())
        self.assertEqual(affected['players'], [self.player])
        self.assertEqual(affected['companies'], [self.buy_company])
        self.assertCountEqual(affected['shares'],
            [self.player_share, self.company_share])

    def test_undo_player_buying_share_from_player_returns_affected(self, mock):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='player', player_source=self.other_player, price=20,
            shares=4)
        affected = utils.undo(self.game)
        self.assertNotIn('game', affected.keys())
        self.assertCountEqual(affected['players'],
            [self.player, self.other_player])
        self.assertCountEqual(affected['shares'],
            [self.player_share, self.other_player_share])

    def test_undo_company_buying_share_from_ipo_returns_affected(self, mock):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='ipo', price=21, shares=5)
        affected = utils.undo(self.game)
        self.assertEqual(affected['game'], self.game)
        self.assertNotIn('players', affected.keys())
        self.assertCountEqual(affected['companies'],
            [self.buy_company, self.share_company])
        self.assertEqual(affected['shares'], [self.company_share])

    def test_undo_company_buying_share_from_bank_returns_affected(self, mock):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='bank', price=22, shares=6)
        affected = utils.undo(self.game)
        self.assertEqual(affected['game'], self.game)
        self.assertNotIn('players', affected.keys())
        self.assertCountEqual(affected['companies'],
            [self.buy_company, self.share_company])
        self.assertEqual(affected['shares'], [self.company_share])

    def test_undo_company_buying_share_from_company_returns_affected(self,
            mock):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='company', company_source=self.source_company, price=23,
            shares=7)
        affected = utils.undo(self.game)
        self.assertNotIn('game', affected.keys())
        self.assertNotIn('players', affected.keys())
        self.assertCountEqual(affected['companies'],
            [self.buy_company, self.source_company])
        self.assertCountEqual(affected['shares'],
            [self.company_share, self.source_company_share])

    def test_undo_company_buying_share_from_player_returns_affected(self,
            mock):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='player', player_source=self.player, price=24,
            shares=8)
        affected = utils.undo(self.game)
        self.assertNotIn('game', affected.keys())
        self.assertEqual(affected['players'], [self.player])
        self.assertEqual(affected['companies'], [self.buy_company])
        self.assertCountEqual(affected['shares'],
            [self.company_share, self.player_share])

    def test_undo_player_selling_share_to_ipo_returns_affected(self, mock):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='ipo', price=25, shares=-1)
        affected = utils.undo(self.game)
        self.assertEqual(affected['game'], self.game)
        self.assertEqual(affected['players'], [self.player])
        self.assertEqual(affected['shares'], [self.player_share])
        self.assertEqual(affected['companies'], [self.share_company])

    def test_undo_player_selling_share_to_bank_returns_affected(self, mock):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='bank', price=26, shares=-2)
        affected = utils.undo(self.game)
        self.assertEqual(affected['game'], self.game)
        self.assertEqual(affected['players'], [self.player])
        self.assertEqual(affected['shares'], [self.player_share])
        self.assertEqual(affected['companies'], [self.share_company])

    def test_undo_player_selling_share_to_company_returns_affected(self,
            mock):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='company', company_source=self.buy_company, price=27,
            shares=-3)
        affected = utils.undo(self.game)
        self.assertNotIn('game', affected.keys())
        self.assertEqual(affected['players'], [self.player])
        self.assertEqual(affected['companies'], [self.buy_company])
        self.assertCountEqual(affected['shares'],
            [self.player_share, self.company_share])

    def test_undo_player_selling_share_to_player_returns_affected(self, mock):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='player', player_source=self.other_player, price=28,
            shares=-4)
        affected = utils.undo(self.game)
        self.assertNotIn('game', affected.keys())
        self.assertCountEqual(affected['players'],
            [self.player, self.other_player])
        self.assertCountEqual(affected['shares'],
            [self.player_share, self.other_player_share])

    def test_undo_company_selling_share_to_ipo_returns_affected(self, mock):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='ipo', price=29, shares=-5)
        affected = utils.undo(self.game)
        self.assertEqual(affected['game'], self.game)
        self.assertNotIn('players', affected.keys())
        self.assertCountEqual(affected['companies'],
            [self.buy_company, self.share_company])
        self.assertEqual(affected['shares'], [self.company_share])

    def test_undo_company_selling_share_to_bank_returns_affected(self, mock):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='bank', price=30, shares=-6)
        affected = utils.undo(self.game)
        self.assertEqual(affected['game'], self.game)
        self.assertNotIn('players', affected.keys())
        self.assertCountEqual(affected['companies'],
            [self.buy_company, self.share_company])
        self.assertEqual(affected['shares'], [self.company_share])

    def test_undo_company_selling_share_to_company_returns_affected(self,
            mock):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='company', company_source=self.source_company, price=31,
            shares=-7)
        affected = utils.undo(self.game)
        self.assertNotIn('game', affected.keys())
        self.assertNotIn('players', affected.keys())
        self.assertCountEqual(affected['companies'],
            [self.buy_company, self.source_company])
        self.assertCountEqual(affected['shares'],
            [self.company_share, self.source_company_share])

    def test_undo_company_selling_share_to_player_returns_affected(self,
            mock):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='player', player_source=self.player, price=32,
            shares=-8)
        affected = utils.undo(self.game)
        self.assertNotIn('game', affected.keys())
        self.assertEqual(affected['players'], [self.player])
        self.assertEqual(affected['companies'], [self.buy_company])
        self.assertCountEqual(affected['shares'],
            [self.company_share, self.player_share])


@mock.patch.object(utils, 'buy_share')
class RedoTransferShareTests(TestCase):
    def setUp(self):
        self.game = factories.GameFactory(cash=1000)
        self.start_entry = models.LogEntry.objects.create(game=self.game,
            text='New game')
        self.game.log_cursor = self.start_entry
        self.game.save()
        self.player = factories.PlayerFactory(game=self.game)
        self.other_player = factories.PlayerFactory(game=self.game)
        self.buy_company = factories.CompanyFactory(game=self.game)
        self.share_company = factories.CompanyFactory(game=self.game)
        self.source_company = factories.CompanyFactory(game=self.game)
        self.player_share = factories.PlayerShareFactory(owner=self.player,
            company=self.share_company, shares=0)
        self.other_player_share = factories.PlayerShareFactory(
            owner=self.other_player, company=self.share_company, shares=0)
        self.company_share = factories.CompanyShareFactory(
            owner=self.buy_company, company=self.share_company, shares=0)
        self.source_company_share = factories.CompanyShareFactory(
            owner=self.source_company, company=self.share_company, shares=0)

    def create_entry(self, **kwargs):
        models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_SHARE, company=self.share_company,
            **kwargs)

    def test_can_redo_player_buying_share_from_ipo(self, mock_buy_share):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='ipo', price=1, shares=2)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.player, self.share_company,
            utils.Share.IPO, 1, 2)

    def test_can_redo_player_buying_share_from_bank(self, mock_buy_share):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='bank', price=1, shares=5)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.player, self.share_company,
            utils.Share.BANK, 1, 5)

    def test_can_redo_player_buying_share_from_company(self, mock_buy_share):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='company', company_source=self.buy_company, price=2,
            shares=1)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.player, self.share_company,
           self.buy_company, 2, 1)

    def test_can_redo_player_buying_share_from_player(self, mock_buy_share):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='player', player_source=self.other_player, price=3,
            shares=4)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.player, self.share_company,
            self.other_player, 3, 4)

    def test_can_redo_company_buying_share_from_ipo(self, mock_buy_share):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='ipo', price=5, shares=1)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.share_company, utils.Share.IPO, 5, 1)

    def test_can_redo_company_buying_share_from_bank(self, mock_buy_share):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='bank', price=8, shares=6)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.share_company, utils.Share.BANK, 8, 6)

    def test_can_redo_company_buying_share_from_company(self, mock_buy_share):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='company', company_source=self.source_company, price=13,
            shares=7)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.share_company, self.source_company, 13, 7)

    def test_can_redo_company_buying_share_from_player(self, mock_buy_share):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='player', player_source=self.player, price=21, shares=4)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.share_company, self.player, 21, 4)

    def test_can_redo_player_selling_share_to_ipo(self, mock_buy_share):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='ipo', price=34, shares=-2)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.player, self.share_company,
            utils.Share.IPO, 34, -2)

    def test_can_redo_player_selling_share_to_bank(self, mock_buy_share):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='bank', price=55, shares=-5)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.player, self.share_company,
            utils.Share.BANK, 55, -5)

    def test_can_redo_player_selling_share_to_company(self, mock_buy_share):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='company', company_source=self.buy_company, price=89,
            shares=-3)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.player, self.share_company,
           self.buy_company, 89, -3)

    def test_can_redo_player_selling_share_to_player(self, mock_buy_share):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='player', player_source=self.other_player, price=144,
            shares=-2)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.player, self.share_company,
            self.other_player, 144, -2)

    def test_can_redo_company_selling_share_to_ipo(self, mock_buy_share):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='ipo', price=233, shares=-9)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.share_company, utils.Share.IPO, 233, -9)

    def test_can_redo_company_selling_share_to_bank(self, mock_buy_share):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='bank', price=377, shares=-2)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.share_company, utils.Share.BANK, 377, -2)

    def test_can_redo_company_selling_share_to_company(self, mock_buy_share):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='company', company_source=self.source_company, price=610,
            shares=-3)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.share_company, self.source_company, 610, -3)

    def test_can_redo_company_selling_share_to_player(self, mock_buy_share):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='player', player_source=self.player, price=987, shares=-7)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.share_company, self.player, 987, -7)

    def test_redo_player_buying_share_from_ipo_returns_affected(self, mock):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='ipo', price=1597, shares=1)
        affected = utils.redo(self.game)
        self.assertEqual(affected['game'], self.game)
        self.assertEqual(affected['players'], [self.player])
        self.assertEqual(affected['companies'], [self.share_company])
        self.assertEqual(affected['shares'], [self.player_share])

    def test_redo_player_buying_share_from_bank_returns_affected(self, mock):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='bank', price=2584, shares=2)
        affected = utils.redo(self.game)
        self.assertEqual(affected['game'], self.game)
        self.assertEqual(affected['players'], [self.player])
        self.assertEqual(affected['companies'], [self.share_company])
        self.assertEqual(affected['shares'], [self.player_share])

    def test_redo_player_buying_share_from_company_returns_affected(self,
            mock):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='company', company_source=self.buy_company, price=4181,
            shares=3)
        affected = utils.redo(self.game)
        self.assertNotIn('game', affected.keys())
        self.assertEqual(affected['players'], [self.player])
        self.assertEqual(affected['companies'], [self.buy_company])
        self.assertCountEqual(affected['shares'],
            [self.player_share, self.company_share])

    def test_redo_player_buying_share_from_player_returns_affected(self, mock):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='player', player_source=self.other_player, price=6765,
            shares=4)
        affected = utils.redo(self.game)
        self.assertNotIn('game', affected.keys())
        self.assertCountEqual(affected['players'],
            [self.player, self.other_player])
        self.assertCountEqual(affected['shares'],
            [self.player_share, self.other_player_share])

    def test_redo_company_buying_share_from_ipo_returns_affected(self, mock):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='ipo', price=10946, shares=5)
        affected = utils.redo(self.game)
        self.assertEqual(affected['game'], self.game)
        self.assertNotIn('players', affected.keys())
        self.assertCountEqual(affected['companies'],
            [self.buy_company, self.share_company])
        self.assertEqual(affected['shares'], [self.company_share])

    def test_redo_company_buying_share_from_bank_returns_affected(self, mock):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='bank', price=17711, shares=6)
        affected = utils.redo(self.game)
        self.assertEqual(affected['game'], self.game)
        self.assertNotIn('players', affected.keys())
        self.assertCountEqual(affected['companies'],
            [self.buy_company, self.share_company])
        self.assertEqual(affected['shares'], [self.company_share])

    def test_redo_company_buying_share_from_company_returns_affected(self,
            mock):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='company', company_source=self.source_company, price=28657,
            shares=7)
        affected = utils.redo(self.game)
        self.assertNotIn('game', affected.keys())
        self.assertNotIn('players', affected.keys())
        self.assertCountEqual(affected['companies'],
            [self.buy_company, self.source_company])
        self.assertCountEqual(affected['shares'],
            [self.company_share, self.source_company_share])

    def test_redo_company_buying_share_from_player_returns_affected(self,
            mock):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='player', player_source=self.player, price=46368,
            shares=8)
        affected = utils.redo(self.game)
        self.assertNotIn('game', affected.keys())
        self.assertEqual(affected['players'], [self.player])
        self.assertEqual(affected['companies'], [self.buy_company])
        self.assertCountEqual(affected['shares'],
            [self.company_share, self.player_share])

    def test_redo_player_selling_share_to_ipo_returns_affected(self, mock):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='ipo', price=75025, shares=-1)
        affected = utils.redo(self.game)
        self.assertEqual(affected['game'], self.game)
        self.assertEqual(affected['players'], [self.player])
        self.assertEqual(affected['companies'], [self.share_company])
        self.assertEqual(affected['shares'], [self.player_share])

    def test_redo_player_selling_share_to_bank_returns_affected(self, mock):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='bank', price=121393, shares=-2)
        affected = utils.redo(self.game)
        self.assertEqual(affected['game'], self.game)
        self.assertEqual(affected['players'], [self.player])
        self.assertEqual(affected['companies'], [self.share_company])
        self.assertEqual(affected['shares'], [self.player_share])

    def test_redo_player_selling_share_to_company_returns_affected(self,
            mock):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='company', company_source=self.buy_company, price=196418,
            shares=-3)
        affected = utils.redo(self.game)
        self.assertNotIn('game', affected.keys())
        self.assertEqual(affected['players'], [self.player])
        self.assertEqual(affected['companies'], [self.buy_company])
        self.assertCountEqual(affected['shares'],
            [self.player_share, self.company_share])

    def test_redo_player_selling_share_to_player_returns_affected(self, mock):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='player', player_source=self.other_player, price=317811,
            shares=-4)
        affected = utils.redo(self.game)
        self.assertNotIn('game', affected.keys())
        self.assertCountEqual(affected['players'],
            [self.player, self.other_player])
        self.assertCountEqual(affected['shares'],
            [self.player_share, self.other_player_share])

    def test_redo_company_selling_share_to_ipo_returns_affected(self, mock):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='ipo', price=514229, shares=-5)
        affected = utils.redo(self.game)
        self.assertEqual(affected['game'], self.game)
        self.assertNotIn('players', affected.keys())
        self.assertCountEqual(affected['companies'],
            [self.buy_company, self.share_company])
        self.assertEqual(affected['shares'], [self.company_share])

    def test_redo_company_selling_share_to_bank_returns_affected(self, mock):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='bank', price=832040, shares=-6)
        affected = utils.redo(self.game)
        self.assertEqual(affected['game'], self.game)
        self.assertNotIn('players', affected.keys())
        self.assertCountEqual(affected['companies'],
            [self.buy_company, self.share_company])
        self.assertEqual(affected['shares'], [self.company_share])

    def test_redo_company_selling_share_to_company_returns_affected(self,
            mock):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='company', company_source=self.source_company,
            price=1346269, shares=-7)
        affected = utils.redo(self.game)
        self.assertNotIn('game', affected.keys())
        self.assertNotIn('players', affected.keys())
        self.assertCountEqual(affected['companies'],
            [self.buy_company, self.source_company])
        self.assertCountEqual(affected['shares'],
            [self.company_share, self.source_company_share])

    def test_redo_company_selling_share_to_player_returns_affected(self,
            mock):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='player', player_source=self.player, price=2178309,
            shares=-8)
        affected = utils.redo(self.game)
        self.assertNotIn('game', affected.keys())
        self.assertEqual(affected['players'], [self.player])
        self.assertEqual(affected['companies'], [self.buy_company])
        self.assertCountEqual(affected['shares'],
            [self.company_share, self.player_share])
