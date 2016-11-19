# -*- coding: utf-8 -*-
from django.views.generic import TemplateView

class HomepageView(TemplateView):
    template_name = 'game/homepage.html'


class GameView(TemplateView):
    template_name = 'game/game_base.html'
