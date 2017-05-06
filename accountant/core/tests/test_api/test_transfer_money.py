# -*- coding: utf-8 -*-
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import unittest
from unittest import mock

from ... import models
from ... import factories
from ... import serializers
from ... import utils

class TransferMoneyTests(APITestCase):
    def setUp(self):
        self.game = factories.GameFactory.create()
        self.url = reverse('transfer_money')
        self.player = factories.PlayerFactory(game=self.game, cash=100)
        self.company = factories.CompanyFactory(game=self.game, cash=100)

    def test_transfering_from_bank_includes_game_instance_in_response(self):
        data = {'to_player': self.player.pk, 'amount': 1}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertEqual(response.data['game']['cash'], 11999)

    def test_transfering_to_bank_includes_game_instance_in_response(self):
        data = {'from_player': self.player.pk, 'amount': 2}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
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
        self.game = factories.GameFactory.create(cash=1000)
        self.url = reverse('transfer_money')
        self.player = factories.PlayerFactory(game=self.game, cash=100)
        self.company = factories.CompanyFactory(game=self.game, cash=100)

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
