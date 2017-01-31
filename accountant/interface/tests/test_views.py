# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve, reverse
from django.http.response import Http404
from django.test import RequestFactory, TestCase

from core import models
from core import factories
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

    def test_main_page_creates_game_on_successful_POST_request(self):
        self.assertEqual(models.Game.objects.count(), 0)
        factory = RequestFactory()
        request = factory.post(reverse('ui:main'), data={})
        views.MainPageView.as_view()(request)
        self.assertEqual(models.Game.objects.count(), 1)

    def test_main_page_redirects_to_game_after_creating_it(self):
        factory = RequestFactory()
        request = factory.post(reverse('ui:main'), data={})
        response = views.MainPageView.as_view()(request)
        self.assertEqual(response.url,
            reverse('ui:game', kwargs={'uuid': models.Game.objects.last().pk}))

    def test_can_set_bank_cash_when_creating_game(self):
        factory = RequestFactory()
        request = factory.post(reverse('ui:main'), data={'bank_cash': 22})
        response = views.MainPageView.as_view()(request)
        game = models.Game.objects.last()
        self.assertEqual(game.cash, 22)


class GameViewTests(TestCase):
    def setUp(self):
        self.game = factories.GameFactory()

    def test_uses_correct_templates(self):
        response = self.client.get(reverse('ui:game',
            kwargs={'uuid': self.game.pk}))
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'interface/base.html')
        self.assertTemplateUsed(response, 'interface/game.html')

    def test_url_resolves_to_correct_view(self):
        found = resolve(reverse('ui:game', kwargs={'uuid': self.game.pk}))
        self.assertEqual(found.func.__name__,
            views.GameView.as_view().__name__)

    def test_game_instance_is_added_to_context_data(self):
        factory = RequestFactory()
        request = factory.get(reverse('ui:game',
            kwargs={'uuid': self.game.pk}))
        response = views.GameView.as_view()(request, uuid=self.game.pk)
        self.assertEqual(response.context_data['game'], self.game)

    def test_returns_404_when_game_does_not_exist(self):
        factory = RequestFactory()
        request = factory.get(reverse('ui:game',
            kwargs={'uuid': '00000000-0000-0000-0000-000000000000'}))
        with self.assertRaises(Http404):
            response = views.GameView.as_view()(request,
                uuid='00000000-0000-0000-0000-000000000000')
