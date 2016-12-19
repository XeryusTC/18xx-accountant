# -*- coding: utf-8 -*-
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .. import models
from .. import factories

class GameTests(APITestCase):
    def test_create_game(self):
        """Ensure that we can create a game."""
        url = reverse('game-list')
        data = {'players': [], 'companies': []}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            "Could not create game: " + str(response.data))
        self.assertEqual(models.Game.objects.count(), 1)


class PlayerTests(APITestCase):
    def test_create_player(self):
        """Ensure that we can create players."""
        game = factories.GameFactory.create()
        url = reverse('player-list')
        data = {'name': 'Alice', 'game': game.pk}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            "Could not create a player: " + str(response.data))
        self.assertEqual(models.Player.objects.count(), 1)

    def test_cannot_create_duplicate_player_for_single_game(self):
        """Disallow creating two players with the same name in a game."""
        game = factories.GameFactory.create()
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
        game = factories.GameFactory.create()
        url = reverse('company-list')
        data = {'name': 'B&O', 'game': game.pk}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            "Could not create a company: " + str(response.data))
        self.assertEqual(models.Company.objects.count(), 1)

    def test_cannot_create_duplicate_company_for_single_game(self):
        """Disallow creating two companies with the same name in a game."""
        game = factories.GameFactory.create()
        company = factories.CompanyFactory.create(game=game, name='B&O')
        url = reverse('company-list')
        data = {'name': 'B&O', 'game': game.pk}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            "Created duplicate company: " + str(response.data))
        self.assertEqual(models.Company.objects.count(), 1)


class ShareTests(APITestCase):
    def test_create_share(self):
        """Ensure that we can create shares."""
        game = factories.GameFactory.create()
        player = factories.PlayerFactory.create(game=game)
        company = factories.CompanyFactory.create(game=game)
        url = reverse('share-list')
        data = {'game': game.pk, 'player': player.pk, 'company': company.pk}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            "Could not create a share: " + str(response.data))
        self.assertEqual(models.Share.objects.count(), 1)

    def test_cannot_create_duplicate_share_holdings(self):
        """
        Ensure that a player doesn't have two share holding records for
        a single company
        """
        game = factories.GameFactory.create()
        player = factories.PlayerFactory.create(game=game)
        company = factories.CompanyFactory.create(game=game)
        share = factories.ShareFactory.create(player=player, company=company)
        url = reverse('share-list')
        data = {'player': player.pk, 'company': company.pk}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            "Created duplicate share holdings: " + str(response.data))
        self.assertEqual(models.Share.objects.count(), 1)
