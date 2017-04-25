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

    def test_retrieve_players_within_a_single_game(self):
        """Filter the players based on the game in the query url"""
        players = factories.PlayerFactory.create_batch(game=game, size=3)
        factories.PlayerFactory.create_batch(size=2)
        url = reverse('player-list') + '?game=' + str(game.pk)

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual([p.name for p in players],
            [p['name'] for p in response.data])

    def test_retrieve_all_players_when_no_query_params_set(self):
        factories.PlayerFactory.create_batch(size=5)
        url = reverse('player-list')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual([p.name for p in models.Player.objects.all()],
            [p['name'] for p in response.data])


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

    def test_retrieve_all_companies_when_no_query_params_set(self):
        factories.CompanyFactory.create_batch(size=5)
        url = reverse('company-list')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual([c.name for c in models.Company.objects.all()],
            [c['name'] for c in response.data])

    def test_retrieve_companies_within_a_single_game(self):
        """Filter companies based on the game in the query parameters"""
        companies = factories.CompanyFactory.create_batch(game=game, size=2)
        factories.CompanyFactory.create_batch(size=2)
        url = reverse('company-list') + '?game=' + str(game.pk)

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual([c.name for c in companies],
            [c['name'] for c in response.data])


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

    def test_retrieve_all_shares_when_no_query_params_set(self):
        factories.PlayerShareFactory.create_batch(size=5)
        url = reverse('playershare-list')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual([s['uuid'] for s in response.data],
            [str(s.uuid) for s in models.PlayerShare.objects.all()])

    def test_retrieve_shares_of_single_player(self):
        """Filter shares based on the player in the query parameters"""
        player = factories.PlayerFactory.create(game=game)
        shares = factories.PlayerShareFactory.create_batch(owner=player,
            size=2)
        factories.PlayerShareFactory.create_batch(size=3)
        url = reverse('playershare-list') + '?owner=' + str(player.pk)

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual([s['uuid'] for s in response.data],
            [str(s.uuid) for s in shares])

    def test_retrieve_all_player_shares_in_a_game(self):
        """Filter shares based on the game in the query parameters"""
        players = factories.PlayerFactory.create_batch(game=game, size=2)
        shares = factories.PlayerShareFactory.create_batch(size=11,
            owner=players[0]) + factories.PlayerShareFactory.create_batch(
                size=13, owner=players[1])
        factories.PlayerShareFactory.create_batch(size=17)
        url = reverse('playershare-list') + '?game=' + str(game.pk)

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.maxDiff = None
        self.assertCountEqual([s['uuid'] for s in response.data],
            [str(s.uuid) for s in shares])


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

    def test_retrieve_all_shares_when_no_query_params_set(self):
        factories.CompanyShareFactory.create_batch(size=7)
        url = reverse('companyshare-list')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual([s['uuid'] for s in response.data],
            [str(s.uuid) for s in models.CompanyShare.objects.all()])

    def test_retrieve_shares_of_single_company(self):
        company = factories.CompanyFactory.create()
        shares = factories.CompanyShareFactory.create_batch(owner=company,
            size=3)
        factories.CompanyShareFactory.create_batch(size=5)
        url = reverse('companyshare-list') + '?owner=' + str(company.pk)

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual([s['uuid'] for s in response.data],
            [str(s.uuid) for s in  shares])

    def test_retrieve_all_shares_in_a_game(self):
        companies = factories.CompanyFactory.create_batch(game=game, size=2)
        shares = factories.CompanyShareFactory.create_batch(size=2,
            owner=companies[0]) + factories.CompanyShareFactory.create_batch(
                size=3, owner=companies[1])
        factories.CompanyShareFactory.create_batch(size=5)
        url = reverse('companyshare-list') + '?game=' + str(game.pk)

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual([s['uuid'] for s in response.data],
            [str(s.uuid) for s in  shares])


class TransferMoneyTests(APITestCase):
    def setUp(self):
        self.url = reverse('transfer_money')
        self.player = factories.PlayerFactory(game=game, cash=100)
        self.company = factories.CompanyFactory(game=game, cash=100)

    def test_transfering_from_bank_includes_game_instance_in_response(self):
        data = {'to_player': self.player.pk, 'amount': 1}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.data['game']['uuid'], str(game.pk))
        self.assertEqual(response.data['game']['cash'], 11999)

    def test_transfering_to_bank_includes_game_instance_in_response(self):
        data = {'from_player': self.player.pk, 'amount': 2}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.data['game']['uuid'], str(game.pk))
        self.assertEqual(response.data['game']['cash'], 12002)

    def test_transfering_from_player_includes_instance_in_response(self):
        data = {'from_player': self.player.pk, 'amount': 3}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.data['players'][0]['uuid'],
            str(self.player.pk))
        self.assertEqual(response.data['players'][0]['cash'], 97)

    def test_transfering_to_player_includes_instance_in_response(self):
        data = {'to_player': self.player.pk, 'amount': 4}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.data['players'][0]['uuid'],
            str(self.player.pk))
        self.assertEqual(response.data['players'][0]['cash'], 104)

    def test_transfering_from_company_includes_instance_in_response(self):
        data = {'from_company': self.company.pk, 'amount': 5}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.data['companies'][0]['uuid'],
            str(self.company.pk))
        self.assertEqual(response.data['companies'][0]['cash'], 95)

    def test_transfering_to_company_includes_instance_in_response(self):
        data = {'to_company': self.company.pk, 'amount': 6}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.data['companies'][0]['uuid'],
            str(self.company.pk))
        self.assertEqual(response.data['companies'][0]['cash'], 106)

    def test_game_should_not_be_in_response_if_no_transfer_with_bank(self):
        data = {'from_player': self.player.pk, 'to_company': self.company.pk,
            'amount': 7}
        response = self.client.post(self.url, data, format='json')
        self.assertNotIn('game', response.data)

    def test_players_should_not_be_in_response_if_no_player_involved(self):
        data = {'from_company': self.company.pk, 'amount': 8}
        response = self.client.post(self.url, data, format='json')
        self.assertNotIn('players', response.data)

    def test_companies_should_not_be_in_response_if_no_company_involved(self):
        data = {'from_player': self.player.pk, 'amount': 9}
        response = self.client.post(self.url, data, format='json')
        self.assertNotIn('companies', response.data)


@mock.patch.object(utils, 'transfer_money')
class TransferMoneyWithTransferMockTests(APITestCase):
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


class ShareTransactionTests(APITestCase):
    def setUp(self):
        self.url = reverse('transfer_share')
        self.player = factories.PlayerFactory(game=game, cash=100)
        # Company to buy shares from
        self.source_company = factories.CompanyFactory(game=game, cash=100)
        # Company to buy shares with
        self.buy_company = factories.CompanyFactory(game=game, cash=100)
        # Company to buy shares in
        self.share_company = factories.CompanyFactory(game=game, cash=0,
            ipo_shares=5, bank_shares=5)
        self.data = {'share': self.share_company.pk, 'amount': 1}

    def test_buying_from_ipo_includes_game_instance_in_response(self):
        self.data.update({'source_type': 'ipo', 'price': 10,
            'buyer_type': 'player', 'player_buyer': self.player.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.data['game']['uuid'], str(game.pk))
        self.assertEqual(response.data['game']['cash'], 12010)

    def test_buying_from_bank_includes_game_instance_in_response(self):
        self.data.update({'source_type': 'bank', 'price': 20,
            'buyer_type': 'player', 'player_buyer': self.player.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.data['game']['uuid'], str(game.pk))
        self.assertEqual(response.data['game']['cash'], 12020)

    def test_ipo_buying_share_includes_game_instance_in_response(self):
        self.data.update({'buyer_type': 'ipo', 'price': 30,
            'source_type': 'player', 'player_source': self.player.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.data['game']['uuid'], str(game.pk))
        self.assertEqual(response.data['game']['cash'], 11970)

    def test_bank_buying_share_includes_game_instance_in_response(self):
        self.data.update({'buyer_type': 'bank', 'price': 40,
            'source_type': 'player', 'player_source': self.player.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.data['game']['uuid'], str(game.pk))
        self.assertEqual(response.data['game']['cash'], 11960)

    def test_company_whos_share_is_being_bought_is_always_in_response(self):
        self.data.update({'source_type': 'ipo', 'price': 50,
            'buyer_type': 'player', 'player_buyer': self.player.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(len(response.data['companies']), 1)
        self.assertEqual(str(self.share_company.pk),
            response.data['companies'][0]['uuid'])

    def test_company_buying_share_is_in_response(self):
        self.data.update({'source_type': 'ipo', 'price': 60,
            'buyer_type': 'company', 'company_buyer': self.buy_company.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.buy_company.refresh_from_db()
        self.assertIn(str(self.buy_company.pk),
            [c['uuid'] for c in response.data['companies']])
        self.assertEqual(self.buy_company.cash, 40)
        self.assertIn(40, [c['cash'] for c in response.data['companies']])

    def test_player_buying_share_is_in_response(self):
        self.data.update({'source_type': 'ipo', 'price': 70,
            'buyer_type': 'player', 'player_buyer': self.player.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.player.refresh_from_db()
        self.assertEqual(str(self.player.pk),
            response.data['players'][0]['uuid'])
        self.assertEqual(response.data['players'][0]['cash'], 30)
        self.assertEqual(self.player.cash, 30)

    def test_company_selling_share_is_in_response(self):
        factories.CompanyShareFactory(owner=self.source_company,
            company=self.share_company)
        self.data.update({'buyer_type': 'bank', 'price': 80,
            'source_type': 'company',
            'company_source': self.source_company.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.source_company.refresh_from_db()
        self.assertIn(str(self.source_company.pk),
            [c['uuid'] for c in response.data['companies']])
        self.assertEqual(self.source_company.cash, 180)
        self.assertIn(180, [c['cash'] for c in response.data['companies']])

    def test_player_selling_share_is_in_response(self):
        self.data.update({'buyer_type': 'bank', 'price': 90,
            'source_type': 'player', 'player_source': self.player.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.player.refresh_from_db()
        self.assertEqual(str(self.player.pk),
            response.data['players'][0]['uuid'])
        self.assertEqual(response.data['players'][0]['cash'], 190)
        self.assertEqual(self.player.cash, 190)

    def test_when_player_buys_share_the_share_instance_is_in_response(self):
        self.data.update({'price': 100, 'buyer_type': 'player',
            'player_buyer': self.player.pk, 'source_type': 'ipo'})
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(len(response.data['shares']), 1)
        self.assertEqual(str(self.player.share_set.first().pk),
            response.data['shares'][0]['uuid'])

    def test_game_not_in_response_when_bank_or_ipo_not_involved(self):
        factories.CompanyShareFactory(owner=self.share_company,
            company=self.share_company)
        self.data.update({'price': 105, 'buyer_type': 'company',
            'company_buyer': self.buy_company.pk, 'source_type': 'company',
            'company_source': self.share_company.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.assertNotIn('game', response.data)

    def test_players_key_not_in_response_when_no_player_involved(self):
        factories.CompanyShareFactory(owner=self.share_company,
            company=self.share_company)
        self.data.update({'price': 105, 'buyer_type': 'company',
            'company_buyer': self.buy_company.pk, 'source_type': 'company',
            'company_source': self.share_company.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.assertNotIn('players', response.data)

    def test_when_company_buys_share_the_share_instance_is_in_response(self):
        self.data.update({'price': 110, 'buyer_type': 'company',
            'company_buyer': self.buy_company.pk, 'source_type': 'ipo'})
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(len(response.data['shares']), 1)
        self.assertEqual(str(self.buy_company.share_set.first().pk),
            response.data['shares'][0]['uuid'])

    def test_when_player_sells_share_the_share_instance_is_in_response(self):
        factories.PlayerShareFactory(owner=self.player,
            company=self.share_company, shares=3)
        self.data.update({'price': 120, 'buyer_type': 'bank',
            'source_type': 'player', 'player_source': self.player.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(len(response.data['shares']), 1)
        self.assertEqual(str(self.player.share_set.first().pk),
            response.data['shares'][0]['uuid'])
        self.assertEqual(response.data['shares'][0]['shares'], 2)

    def test_when_companY_sells_share_the_share_instance_is_in_response(self):
        factories.CompanyShareFactory(owner=self.buy_company,
            company=self.share_company, shares=4)
        self.data.update({'price': 130, 'buyer_type': 'bank',
            'source_type': 'company', 'company_source': self.buy_company.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(len(response.data['shares']), 1)
        self.assertEqual(str(self.buy_company.share_set.first().pk),
            response.data['shares'][0]['uuid'])
        self.assertEqual(response.data['shares'][0]['shares'], 3)


@mock.patch.object(utils, 'buy_share')
class ShareTransactionWithMockTests(APITestCase):
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

    def test_handles_invalid_transaction(self, mock_buy_share):
        mock_buy_share.side_effect = utils.InvalidShareTransaction
        data = {'buyer_type': 'company', 'company_buyer': self.buy_company.pk,
            'source_type': 'ipo', 'share': self.source_company.pk,
            'price': 29, 'amount': 1}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.data['non_field_errors'],
            [views.NO_AVAILABLE_SHARES_ERROR])

    def test_handles_different_game_exception(self, mock_buy_share):
        company = factories.CompanyFactory()
        player = factories.PlayerFactory()
        mock_buy_share.side_effect = utils.DifferentGameException
        data = {'buyer_type': 'player', 'player_buyer': player.pk,
            'source_type': 'ipo', 'amount': 1,
            'price': 30, 'share': self.source_company.pk}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.data['non_field_errors'],
            [views.DIFFERENT_GAME_ERROR])

    def test_does_not_handle_other_exceptions(self, mock_buy_share):
        mock_buy_share.side_effect = Exception
        data = {'buyer_type': 'company', 'company_buyer': self.buy_company.pk,
            'source_type': 'ipo', 'share': self.source_company.pk,
            'price': 31, 'amount': 1}
        with self.assertRaises(Exception):
            response = self.client.post(self.url, data, format='json')


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
