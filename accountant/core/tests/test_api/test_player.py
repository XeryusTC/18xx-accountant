# -*- coding: utf-8 -*-
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ... import models
from ... import factories

class PlayerTests(APITestCase):
    def setUp(self):
        self.game = factories.GameFactory.create()

    def test_create_player(self):
        """Ensure that we can create players."""
        url = reverse('player-list')
        data = {'name': 'Alice', 'game': self.game.pk}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            "Could not create a player: " + str(response.data))
        self.assertEqual(models.Player.objects.count(), 1)

    def test_cannot_create_duplicate_player_for_single_game(self):
        """Disallow creating two players with the same name in a game."""
        factories.PlayerFactory.create(game=self.game, name='Alice')
        url = reverse('player-list')
        data = {'name': 'Alice', 'game': self.game.pk}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            "Created duplicate player: " + str(response.data))
        self.assertEqual(models.Player.objects.count(), 1)

    def test_creating_player_decreases_cash_in_bank(self):
        self.game.cash = 12000
        self.game.save()
        url = reverse('player-list')
        data = {'name': 'Alice', 'game': self.game.pk, 'cash': 500}

        response = self.client.post(url, data, format='json')

        self.game.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Player.objects.first().cash, 500)
        self.assertEqual(self.game.cash, 11500)

    def test_retrieve_players_within_a_single_game(self):
        """Filter the players based on the game in the query url"""
        players = factories.PlayerFactory.create_batch(game=self.game, size=3)
        factories.PlayerFactory.create_batch(size=2)
        url = reverse('player-list') + '?game=' + str(self.game.pk)

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


class PlayerShareTests(APITestCase):
    def setUp(self):
        self.game = factories.GameFactory.create()

    def test_create_share(self):
        """Ensure that we can create shares."""
        player = factories.PlayerFactory.create(game=self.game)
        company = factories.CompanyFactory.create(game=self.game)
        url = reverse('playershare-list')
        data = {'game': self.game.pk, 'owner': player.pk,
            'company': company.pk}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            "Could not create a share: " + str(response.data))
        self.assertEqual(models.PlayerShare.objects.count(), 1)

    def test_cannot_create_duplicate_share_holdings(self):
        """
        Ensure that a player doesn't have two share holding records for
        a single company
        """
        player = factories.PlayerFactory.create(game=self.game)
        company = factories.CompanyFactory.create(game=self.game)
        factories.PlayerShareFactory.create(owner=player,
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
        player = factories.PlayerFactory.create(game=self.game)
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
        players = factories.PlayerFactory.create_batch(game=self.game, size=2)
        shares = factories.PlayerShareFactory.create_batch(size=11,
            owner=players[0]) + factories.PlayerShareFactory.create_batch(
                size=13, owner=players[1])
        factories.PlayerShareFactory.create_batch(size=17)
        url = reverse('playershare-list') + '?game=' + str(self.game.pk)

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.maxDiff = None
        self.assertCountEqual([s['uuid'] for s in response.data],
            [str(s.uuid) for s in shares])
