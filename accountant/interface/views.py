# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
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
    template_name = 'interface/base.html'
