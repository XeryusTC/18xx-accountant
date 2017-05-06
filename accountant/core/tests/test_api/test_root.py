# -*- coding: utf-8 -*-
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ... import models

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
        self.assertEqual(models.Game.objects.count(), 1)


class ColorsTests(APITestCase):
    def setUp(self):
        self.url = reverse('colors')

    def test_returns_list_of_company_colors(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.data, models.Company.COLOR_CODES)
