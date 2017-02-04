# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve, reverse
from django.http.response import Http404
from django.test import RequestFactory, TestCase

from core import models
from core import factories
from .. import forms
from .. import views

FAKE_UUID = '00000000-0000-0000-0000-000000000000'

class MainPageTests(TestCase):
    def setUp(self):
        self.url = reverse('ui:main')
        self.view = views.MainPageView.as_view()
        self.factory = RequestFactory()

    def test_uses_correct_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'interface/base.html')
        self.assertTemplateUsed(response, 'interface/index.html')

    def test_url_resolves_to_correct_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, self.view.__name__)

    def test_main_page_uses_create_game_form(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertIsInstance(response.context_data['form'],
            forms.CreateGameForm)

    def test_main_page_creates_game_on_successful_POST_request(self):
        self.assertEqual(models.Game.objects.count(), 0)
        request = self.factory.post(self.url, data={})
        self.view(request)
        self.assertEqual(models.Game.objects.count(), 1)

    def test_main_page_redirects_to_game_after_creating_it(self):
        request = self.factory.post(self.url, data={})
        response = self.view(request)
        self.assertEqual(response.url,
            reverse('ui:game', kwargs={'uuid': models.Game.objects.last().pk}))

    def test_can_set_bank_cash_when_creating_game(self):
        request = self.factory.post(self.url, data={'bank_cash': 22})
        response = self.view(request)
        game = models.Game.objects.last()
        self.assertEqual(game.cash, 22)


class GameViewTests(TestCase):
    def setUp(self):
        self.game = factories.GameFactory()
        self.url = reverse('ui:game', kwargs={'uuid': self.game.pk})
        self.view = views.GameView.as_view()
        self.factory = RequestFactory()

    def test_uses_correct_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'interface/base.html')
        self.assertTemplateUsed(response, 'interface/game.html')

    def test_url_resolves_to_correct_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, self.view.__name__)

    def test_game_instance_is_added_to_context_data(self):
        request = self.factory.get(self.url)
        response = self.view(request, uuid=self.game.pk)
        self.assertEqual(response.context_data['game'], self.game)

    def test_returns_404_when_game_does_not_exist(self):
        request = self.factory.get(reverse('ui:game',
            kwargs={'uuid': FAKE_UUID}))
        with self.assertRaises(Http404):
            response = self.view(request, uuid=FAKE_UUID)


class AddPlayerViewTests(TestCase):
    def setUp(self):
        self.game = factories.GameFactory()
        self.url = reverse('ui:add_player', kwargs={'uuid': self.game.pk})
        self.view = views.AddPlayerView.as_view()
        self.factory = RequestFactory()

    def test_uses_correct_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'interface/base.html')
        self.assertTemplateUsed(response, 'interface/add_player.html')

    def test_url_resolves_to_correct_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, self.view.__name__)

    def test_uses_add_player_form(self):
        request = self.factory.get(self.url)
        response = self.view(request, uuid=self.game.pk)
        self.assertIsInstance(response.context_data['form'],
            forms.AddPlayerForm)

    def test_form_game_field_equals_uuid_in_url(self):
        request = self.factory.get(self.url)
        response = self.view(request, uuid=self.game.pk)
        self.assertEqual(response.context_data['form'].initial['game'],
            self.game)

    def test_reference_to_game_is_available_in_template(self):
        request = self.factory.get(self.url)
        response = self.view(request, uuid=self.game.pk)
        self.assertEqual(response.context_data['game'], self.game)

    def test_adds_player_to_game_on_successful_POST_request(self):
        self.assertEqual(self.game.players.count(), 0)
        request = self.factory.post(self.url, data={'name': 'Bob', 'cash': 19})
        self.view(request, uuid=self.game.pk)
        self.assertEqual(self.game.players.count(), 1)
        self.assertEqual(self.game.players.first().name, 'Bob')
        self.assertEqual(self.game.players.first().cash, 19)

    def test_adding_player_redirects_to_game(self):
        request = self.factory.post(self.url, data={'name': 'Alice',
            'cash': 1})
        response = self.view(request, uuid=self.game.pk)
        self.assertEqual(response.url,
            reverse('ui:game', kwargs={'uuid': self.game.pk}))

    def test_creating_duplicate_player_shows_error(self):
        player = factories.PlayerFactory(game=self.game)
        request = self.factory.post(self.url, data={'name': player.name,
            'cash': 2})
        response = self.view(request, uuid=self.game.pk)
        self.assertEqual(models.Player.objects.count(), 1)
        self.assertContains(response, forms.DUPLICATE_PLAYER_ERROR)

    def test_returns_404_on_get_request_when_game_in_url_doesnt_exist(self):
        request = self.factory.get(reverse('ui:game',
            kwargs={'uuid': FAKE_UUID}))
        with self.assertRaises(Http404):
            response = self.view(request, uuid=FAKE_UUID)

    def test_returns_404_on_post_request_when_game_in_url_doesnt_exist(self):
        request = self.factory.post(reverse('ui:game',
            kwargs={'uuid': FAKE_UUID}), data={})
        with self.assertRaises(Http404):
            response = self.view(request, uuid=FAKE_UUID)
