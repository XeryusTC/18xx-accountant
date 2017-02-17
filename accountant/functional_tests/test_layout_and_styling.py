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

    def test_main_stylesheet_loaded(self):
        # Load the start page
        self.browser.get(self.live_server_url)
        page = game.Homepage(self.browser)

        self.assertTrue(any('style.css' in s.get_attribute('href')
            for s in page.stylesheets))


class JavascriptTests(FunctionalTestCase):
    def test_jquery_loaded(self):
        # Go to the company creation page
        self.browser.get(self.live_server_url)
        homepage = game.Homepage(self.browser)
        homepage.start_button.click()
        game_page = game.GamePage(self.browser)
        game_page.add_company_link.click()

        self.assertTrue(any('jquery' in s.get_attribute('src')
            for s in homepage.scripts))

    def test_game_js_loaded(self):
        # Go to the company creation page
        self.browser.get(self.live_server_url)
        homepage = game.Homepage(self.browser)
        homepage.start_button.click()

        # game.js should be loaded on the main game page
        self.assertTrue(any('static/game.js' in s.get_attribute('src')
            for s in homepage.scripts))

        game_page = game.GamePage(self.browser)
        game_page.add_company_link.click()

        # game.js should be loaded on the add company page
        self.assertTrue(any('static/game.js' in s.get_attribute('src')
            for s in homepage.scripts))
