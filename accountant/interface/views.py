# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import FormView, TemplateView

from . import forms
from core import models

class MainPageView(FormView):
    template_name = 'interface/index.html'
    form_class = forms.CreateGameForm
    success_url = '/'

    def form_valid(self, form):
        game = models.Game.objects.create(cash=form.cleaned_data['bank_cash'])
        self.success_url = reverse('ui:game', kwargs={'uuid': game.pk})
        return super(FormView, self).form_valid(form)


class GameView(TemplateView):
    template_name = 'interface/game.html'

    def get_context_data(self, **kwargs):
        context = super(GameView, self).get_context_data(**kwargs)
        context['game'] = get_object_or_404(models.Game, pk=kwargs['uuid'])
        return context


class AddPlayerView(FormView):
    template_name = 'interface/add_player.html'
    form_class = forms.AddPlayerForm

    def get_success_url(self):
        return reverse('ui:game', kwargs={'uuid': self.kwargs['uuid']})

    def form_valid(self, form):
        game = models.Game.objects.get(pk=self.kwargs['uuid'])
        player = models.Player.objects.create(game=game,
            name=form.cleaned_data['name'], cash=form.cleaned_data['cash'])
        return super(FormView, self).form_valid(form)
