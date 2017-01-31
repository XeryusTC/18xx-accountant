# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase

from .. import views

class MainPageTests(TestCase):
    def test_uses_correct_templates(self):
        response = self.client.get(reverse('ui:main'))
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'interface/base.html')
        self.assertTemplateUsed(response, 'interface/index.html')
