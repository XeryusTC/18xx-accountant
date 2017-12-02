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
        self.alice = factories.PlayerFactory(game=self.game, cash=0)
        self.bob = factories.PlayerFactory(game=self.game, cash=0)
        self.company = factories.CompanyFactory(game=self.game, cash=0,
            bank_shares=4)
        self.other_company = factories.CompanyFactory(game=self.game, cash=0)
        factories.PlayerShareFactory(owner=self.alice, company=self.company,
            shares=1)
        factories.PlayerShareFactory(owner=self.bob, company=self.company,
            shares=2)
        factories.CompanyShareFactory(owner=self.other_company,
            company=self.company, shares=3)
        self.url = reverse('undo')

    def create_entry(self, **kwargs):
        entry = models.LogEntry.objects.create(
            action=models.LogEntry.OPERATE, game=self.game,
            company=self.company, **kwargs)
        self.game.log_cursor = entry
        self.game.save()

    def test_undoing_company_paying_full_includes_data(self):
        self.create_entry(mode=models.LogEntry.FULL, revenue=10)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'undo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertCountEqual([p['uuid'] for p in response.data['players']],
            [str(self.alice.pk), str(self.bob.pk)])
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.other_company.pk)])

    def test_undoing_company_paying_half_includes_data(self):
        self.create_entry(mode=models.LogEntry.HALF, revenue=20)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'undo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertCountEqual([p['uuid'] for p in response.data['players']],
            [str(self.alice.pk), str(self.bob.pk)])
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.company.pk), str(self.other_company.pk)])

    def test_undoing_company_withholding_includes_data(self):
        self.create_entry(mode=models.LogEntry.WITHHOLD, revenue=30)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'undo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertNotIn('players', response.data.keys())
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.company.pk)])


class redoTests(APITestCase):
    def setUp(self):
        self.game = factories.GameFactory(cash=1000)
        self.start_entry = models.LogEntry.objects.create(game=self.game,
            text='New game started')
        self.game.log_cursor = self.start_entry
        self.game.save()
        self.alice = factories.PlayerFactory(game=self.game, cash=0)
        self.bob = factories.PlayerFactory(game=self.game, cash=0)
        self.company = factories.CompanyFactory(game=self.game, cash=0,
            bank_shares=4)
        self.other_company = factories.CompanyFactory(game=self.game, cash=0)
        factories.PlayerShareFactory(owner=self.alice, company=self.company,
            shares=1)
        factories.PlayerShareFactory(owner=self.bob, company=self.company,
            shares=2)
        factories.CompanyShareFactory(owner=self.other_company,
            company=self.company, shares=3)
        self.url = reverse('undo')

    def create_entry(self, **kwargs):
        entry = models.LogEntry.objects.create(
            action=models.LogEntry.OPERATE, game=self.game,
            company=self.company, **kwargs)

    def test_redoing_company_paying_full_includes_data(self):
        self.create_entry(mode=models.LogEntry.FULL, revenue=10)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'redo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertCountEqual([p['uuid'] for p in response.data['players']],
            [str(self.alice.pk), str(self.bob.pk)])
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.other_company.pk)])

    def test_redoing_company_paying_half_includes_data(self):
        self.create_entry(mode=models.LogEntry.HALF, revenue=20)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'redo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertCountEqual([p['uuid'] for p in response.data['players']],
            [str(self.alice.pk), str(self.bob.pk)])
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.company.pk), str(self.other_company.pk)])

    def test_redoing_company_withholding_includes_data(self):
        self.create_entry(mode=models.LogEntry.WITHHOLD, revenue=30)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'redo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertNotIn('players', response.data.keys())
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.company.pk)])
