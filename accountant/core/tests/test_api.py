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

game = None

def setUpModule():
    global game
    game = factories.GameFactory.create()

def tearDownModule():
    game.delete()

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

    def test_GET_request_is_empty(self, mock):
        """GET is for debug (and doc) purposes only"""
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data)

    def test_can_transfer_money_from_player_to_bank(self, mock_transfer_money):
        player = factories.PlayerFactory(game=game, cash=100)
        data = {'from_player': player.pk, 'amount': 99}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_transfer_money.assert_called_once_with(player, None, 99)

    def test_can_transfer_money_from_bank_to_player(self, mock_transfer_money):
        player = factories.PlayerFactory(game=game)
        data = {'to_player': player.pk, 'amount': 98}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_transfer_money.assert_called_once_with(None, player, 98)

    def test_can_transfer_money_from_company_to_bank(self,
            mock_transfer_money):
        company = factories.CompanyFactory(game=game, cash=100)
        data = {'from_company': company.pk, 'amount': 97}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_transfer_money.assert_called_once_with(company, None, 97)

    def test_can_transfer_money_from_bank_to_company(self,
            mock_transfer_money):
        company = factories.CompanyFactory(game=game, cash=100)
        data = {'to_company': company.pk, 'amount': 96}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_transfer_money.assert_called_once_with(None, company, 96)

    def test_can_transfer_money_from_player_to_company(self,
            mock_transfer_money):
        player = factories.PlayerFactory(game=game, cash=100)
        company = factories.CompanyFactory(game=game, cash=100)
        data = {'from_player': player.pk, 'to_company': company.pk,
            'amount': 95}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_transfer_money.assert_called_once_with(player, company, 95)

    def test_can_transfer_money_from_company_to_player(self,
            mock_transfer_money):
        player = factories.PlayerFactory(game=game, cash=100)
        company = factories.CompanyFactory(game=game, cash=100)
        data = {'to_player': player.pk, 'from_company': company.pk,
            'amount': 94}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_transfer_money.assert_called_once_with(company, player, 94)

    def test_transfering_from_bank_to_bank_raises_error(self, mock):
        data = {'amount': 93}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(serializers.SOURCE_OR_DEST_REQUIRED_ERROR,
            response.data['non_field_errors'])

    def test_transfer_from_player_to_company_in_other_game_raises_error(self,
            mock):
        game2 = factories.GameFactory()
        player = factories.PlayerFactory(game=game, cash=100)
        company = factories.CompanyFactory(game=game2, cash=100)
        data = {'from_player': player.pk, 'to_company': company.pk,
            'amount': 92}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(serializers.DIFFERENT_GAME_ERROR,
            response.data['non_field_errors'])

    def test_transfer_from_company_to_player_in_other_game_raises_error(self,
            mock):
        game2 = factories.GameFactory()
        player = factories.PlayerFactory(game=game, cash=100)
        company = factories.CompanyFactory(game=game2, cash=100)
        data = {'to_player': player.pk, 'from_company': company.pk,
            'amount': 91}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(serializers.DIFFERENT_GAME_ERROR,
            response.data['non_field_errors'])

    def test_transfer_between_players_in_different_games_raises_error(self,
            mock):
        game2 = factories.GameFactory()
        player1 = factories.PlayerFactory(game=game, cash=100)
        player2 = factories.PlayerFactory(game=game2, cash=100)
        data = {'from_player': player1.pk, 'to_player': player2.pk,
            'amount': 90}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(serializers.DIFFERENT_GAME_ERROR,
            response.data['non_field_errors'])

    def test_transfer_between_companies_in_different_games_raises_error(self,
            mock):
        game2 = factories.GameFactory()
        company1 = factories.CompanyFactory(game=game, cash=100)
        company2 = factories.CompanyFactory(game=game2, cash=100)
        data = {'from_company': company1.pk, 'to_company': company2.pk,
            'amount': 89}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(serializers.DIFFERENT_GAME_ERROR,
            response.data['non_field_errors'])
