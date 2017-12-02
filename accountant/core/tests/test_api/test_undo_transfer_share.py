# -*- coding: utf-8 -*-
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ... import models
from ... import factories

class UndoTests(APITestCase):
    def setUp(self):
        self.game = factories.GameFactory(cash=1000)
        self.start_entry = models.LogEntry.objects.create(game=self.game,
            text='New game started')
        self.game.log_cursor = self.start_entry
        self.game.save()
        self.player = factories.PlayerFactory(game=self.game, cash=100)
        self.other_player = factories.PlayerFactory(game=self.game, cash=0)
        self.buy_company = factories.CompanyFactory(game=self.game, cash=100)
        self.share_company = factories.CompanyFactory(game=self.game, cash=0)
        self.source_company = factories.CompanyFactory(game=self.game, cash=0)
        self.player_share = factories.PlayerShareFactory(owner=self.player,
            company=self.share_company, shares=0)
        self.other_player_share = factories.PlayerShareFactory(
            owner=self.other_player, company=self.share_company, shares=0)
        self.company_share = factories.CompanyShareFactory(
            owner=self.buy_company, company=self.share_company, shares=10)
        self.source_company_share = factories.CompanyShareFactory(
            owner=self.source_company, company=self.share_company, shares=10)
        self.url = reverse('undo')

    def create_entry(self, **kwargs):
        entry = models.LogEntry.objects.create(
            action=models.LogEntry.TRANSFER_SHARE, game=self.game,
            company=self.share_company, **kwargs)
        self.game.log_cursor = entry
        self.game.save()

    def test_undoing_player_buying_share_from_ipo_includes_data(self):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='ipo', price=1, amount=2)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'undo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertCountEqual([p['uuid'] for p in response.data['players']],
            [str(self.player.pk)])
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.share_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.player_share.pk)])

    def test_undoing_player_buying_share_from_bank_includes_data(self):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='bank', price=2, amount=1)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'undo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertCountEqual([p['uuid'] for p in response.data['players']],
            [str(self.player.pk)])
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.share_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.player_share.pk)])

    def test_undoing_player_buying_share_from_company_includes_data(self):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='company', company_source=self.buy_company,
            price=3, amount=5)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'undo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('game', response.data.keys())
        self.assertCountEqual([p['uuid'] for p in response.data['players']],
            [str(self.player.pk)])
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.buy_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.player_share.pk), str(self.company_share.pk)])

    def test_undoing_player_buying_share_from_player_includes_data(self):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='player', player_source=self.other_player, price=4,
            amount=3)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'undo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('game', response.data.keys())
        self.assertCountEqual([p['uuid'] for p in response.data['players']],
            [str(self.player.pk), str(self.other_player.pk)])
        self.assertNotIn('companies', response.data.keys())
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.player_share.pk), str(self.other_player_share.pk)])

    def test_undoing_company_buying_share_from_ipo_includes_data(self):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='ipo', price=5, amount=7)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'undo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertNotIn('players', response.data.keys())
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.buy_company.pk), str(self.share_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.company_share.pk)])

    def test_undoing_company_buying_share_from_bank_includes_data(self):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='bank', price=6, amount=2)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'undo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertNotIn('players', response.data.keys())
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.buy_company.pk), str(self.share_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.company_share.pk)])

    def test_undoing_company_buying_share_from_company_includes_data(self):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='company', company_source=self.source_company,
            price=7, amount=3)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'undo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('game', response.data.keys())
        self.assertNotIn('players', response.data.keys())
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.buy_company.pk), str(self.source_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.company_share.pk), str(self.source_company_share.pk)])

    def test_undoing_company_buying_share_from_player_includes_data(self):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='player', player_source=self.player, price=8, amount=1)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'undo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('game', response.data.keys())
        self.assertCountEqual([p['uuid'] for p in response.data['players']],
            [str(self.player.pk)])
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.buy_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.company_share.pk), str(self.player_share.pk)])

    def test_undoing_player_selling_share_to_ipo_includes_data(self):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='ipo', price=9, amount=2)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'undo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertCountEqual([p['uuid'] for p in response.data['players']],
            [str(self.player.pk)])
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.share_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.player_share.pk)])

    def test_undoing_player_selling_share_to_bank_includes_data(self):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='bank', price=10, amount=4)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'undo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertCountEqual([p['uuid'] for p in response.data['players']],
            [str(self.player.pk)])
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.share_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.player_share.pk)])

    def test_undoing_player_selling_share_to_company_includes_data(self):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='company', company_source=self.source_company, price=11,
            amount=5)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'undo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('game', response.data.keys())
        self.assertCountEqual([p['uuid'] for p in response.data['players']],
            [str(self.player.pk)])
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.source_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.player_share.pk), str(self.source_company_share.pk)])

    def test_undoing_player_selling_share_to_player_includes_data(self):
        self.create_entry(buyer='player', player_buyer=self.player,
            source='player', player_source=self.other_player, price=12,
            amount=3)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'undo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('game', response.data.keys())
        self.assertCountEqual([p['uuid'] for p in response.data['players']],
            [str(self.player.pk), str(self.other_player.pk)])
        self.assertNotIn('companies', response.data.keys())
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.player_share.pk), str(self.other_player_share.pk)])

    def test_undoing_company_selling_share_to_ipo_includes_data(self):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='ipo', price=13, amount=3)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'undo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertNotIn('players', response.data.keys())
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.buy_company.pk), str(self.share_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.company_share.pk)])

    def test_undoing_company_selling_share_to_bank_includes_data(self):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='bank', price=14, amount=6)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'undo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertNotIn('players', response.data.keys())
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.buy_company.pk), str(self.share_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.company_share.pk)])

    def test_undoing_company_selling_share_to_company_includes_data(self):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='company', company_source=self.source_company, price=15,
            amount=4)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'undo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('game', response.data.keys())
        self.assertNotIn('players', response.data.keys())
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.buy_company.pk), str(self.source_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.company_share.pk), str(self.source_company_share.pk)])

    def test_undoing_company_selling_share_to_player_includes_data(self):
        self.create_entry(buyer='company', company_buyer=self.buy_company,
            source='player', player_source=self.player, price=16, amount=1)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'undo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('game', response.data.keys())
        self.assertCountEqual([p['uuid'] for p in response.data['players']],
            [str(self.player.pk)])
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.buy_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.company_share.pk), str(self.player_share.pk)])


class RedoTests(APITestCase):
    def setUp(self):
        self.game = factories.GameFactory(cash=1000)
        start_entry = models.LogEntry.objects.create(game=self.game,
            text='New game started')
        self.game.log_cursor = start_entry
        self.game.save()
        self.player = factories.PlayerFactory(game=self.game, cash=100)
        self.other_player = factories.PlayerFactory(game=self.game, cash=0)
        self.buy_company = factories.CompanyFactory(game=self.game, cash=100)
        self.share_company = factories.CompanyFactory(game=self.game, cash=0)
        self.source_company = factories.CompanyFactory(game=self.game, cash=0)
        self.player_share = factories.PlayerShareFactory(owner=self.player,
            company=self.share_company, shares=0)
        self.other_player_share = factories.PlayerShareFactory(
            owner=self.other_player, company=self.share_company, shares=0)
        self.company_share = factories.CompanyShareFactory(
            owner=self.buy_company, company=self.share_company, shares=10)
        self.source_company_share = factories.CompanyShareFactory(
            owner=self.source_company, company=self.share_company, shares=10)
        self.url = reverse('undo')

    def create_entry(self, **kwargs):
        models.LogEntry.objects.create(action=models.LogEntry.TRANSFER_SHARE,
            game=self.game, company=self.share_company, **kwargs)

    def test_redoing_player_buying_share_from_ipo_includes_data(self):
        self.create_entry(price=1, amount=8, buyer='player',
            player_buyer=self.player, source='ipo')
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'redo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertCountEqual([p['uuid'] for p in response.data['players']],
            [str(self.player.pk)])
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.share_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.player_share.pk)])

    def test_redoing_player_buying_share_from_bank_includes_data(self):
        self.create_entry(price=2, amount=7, buyer='player',
            player_buyer=self.player, source='bank')
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'redo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertCountEqual([p['uuid'] for p in response.data['players']],
            [str(self.player.pk)])
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.share_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.player_share.pk)])

    def test_redoing_player_buying_share_from_company_includes_data(self):
        self.create_entry(price=3, amount=6, buyer='player',
            player_buyer=self.player, source='company',
            company_source=self.source_company)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'redo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('game', response.data.keys())
        self.assertCountEqual([p['uuid'] for p in response.data['players']],
            [str(self.player.pk)])
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.source_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.player_share.pk), str(self.source_company_share.pk)])

    def test_redoing_player_buying_share_from_player_includes_data(self):
        self.create_entry(price=4, amount=5, buyer='player',
            player_buyer=self.player, source='player',
            player_source=self.other_player)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'redo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('game', response.data.keys())
        self.assertCountEqual([p['uuid'] for p in response.data['players']],
            [str(self.player.pk), str(self.other_player.pk)])
        self.assertNotIn('company', response.data.keys())
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.player_share.pk), str(self.other_player_share.pk)])

    def test_redoing_company_buying_share_from_ipo_includes_data(self):
        self.create_entry(price=5, amount=4, buyer='company',
            company_buyer=self.buy_company, source='ipo')
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'redo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertNotIn('players', response.data.keys())
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.buy_company.pk), str(self.share_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.company_share.pk)])

    def test_redoing_company_buying_share_from_bank_includes_data(self):
        self.create_entry(price=6, amount=3, buyer='company',
            company_buyer=self.buy_company, source='bank')
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'redo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertNotIn('players', response.data.keys())
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.buy_company.pk), str(self.share_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.company_share.pk)])

    def test_redoing_company_buying_share_from_company_includes_data(self):
        self.create_entry(price=7, amount=2, buyer='company',
            company_buyer=self.buy_company, source='company',
            company_source=self.source_company)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'redo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('game', response.data.keys())
        self.assertNotIn('players', response.data.keys())
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.buy_company.pk), str(self.source_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.company_share.pk), str(self.source_company_share.pk)])

    def test_redoing_company_buying_share_from_player_includes_data(self):
        self.create_entry(price=8, amount=1, buyer='company',
            company_buyer=self.buy_company, source='player',
            player_source=self.player)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'redo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('game', response.data.keys())
        self.assertCountEqual([p['uuid'] for p in response.data['players']],
            [str(self.player.pk)])
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.buy_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.company_share.pk), str(self.player_share.pk)])

    def test_redoing_player_selling_share_to_ipo_includes_data(self):
        self.create_entry(price=9, amount=-1, buyer='player',
            player_buyer=self.player, source='ipo')
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'redo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertCountEqual([p['uuid'] for p in response.data['players']],
            [str(self.player.pk)])
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.share_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.player_share.pk)])

    def test_redoing_player_selling_share_to_bank_includes_data(self):
        self.create_entry(price=10, amount=-2, buyer='player',
            player_buyer=self.player, source='bank')
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'redo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertCountEqual([p['uuid'] for p in response.data['players']],
            [str(self.player.pk)])
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.share_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.player_share.pk)])

    def test_redoing_player_selling_share_to_company_includes_data(self):
        self.create_entry(price=11, amount=-3, buyer='player',
            player_buyer=self.player, source='company',
            company_source=self.source_company)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'redo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('game', response.data.keys())
        self.assertCountEqual([p['uuid'] for p in response.data['players']],
            [str(self.player.pk)])
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.source_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.player_share.pk), str(self.source_company_share.pk)])

    def test_redoing_player_selling_share_to_player_includes_data(self):
        self.create_entry(price=12, amount=-4, buyer='player',
            player_buyer=self.player, source='player',
            player_source=self.other_player)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'redo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('game', response.data.keys())
        self.assertCountEqual([p['uuid'] for p in response.data['players']],
            [str(self.player.pk), str(self.other_player.pk)])
        self.assertNotIn('company', response.data.keys())
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.player_share.pk), str(self.other_player_share.pk)])

    def test_redoing_company_selling_share_to_ipo_includes_data(self):
        self.create_entry(price=13, amount=-5, buyer='company',
            company_buyer=self.buy_company, source='ipo')
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'redo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertNotIn('players', response.data.keys())
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.buy_company.pk), str(self.share_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.company_share.pk)])

    def test_redoing_company_selling_share_to_bank_includes_data(self):
        self.create_entry(price=14, amount=-6, buyer='company',
            company_buyer=self.buy_company, source='bank')
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'redo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertNotIn('players', response.data.keys())
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.buy_company.pk), str(self.share_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.company_share.pk)])

    def test_redoing_company_selling_share_to_company_includes_data(self):
        self.create_entry(price=15, amount=-7, buyer='company',
            company_buyer=self.buy_company, source='company',
            company_source=self.source_company)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'redo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('game', response.data.keys())
        self.assertNotIn('players', response.data.keys())
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.buy_company.pk), str(self.source_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.company_share.pk), str(self.source_company_share.pk)])

    def test_redoing_company_selling_share_to_player_includes_data(self):
        self.create_entry(price=16, amount=-8, buyer='company',
            company_buyer=self.buy_company, source='player',
            player_source=self.player)
        response = self.client.post(self.url, {'game': str(self.game.pk),
            'action': 'redo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('game', response.data.keys())
        self.assertCountEqual([p['uuid'] for p in response.data['players']],
            [str(self.player.pk)])
        self.assertCountEqual([c['uuid'] for c in response.data['companies']],
            [str(self.buy_company.pk)])
        self.assertCountEqual([s['uuid'] for s in response.data['shares']],
            [str(self.company_share.pk), str(self.player_share.pk)])
