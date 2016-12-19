# -*- coding: utf-8 -*-
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .. import models

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
        game = models.Game()
        game.save()
        url = reverse('player-list')
        data = {'name': 'Alice', 'game': game.pk}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            "Could not create a player: " + str(response.data))
        self.assertEqual(models.Player.objects.count(), 1)


class CompanyTests(APITestCase):
    def test_create_company(self):
        """Ensure that we can create companies."""
        game = models.Game()
        game.save()
        url = reverse('company-list')
        data = {'name': 'B&O', 'game': game.pk}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            "Could not create a company: " + str(response.data))
        self.assertEqual(models.Company.objects.count(), 1)
