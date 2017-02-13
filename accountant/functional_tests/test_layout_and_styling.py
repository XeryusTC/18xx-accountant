# -*- coding: utf-8 -*-
from .base import FunctionalTestCase
from .pages import game

class StylesheetTests(FunctionalTestCase):
    def test_modestgrid_loaded(self):
        # Load the start page
        self.browser.get(self.live_server_url)
        page = game.Homepage(self.browser)

        self.assertTrue(any('modestgrid.css' in s.get_attribute('href')
            for s in page.stylesheets))

    def test_color_css_loaded(self):
        # Create a game
        self.browser.get(self.live_server_url)
        page = game.Homepage(self.browser)
        page.start_button.click()

        self.assertTrue(any('color.css' in s.get_attribute('href')
            for s in page.stylesheets))
