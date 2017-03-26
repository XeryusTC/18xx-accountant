# -*- coding: utf-8 -*-
import unittest
from .base import FunctionalTestCase
from .pages import game

class StylesheetTests(FunctionalTestCase):
    def test_color_css_loaded(self):
        self.story('Create a game')
        self.browser.get(self.live_server_url)
        page = game.Homepage(self.browser)
        page.start_button.click()

        self.assertTrue(any('css/color.css' in s.get_attribute('href')
            for s in page.stylesheets))

    def test_main_stylesheet_loaded(self):
        self.story('Load the start page')
        self.browser.get(self.live_server_url)
        page = game.Homepage(self.browser)

        self.assertTrue(any('css/main.css' in s.get_attribute('href')
            for s in page.stylesheets))

        # Test constant to see if css actually gets loaded
        self.assertEqual('rgb(55, 71, 79)',
            page.bank_cash.value_of_css_property('border-color'))
