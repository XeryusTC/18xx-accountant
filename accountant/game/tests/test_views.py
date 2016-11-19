# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase

from common.test import ViewTestMixin

from .. import views

class HomepageViewTest(ViewTestMixin, TestCase):
    explicit_url = '/en/'
    templates = ('base.html', 'game/homepage.html')

    def setUp(self):
        self.url = reverse('game:start')
        self.view = views.HomepageView.as_view()
