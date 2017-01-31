# -*- coding: utf-8 -*-
from unittest import TestCase

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
