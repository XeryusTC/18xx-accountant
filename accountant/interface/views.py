# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.views import View
from django.views.generic import FormView

from . import forms
from core import models

class MainPageView(FormView):
    template_name = 'interface/index.html'
    form_class = forms.CreateGameForm
    success_url = '/'

    def form_valid(self, form):
        game = models.Game.objects.create()
        self.success_url = reverse('ui:game', kwargs={'uuid': game.pk})
        return super(FormView, self).form_valid(form)


class GameView(View):
    pass
