# -*- coding: utf-8 -*-
from .base import FunctionalTestCase

class DjangoWorkingTest(FunctionalTestCase):
    def test_django_returns_default_output(self):
        self.browser.get('http://localhost:8000')

        self.assertIn('Django', self.browser.title)
