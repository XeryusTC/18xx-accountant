# -*- coding: utf-8 -*-
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ... import models
from ... import factories
from ... import utils

class UndoTests(APITestCase):
    def setUp(self):
        self.game = factories.GameFactory(cash=1000)
        self.start_entry = models.LogEntry.objects.create(game=self.game,
            text='New game started')
        self.game.log_cursor = self.start_entry
        self.game.save()
        self.player = factories.PlayerFactory(game=self.game, cash=100)
        self.company = factories.CompanyFactory(game=self.game, cash=100)
        self.url = reverse('undo')

    def test_GET_request_is_empty(self):
        """GET is for debug (and doc) purposes only"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data)

    def test_undoing_player_to_bank_money_transfer_includes_instances(self):
        entry = models.LogEntry.objects.create(game=self.game,
            acting_player=self.player, amount=1,
            action=models.LogEntry.TRANSFER_MONEY)
        self.game.log_cursor = entry
        self.game.save()

        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'undo'})

        self.game.refresh_from_db()
        self.player.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertEqual(response.data['game']['cash'], 999)
        self.assertEqual(len(response.data['players']), 1)
        self.assertEqual(response.data['players'][0]['uuid'],
            str(self.player.pk))
        self.assertEqual(response.data['players'][0]['cash'], 101)

    def test_undoing_company_to_bank_money_transfer_includes_instances(self):
        entry = models.LogEntry.objects.create(game=self.game,
            acting_company=self.company, amount=2,
            action=models.LogEntry.TRANSFER_MONEY)
        self.game.log_cursor = entry
        self.game.save()

        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'undo'})

        self.game.refresh_from_db()
        self.company.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertEqual(response.data['game']['cash'], 998)
        self.assertNotIn('players', response.data.keys())
        self.assertEqual(len(response.data['companies']), 1)
        self.assertEqual(response.data['companies'][0]['uuid'],
            str(self.company.pk))
        self.assertEqual(response.data['companies'][0]['cash'], 102)

    def test_undoing_player_to_player_transfer_includes_instances(self):
        other_player = factories.PlayerFactory(game=self.game)
        entry = models.LogEntry.objects.create(game=self.game,
            acting_player=self.player, receiving_player=other_player,
            amount=2, action=models.LogEntry.TRANSFER_MONEY)
        self.game.log_cursor = entry
        self.game.save()

        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'undo'})

        self.player.refresh_from_db()
        other_player.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('game', response.data.keys())
        self.assertNotIn('companies', response.data.keys())
        self.assertCountEqual([p['uuid'] for p in response.data['players']],
            [str(self.player.pk), str(other_player.pk)])

    def test_undoing_player_to_company_transfer_includes_instances(self):
        entry = models.LogEntry.objects.create(game=self.game,
            acting_player=self.player, receiving_company=self.company,
            amount=2, action=models.LogEntry.TRANSFER_MONEY)
        self.game.log_cursor = entry
        self.game.save()

        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'undo'})

        self.player.refresh_from_db()
        self.company.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('game', response.data.keys())
        self.assertEqual(len(response.data['players']), 1)
        self.assertEqual(len(response.data['companies']), 1)
        self.assertEqual(response.data['players'][0]['uuid'],
            str(self.player.pk))
        self.assertEqual(response.data['companies'][0]['uuid'],
            str(self.company.pk))

    def test_undoing_company_to_player_transfer_includes_instances(self):
        entry = models.LogEntry.objects.create(game=self.game,
            acting_company=self.company, receiving_player=self.player,
            amount=2, action=models.LogEntry.TRANSFER_MONEY)
        self.game.log_cursor = entry
        self.game.save()

        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'undo'})

        self.player.refresh_from_db()
        self.company.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('game', response.data.keys())
        self.assertEqual(len(response.data['players']), 1)
        self.assertEqual(len(response.data['companies']), 1)
        self.assertEqual(response.data['players'][0]['uuid'],
            str(self.player.pk))
        self.assertEqual(response.data['companies'][0]['uuid'],
            str(self.company.pk))

    def test_undoing_company_to_company_transfer_includes_instances(self):
        other_company = factories.CompanyFactory(game=self.game)
        entry = models.LogEntry.objects.create(game=self.game,
            acting_company=self.company, receiving_company=other_company,
            amount=2, action=models.LogEntry.TRANSFER_MONEY)
        self.game.log_cursor = entry
        self.game.save()

        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'undo'})

        self.company.refresh_from_db()
        other_company.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('game', response.data.keys())
        self.assertNotIn('players', response.data.keys())
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.company.pk), str(other_company.pk)])


class RedoTests(APITestCase):
    def setUp(self):
        self.game = factories.GameFactory(cash=1000)
        self.start_entry = models.LogEntry.objects.create(game=self.game,
            text='New game started')
        self.game.log_cursor = self.start_entry
        self.game.save()
        self.player = factories.PlayerFactory(game=self.game, cash=100)
        self.company = factories.CompanyFactory(game=self.game, cash=100)
        self.url = reverse('undo')

    def test_GET_request_is_empty(self):
        """GET is for debug (and doc) purposes only"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data)

    def test_redoing_player_to_bank_money_transfer_includes_data(self):
        entry = models.LogEntry.objects.create(game=self.game,
            acting_player=self.player, amount=1,
            action=models.LogEntry.TRANSFER_MONEY)

        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'redo'})

        self.game.refresh_from_db()
        self.player.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertEqual(response.data['game']['cash'], 1001)
        self.assertNotIn('companies', response.data.keys())
        self.assertEqual(len(response.data['players']), 1)
        self.assertEqual(response.data['players'][0]['uuid'],
            str(self.player.pk))
        self.assertEqual(response.data['players'][0]['cash'], 99)
        self.assertEqual(response.data['log']['uuid'], str(entry.pk))

    def test_redoing_company_to_bank_money_transfer_includes_data(self):
        entry = models.LogEntry.objects.create(game=self.game,
            action=models.LogEntry.TRANSFER_MONEY, acting_company=self.company,
            amount=2)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'redo'})

        self.game.refresh_from_db()
        self.company.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertEqual(response.data['game']['cash'], 1002)
        self.assertNotIn('players', response.data.keys())
        self.assertEqual(len(response.data['companies']), 1)
        self.assertEqual(response.data['companies'][0]['uuid'],
            str(self.company.pk))
        self.assertEqual(response.data['companies'][0]['cash'], 98)
        self.assertEqual(response.data['log']['uuid'], str(entry.pk))

    def test_redoing_player_to_player_money_transfer_includes_data(self):
        other_player = factories.PlayerFactory(game=self.game)
        entry = models.LogEntry.objects.create(game=self.game,
            acting_player=self.player, receiving_player=other_player,
            amount=3, action=models.LogEntry.TRANSFER_MONEY)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'redo'})

        self.player.refresh_from_db()
        other_player.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('game', response.data.keys())
        self.assertNotIn('companies', response.data.keys())
        self.assertCountEqual([p['uuid'] for p in response.data['players']],
            [str(self.player.pk), str(other_player.pk)])
        self.assertEqual(response.data['log']['uuid'], str(entry.pk))

    def test_redoing_player_to_company_money_transfer_includes_data(self):
        entry = models.LogEntry.objects.create(game=self.game,
            acting_player=self.player, receiving_company=self.company,
            amount=4, action=models.LogEntry.TRANSFER_MONEY)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'redo'})

        self.player.refresh_from_db()
        self.company.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('game', response.data.keys())
        self.assertEqual(len(response.data['players']), 1)
        self.assertEqual(len(response.data['companies']), 1)
        self.assertEqual(response.data['players'][0]['uuid'],
            str(self.player.pk))
        self.assertEqual(response.data['companies'][0]['uuid'],
            str(self.company.pk))
        self.assertEqual(response.data['log']['uuid'], str(entry.pk))

    def test_redoing_company_to_player_money_transfer_includes_data(self):
        entry = models.LogEntry.objects.create(game=self.game,
            acting_company=self.company, receiving_player=self.player,
            amount=5, action=models.LogEntry.TRANSFER_MONEY)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'redo'})

        self.player.refresh_from_db()
        self.company.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('game', response.data.keys())
        self.assertEqual(len(response.data['players']), 1)
        self.assertEqual(len(response.data['companies']), 1)
        self.assertEqual(response.data['players'][0]['uuid'],
            str(self.player.pk))
        self.assertEqual(response.data['companies'][0]['uuid'],
            str(self.company.pk))
        self.assertEqual(response.data['log']['uuid'], str(entry.pk))

    def test_redoing_company_to_company_money_transfer_includes_data(self):
        other_company = factories.CompanyFactory(game=self.game)
        entry = models.LogEntry.objects.create(game=self.game,
            acting_company=self.company, receiving_company=other_company,
            amount=6, action=models.LogEntry.TRANSFER_MONEY)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'redo'})

        self.company.refresh_from_db()
        other_company.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('game', response.data.keys())
        self.assertNotIn('players', response.data.keys())
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.company.pk), str(other_company.pk)])
        self.assertEqual(response.data['log']['uuid'], str(entry.pk))
