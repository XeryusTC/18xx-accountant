# -*- coding: utf-8 -*-
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import unittest
from unittest import mock

from .. import models
from .. import factories
from .. import utils
from .. import serializers
from .. import views

game = None

def setUpModule():
    global game
    game = factories.GameFactory.create()

def tearDownModule():
    game.delete()


class ApiRootTests(APITestCase):
    def setUp(self):
        self.url = reverse('api-root')

    def test_Game_viewset_is_on_api_root(self):
        response = self.client.get(self.url, {}, format='json')
        self.assertTrue(response.data['game'].endswith(reverse('game-list')))

    def test_Player_viewset_is_on_api_root(self):
        response = self.client.get(self.url, {}, format='json')
        self.assertTrue(response.data['player'].endswith(
            reverse('player-list')))

    def test_Company_viewset_is_on_api_root(self):
        response = self.client.get(self.url, {}, format='json')
        self.assertTrue(response.data['company'].endswith(
            reverse('company-list')))

    def test_PlayerShare_viewset_is_on_api_root(self):
        response = self.client.get(self.url, {}, format='json')
        self.assertTrue(response.data['playershare'].endswith(
            reverse('playershare-list')))

    def test_CompanyShare_viewset_is_on_api_root(self):
        response = self.client.get(self.url, {}, format='json')
        self.assertTrue(response.data['companyshare'].endswith(
            reverse('companyshare-list')))

    def test_transfer_money_view_is_on_api_root(self):
        response = self.client.get(self.url, {}, format='json')
        self.assertTrue(response.data['transfer_money'].endswith(
            reverse('transfer_money')))

    def test_transfer_share_view_is_on_api_root(self):
        response = self.client.get(self.url, {}, format='json')
        self.assertTrue(response.data['transfer_share'].endswith(
            reverse('transfer_share')))

    def test_operate_view_is_on_api_root(self):
        response = self.client.get(self.url, {}, format='json')
        self.assertTrue(response.data['operate'].endswith(reverse('operate')))


class GameTests(APITestCase):
    def test_create_game(self):
        """Ensure that we can create a game."""
        url = reverse('game-list')
        data = {'players': [], 'companies': []}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            "Could not create game: " + str(response.data))
        # We have 2 games since there is also a global game
        self.assertEqual(models.Game.objects.count(), 2)


class PlayerTests(APITestCase):
    def test_create_player(self):
        """Ensure that we can create players."""
        url = reverse('player-list')
        data = {'name': 'Alice', 'game': game.pk}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            "Could not create a player: " + str(response.data))
        self.assertEqual(models.Player.objects.count(), 1)

    def test_cannot_create_duplicate_player_for_single_game(self):
        """Disallow creating two players with the same name in a game."""
        player = factories.PlayerFactory.create(game=game, name='Alice')
        url = reverse('player-list')
        data = {'name': 'Alice', 'game': game.pk}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            "Created duplicate player: " + str(response.data))
        self.assertEqual(models.Player.objects.count(), 1)

    def test_creating_player_decreases_cash_in_bank(self):
        game.cash = 12000
        game.save()
        url = reverse('player-list')
        data = {'name': 'Alice', 'game': game.pk, 'cash': 500}

        response = self.client.post(url, data, format='json')

        game.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Player.objects.first().cash, 500)
        self.assertEqual(game.cash, 11500)


class CompanyTests(APITestCase):
    def test_create_company(self):
        """Ensure that we can create companies."""
        url = reverse('company-list')
        data = {'name': 'B&O', 'game': game.pk}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            "Could not create a company: " + str(response.data))
        self.assertEqual(models.Company.objects.count(), 1)

    def test_cannot_create_duplicate_company_for_single_game(self):
        """Disallow creating two companies with the same name in a game."""
        company = factories.CompanyFactory.create(game=game, name='B&O')
        url = reverse('company-list')
        data = {'name': 'B&O', 'game': game.pk}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            "Created duplicate company: " + str(response.data))
        self.assertEqual(models.Company.objects.count(), 1)

    def test_creating_company_decreases_cash_in_bank(self):
        game.cash = 1000
        game.save()
        url = reverse('company-list')
        data = {'name': 'PRR', 'game': game.pk, 'cash': 300}

        response = self.client.post(url, data, format='json')

        game.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Company.objects.first().cash, 300)
        self.assertEqual(game.cash, 700)


class PlayerShareTests(APITestCase):
    def test_create_share(self):
        """Ensure that we can create shares."""
        player = factories.PlayerFactory.create(game=game)
        company = factories.CompanyFactory.create(game=game)
        url = reverse('playershare-list')
        data = {'game': game.pk, 'owner': player.pk, 'company': company.pk}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            "Could not create a share: " + str(response.data))
        self.assertEqual(models.PlayerShare.objects.count(), 1)

    def test_cannot_create_duplicate_share_holdings(self):
        """
        Ensure that a player doesn't have two share holding records for
        a single company
        """
        player = factories.PlayerFactory.create(game=game)
        company = factories.CompanyFactory.create(game=game)
        share = factories.PlayerShareFactory.create(owner=player,
            company=company)
        url = reverse('playershare-list')
        data = {'owner': player.pk, 'company': company.pk}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            "Created duplicate share holdings: " + str(response.data))
        self.assertEqual(models.PlayerShare.objects.count(), 1)
        self.assertIn('non_field_errors', response.data.keys())


class CompanyShareTests(APITestCase):
    def test_create_self_owning_share(self):
        """Ensure that we can create company shares."""
        company = factories.CompanyFactory.create(game=game)
        url = reverse('companyshare-list')
        data = {'owner': company.pk, 'company': company.pk}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            "Could not create a self owning share: " + str(response.data))
        self.assertEqual(models.CompanyShare.objects.count(), 1)

    def test_create_share_owning_other_company(self):
        """Ensure that companies can own shares in other companies."""
        company1, company2 = factories.CompanyFactory.create_batch(size=2,
            game=game)
        url = reverse('companyshare-list')
        data = {'owner': company1.pk, 'company': company2.pk}

        response = self.client.post(url, data, format='json')

        share = models.CompanyShare.objects.first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            "Could not create a company share: " + str(response.data))
        self.assertEqual(models.CompanyShare.objects.count(), 1)
        self.assertEqual(share.owner, company1)
        self.assertEqual(share.company, company2)

    def test_cannot_create_duplicate_share_holdings(self):
        """
        Ensure that a company doesn't have two share holding records for a
        single company
        """
        company1, company2 = factories.CompanyFactory.create_batch(size=2,
            game=game)
        share = factories.CompanyShareFactory.create(owner=company1,
            company=company2)
        url = reverse('companyshare-list')
        data = {'owner': company1.pk, 'company': company2.pk}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            "Created duplicate share holdings: " + str(response.data))
        self.assertEqual(models.CompanyShare.objects.count(), 1)
        self.assertIn('non_field_errors', response.data.keys())


@mock.patch.object(utils, 'transfer_money')
class TransferMoneyTests(APITestCase):
    def setUp(self):
        game.cash = 1000
        self.url = reverse('transfer_money')
        self.player = factories.PlayerFactory(game=game, cash=100)
        self.company = factories.CompanyFactory(game=game, cash=100)

    def test_GET_request_is_empty(self, mock):
        """GET is for debug (and doc) purposes only"""
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data)

    def test_can_transfer_money_from_player_to_bank(self, mock_transfer_money):
        data = {'from_player': self.player.pk, 'amount': 99}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_transfer_money.assert_called_once_with(self.player, None, 99)

    def test_can_transfer_money_from_bank_to_player(self, mock_transfer_money):
        data = {'to_player': self.player.pk, 'amount': 98}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_transfer_money.assert_called_once_with(None, self.player, 98)

    def test_can_transfer_money_from_company_to_bank(self,
            mock_transfer_money):
        data = {'from_company': self.company.pk, 'amount': 97}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_transfer_money.assert_called_once_with(self.company, None, 97)

    def test_can_transfer_money_from_bank_to_company(self,
            mock_transfer_money):
        data = {'to_company': self.company.pk, 'amount': 96}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_transfer_money.assert_called_once_with(None, self.company, 96)

    def test_can_transfer_money_from_player_to_company(self,
            mock_transfer_money):
        data = {'from_player': self.player.pk, 'to_company': self.company.pk,
            'amount': 95}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_transfer_money.assert_called_once_with(self.player, self.company,
            95)

    def test_can_transfer_money_from_company_to_player(self,
            mock_transfer_money):
        data = {'to_player': self.player.pk, 'from_company': self.company.pk,
            'amount': 94}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_transfer_money.assert_called_once_with(self.company, self.player,
            94)

    def test_transfering_from_bank_to_bank_raises_error(self, mock):
        data = {'amount': 93}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(serializers.SOURCE_OR_DEST_REQUIRED_ERROR,
            response.data['non_field_errors'])

    def test_transfer_from_player_to_company_in_other_game_raises_error(self,
            mock):
        company = factories.CompanyFactory(cash=100)
        data = {'from_player': self.player.pk, 'to_company': company.pk,
            'amount': 92}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(serializers.DIFFERENT_GAME_ERROR,
            response.data['non_field_errors'])

    def test_transfer_from_company_to_player_in_other_game_raises_error(self,
            mock):
        company = factories.CompanyFactory(cash=100)
        data = {'to_player': self.player.pk, 'from_company': company.pk,
            'amount': 91}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(serializers.DIFFERENT_GAME_ERROR,
            response.data['non_field_errors'])

    def test_transfer_between_players_in_different_games_raises_error(self,
            mock):
        player2 = factories.PlayerFactory(cash=100)
        data = {'from_player': self.player.pk, 'to_player': player2.pk,
            'amount': 90}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(serializers.DIFFERENT_GAME_ERROR,
            response.data['non_field_errors'])

    def test_transfer_between_companies_in_different_games_raises_error(self,
            mock):
        company2 = factories.CompanyFactory(cash=100)
        data = {'from_company': self.company.pk, 'to_company': company2.pk,
            'amount': 89}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(serializers.DIFFERENT_GAME_ERROR,
            response.data['non_field_errors'])


@mock.patch.object(utils, 'buy_share')
class ShareTransactionTests(APITestCase):
    def setUp(self):
        game.cash = 1000
        self.url = reverse('transfer_share')
        self.player = factories.PlayerFactory(game=game, cash=100)
        self.source_company = factories.CompanyFactory(game=game, cash=0)
        self.buy_company = factories.CompanyFactory(game=game, cash=0)

    def test_GET_request_is_empty(self, mock):
        """GET is for debug (and doc) purposes only"""
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data)

    def test_player_can_buy_from_ipo(self, mock_buy_share):
        data = {'buyer_type': 'player', 'player_buyer': self.player.pk,
            'source_type': 'ipo', 'share': self.source_company.pk, 'price': 1}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(self.player,
            self.source_company, utils.Share.IPO, 1, 1)

    def test_player_can_buy_from_bank_pool(self, mock_buy_share):
        data = {'buyer_type': 'player', 'player_buyer': self.player.pk,
            'source_type': 'bank', 'share': self.source_company.pk, 'price': 2}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(self.player,
            self.source_company, utils.Share.BANK, 2, 1)

    def test_player_can_buy_from_company_treasury(self, mock_buy_share):
        data = {'buyer_type': 'player', 'player_buyer': self.player.pk,
            'source_type': 'company', 'company_source': self.source_company.pk,
            'share': self.source_company.pk, 'price': 3}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(self.player,
            self.source_company, self.source_company, 3, 1)

    def test_player_can_sell_to_ipo(self, mock_buy_share):
        factories.PlayerShareFactory(owner=self.player,
            company=self.source_company)
        data = {'buyer_type': 'ipo', 'source_type': 'player',
            'player_source': self.player.pk, 'share': self.source_company.pk,
            'price': 4}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(utils.Share.IPO,
            self.source_company, self.player, 4, 1)

    def test_player_can_sell_to_bank_pool(self, mock_buy_share):
        factories.PlayerShareFactory(owner=self.player,
            company=self.source_company)
        data = {'buyer_type': 'bank', 'source_type': 'player',
            'player_source': self.player.pk, 'share': self.source_company.pk,
            'price': 5}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(utils.Share.BANK,
            self.source_company, self.player, 5, 1)

    def test_company_can_buy_own_share_from_ipo(self, mock_buy_share):
        data = {'buyer_type': 'company', 'company_buyer': self.buy_company.pk,
            'source_type': 'ipo', 'share': self.buy_company.pk,
            'price': 6}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.buy_company, utils.Share.IPO, 6, 1)

    def test_company_can_buy_own_share_from_bank_pool(self, mock_buy_share):
        data = {'buyer_type': 'company', 'company_buyer': self.buy_company.pk,
            'source_type': 'bank', 'share': self.buy_company.pk,
            'price': 7}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.buy_company, utils.Share.BANK, 7, 1)

    def test_company_can_buy_from_other_company_ipo(self, mock_buy_share):
        data = {'buyer_type': 'company', 'company_buyer': self.buy_company.pk,
            'source_type': 'ipo', 'share': self.source_company.pk,
            'price': 8}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.source_company, utils.Share.IPO, 8, 1)

    def test_company_can_buy_from_other_company_bank_pool(self,
            mock_buy_share):
        data = {'buyer_type': 'company', 'company_buyer': self.buy_company.pk,
            'source_type': 'bank', 'share': self.source_company.pk,
            'price': 9}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.source_company, utils.Share.BANK, 9, 1)

    def test_company_can_buy_from_other_company_treasury(self, mock_buy_share):
        data = {'buyer_type': 'company', 'company_buyer': self.buy_company.pk,
            'source_type': 'company', 'company_source': self.source_company.pk,
            'share': self.source_company.pk, 'price': 10}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.source_company, self.source_company, 10, 1)

    def test_company_can_sell_to_ipo(self, mock_buy_share):
        factories.CompanyShareFactory(owner=self.buy_company,
            company=self.source_company)
        data = {'buyer_type': 'ipo', 'source_type': 'company',
            'company_source': self.buy_company.pk,
            'share': self.source_company.pk, 'price': 11}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(utils.Share.IPO,
            self.source_company, self.buy_company, 11, 1)

    def test_company_can_sell_to_bank_pool(self, mock_buy_share):
        factories.CompanyShareFactory(owner=self.buy_company,
            company=self.source_company)
        data = {'buyer_type': 'bank', 'source_type': 'company',
            'company_source': self.buy_company.pk,
            'share': self.source_company.pk, 'price': 12}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(utils.Share.BANK,
            self.source_company, self.buy_company, 12, 1)

    def test_player_cannot_buy_from_ipo_if_it_has_no_shares(self,
            mock_buy_share):
        self.source_company.ipo_shares = 0
        self.source_company.save()
        mock_buy_share.side_effect = utils.InvalidShareTransaction
        data = {'buyer_type': 'player', 'player_buyer': self.player.pk,
            'source_type': 'ipo', 'share': self.source_company.pk, 'price': 13}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(views.NO_AVAILABLE_SHARES_ERROR,
            response.data['non_field_errors'])

    def test_player_cannot_buy_from_bank_pool_if_it_has_no_shares(self,
            mock_buy_share):
        mock_buy_share.side_effect = utils.InvalidShareTransaction
        data = {'buyer_type': 'player', 'player_buyer': self.player.pk,
            'source_type': 'bank', 'share': self.source_company.pk,
            'price': 14}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(views.NO_AVAILABLE_SHARES_ERROR,
            response.data['non_field_errors'])

    def test_player_cannot_buy_from_company_if_it_has_no_shares(self,
            mock_buy_share):
        factories.CompanyShareFactory(owner=self.buy_company,
            company=self.source_company, shares=0)
        mock_buy_share.side_effect = utils.InvalidShareTransaction
        data = {'buyer_type': 'player', 'player_buyer': self.player.pk,
            'source_type': 'company', 'company_source': self.buy_company.pk,
            'share': self.source_company.pk, 'price': 15}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(views.NO_AVAILABLE_SHARES_ERROR,
            response.data['non_field_errors'])

    def test_company_cannot_buy_from_ipo_if_it_has_no_shares(self,
            mock_buy_share):
        self.source_company.ipo_shares = 0
        data = {'buyer_type': 'company', 'company_buyer': self.buy_company.pk,
            'source_type': 'ipo', 'share': self.source_company.pk, 'price': 18}
        mock_buy_share.side_effect = utils.InvalidShareTransaction
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(views.NO_AVAILABLE_SHARES_ERROR,
            response.data['non_field_errors'])

    def test_company_cannot_buy_from_bank_pool_if_it_has_no_shares(self,
            mock_buy_share):
        self.source_company.bank_shares = 0
        data = {'buyer_type': 'company', 'company_buyer': self.buy_company.pk,
            'source_type': 'bank', 'share': self.source_company.pk,
            'price': 19}
        mock_buy_share.side_effect = utils.InvalidShareTransaction
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(views.NO_AVAILABLE_SHARES_ERROR,
            response.data['non_field_errors'])

    def test_company_cannot_buy_from_other_company_if_it_has_no_shares(self,
            mock_buy_share):
        factories.CompanyShareFactory(owner=self.source_company,
            company=self.source_company, shares=0)
        mock_buy_share.side_effect = utils.InvalidShareTransaction
        data = {'buyer_type': 'company', 'company_buyer': self.buy_company.pk,
            'source_type': 'company', 'company_source': self.source_company.pk,
            'share': self.source_company.pk, 'price': 20}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(views.NO_AVAILABLE_SHARES_ERROR,
            response.data['non_field_errors'])

    def test_company_cannot_sell_to_ipo_if_it_has_no_shares(self,
            mock_buy_share):
        factories.CompanyShareFactory(owner=self.buy_company,
            company=self.source_company, shares=0)
        mock_buy_share.side_effect = utils.InvalidShareTransaction
        data = {'buyer_type': 'ipo', 'source_type': 'company',
            'company_source': self.buy_company.pk,
            'share': self.source_company.pk, 'share': self.source_company.pk,
            'price': 21}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(views.NO_AVAILABLE_SHARES_ERROR,
            response.data['non_field_errors'])

    def test_company_cannot_sell_to_bank_pool_if_it_has_no_shares(self,
            mock_buy_share):
        factories.CompanyShareFactory(owner=self.buy_company,
            company=self.source_company, shares=0)
        mock_buy_share.side_effect = utils.InvalidShareTransaction
        data = {'buyer_type': 'bank', 'source_type': 'company',
            'company_source': self.buy_company.pk,
            'share': self.source_company.pk, 'share': self.source_company.pk,
            'price': 22}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(views.NO_AVAILABLE_SHARES_ERROR,
            response.data['non_field_errors'])

    def test_player_buying_negative_ipo_shares_turns_into_sell_action(self,
            mock_buy_share):
        data = {'buyer_type': 'player', 'player_buyer': self.player.pk,
            'source_type': 'ipo', 'share': self.source_company.pk, 'price': 23,
            'amount': -2}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(utils.Share.IPO,
            self.source_company, self.player, 23, 2)

    def test_player_buying_negative_bank_shares_turns_into_sell_action(self,
            mock_buy_share):
        data = {'buyer_type': 'player', 'player_buyer': self.player.pk,
            'source_type': 'bank', 'share': self.source_company.pk,
            'price': 24, 'amount': -5}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(utils.Share.BANK,
            self.source_company, self.player, 24, 5)

    def test_company_buying_negative_ipo_shares_turns_into_sell_action(self,
            mock_buy_share):
        data = {'buyer_type': 'company', 'company_buyer': self.buy_company.pk,
            'source_type': 'ipo', 'share': self.source_company.pk, 'price': 25,
            'amount': -3}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(utils.Share.IPO,
            self.source_company, self.buy_company, 25, 3)

    def test_company_buying_negative_bank_shares_turns_into_sell_action(self,
            mock_buy_share):
        data = {'buyer_type': 'company', 'company_buyer': self.buy_company.pk,
            'source_type': 'bank', 'share': self.source_company.pk,
            'price': 26, 'amount': -1}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(utils.Share.BANK,
            self.source_company, self.buy_company, 26, 1)

    def test_player_buying_negative_company_shares_turns_into_sell_action(self,
            mock_buy_share):
        data = {'buyer_type': 'player', 'player_buyer': self.player.pk,
            'source_type': 'company', 'company_source': self.buy_company.pk,
            'share': self.source_company.pk, 'price': 27, 'amount': -1}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.source_company, self.player, 27, 1)

    def test_company_buying_negative_company_shares_turns_into_sell_action(
            self, mock_buy_share):
        data = {'buyer_type': 'company', 'company_buyer': self.buy_company.pk,
            'source_type': 'company', 'company_source': self.source_company.pk,
            'share': self.source_company.pk, 'price': 28, 'amount': -2}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(self.source_company,
            self.source_company, self.buy_company, 28, 2)

    def test_gives_error_if_request_is_invalid(self, mock_buy_share):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@mock.patch.object(utils, 'operate')
class OperateTests(APITestCase):
    def setUp(self):
        self.url = reverse('operate')
        self.company = factories.CompanyFactory()

    def test_GET_request_is_empty(self, mock):
        """GET is for debug (and doc) purposes only"""
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data)

    def test_company_can_pay_full_dividends(self, mock_operate):
        data = {'company': self.company.pk, 'amount': 10, 'method': 'full'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_operate.assert_called_once_with(self.company, 10,
            utils.OperateMethod.FULL)

    def test_company_can_pay_half_dividends(self, mock_operate):
        data = {'company': self.company.pk, 'amount': 20, 'method': 'half'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_operate.assert_called_once_with(self.company, 20,
            utils.OperateMethod.HALF)

    def test_company_can_withhold_revenue(self, mock_operate):
        data = {'company': self.company.pk, 'amount': 30, 'method': 'withhold'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_operate.assert_called_once_with(self.company, 30,
            utils.OperateMethod.WITHHOLD)

    def test_gives_error_if_request_is_invalid(self, mock_buy_share):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ColorsTests(APITestCase):
    def setUp(self):
        self.url = reverse('colors')

    def test_returns_list_of_company_colors(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.data, models.Company.COLOR_CODES)
