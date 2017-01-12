# -*- coding: utf-8 -*-
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .. import models
from .. import factories

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
