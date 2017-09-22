# -*- coding: utf-8 -*-
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest import mock

from ... import factories
from ... import models
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
        response = self.client.post(self.url, data)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertEqual(response.data['game']['cash'], 11999)

    def test_transfering_to_bank_includes_game_instance_in_response(self):
        data = {'from_player': self.player.pk, 'amount': 2}
        response = self.client.post(self.url, data)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertEqual(response.data['game']['cash'], 12002)

    def test_transfering_from_player_includes_instance_in_response(self):
        data = {'from_player': self.player.pk, 'amount': 3}
        response = self.client.post(self.url, data)
        self.assertEqual(response.data['players'][0]['uuid'],
            str(self.player.pk))
        self.assertEqual(response.data['players'][0]['cash'], 97)

    def test_transfering_to_player_includes_instance_in_response(self):
        data = {'to_player': self.player.pk, 'amount': 4}
        response = self.client.post(self.url, data)
        self.assertEqual(response.data['players'][0]['uuid'],
            str(self.player.pk))
        self.assertEqual(response.data['players'][0]['cash'], 104)

    def test_transfering_from_company_includes_instance_in_response(self):
        data = {'from_company': self.company.pk, 'amount': 5}
        response = self.client.post(self.url, data)
        self.assertEqual(response.data['companies'][0]['uuid'],
            str(self.company.pk))
        self.assertEqual(response.data['companies'][0]['cash'], 95)

    def test_transfering_to_company_includes_instance_in_response(self):
        data = {'to_company': self.company.pk, 'amount': 6}
        response = self.client.post(self.url, data)
        self.assertEqual(response.data['companies'][0]['uuid'],
            str(self.company.pk))
        self.assertEqual(response.data['companies'][0]['cash'], 106)

    def test_game_should_not_be_in_response_if_no_transfer_with_bank(self):
        data = {'from_player': self.player.pk, 'to_company': self.company.pk,
            'amount': 7}
        response = self.client.post(self.url, data)
        self.assertNotIn('game', response.data)

    def test_players_should_not_be_in_response_if_no_player_involved(self):
        data = {'from_company': self.company.pk, 'amount': 8}
        response = self.client.post(self.url, data)
        self.assertNotIn('players', response.data)

    def test_companies_should_not_be_in_response_if_no_company_involved(self):
        data = {'from_player': self.player.pk, 'amount': 9}
        response = self.client.post(self.url, data)
        self.assertNotIn('companies', response.data)

    def test_transfering_includes_log_entry_in_response(self):
        data = {'from_player': self.player.pk, 'amount': 1}
        response = self.client.post(self.url, data)
        self.game.refresh_from_db()
        self.assertEqual(response.data['log']['uuid'],
            str(self.game.log.last().pk))

    def test_transfering_from_player_to_bank_creates_log_entry(self):
        self.assertEqual(0,
            models.LogEntry.objects.filter(game=self.game).count())
        data = {'from_player': self.player.pk, 'amount': 10}
        self.client.post(self.url, data)
        self.game.refresh_from_db()
        self.assertEqual(1,
            models.LogEntry.objects.filter(game=self.game).count())
        self.assertEqual(self.game.log.last().text,
            '{} transfered 10 to the bank'.format(self.player.name))
        self.assertEqual(self.game.log.last(), self.game.log_cursor)

    def test_transfering_from_player_to_player_creates_log_entry(self):
        other_player = factories.PlayerFactory(game=self.game)
        self.assertEqual(0,
            models.LogEntry.objects.filter(game=self.game).count())
        data = {'from_player': self.player.pk, 'amount': 11,
                'to_player': other_player.pk}
        self.client.post(self.url, data)
        self.game.refresh_from_db()
        self.assertEqual(1,
            models.LogEntry.objects.filter(game=self.game).count())
        self.assertEqual(self.game.log.last().text,
            '{} transfered 11 to {}'.format(self.player.name,
                other_player.name))
        self.assertEqual(self.game.log.last(), self.game.log_cursor)

    def test_transfering_from_player_to_company_creates_log_entry(self):
        self.assertEqual(0,
            models.LogEntry.objects.filter(game=self.game).count())
        data = {'from_player': self.player.pk, 'amount': 12,
                'to_company': self.company.pk}
        self.client.post(self.url, data)
        self.game.refresh_from_db()
        self.assertEqual(1,
            models.LogEntry.objects.filter(game=self.game).count())
        self.assertEqual(self.game.log.last().text,
            '{} transfered 12 to {}'.format(self.player.name,
                self.company.name))
        self.assertEqual(self.game.log.last(), self.game.log_cursor)

    def test_transfering_from_company_to_bank_creates_log_entry(self):
        self.assertEqual(0,
            models.LogEntry.objects.filter(game=self.game).count())
        data = {'from_company': self.company.pk, 'amount': 13}
        self.client.post(self.url, data)
        self.game.refresh_from_db()
        self.assertEqual(1,
            models.LogEntry.objects.filter(game=self.game).count())
        self.assertEqual(self.game.log.last().text,
            '{} transfered 13 to the bank'.format(self.company.name))
        self.assertEqual(self.game.log.last(), self.game.log_cursor)
        self.assertEqual(self.game.log.last().acting_company, self.company)

    def test_transfering_from_company_to_player_creates_log_entry(self):
        self.assertEqual(0,
            models.LogEntry.objects.filter(game=self.game).count())
        data = {'from_company': self.company.pk, 'amount': 14,
                'to_player': self.player.pk}
        self.client.post(self.url, data)
        self.game.refresh_from_db()
        self.assertEqual(1,
            models.LogEntry.objects.filter(game=self.game).count())
        self.assertEqual(self.game.log.last().text,
            '{} transfered 14 to {}'.format(self.company.name,
                self.player.name))
        self.assertEqual(self.game.log.last(), self.game.log_cursor)
        self.assertEqual(self.game.log.last().acting_company, self.company)

    def test_transfering_from_company_to_company_creates_log_entry(self):
        other_company = factories.CompanyFactory(game=self.game)
        self.assertEqual(0,
            models.LogEntry.objects.filter(game=self.game).count())
        data = {'from_company': self.company.pk, 'amount': 15,
                'to_company': other_company.pk}
        self.client.post(self.url, data)
        self.game.refresh_from_db()
        self.assertEqual(1,
            models.LogEntry.objects.filter(game=self.game).count())
        self.assertEqual(self.game.log.last().text,
            '{} transfered 15 to {}'.format(self.company.name,
                other_company.name))
        self.assertEqual(self.game.log.last(), self.game.log_cursor)
        self.assertEqual(self.game.log.last().acting_company, self.company)

    def test_transfering_from_bank_to_player_creates_log_entry(self):
        self.assertEqual(0,
            models.LogEntry.objects.filter(game=self.game).count())
        data = {'to_player': self.player.pk, 'amount': 16}
        self.client.post(self.url, data)
        self.game.refresh_from_db()
        self.assertEqual(1,
            models.LogEntry.objects.filter(game=self.game).count())
        self.assertEqual(self.game.log.last().text,
            'The bank transfered 16 to {}'.format(self.player.name))
        self.assertEqual(self.game.log.last(), self.game.log_cursor)

    def test_transfering_from_bank_to_company_creates_log_entry(self):
        self.assertEqual(0,
            models.LogEntry.objects.filter(game=self.game).count())
        data = {'to_company': self.company.pk, 'amount': 17}
        self.client.post(self.url, data)
        self.game.refresh_from_db()
        self.assertEqual(1,
            models.LogEntry.objects.filter(game=self.game).count())
        self.assertEqual(self.game.log.last().text,
            'The bank transfered 17 to {}'.format(self.company.name))
        self.assertEqual(self.game.log.last(), self.game.log_cursor)

    def test_transfering_from_bank_to_player_creates_log_with_undo_data(self):
        self.client.post(self.url, {'to_player': self.player.pk, 'amount': 24})
        self.game.refresh_from_db()
        entry = self.game.log.last()
        self.assertEqual(entry.action, models.LogEntry.TRANSFER_MONEY)
        self.assertEqual(entry.receiving_player, self.player)
        self.assertEqual(entry.amount, 24)

    def test_transfering_from_bank_to_company_creates_log_with_undo_data(self):
        self.client.post(self.url,
            {'to_company': self.company.pk, 'amount': 25})
        self.game.refresh_from_db()
        entry = self.game.log.last()
        self.assertEqual(entry.action, models.LogEntry.TRANSFER_MONEY)
        self.assertEqual(entry.receiving_company, self.company)
        self.assertEqual(entry.amount, 25)

    def test_transfering_from_player_to_bank_creates_log_with_undo_data(self):
        self.client.post(self.url,
            {'from_player': self.player.pk, 'amount': 18})
        self.game.refresh_from_db()
        entry = self.game.log.last()
        self.assertEqual(entry.action, models.LogEntry.TRANSFER_MONEY)
        self.assertEqual(entry.acting_player, self.player)
        self.assertEqual(entry.amount, 18)

    def test_transfering_from_company_to_bank_creates_log_with_undo_data(self):
        self.client.post(self.url, {'from_company': self.company.pk,
            'amount': 19})
        self.game.refresh_from_db()
        entry = self.game.log.last()
        self.assertEqual(entry.action, models.LogEntry.TRANSFER_MONEY)
        self.assertEqual(entry.acting_company, self.company)
        self.assertEqual(entry.amount, 19)

    def test_transfer_from_player_to_player_creates_log_with_undo_data(self):
        other_player = factories.PlayerFactory(game=self.game)
        self.client.post(self.url, {'from_player': self.player.pk,
            'to_player': other_player.pk, 'amount': 20})
        self.game.refresh_from_db()
        entry = self.game.log.last()
        self.assertEqual(entry.action, models.LogEntry.TRANSFER_MONEY)
        self.assertEqual(entry.acting_player, self.player)
        self.assertEqual(entry.receiving_player, other_player)
        self.assertEqual(entry.amount, 20)

    def test_transfer_from_player_to_company_creates_log_with_undo_data(self):
        self.client.post(self.url, {'from_player': self.player.pk,
            'to_company': self.company.pk, 'amount': 21})
        self.game.refresh_from_db()
        entry = self.game.log.last()
        self.assertEqual(entry.action, models.LogEntry.TRANSFER_MONEY)
        self.assertEqual(entry.acting_player, self.player)
        self.assertEqual(entry.receiving_company, self.company)
        self.assertEqual(entry.amount, 21)

    def test_transfer_from_company_to_player_creates_log_with_undo_data(self):
        self.client.post(self.url, {'from_company': self.company.pk,
            'to_player': self.player.pk, 'amount': 22})
        self.game.refresh_from_db()
        entry = self.game.log.last()
        self.assertEqual(entry.action, models.LogEntry.TRANSFER_MONEY)
        self.assertEqual(entry.acting_company, self.company)
        self.assertEqual(entry.receiving_player, self.player)
        self.assertEqual(entry.amount, 22)

    def test_transfer_from_company_to_company_creates_log_with_undo_data(self):
        other_company = factories.CompanyFactory(game=self.game)
        self.client.post(self.url, {'from_company': self.company.pk,
            'to_company': other_company.pk, 'amount': 23})
        self.game.refresh_from_db()
        entry = self.game.log.last()
        self.assertEqual(entry.action, models.LogEntry.TRANSFER_MONEY)
        self.assertEqual(entry.acting_company, self.company)
        self.assertEqual(entry.receiving_company, other_company)
        self.assertEqual(entry.amount, 23)


@mock.patch.object(utils, 'transfer_money')
class TransferMoneyWithTransferMockTests(APITestCase):
    def setUp(self):
        self.game = factories.GameFactory.create(cash=1000)
        self.url = reverse('transfer_money')
        self.player = factories.PlayerFactory(game=self.game, cash=100)
        self.company = factories.CompanyFactory(game=self.game, cash=100)

    def test_GET_request_is_empty(self, mock):
        """GET is for debug (and doc) purposes only"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data)

    def test_can_transfer_money_from_player_to_bank(self, mock_transfer_money):
        data = {'from_player': self.player.pk, 'amount': 99}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_transfer_money.assert_called_once_with(self.player, None, 99)

    def test_can_transfer_money_from_bank_to_player(self, mock_transfer_money):
        data = {'to_player': self.player.pk, 'amount': 98}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_transfer_money.assert_called_once_with(None, self.player, 98)

    def test_can_transfer_money_from_company_to_bank(self,
            mock_transfer_money):
        data = {'from_company': self.company.pk, 'amount': 97}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_transfer_money.assert_called_once_with(self.company, None, 97)

    def test_can_transfer_money_from_bank_to_company(self,
            mock_transfer_money):
        data = {'to_company': self.company.pk, 'amount': 96}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_transfer_money.assert_called_once_with(None, self.company, 96)

    def test_can_transfer_money_from_player_to_company(self,
            mock_transfer_money):
        data = {'from_player': self.player.pk, 'to_company': self.company.pk,
            'amount': 95}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_transfer_money.assert_called_once_with(self.player, self.company,
            95)

    def test_can_transfer_money_from_company_to_player(self,
            mock_transfer_money):
        data = {'to_player': self.player.pk, 'from_company': self.company.pk,
            'amount': 94}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_transfer_money.assert_called_once_with(self.company, self.player,
            94)

    def test_transfering_from_bank_to_bank_raises_error(self, mock):
        data = {'amount': 93}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(serializers.SOURCE_OR_DEST_REQUIRED_ERROR,
            response.data['non_field_errors'])

    def test_transfer_from_player_to_company_in_other_game_raises_error(self,
            mock):
        company = factories.CompanyFactory(cash=100)
        data = {'from_player': self.player.pk, 'to_company': company.pk,
            'amount': 92}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(serializers.DIFFERENT_GAME_ERROR,
            response.data['non_field_errors'])

    def test_transfer_from_company_to_player_in_other_game_raises_error(self,
            mock):
        company = factories.CompanyFactory(cash=100)
        data = {'to_player': self.player.pk, 'from_company': company.pk,
            'amount': 91}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(serializers.DIFFERENT_GAME_ERROR,
            response.data['non_field_errors'])

    def test_transfer_between_players_in_different_games_raises_error(self,
            mock):
        player2 = factories.PlayerFactory(cash=100)
        data = {'from_player': self.player.pk, 'to_player': player2.pk,
            'amount': 90}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(serializers.DIFFERENT_GAME_ERROR,
            response.data['non_field_errors'])

    def test_transfer_between_companies_in_different_games_raises_error(self,
            mock):
        company2 = factories.CompanyFactory(cash=100)
        data = {'from_company': self.company.pk, 'to_company': company2.pk,
            'amount': 89}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(serializers.DIFFERENT_GAME_ERROR,
            response.data['non_field_errors'])
