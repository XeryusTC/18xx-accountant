# -*- coding: utf-8 -*-
from django.test import TestCase
from unittest import mock

from .. import factories
from .. import models
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


class PlayerShareTransactionTests(TestCase):
    """Test buying and selling shares for players"""
    def setUp(self):
        self.game = factories.GameFactory()
        self.player = factories.PlayerFactory(game=self.game, cash=1000)
        self.company = factories.CompanyFactory(game=self.game, cash=1000)

    def test_player_share_record_does_not_exist_by_default(self):
        with self.assertRaises(models.PlayerShare.DoesNotExist):
            self.player.share_set.get(company=self.company)

    def test_player_buying_share_auto_creates_playershare_record(self):
        utils.buy_share(self.player, self.company, utils.IPO_SHARES, 10)
        self.assertEqual(models.PlayerShare.objects.count(), 1)
        self.player.share_set.get(company=self.company)

    def test_player_buying_from_ipo_gives_share_to_player(self):
        utils.buy_share(self.player, self.company, utils.IPO_SHARES, 10)
        self.assertEqual(1,
            self.player.share_set.get(company=self.company).shares)

    def test_player_can_buy_multiple_shares_at_the_same_time(self):
        utils.buy_share(self.player, self.company, utils.IPO_SHARES, 1, 2)
        self.assertEqual(2,
            self.player.share_set.get(company=self.company).shares)

    # mock.patch does not work on relative imports so use mock.patch.object
    @mock.patch.object(utils, 'transfer_money')
    def test_player_buying_from_ipo_gives_money_to_bank(self,
            mock_transfer_money):
        utils.buy_share(self.player, self.company, utils.IPO_SHARES, 11)
        mock_transfer_money.assert_called_once_with(self.player, None, 11)

    def test_player_buying_from_bank_pool_gives_share_to_player(self):
        self.company.bank_shares = 10
        utils.buy_share(self.player, self.company, utils.BANK_SHARES, 10)
        self.assertEqual(1,
            self.player.share_set.get(company=self.company).shares)

    @mock.patch.object(utils, 'transfer_money')
    def test_player_buying_from_bank_pool_gives_money_to_bank(self,
            mock_transfer_money):
        self.company.bank_shares = 10
        utils.buy_share(self.player, self.company, utils.BANK_SHARES, 6)
        mock_transfer_money.assert_called_once_with(self.player, None, 6)

    def test_player_cannot_buy_from_pool_if_there_are_no_pool_shares(self):
        self.company.bank_shares = 0
        with self.assertRaises(utils.InvalidShareTransaction):
            utils.buy_share(self.player, self.company, utils.BANK_SHARES, 8)

    def test_player_cannot_buy_from_ipo_if_there_are_no_ipo_shares(self):
        self.company.ipo_shares = 0
        with self.assertRaises(utils.InvalidShareTransaction):
            utils.buy_share(self.player, self.company, utils.IPO_SHARES, 10)

    def test_player_buying_from_ipo_removes_share_from_ipo(self):
        self.company.ipo_shares = 10
        utils.buy_share(self.player, self.company, utils.IPO_SHARES, 1)
        self.assertEqual(self.company.ipo_shares, 9)

    def test_player_buying_from_bank_pool_removes_share_from_pool(self):
        self.company.bank_shares = 10
        utils.buy_share(self.player, self.company, utils.BANK_SHARES, 1)
        self.assertEqual(self.company.bank_shares, 9)

    @mock.patch.object(utils, 'transfer_money')
    def test_player_buying_from_company_gives_money_to_company(self,
            mock_transfer_money):
        factories.CompanyShareFactory(owner=self.company, company=self.company)
        utils.buy_share(self.player, self.company, self.company, 13)
        mock_transfer_money.assert_called_once_with(self.player, self.company,
            13)

    def test_player_buying_from_company_removes_share_from_company(self):
        share = factories.CompanyShareFactory(owner=self.company,
            company=self.company, shares=3)
        utils.buy_share(self.player, self.company, self.company, 14)
        share.refresh_from_db()
        self.assertEqual(share.shares, 2)

    def test_player_cannot_buy_from_company_if_it_has_no_shares(self):
        with self.assertRaises(utils.InvalidShareTransaction):
            utils.buy_share(self.player, self.company, self.company, 0)

    def test_player_cannot_buy_from_company_if_it_has_no_shares_anymore(self):
        factories.CompanyShareFactory(owner=self.company, company=self.company,
            shares=0)
        with self.assertRaises(utils.InvalidShareTransaction):
            utils.buy_share(self.player, self.company, self.company, 1)

    def test_player_cannot_buy_from_ipo_if_it_has_too_few_shares(self):
        self.company.ipo_shares = 2
        with self.assertRaises(utils.InvalidShareTransaction):
            utils.buy_share(self.player, self.company, utils.IPO_SHARES, 1, 3)

    def test_player_cannot_buy_from_bank_pool_if_it_has_too_few_shares(self):
        self.company.bank_shares = 2
        with self.assertRaises(utils.InvalidShareTransaction):
            utils.buy_share(self.player, self.company, utils.BANK_SHARES, 1, 3)

    def test_player_cannot_buy_from_company_if_it_has_too_few_shares(self):
        factories.CompanyShareFactory(owner=self.company, company=self.company,
            shares=2)
        with self.assertRaises(utils.InvalidShareTransaction):
            utils.buy_share(self.player, self.company, self.company, 0, 3)

    def test_player_can_buy_additional_share_from_ipo(self):
        factories.PlayerShareFactory(owner=self.player, company=self.company)
        utils.buy_share(self.player, self.company, utils.IPO_SHARES, 1)
        self.assertEqual(2,
            self.player.share_set.get(company=self.company).shares)

    def test_player_can_buy_additional_share_from_bank_pool(self):
        self.company.bank_shares = 10
        factories.PlayerShareFactory(owner=self.player, company=self.company)
        utils.buy_share(self.player, self.company, utils.BANK_SHARES, 2)
        self.assertEqual(2,
            self.player.share_set.get(company=self.company).shares)

    def test_player_can_buy_additional_share_from_company(self):
        factories.PlayerShareFactory(owner=self.player, company=self.company)
        factories.CompanyShareFactory(owner=self.company, company=self.company)
        utils.buy_share(self.player, self.company, self.company, 3)
        self.assertEqual(2,
            self.player.share_set.get(company=self.company).shares)


class CompanyShareTransactionTests(TestCase):
    """Test buying and selling shares for companies"""
    def setUp(self):
        self.game = factories.GameFactory()
        self.company1, self.company2 = factories.CompanyFactory.create_batch(
            size=2, game=self.game, cash=1000)

    def test_company_share_record_does_not_exist_by_default(self):
        with self.assertRaises(models.CompanyShare.DoesNotExist):
            self.company1.share_set.get(company=self.company1)

    def test_company_buying_share_auto_creates_companyshare_record(self):
        utils.buy_share(self.company1, self.company2, utils.IPO_SHARES, 10)
        self.assertEqual(models.CompanyShare.objects.count(), 1)
        self.company1.share_set.get(company=self.company2)

    def test_company_buying_from_ipo_gives_share_to_company(self):
        utils.buy_share(self.company1, self.company2, utils.IPO_SHARES, 10)
        self.assertEqual(1,
            self.company1.share_set.get(company=self.company2).shares)

    def test_company_can_buy_multiple_shares_at_the_same_time(self):
        utils.buy_share(self.company1, self.company2, utils.IPO_SHARES, 2, 3)
        self.assertEqual(3,
            self.company1.share_set.get(company=self.company2).shares)

    @mock.patch.object(utils, 'transfer_money')
    def test_company_buying_from_ipo_gives_money_to_bank(self,
            mock_transfer_money):
        utils.buy_share(self.company1, self.company2, utils.IPO_SHARES, 12)
        mock_transfer_money.assert_called_once_with(self.company1, None, 12)

    def test_company_buying_from_bank_pool_gives_share_to_company(self):
        self.company2.bank_shares = 10
        utils.buy_share(self.company1, self.company2, utils.BANK_SHARES, 10)
        self.assertEqual(1,
            self.company1.share_set.get(company=self.company2).shares)

    @mock.patch.object(utils, 'transfer_money')
    def test_company_buying_from_bank_pool_gives_money_to_bank(self,
            mock_transfer_money):
        self.company2.bank_shares = 10
        utils.buy_share(self.company1, self.company2, utils.BANK_SHARES, 7)
        mock_transfer_money.assert_called_once_with(self.company1, None, 7)

    def test_company_cannot_buy_from_pool_if_there_are_no_pool_shares(self):
        self.company2.bank_shares = 0
        with self.assertRaises(utils.InvalidShareTransaction):
            utils.buy_share(self.company1, self.company2, utils.BANK_SHARES, 9)

    def test_company_cannot_buy_from_ipo_if_there_are_no_ipo_shares(self):
        self.company2.ipo_shares = 0
        with self.assertRaises(utils.InvalidShareTransaction):
            utils.buy_share(self.company1, self.company2, utils.IPO_SHARES, 11)

    def test_company_can_buy_shares_from_different_company_from_bank(self):
        self.company2.bank_shares = 10
        utils.buy_share(self.company1, self.company2, utils.BANK_SHARES, 16)
        self.assertEqual(1,
            self.company1.share_set.get(company=self.company2).shares)

    def test_company_can_buy_shares_from_different_company(self):
        factories.CompanyShareFactory(owner=self.company2,
            company=self.company2)
        utils.buy_share(self.company1, self.company2, self.company2, 17)
        self.assertEqual(1,
            self.company1.share_set.get(company=self.company2).shares)

    @mock.patch.object(utils, 'transfer_money')
    def test_company_buying_from_different_company_transfers_money(self,
            mock_transfer_money):
        factories.CompanyShareFactory(owner=self.company2,
            company=self.company2)
        utils.buy_share(self.company1, self.company2, self.company2, 18)
        mock_transfer_money.assert_called_once_with(self.company1,
            self.company2, 18)

    def test_company_buying_from_different_company_removes_share(self):
        share = factories.CompanyShareFactory(owner=self.company2,
            company=self.company2)
        utils.buy_share(self.company1, self.company2, self.company2, 17)
        share.refresh_from_db()
        self.assertEqual(share.shares, 0)

    def test_company_cannot_buy_from_company_if_it_has_no_shares(self):
        with self.assertRaises(utils.InvalidShareTransaction):
            utils.buy_share(self.company1, self.company2, self.company2, 2)

    def test_company_cannot_buy_from_company_if_it_has_no_shares_anymore(self):
        factories.CompanyShareFactory(owner=self.company2,
            company=self.company2, shares=0)
        with self.assertRaises(utils.InvalidShareTransaction):
            utils.buy_share(self.company1, self.company2, self.company2, 3)

    def test_company_cannot_buy_from_company_if_it_has_not_enough_shares(self):
        factories.CompanyShareFactory(owner=self.company2,
            company=self.company2, shares=2)
        with self.assertRaises(utils.InvalidShareTransaction):
            utils.buy_share(self.company1, self.company2, self.company2, 0, 3)

    def test_company_can_buy_additional_share_from_ipo(self):
        factories.CompanyShareFactory(owner=self.company1,
            company=self.company1)
        utils.buy_share(self.company1, self.company1, utils.IPO_SHARES, 4)
        self.assertEqual(2,
            self.company1.share_set.get(company=self.company1).shares)

    def test_company_can_buy_additional_share_from_bank_pool(self):
        self.company2.bank_shares = 10
        factories.CompanyShareFactory(owner=self.company1,
            company=self.company2)
        utils.buy_share(self.company1, self.company2, utils.BANK_SHARES, 5)
        self.assertEqual(2,
            self.company1.share_set.get(company=self.company2).shares)

    def test_company_can_buy_additional_share_from_company(self):
        factories.CompanyShareFactory(owner=self.company1,
            company=self.company2)
        factories.CompanyShareFactory(owner=self.company2,
            company=self.company2, shares = 3)
        utils.buy_share(self.company1, self.company2, self.company2, 6)
        self.assertEqual(2,
            self.company1.share_set.get(company=self.company2).shares)

    def test_company_can_buy_its_own_shares_from_its_ipo(self):
        utils.buy_share(self.company1, self.company1, utils.IPO_SHARES, 1, 5)
        self.assertEqual(5,
            self.company1.share_set.get(company=self.company1).shares)

    def test_company_can_buy_its_own_shares_from_the_bank_pool(self):
        self.company1.bank_shares = 4
        utils.buy_share(self.company1, self.company1, utils.BANK_SHARES, 1, 4)
        self.assertEqual(4,
            self.company1.share_set.get(company=self.company1).shares)

    def test_company_buying_from_ipo_removes_share_from_ipo(self):
        self.company2.ipo_shares = 10
        utils.buy_share(self.company1, self.company2, utils.IPO_SHARES, 1)
        self.assertEqual(9, self.company2.ipo_shares)

    def test_company_buying_from_bank_pool_removes_share_from_pool(self):
        self.company2.bank_shares = 10
        utils.buy_share(self.company1, self.company2, utils.BANK_SHARES, 1)
        self.company2.refresh_from_db()
        self.assertEqual(9, self.company2.bank_shares)

    def test_company_cannot_buy_from_ipo_if_it_has_too_few_shares(self):
        self.company2.ipo_shares = 0
        with self.assertRaises(utils.InvalidShareTransaction):
            utils.buy_share(self.company1, self.company2, utils.IPO_SHARES, 1)

    def test_company_cannot_buy_from_bank_pool_if_it_has_too_few_shares(self):
        self.company2.bank_shares = 0
        with self.assertRaises(utils.InvalidShareTransaction):
            utils.buy_share(self.company1, self.company2, utils.BANK_SHARES, 1)