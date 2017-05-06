# -*- coding: utf-8 -*-
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest import mock

from ... import models
from ... import factories
from ... import utils
from ... import serializers
from ... import views

class ShareTransactionTests(APITestCase):
    def setUp(self):
        self.game = factories.GameFactory()
        self.url = reverse('transfer_share')
        self.player = factories.PlayerFactory(game=self.game, cash=100)
        # Company to buy shares from
        self.source_company = factories.CompanyFactory(game=self.game,
            cash=100)
        # Company to buy shares with
        self.buy_company = factories.CompanyFactory(game=self.game, cash=100)
        # Company to buy shares in
        self.share_company = factories.CompanyFactory(game=self.game, cash=0,
            ipo_shares=5, bank_shares=5)
        self.data = {'share': self.share_company.pk, 'amount': 1}

    def test_buying_from_ipo_includes_game_instance_in_response(self):
        self.data.update({'source_type': 'ipo', 'price': 10,
            'buyer_type': 'player', 'player_buyer': self.player.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertEqual(response.data['game']['cash'], 12010)

    def test_buying_from_bank_includes_game_instance_in_response(self):
        self.data.update({'source_type': 'bank', 'price': 20,
            'buyer_type': 'player', 'player_buyer': self.player.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertEqual(response.data['game']['cash'], 12020)

    def test_ipo_buying_share_includes_game_instance_in_response(self):
        self.data.update({'buyer_type': 'ipo', 'price': 30,
            'source_type': 'player', 'player_source': self.player.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertEqual(response.data['game']['cash'], 11970)

    def test_bank_buying_share_includes_game_instance_in_response(self):
        self.data.update({'buyer_type': 'bank', 'price': 40,
            'source_type': 'player', 'player_source': self.player.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.data['game']['uuid'], str(self.game.pk))
        self.assertEqual(response.data['game']['cash'], 11960)

    def test_company_whos_share_is_being_bought_is_always_in_response(self):
        self.data.update({'source_type': 'ipo', 'price': 50,
            'buyer_type': 'player', 'player_buyer': self.player.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(len(response.data['companies']), 1)
        self.assertEqual(str(self.share_company.pk),
            response.data['companies'][0]['uuid'])

    def test_company_buying_share_is_in_response(self):
        self.data.update({'source_type': 'ipo', 'price': 60,
            'buyer_type': 'company', 'company_buyer': self.buy_company.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.buy_company.refresh_from_db()
        self.assertIn(str(self.buy_company.pk),
            [c['uuid'] for c in response.data['companies']])
        self.assertEqual(self.buy_company.cash, 40)
        self.assertIn(40, [c['cash'] for c in response.data['companies']])

    def test_company_buying_itself_is_not_in_response_twice(self):
        self.data.update({'source_type': 'ipo', 'price': 0,
            'buyer_type': 'company', 'company_buyer': self.share_company.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.share_company.refresh_from_db()
        self.assertEqual(len(response.data['companies']), 1)
        self.assertEqual(response.data['companies'][0]['uuid'],
            str(self.share_company.pk))
        self.assertEqual(response.data['companies'][0]['ipo_shares'], 4)

    def test_company_selling_itself_is_not_in_response_twice(self):
        factories.CompanyShareFactory(owner=self.share_company,
            company=self.share_company, shares=5)
        self.data.update({'price': 1, 'source_type': 'company',
            'company_source': self.share_company.pk, 'buyer_type': 'ipo',
            'share': self.share_company.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.share_company.refresh_from_db()
        self.assertEqual(len(response.data['companies']), 1)
        self.assertEqual(str(self.share_company.pk),
            response.data['companies'][0]['uuid'])
        self.assertEqual(response.data['companies'][0]['ipo_shares'], 6)

    def test_player_buying_share_is_in_response(self):
        self.data.update({'source_type': 'ipo', 'price': 70,
            'buyer_type': 'player', 'player_buyer': self.player.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.player.refresh_from_db()
        self.assertEqual(str(self.player.pk),
            response.data['players'][0]['uuid'])
        self.assertEqual(response.data['players'][0]['cash'], 30)
        self.assertEqual(self.player.cash, 30)

    def test_company_selling_share_is_in_response(self):
        factories.CompanyShareFactory(owner=self.source_company,
            company=self.share_company)
        self.data.update({'buyer_type': 'bank', 'price': 80,
            'source_type': 'company',
            'company_source': self.source_company.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.source_company.refresh_from_db()
        self.assertIn(str(self.source_company.pk),
            [c['uuid'] for c in response.data['companies']])
        self.assertEqual(self.source_company.cash, 180)
        self.assertIn(180, [c['cash'] for c in response.data['companies']])

    def test_player_selling_share_is_in_response(self):
        self.data.update({'buyer_type': 'bank', 'price': 90,
            'source_type': 'player', 'player_source': self.player.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.player.refresh_from_db()
        self.assertEqual(str(self.player.pk),
            response.data['players'][0]['uuid'])
        self.assertEqual(response.data['players'][0]['cash'], 190)
        self.assertEqual(self.player.cash, 190)

    def test_when_player_buys_share_the_share_instance_is_in_response(self):
        self.data.update({'price': 100, 'buyer_type': 'player',
            'player_buyer': self.player.pk, 'source_type': 'ipo'})
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(len(response.data['shares']), 1)
        self.assertEqual(str(self.player.share_set.first().pk),
            response.data['shares'][0]['uuid'])

    def test_game_not_in_response_when_bank_or_ipo_not_involved(self):
        factories.CompanyShareFactory(owner=self.share_company,
            company=self.share_company)
        self.data.update({'price': 105, 'buyer_type': 'company',
            'company_buyer': self.buy_company.pk, 'source_type': 'company',
            'company_source': self.share_company.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.assertNotIn('game', response.data)

    def test_players_key_not_in_response_when_no_player_involved(self):
        factories.CompanyShareFactory(owner=self.share_company,
            company=self.share_company)
        self.data.update({'price': 105, 'buyer_type': 'company',
            'company_buyer': self.buy_company.pk, 'source_type': 'company',
            'company_source': self.share_company.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.assertNotIn('players', response.data)

    def test_when_company_buys_share_the_share_instance_is_in_response(self):
        self.data.update({'price': 110, 'buyer_type': 'company',
            'company_buyer': self.buy_company.pk, 'source_type': 'ipo'})
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(len(response.data['shares']), 1)
        self.assertEqual(str(self.buy_company.share_set.first().pk),
            response.data['shares'][0]['uuid'])

    def test_when_player_sells_share_the_share_instance_is_in_response(self):
        factories.PlayerShareFactory(owner=self.player,
            company=self.share_company, shares=3)
        self.data.update({'price': 120, 'buyer_type': 'bank',
            'source_type': 'player', 'player_source': self.player.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(len(response.data['shares']), 1)
        self.assertEqual(str(self.player.share_set.first().pk),
            response.data['shares'][0]['uuid'])
        self.assertEqual(response.data['shares'][0]['shares'], 2)

    def test_when_company_sells_share_the_share_instance_is_in_response(self):
        factories.CompanyShareFactory(owner=self.buy_company,
            company=self.share_company, shares=4)
        self.data.update({'price': 130, 'buyer_type': 'bank',
            'source_type': 'company', 'company_source': self.buy_company.pk})
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(len(response.data['shares']), 1)
        self.assertEqual(str(self.buy_company.share_set.first().pk),
            response.data['shares'][0]['uuid'])
        self.assertEqual(response.data['shares'][0]['shares'], 3)


@mock.patch.object(utils, 'buy_share')
class ShareTransactionWithMockTests(APITestCase):
    def setUp(self):
        self.game = factories.GameFactory(cash=1000)
        self.url = reverse('transfer_share')
        self.player = factories.PlayerFactory(game=self.game, cash=100)
        self.source_company = factories.CompanyFactory(game=self.game, cash=0)
        self.buy_company = factories.CompanyFactory(game=self.game, cash=0)
        factories.PlayerShareFactory(owner=self.player,
            company=self.source_company, shares=5)
        factories.CompanyShareFactory(owner=self.source_company,
            company=self.source_company)
        factories.CompanyShareFactory(owner=self.buy_company,
            company=self.source_company)
        factories.CompanyShareFactory(owner=self.buy_company,
            company=self.buy_company)

    def test_GET_request_is_empty(self, mock):
        """GET is for debug (and doc) purposes only"""
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data)

    def test_player_can_buy_from_ipo(self, mock_buy_share):
        data = {'buyer_type': 'player', 'player_buyer': self.player.pk,
            'source_type': 'ipo', 'share': self.source_company.pk, 'price': 1}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(self.player,
            self.source_company, utils.Share.IPO, 1, 1)

    def test_player_can_buy_from_bank_pool(self, mock_buy_share):
        data = {'buyer_type': 'player', 'player_buyer': self.player.pk,
            'source_type': 'bank', 'share': self.source_company.pk, 'price': 2}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(self.player,
            self.source_company, utils.Share.BANK, 2, 1)

    def test_player_can_buy_from_company_treasury(self, mock_buy_share):
        data = {'buyer_type': 'player', 'player_buyer': self.player.pk,
            'source_type': 'company', 'company_source': self.source_company.pk,
            'share': self.source_company.pk, 'price': 3}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(self.player,
            self.source_company, self.source_company, 3, 1)

    def test_player_can_sell_to_ipo(self, mock_buy_share):
        data = {'buyer_type': 'ipo', 'source_type': 'player',
            'player_source': self.player.pk, 'share': self.source_company.pk,
            'price': 4}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(utils.Share.IPO,
            self.source_company, self.player, 4, 1)

    def test_player_can_sell_to_bank_pool(self, mock_buy_share):
        data = {'buyer_type': 'bank', 'source_type': 'player',
            'player_source': self.player.pk, 'share': self.source_company.pk,
            'price': 5}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(utils.Share.BANK,
            self.source_company, self.player, 5, 1)

    def test_company_can_buy_own_share_from_ipo(self, mock_buy_share):
        data = {'buyer_type': 'company', 'company_buyer': self.buy_company.pk,
            'source_type': 'ipo', 'share': self.buy_company.pk,
            'price': 6}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.buy_company, utils.Share.IPO, 6, 1)

    def test_company_can_buy_own_share_from_bank_pool(self, mock_buy_share):
        data = {'buyer_type': 'company', 'company_buyer': self.buy_company.pk,
            'source_type': 'bank', 'share': self.buy_company.pk,
            'price': 7}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.buy_company, utils.Share.BANK, 7, 1)

    def test_company_can_buy_from_other_company_ipo(self, mock_buy_share):
        data = {'buyer_type': 'company', 'company_buyer': self.buy_company.pk,
            'source_type': 'ipo', 'share': self.source_company.pk,
            'price': 8}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.source_company, utils.Share.IPO, 8, 1)

    def test_company_can_buy_from_other_company_bank_pool(self,
            mock_buy_share):
        data = {'buyer_type': 'company', 'company_buyer': self.buy_company.pk,
            'source_type': 'bank', 'share': self.source_company.pk,
            'price': 9}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.source_company, utils.Share.BANK, 9, 1)

    def test_company_can_buy_from_other_company_treasury(self, mock_buy_share):
        data = {'buyer_type': 'company', 'company_buyer': self.buy_company.pk,
            'source_type': 'company', 'company_source': self.source_company.pk,
            'share': self.source_company.pk, 'price': 10}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.source_company, self.source_company, 10, 1)

    def test_company_can_sell_to_ipo(self, mock_buy_share):
        data = {'buyer_type': 'ipo', 'source_type': 'company',
            'company_source': self.buy_company.pk,
            'share': self.source_company.pk, 'price': 11}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(utils.Share.IPO,
            self.source_company, self.buy_company, 11, 1)

    def test_company_can_sell_to_bank_pool(self, mock_buy_share):
        data = {'buyer_type': 'bank', 'source_type': 'company',
            'company_source': self.buy_company.pk,
            'share': self.source_company.pk, 'price': 12}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(utils.Share.BANK,
            self.source_company, self.buy_company, 12, 1)

    def test_player_cannot_buy_from_ipo_if_it_has_no_shares(self,
            mock_buy_share):
        self.source_company.ipo_shares = 0
        self.source_company.save()
        mock_buy_share.side_effect = utils.InvalidShareTransaction
        data = {'buyer_type': 'player', 'player_buyer': self.player.pk,
            'source_type': 'ipo', 'share': self.source_company.pk, 'price': 13}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(views.NO_AVAILABLE_SHARES_ERROR,
            response.data['non_field_errors'])

    def test_player_cannot_buy_from_bank_pool_if_it_has_no_shares(self,
            mock_buy_share):
        mock_buy_share.side_effect = utils.InvalidShareTransaction
        data = {'buyer_type': 'player', 'player_buyer': self.player.pk,
            'source_type': 'bank', 'share': self.source_company.pk,
            'price': 14}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(views.NO_AVAILABLE_SHARES_ERROR,
            response.data['non_field_errors'])

    def test_player_cannot_buy_from_company_if_it_has_no_shares(self,
            mock_buy_share):
        mock_buy_share.side_effect = utils.InvalidShareTransaction
        data = {'buyer_type': 'player', 'player_buyer': self.player.pk,
            'source_type': 'company', 'company_source': self.buy_company.pk,
            'share': self.source_company.pk, 'price': 15}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(views.NO_AVAILABLE_SHARES_ERROR,
            response.data['non_field_errors'])

    def test_company_cannot_buy_from_ipo_if_it_has_no_shares(self,
            mock_buy_share):
        self.source_company.ipo_shares = 0
        data = {'buyer_type': 'company', 'company_buyer': self.buy_company.pk,
            'source_type': 'ipo', 'share': self.source_company.pk, 'price': 18}
        mock_buy_share.side_effect = utils.InvalidShareTransaction
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(views.NO_AVAILABLE_SHARES_ERROR,
            response.data['non_field_errors'])

    def test_company_cannot_buy_from_bank_pool_if_it_has_no_shares(self,
            mock_buy_share):
        self.source_company.bank_shares = 0
        data = {'buyer_type': 'company', 'company_buyer': self.buy_company.pk,
            'source_type': 'bank', 'share': self.source_company.pk,
            'price': 19}
        mock_buy_share.side_effect = utils.InvalidShareTransaction
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(views.NO_AVAILABLE_SHARES_ERROR,
            response.data['non_field_errors'])

    def test_company_cannot_buy_from_other_company_if_it_has_no_shares(self,
            mock_buy_share):
        mock_buy_share.side_effect = utils.InvalidShareTransaction
        data = {'buyer_type': 'company', 'company_buyer': self.buy_company.pk,
            'source_type': 'company', 'company_source': self.source_company.pk,
            'share': self.source_company.pk, 'price': 20}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(views.NO_AVAILABLE_SHARES_ERROR,
            response.data['non_field_errors'])

    def test_company_cannot_sell_to_ipo_if_it_has_no_shares(self,
            mock_buy_share):
        mock_buy_share.side_effect = utils.InvalidShareTransaction
        data = {'buyer_type': 'ipo', 'source_type': 'company',
            'company_source': self.buy_company.pk,
            'share': self.source_company.pk, 'share': self.source_company.pk,
            'price': 21}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(views.NO_AVAILABLE_SHARES_ERROR,
            response.data['non_field_errors'])

    def test_company_cannot_sell_to_bank_pool_if_it_has_no_shares(self,
            mock_buy_share):
        mock_buy_share.side_effect = utils.InvalidShareTransaction
        data = {'buyer_type': 'bank', 'source_type': 'company',
            'company_source': self.buy_company.pk,
            'share': self.source_company.pk, 'share': self.source_company.pk,
            'price': 22}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(views.NO_AVAILABLE_SHARES_ERROR,
            response.data['non_field_errors'])

    def test_player_buying_negative_ipo_shares_turns_into_sell_action(self,
            mock_buy_share):
        data = {'buyer_type': 'player', 'player_buyer': self.player.pk,
            'source_type': 'ipo', 'share': self.source_company.pk, 'price': 23,
            'amount': -2}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(utils.Share.IPO,
            self.source_company, self.player, 23, 2)

    def test_player_buying_negative_bank_shares_turns_into_sell_action(self,
            mock_buy_share):
        data = {'buyer_type': 'player', 'player_buyer': self.player.pk,
            'source_type': 'bank', 'share': self.source_company.pk,
            'price': 24, 'amount': -5}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(utils.Share.BANK,
            self.source_company, self.player, 24, 5)

    def test_company_buying_negative_ipo_shares_turns_into_sell_action(self,
            mock_buy_share):
        data = {'buyer_type': 'company', 'company_buyer': self.buy_company.pk,
            'source_type': 'ipo', 'share': self.source_company.pk, 'price': 25,
            'amount': -3}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(utils.Share.IPO,
            self.source_company, self.buy_company, 25, 3)

    def test_company_buying_negative_bank_shares_turns_into_sell_action(self,
            mock_buy_share):
        data = {'buyer_type': 'company', 'company_buyer': self.buy_company.pk,
            'source_type': 'bank', 'share': self.source_company.pk,
            'price': 26, 'amount': -1}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(utils.Share.BANK,
            self.source_company, self.buy_company, 26, 1)

    def test_player_buying_negative_company_shares_turns_into_sell_action(self,
            mock_buy_share):
        data = {'buyer_type': 'player', 'player_buyer': self.player.pk,
            'source_type': 'company', 'company_source': self.buy_company.pk,
            'share': self.source_company.pk, 'price': 27, 'amount': -1}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(self.buy_company,
            self.source_company, self.player, 27, 1)

    def test_company_buying_negative_company_shares_turns_into_sell_action(
            self, mock_buy_share):
        data = {'buyer_type': 'company', 'company_buyer': self.buy_company.pk,
            'source_type': 'company', 'company_source': self.source_company.pk,
            'share': self.source_company.pk, 'price': 28, 'amount': -2}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_buy_share.assert_called_once_with(self.source_company,
            self.source_company, self.buy_company, 28, 2)

    def test_gives_error_if_request_is_invalid(self, mock_buy_share):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_handles_invalid_transaction(self, mock_buy_share):
        mock_buy_share.side_effect = utils.InvalidShareTransaction
        data = {'buyer_type': 'company', 'company_buyer': self.buy_company.pk,
            'source_type': 'ipo', 'share': self.source_company.pk,
            'price': 29, 'amount': 1}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.data['non_field_errors'],
            [views.NO_AVAILABLE_SHARES_ERROR])

    def test_handles_different_game_exception(self, mock_buy_share):
        company = factories.CompanyFactory()
        player = factories.PlayerFactory()
        mock_buy_share.side_effect = utils.DifferentGameException
        data = {'buyer_type': 'player', 'player_buyer': player.pk,
            'source_type': 'ipo', 'amount': 1,
            'price': 30, 'share': self.source_company.pk}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.data['non_field_errors'],
            [views.DIFFERENT_GAME_ERROR])

    def test_does_not_handle_other_exceptions(self, mock_buy_share):
        mock_buy_share.side_effect = Exception
        data = {'buyer_type': 'company', 'company_buyer': self.buy_company.pk,
            'source_type': 'ipo', 'share': self.source_company.pk,
            'price': 31, 'amount': 1}
        with self.assertRaises(Exception):
            response = self.client.post(self.url, data, format='json')
