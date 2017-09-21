# -*- coding: utf-8 -*-
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ... import models
from ... import factories
from ... import utils

class ApiRootTests(APITestCase):
    def setUp(self):
        self.url = reverse('api-root')

    def test_Game_viewset_is_on_api_root(self):
        response = self.client.get(self.url, {})
        self.assertTrue(response.data['game'].endswith(reverse('game-list')))

    def test_Player_viewset_is_on_api_root(self):
        response = self.client.get(self.url, {})
        self.assertTrue(response.data['player'].endswith(
            reverse('player-list')))

    def test_Company_viewset_is_on_api_root(self):
        response = self.client.get(self.url, {})
        self.assertTrue(response.data['company'].endswith(
            reverse('company-list')))

    def test_PlayerShare_viewset_is_on_api_root(self):
        response = self.client.get(self.url, {})
        self.assertTrue(response.data['playershare'].endswith(
            reverse('playershare-list')))

    def test_CompanyShare_viewset_is_on_api_root(self):
        response = self.client.get(self.url, {})
        self.assertTrue(response.data['companyshare'].endswith(
            reverse('companyshare-list')))

    def test_transfer_money_view_is_on_api_root(self):
        response = self.client.get(self.url, {})
        self.assertTrue(response.data['transfer_money'].endswith(
            reverse('transfer_money')))

    def test_transfer_share_view_is_on_api_root(self):
        response = self.client.get(self.url, {})
        self.assertTrue(response.data['transfer_share'].endswith(
            reverse('transfer_share')))

    def test_operate_view_is_on_api_root(self):
        response = self.client.get(self.url, {})
        self.assertTrue(response.data['operate'].endswith(reverse('operate')))

    def test_LogEntry_viewwset_is_on_api_root(self):
        response = self.client.get(self.url, {})
        self.assertTrue(response.data['logentry'].endswith(
            reverse('logentry-list')))


class GameTests(APITestCase):
    def test_create_game(self):
        """Ensure that we can create a game."""
        url = reverse('game-list')
        data = {'players': [], 'companies': []}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            "Could not create game: " + str(response.data))
        # We have 2 games since there is also a global game
        self.assertEqual(models.Game.objects.count(), 1)

    def test_creating_game_adds_new_log_entry(self):
        url = reverse('game-list')
        data = {}
        response = self.client.post(url, data)

        game = models.Game.objects.first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['uuid'], str(game.pk))
        self.assertEqual(models.LogEntry.objects.filter(game=game).count(), 1)
        self.assertEqual(game.log.first().text, 'New game started')


class ColorsTests(APITestCase):
    def setUp(self):
        self.url = reverse('colors')

    def test_returns_list_of_company_colors(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data, models.Company.COLOR_CODES)


class LogEntryAPITests(APITestCase):
    def test_retrieve_log_entries_within_a_single_game(self):
        """Filter the log entries based on the game in the query url"""
        game = factories.GameFactory.create()
        entries = factories.LogEntryFactory.create_batch(game=game, size=4)
        factories.LogEntryFactory.create_batch(size=7)
        game.log_cursor = entries[-1]
        game.save()
        url = reverse('logentry-list') + '?game=' + str(game.pk)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual([str(e.uuid) for e in entries],
            [e['uuid'] for e in response.data])

    def test_retrieve_log_entries_within_a_game_up_to_log_cursor(self):
        game = factories.GameFactory()
        entries = factories.LogEntryFactory.create_batch(game=game, size=5)
        game.log_cursor = entries[2]
        game.save()
        url = reverse('logentry-list') + '?game=' + str(game.pk)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual([str(e.uuid) for e in entries[:3]],
            [e['uuid'] for e in response.data])

    def test_retrieve_all_log_entries_when_no_query_params_set(self):
        factories.LogEntryFactory.create_batch(size=12)
        url = reverse('logentry-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([str(e.uuid) for e in models.LogEntry.objects.all()],
            [e['uuid'] for e in response.data])

    def test_cannot_write_to_view(self):
        url = reverse('logentry-list')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED)


class UndoTests(APITestCase):
    def setUp(self):
        self.game = factories.GameFactory(cash=1000)
        self.start_entry = models.LogEntry.objects.create(game=self.game,
            text='New game started')
        self.game.log_cursor = self.start_entry
        self.game.save()
        self.url = reverse('undo')

    def test_GET_request_is_empty(self):
        """GET is for debug (and doc) purposes only"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data)

    def test_undoing_player_to_bank_money_transfer_includes_instances(self):
        player = factories.PlayerFactory(game=self.game, cash=10)
        entry = models.LogEntry.objects.create(game=self.game,
            acting_player=player, amount=10,
            action=models.LogEntry.TRANSFER_MONEY)
        self.game.log_cursor = entry
        self.game.save()

        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'undo'})

        self.game.refresh_from_db()
        player.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertEqual(response.data['game']['cash'], 990)
        self.assertEqual(len(response.data['players']), 1)
        self.assertEqual(response.data['players'][0]['uuid'], str(player.pk))
        self.assertEqual(response.data['players'][0]['cash'], 20)


class RedoTests(APITestCase):
    def setUp(self):
        self.game = factories.GameFactory(cash=1000)
        self.start_entry = models.LogEntry.objects.create(game=self.game,
            text='New game started')
        self.game.log_cursor = self.start_entry
        self.game.save()
        self.url = reverse('undo')

    def test_GET_request_is_empty(self):
        """GET is for debug (and doc) purposes only"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data)

    def test_redoing_player_to_bank_money_transfer_includes_log(self):
        player = factories.PlayerFactory(game=self.game, cash=100)
        entry = models.LogEntry.objects.create(game=self.game,
            acting_player=player, amount=1,
            action=models.LogEntry.TRANSFER_MONEY)

        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'redo'})

        self.game.refresh_from_db()
        player.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertEqual(response.data['game']['cash'], 1001)
        self.assertEqual(len(response.data['players']), 1)
        self.assertEqual(response.data['players'][0]['uuid'], str(player.pk))
        self.assertEqual(response.data['players'][0]['cash'], 99)
        self.assertEqual(response.data['log']['uuid'], str(entry.pk))
