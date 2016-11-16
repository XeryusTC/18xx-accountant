# -*- coding: utf-8 -*-
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

DEFAULT_WAIT = 3

class FunctionalTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.webdriver = webdriver.PhantomJS
        self.browser = self.webdriver()
        self.browser.implicitly_wait(DEFAULT_WAIT)

    def tearDown(self):
        self.browser.quit()
