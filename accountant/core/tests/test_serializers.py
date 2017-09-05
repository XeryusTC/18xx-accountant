# -*- coding: utf-8 -*-
from rest_framework import exceptions
from unittest import TestCase

from ..models import LogEntry
from .. import factories
from .. import serializers

class GameSerializerTests(TestCase):
    def test_creates_log_entry_on_game_creation(self):
        s = serializers.GameSerializer(data={})
        s.is_valid(raise_exception=True)
        game = s.save()

        self.assertEqual(LogEntry.objects.filter(game=game).count(), 1)
        self.assertEqual(game.log.last().text,
            'New game started')
        self.assertEqual(game.log_cursor, game.log.last())


class CompanySerializerTests(TestCase):
    def test_returns_user_friendly_message_when_company_not_unique(self):
        game = factories.GameFactory()
        factories.CompanyFactory(game=game, name='test')
        s = serializers.CompanySerializer(data={'game': game.pk,
            'name': 'test'})
        with self.assertRaises(exceptions.ValidationError):
            s.is_valid(raise_exception=True)
        self.assertIn(serializers.DUPLICATE_COMPANY_ERROR,
            s.errors['non_field_errors'])

    def test_creates_log_entry_on_company_creation(self):
        game = factories.GameFactory()
        s = serializers.CompanySerializer(data={'game': game.pk, 'name': 'C&O',
            'share_count': 20, 'cash': 300})
        s.is_valid(raise_exception=True)
        s.save()

        game.refresh_from_db()
        self.assertEqual(LogEntry.objects.filter(game=game).count(), 1)
        self.assertEqual(game.log.last().text,
            'Added 20-share company C&O with 300 starting cash')
        self.assertEqual(game.log_cursor, game.log.last())

    def test_creates_log_entry_on_company_update(self):
        game = factories.GameFactory()
        company = factories.CompanyFactory(game=game)
        s = serializers.CompanySerializer(company, data={'name': 'TEST',
            'game': game.pk, 'share_count': company.share_count})
        s.is_valid(raise_exception=True)
        s.save()

        game.refresh_from_db()
        company.refresh_from_db()
        self.assertEqual(LogEntry.objects.filter(game=game).count(), 1)
        self.assertEqual(game.log.last().text,
            'Company TEST has been edited')
        self.assertEqual(game.log_cursor, game.log.last())
        self.assertEqual(game.log.last().acting_company, company)

    def test_adds_IPO_shares_when_updating_with_extra_shares(self):
        game = factories.GameFactory()
        company = factories.CompanyFactory(game=game, name='test',
            share_count=5, ipo_shares=5)
        s = serializers.CompanySerializer(company, data={'share_count': 10,
            'game': game.pk, 'ipo_shares': 5})
        s.is_valid(raise_exception=True)
        s.save()

        company.refresh_from_db()
        self.assertEqual(company.share_count, 10)
        self.assertEqual(company.ipo_shares, 10)

    def test_removes_from_IPO_shares_when_removing_shares(self):
        game = factories.GameFactory()
        company = factories.CompanyFactory(game=game, share_count=5,
            ipo_shares=5)
        s = serializers.CompanySerializer(company, data={'share_count': 2,
            'game': game.pk, 'ipo_shares': 5})
        s.is_valid(raise_exception=True)
        s.save()

        company.refresh_from_db()
        self.assertEqual(company.share_count, 2)
        self.assertEqual(company.ipo_shares, 2)

    def test_removes_from_pool_when_insufficient_shares_in_IPO(self):
        game = factories.GameFactory()
        company = factories.CompanyFactory(game=game, share_count=10,
            ipo_shares=3, bank_shares=7)
        s = serializers.CompanySerializer(company, data={'share_count': 2,
            'game': game.pk, 'ipo_shares': 3, 'bank_shares': 7})
        s.is_valid(raise_exception=True)
        s.save()

        company.refresh_from_db()
        self.assertEqual(company.share_count, 2)
        self.assertEqual(company.ipo_shares, 0)
        self.assertEqual(company.bank_shares, 2)

    def test_removes_from_pool_when_no_shares_in_IPO(self):
        game = factories.GameFactory()
        company = factories.CompanyFactory(game=game, share_count=15,
            ipo_shares=0, bank_shares=6)
        s = serializers.CompanySerializer(company, data={'share_count': 10,
            'game': game.pk, 'ipo_shares': 0, 'bank_shares': 6})
        s.is_valid(raise_exception=True)
        s.save()

        company.refresh_from_db()
        self.assertEqual(company.share_count, 10)
        self.assertEqual(company.ipo_shares, 0)
        self.assertEqual(company.bank_shares, 1)

    def test_pool_shares_can_be_negative_as_after_changing_share_count(self):
        game = factories.GameFactory()
        company = factories.CompanyFactory(game=game, share_count=10,
            ipo_shares=1, bank_shares=1)
        s = serializers.CompanySerializer(company, data={'share_count': 5,
            'game': game.pk, 'ipo_shares': 1, 'bank_shares': 1})
        s.is_valid(raise_exception=True)
        s.save()

        company.refresh_from_db()
        self.assertEqual(company.share_count, 5)
        self.assertEqual(company.ipo_shares, 0)
        self.assertEqual(company.bank_shares, -3)


class PlayerSerializerTests(TestCase):
    def test_returns_user_friendly_message_when_player_not_unique(self):
        game = factories.GameFactory()
        factories.PlayerFactory(game=game, name='test')
        s = serializers.PlayerSerializer(data={'game': game.pk,
            'name': 'test'})
        with self.assertRaises(exceptions.ValidationError):
            s.is_valid(raise_exception=True)
        self.assertIn(serializers.DUPLICATE_PLAYER_ERROR,
            s.errors['non_field_errors'])

    def test_creates_log_entry_on_player_creation(self):
        game = factories.GameFactory()
        s = serializers.PlayerSerializer(data={'game': game.pk,
            'name': 'Alice', 'cash': 1})
        s.is_valid(raise_exception=True)
        s.save()

        game.refresh_from_db()
        self.assertEqual(LogEntry.objects.filter(game=game).count(), 1)
        self.assertEqual(game.log.last().text,
            'Added player Alice with 1 starting cash')
        self.assertEqual(game.log_cursor, game.log.last())


class TransferMoneySerializerTests(TestCase):
    def setUp(self):
        self.game = factories.GameFactory()
        self.player = factories.PlayerFactory(game=self.game)
        self.company = factories.CompanyFactory(game=self.game)

    def test_transfer_amount_is_required(self):
        s = serializers.TransferMoneySerializer(data={})
        with self.assertRaises(exceptions.ValidationError):
            s.is_valid(raise_exception=True)
        self.assertIn('amount', s.errors.keys())

    def test_need_source_or_destination(self):
        s = serializers.TransferMoneySerializer(data={'amount': 1})
        with self.assertRaises(exceptions.ValidationError):
            s.is_valid(raise_exception=True)
        self.assertIn(serializers.SOURCE_OR_DEST_REQUIRED_ERROR,
            s.errors['non_field_errors'])

    def test_to_player_satisfies_destination_need(self):
        s = serializers.TransferMoneySerializer(data={'amount': 2,
            'to_player': self.player.pk})
        s.is_valid(raise_exception=True)

    def test_from_player_satisfies_source_need(self):
        s = serializers.TransferMoneySerializer(data={'amount': 3,
            'from_player': self.player.pk})
        s.is_valid(raise_exception=True)

    def test_to_company_satisfies_destination_need(self):
        s = serializers.TransferMoneySerializer(data={'amount': 4,
            'to_company': self.company.pk})
        s.is_valid(raise_exception=True)

    def test_from_company_satisfies_source_need(self):
        s = serializers.TransferMoneySerializer(data={'amount': 5,
            'from_company': self.company.pk})
        s.is_valid(raise_exception=True)

    def test_source_instance_refers_to_Player_instance_if_set(self):
        s = serializers.TransferMoneySerializer(data={'amount': 6,
            'from_player': self.player.pk})
        s.is_valid(raise_exception=True)
        self.assertEqual(s.source_instance, self.player)

    def test_source_instance_refers_to_Company_instance_if_set(self):
        s = serializers.TransferMoneySerializer(data={'amount': 7,
            'from_company': self.company.pk})
        s.is_valid(raise_exception=True)
        self.assertEqual(s.source_instance, self.company)

    def test_source_instance_is_None_when_neither_from_field_is_set(self):
        s = serializers.TransferMoneySerializer(data={'amount': 8,
            'to_player': self.player.pk})
        s.is_valid(raise_exception=True)
        self.assertIsNone(s.source_instance)

    def test_dest_instance_refers_to_Player_instance_if_set(self):
        s = serializers.TransferMoneySerializer(data={'amount': 9,
            'to_player': self.player.pk})
        s.is_valid(raise_exception=True)
        self.assertEqual(s.dest_instance, self.player)

    def test_dest_instance_refers_to_Company_instance_if_set(self):
        s = serializers.TransferMoneySerializer(data={'amount': 10,
            'to_company': self.company.pk})
        s.is_valid(raise_exception=True)
        self.assertEqual(s.dest_instance, self.company)

    def test_dest_instance_is_None_when_neither_to_field_is_set(self):
        s = serializers.TransferMoneySerializer(data={'amount': 11,
            'from_player': self.player.pk})
        s.is_valid(raise_exception=True)
        self.assertIsNone(s.dest_instance)

    def test_both_to_fields_cannot_be_set_at_the_same_time(self):
        s = serializers.TransferMoneySerializer(data={'amount': 12,
            'to_player': self.player.pk, 'to_company': self.company.pk})
        with self.assertRaises(exceptions.ValidationError):
            s.is_valid(raise_exception=True)
        self.assertIn(serializers.DUPLICATE_SOURCE_OR_DEST_ERROR,
            s.errors['non_field_errors'])

    def test_both_from_fields_cannot_be_set_at_the_same_time(self):
        s = serializers.TransferMoneySerializer(data={'amount': 13,
            'from_player': self.player.pk, 'from_company': self.company.pk})
        with self.assertRaises(exceptions.ValidationError):
            s.is_valid(raise_exception=True)
        self.assertIn(serializers.DUPLICATE_SOURCE_OR_DEST_ERROR,
            s.errors['non_field_errors'])


class TransferShareSerializerTests(TestCase):
    def setUp(self):
        self.game = factories.GameFactory()
        self.player = factories.PlayerFactory(game=self.game)
        self.buy_company = factories.CompanyFactory(game=self.game)
        self.source_company = factories.CompanyFactory(game=self.game)

    def test_share_price_is_required(self):
        s = serializers.TransferShareSerializer(data={})
        self.assertFalse(s.is_valid())
        self.assertIn('price', s.errors.keys())

    def test_buyer_type_is_required(self):
        s = serializers.TransferShareSerializer(data={})
        self.assertFalse(s.is_valid())
        self.assertIn('buyer_type', s.errors.keys())

    def test_source_type_is_required(self):
        s = serializers.TransferShareSerializer(data={})
        self.assertFalse(s.is_valid())
        self.assertIn('source_type', s.errors.keys())

    def test_share_field_is_required(self):
        s = serializers.TransferShareSerializer(data={})
        self.assertFalse(s.is_valid())
        self.assertIn('share', s.errors.keys())

    def test_amount_is_one_by_default(self):
        s = serializers.TransferShareSerializer(data={'price': 1,
            'buyer_type': 'ipo', 'source_type': 'bank',
            'share': self.source_company.uuid})
        self.assertTrue(s.is_valid())
        self.assertEqual(s.validated_data['amount'], 1)

    def test_player_buyer_is_required_when_buyer_type_is_player(self):
        s = serializers.TransferShareSerializer(data={'price': 0,
            'buyer_type': 'player', 'source_type': 'ipo',
            'share': self.source_company.uuid})
        self.assertFalse(s.is_valid())
        self.assertIn(serializers.BUYER_REQUIRED_ERROR,
            s.errors['non_field_errors'])

    def test_company_buyer_is_required_when_buyer_type_is_company(self):
        s = serializers.TransferShareSerializer(data={'price': 0,
            'buyer_type': 'company', 'source_type': 'ipo',
            'share': self.source_company.uuid})
        self.assertFalse(s.is_valid())
        self.assertIn(serializers.BUYER_REQUIRED_ERROR,
            s.errors['non_field_errors'])

    def test_player_source_is_required_when_source_type_is_player(self):
        s = serializers.TransferShareSerializer(data={'price': 0,
            'source_type': 'player', 'buyer_type': 'bank',
            'share': self.source_company.uuid})
        self.assertFalse(s.is_valid())
        self.assertIn(serializers.SOURCE_REQUIRED_ERROR,
            s.errors['non_field_errors'])

    def test_company_source_is_required_when_source_type_is_company(self):
        s = serializers.TransferShareSerializer(data={'price': 0,
            'source_type': 'company', 'buyer_type': 'bank',
            'share': self.source_company.uuid})
        self.assertFalse(s.is_valid())
        self.assertIn(serializers.SOURCE_REQUIRED_ERROR,
            s.errors['non_field_errors'])

    def test_player_buyer_is_not_required_when_buyer_type_is_ipo(self):
        s = serializers.TransferShareSerializer(data={'price': 0,
            'buyer_type': 'ipo', 'source_type': 'bank',
            'share': self.source_company.uuid})
        self.assertTrue(s.is_valid())

    def test_player_buyer_is_not_required_when_buyer_type_is_bank_pool(self):
        s = serializers.TransferShareSerializer(data={'price': 0,
            'buyer_type': 'bank', 'source_type': 'ipo',
            'share': self.source_company.uuid})
        self.assertTrue(s.is_valid())

    def test_company_buyer_is_not_required_when_buyer_type_is_ipo(self):
        s = serializers.TransferShareSerializer(data={'price': 0,
            'buyer_type': 'ipo', 'source_type': 'bank',
            'share': self.source_company.uuid})
        self.assertTrue(s.is_valid())

    def test_company_buyer_is_not_required_when_buyer_type_is_bank_pool(self):
        s = serializers.TransferShareSerializer(data={'price': 0,
            'buyer_type': 'bank', 'source_type': 'ipo',
            'share': self.source_company.uuid})
        self.assertTrue(s.is_valid())

    def test_player_source_is_not_required_when_source_type_is_ipo(self):
        s = serializers.TransferShareSerializer(data={'price': 0,
            'source_type': 'ipo', 'buyer_type': 'bank',
            'share': self.source_company.uuid})
        self.assertTrue(s.is_valid())

    def test_player_source_is_not_required_when_source_type_is_bank_pool(self):
        s = serializers.TransferShareSerializer(data={'price': 0,
            'source_type': 'bank', 'buyer_type': 'ipo',
            'share': self.source_company.uuid})
        self.assertTrue(s.is_valid())

    def test_company_source_is_not_required_when_source_type_is_ipo(self):
        s = serializers.TransferShareSerializer(data={'price': 0,
            'source_type': 'ipo', 'buyer_type': 'bank',
            'share': self.source_company.uuid})
        self.assertTrue(s.is_valid())

    def test_company_source_is_not_required_when_source_type_is_bank(self):
        s = serializers.TransferShareSerializer(data={'price': 0,
            'source_type': 'bank', 'buyer_type': 'ipo',
            'share': self.source_company.uuid})
        self.assertTrue(s.is_valid())


class OperateTests(TestCase):
    def setUp(self):
        self.company = factories.CompanyFactory()

    def test_company_field_is_required(self):
        s = serializers.OperateSerializer(data={})
        self.assertFalse(s.is_valid())
        self.assertIn('company', s.errors.keys())

    def test_amount_field_is_required(self):
        s = serializers.OperateSerializer(data={})
        self.assertFalse(s.is_valid())
        self.assertIn('amount', s.errors.keys())

    def test_method_field_is_required(self):
        s = serializers.OperateSerializer(data={})
        self.assertFalse(s.is_valid())
        self.assertIn('method', s.errors.keys())

    def test_company_can_pay_full_dividends(self):
        s = serializers.OperateSerializer(data={'company': self.company.pk,
            'amount': 100, 'method': 'full'})
        self.assertTrue(s.is_valid())

    def test_company_can_pay_half_dividends(self):
        s = serializers.OperateSerializer(data={'company': self.company.pk,
            'amount': 200, 'method': 'half'})
        self.assertTrue(s.is_valid())

    def test_company_can_withhold_dividends(self):
        s = serializers.OperateSerializer(data={'company': self.company.pk,
            'amount': 300, 'method': 'withhold'})
        self.assertTrue(s.is_valid())
