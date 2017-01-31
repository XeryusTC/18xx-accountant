# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve, reverse
from django.test import RequestFactory, TestCase

from .. import forms
from .. import views

class MainPageTests(TestCase):
    def test_uses_correct_templates(self):
        response = self.client.get(reverse('ui:main'))
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'interface/base.html')
        self.assertTemplateUsed(response, 'interface/index.html')

    def test_url_resolves_to_correct_view(self):
        found = resolve(reverse('ui:main'))
        self.assertEqual(found.func.__name__,
            views.MainPageView.as_view().__name__)

    def test_main_page_uses_create_game_form(self):
        factory = RequestFactory()
        request = factory.get(reverse('ui:main'))
        response = views.MainPageView.as_view()(request)
        self.assertIsInstance(response.context_data['form'],
            forms.CreateGameForm)
