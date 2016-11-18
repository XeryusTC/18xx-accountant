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
