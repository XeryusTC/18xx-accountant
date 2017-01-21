# -*- coding: utf-8 -*-
from rest_framework import exceptions
from unittest import TestCase

from .. import factories
from .. import serializers

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
