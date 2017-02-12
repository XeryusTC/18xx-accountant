# -*- coding: utf-8 -*-
from django.core.exceptions import NON_FIELD_ERRORS
from unittest import TestCase

from core import factories
from .. import forms

class CreateGameTests(TestCase):
    def test_has_no_required_fields(self):
        form = forms.CreateGameForm(data={})
        self.assertTrue(form.is_valid())

    def test_can_set_bank_cash(self):
        form = forms.CreateGameForm(data={'bank_cash': 1000})
        self.assertTrue(form.is_valid())

    def test_bank_cash_is_0_by_default(self):
        form = forms.CreateGameForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['bank_cash'], 0)


class AddPlayerTests(TestCase):
    def test_name_field_is_required(self):
        form = forms.AddPlayerForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors.keys())

    def test_cash_field_is_required(self):
        form = forms.AddPlayerForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('cash', form.errors.keys())

    def test_game_field_is_required(self):
        form = forms.AddPlayerForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('game', form.errors.keys())

    def test_form_validation_for_duplicate_items(self):
        player = factories.PlayerFactory()
        form = forms.AddPlayerForm(data={'game': player.game.pk,
            'name': player.name, 'cash': 10})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors[NON_FIELD_ERRORS],
            [forms.DUPLICATE_PLAYER_ERROR])


class AddCompanyTests(TestCase):
    def test_name_field_is_required(self):
        form = forms.AddCompanyForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors.keys())

    def test_cash_field_is_required(self):
        form = forms.AddCompanyForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('cash', form.errors.keys())

    def test_shares_field_is_required(self):
        form = forms.AddCompanyForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('share_count', form.errors.keys())

    def test_game_field_is_required(self):
        form = forms.AddCompanyForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('game', form.errors.keys())

    def test_background_color_field_is_not_required(self):
        form = forms.AddCompanyForm(data={})
        self.assertFalse(form.is_valid())
        self.assertNotIn('background_color', form.errors.keys())

    def test_text_color_field_is_not_required(self):
        form = forms.AddCompanyForm(data={})
        self.assertFalse(form.is_valid())
        self.assertNotIn('text_color', form.errors.keys())
