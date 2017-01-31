# -*- coding: utf-8 -*-
from unittest import TestCase

from .. import forms

class CreateGameTests(TestCase):
    def test_has_no_required_fields(self):
        form = forms.CreateGameForm(data={})
        self.assertTrue(form.is_valid())
