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
        self.player = factories.PlayerFactory(game=self.game)
        self.buy_company = factories.CompanyFactory(game=self.game)
        self.share_company = factories.CompanyFactory(game=self.game)

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
        extra_player = factories.PlayerFactory(game=self.game)
        self.create_entry(buyer='player', player_buyer=self.player,
            source='player', player_source=extra_player, price=4, shares=6)
        utils.undo(self.game)
        mock_buy_share.assert_called_once_with(self.player, self.share_company,
            extra_player, 4, -6)

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
        extra_company = factories.CompanyFactory(game=self.game)
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='company', company_source=extra_company, price=7, shares=3)
        utils.undo(self.game)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.share_company, extra_company, 7, -3)

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
        extra_player = factories.PlayerFactory(game=self.game)
        self.create_entry(buyer='player', player_buyer=self.player,
            source='player', player_source=extra_player, price=12,
            shares=-5)
        utils.undo(self.game)
        mock_buy_share.assert_called_once_with(self.player, self.share_company,
            extra_player, 12, 5)

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
        extra_company = factories.CompanyFactory(game=self.game)
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='company', company_source=extra_company, price=15,
            shares=-6)
        utils.undo(self.game)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.share_company, extra_company, 15, 6)

    def test_can_undo_company_selling_shares_to_player(self, mock_buy_share):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='player', player_source=self.player, price=16,
            shares=-8)
        utils.undo(self.game)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.share_company, self.player, 16, 8)


@mock.patch.object(utils, 'buy_share')
class RedoTransferShareTests(TestCase):
    def setUp(self):
        self.game = factories.GameFactory(cash=1000)
        self.start_entry = models.LogEntry.objects.create(game=self.game,
            text='New game')
        self.game.log_cursor = self.start_entry
        self.game.save()
        self.player = factories.PlayerFactory(game=self.game)
        self.buy_company = factories.CompanyFactory(game=self.game)
        self.share_company = factories.CompanyFactory(game=self.game)

    def create_entry(self, **kwargs):
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_SHARE, company=self.share_company,
            **kwargs)

    def test_can_redo_player_buying_share_from_ipo(self, mock_buy_share):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='ipo', price=1, shares=2)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.player, self.share_company,
            utils.Share.IPO, 1, -2)

    def test_can_redo_player_buying_share_from_bank(self, mock_buy_share):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='bank', price=1, shares=5)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.player, self.share_company,
            utils.Share.BANK, 1, -5)

    def test_can_redo_player_buying_share_from_company(self, mock_buy_share):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='company', company_source=self.buy_company, price=2,
            shares=1)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.player, self.share_company,
           self.buy_company, 2, -1)

    def test_can_redo_player_buying_share_from_player(self, mock_buy_share):
        extra_player = factories.PlayerFactory(game=self.game)
        self.create_entry(buyer='player', player_buyer=self.player,
            source='player', player_source=extra_player, price=3, shares=4)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.player, self.share_company,
            extra_player, 3, -4)

    def test_can_redo_company_buying_share_from_ipo(self, mock_buy_share):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='ipo', price=5, shares=1)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.share_company, utils.Share.IPO, 5, -1)

    def test_can_redo_company_buying_share_from_bank(self, mock_buy_share):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='bank', price=8, shares=6)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.share_company, utils.Share.BANK, 8, -6)

    def test_can_redo_company_buying_share_from_company(self, mock_buy_share):
        extra_company = factories.CompanyFactory(game=self.game)
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='company', company_source=extra_company, price=13, shares=7)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.share_company, extra_company, 13, -7)

    def test_can_redo_company_buying_share_from_player(self, mock_buy_share):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='player', player_source=self.player, price=21, shares=4)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.share_company, self.player, 21, -4)

    def test_can_redo_player_selling_share_to_ipo(self, mock_buy_share):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='ipo', price=34, shares=-2)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.player, self.share_company,
            utils.Share.IPO, 34, 2)

    def test_can_redo_player_selling_share_to_bank(self, mock_buy_share):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='bank', price=55, shares=-5)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.player, self.share_company,
            utils.Share.BANK, 55, 5)

    def test_can_redo_player_selling_share_to_company(self, mock_buy_share):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='company', company_source=self.buy_company, price=89,
            shares=-3)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.player, self.share_company,
           self.buy_company, 89, 3)

    def test_can_redo_player_selling_share_to_player(self, mock_buy_share):
        extra_player = factories.PlayerFactory(game=self.game)
        self.create_entry(buyer='player', player_buyer=self.player,
            source='player', player_source=extra_player, price=134, shares=-2)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.player, self.share_company,
            extra_player, 134, 2)

    def test_can_redo_company_selling_share_to_ipo(self, mock_buy_share):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='ipo', price=223, shares=-9)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.share_company, utils.Share.IPO, 223, 9)

    def test_can_redo_company_selling_share_to_bank(self, mock_buy_share):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='bank', price=357, shares=-2)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.share_company, utils.Share.BANK, 357, 2)

    def test_can_redo_company_selling_share_to_company(self, mock_buy_share):
        extra_company = factories.CompanyFactory(game=self.game)
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='company', company_source=extra_company, price=580,
            shares=-3)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.share_company, extra_company, 580, 3)

    def test_can_redo_company_selling_share_to_player(self, mock_buy_share):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='player', player_source=self.player, price=937, shares=-7)
        utils.redo(self.game)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.share_company, self.player, 937, 7)
