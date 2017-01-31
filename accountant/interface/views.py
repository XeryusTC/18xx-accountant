# -*- coding: utf-8 -*-
from django.views.generic import FormView

from . import forms

class MainPageView(FormView):
    template_name = 'interface/index.html'
    form_class = forms.CreateGameForm
