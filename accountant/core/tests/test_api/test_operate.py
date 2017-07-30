# -*- coding: utf-8 -*-
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest import mock

from ... import factories
from ... import models
from ... import utils

@mock.patch.object(utils, 'operate')
class OperateTests(APITestCase):
    def setUp(self):
        self.url = reverse('operate')
        self.game = factories.GameFactory()
        self.alice, self.bob = factories.PlayerFactory.create_batch(size=2,
            game=self.game)
        self.company, self.company2 = factories.CompanyFactory.create_batch(
            size=2, game=self.game)

    def test_GET_request_is_empty(self, mock):
        """GET is for debug (and doc) purposes only"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data)

    def test_company_can_pay_full_dividends(self, mock_operate):
        data = {'company': self.company.pk, 'amount': 10, 'method': 'full'}
        mock_operate.return_value = {}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_operate.assert_called_once_with(self.company, 10,
            utils.OperateMethod.FULL)

    def test_company_can_pay_half_dividends(self, mock_operate):
        data = {'company': self.company.pk, 'amount': 20, 'method': 'half'}
        mock_operate.return_value = {}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_operate.assert_called_once_with(self.company, 20,
            utils.OperateMethod.HALF)

    def test_company_can_withhold_revenue(self, mock_operate):
        data = {'company': self.company.pk, 'amount': 30, 'method': 'withhold'}
        mock_operate.return_value = {}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_operate.assert_called_once_with(self.company, 30,
            utils.OperateMethod.WITHHOLD)

    def test_gives_error_if_request_is_invalid(self, mock_operate):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_gives_list_of_affected_players_on_full_dividends(self,
            mock_operate):
        data = {'company': self.company.pk, 'amount': 40, 'method': 'full'}
        mock_operate.return_value = {self.alice: 1, self.bob: 2,
            self.company: 3}
        response = self.client.post(self.url, data)
        self.assertCountEqual([str(self.alice.pk), str(self.bob.pk)],
            [p['uuid'] for p in response.data['players']])

    def test_gives_list_of_affected_players_on_half_dividends(self,
            mock_operate):
        data = {'company': self.company.pk, 'amount': 50, 'method': 'half'}
        mock_operate.return_value = {self.alice: 1, self.bob: 2,
            self.company: 3}
        response = self.client.post(self.url, data)
        self.assertCountEqual([str(self.alice.pk), str(self.bob.pk)],
            [p['uuid'] for p in response.data['players']])

    def test_does_not_give_list_of_players_when_withholding(self,
            mock_operate):
        data = {'company': self.company.pk, 'amount': 60, 'method': 'withhold'}
        mock_operate.return_value = {self.company: 60}
        response = self.client.post(self.url, data)
        self.assertNotIn('players', response.data)

    def test_gives_list_of_affected_companies_on_full_dividends(self,
            mock_operate):
        data = {'company': self.company.pk, 'amount': 70, 'method': 'full'}
        mock_operate.return_value = {self.company: 35, self.company2: 35}
        response = self.client.post(self.url, data)
        self.assertCountEqual([str(self.company.pk), str(self.company2.pk)],
            [c['uuid'] for c in response.data['companies']])

    def test_gives_list_of_affected_companies_on_half_dividends(self,
            mock_operate):
        data = {'company': self.company.pk, 'amount': 80, 'method': 'half'}
        mock_operate.return_value = {self.company: 60, self.company2: 20}
        response = self.client.post(self.url, data)
        self.assertCountEqual([str(self.company.pk), str(self.company2.pk)],
            [c['uuid'] for c in response.data['companies']])

    def test_gives_list_of_affected_companies_when_withholding(self,
            mock_operate):
        data = {'company': self.company.pk, 'amount': 90, 'method': 'withhold'}
        mock_operate.return_value = {self.company: 90}
        response = self.client.post(self.url, data)
        self.assertCountEqual([str(self.company.pk)],
            [c['uuid'] for c in response.data['companies']])

    def test_always_returns_list_of_affected_game(self,
            mock_operate):
        data = {'company': self.company.pk, 'amount': 100, 'method': 'full'}
        mock_operate.return_value = {self.company: 100}
        response = self.client.post(self.url, data)
        self.assertEqual(str(self.game.pk), response.data['game']['uuid'])

    def test_operating_includes_log_entry_in_response(self, mock):
        data = {'company': self.company.pk, 'amount': 110, 'method': 'full'}
        response = self.client.post(self.url, data)
        self.game.refresh_from_db()
        self.assertEqual(response.data['log']['uuid'],
            str(self.game.log.last().pk))

    def test_paying_full_dividends_creates_log_entry(self, mock):
        data = {'company': self.company.pk, 'amount': 120, 'method': 'full'}
        response = self.client.post(self.url, data)
        self.game.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1,
            models.LogEntry.objects.filter(game=self.game).count())
        self.assertEqual(self.game.log.last(), self.game.log_cursor)
        self.assertEqual(self.game.log.last().text,
            '{} operates for 120 which is paid as dividends'.format(
                self.company.name))
        self.assertEqual(self.game.log.last().acting_company, self.company)

    def test_paying_half_dividends_creates_log_entry(self, mock):
        data = {'company': self.company.pk, 'amount': 130, 'method': 'half'}
        response = self.client.post(self.url, data)
        self.game.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1,
            models.LogEntry.objects.filter(game=self.game).count())
        self.assertEqual(self.game.log.last(), self.game.log_cursor)
        self.assertEqual(self.game.log.last().text,
            '{} operates for 130 of which it retains half'.format(
                self.company.name))
        self.assertEqual(self.game.log.last().acting_company, self.company)

    def test_withholding_creates_log_entry(self, mock):
        data = {'company': self.company.pk, 'amount': 140,
            'method': 'withhold'}
        response = self.client.post(self.url, data)
        self.game.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1,
            models.LogEntry.objects.filter(game=self.game).count())
        self.assertEqual(self.game.log.last(), self.game.log_cursor)
        self.assertEqual(self.game.log.last().text,
            '{} withholds 140'.format(
                self.company.name))
        self.assertEqual(self.game.log.last().acting_company, self.company)
