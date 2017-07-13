# -*- coding: utf-8 -*-
from .base import FunctionalTestCase
from .pages import game

class LogTests(FunctionalTestCase):
    """Tests for logging events"""
    def test_shows_new_game_message_on_game_creation(self):
        self.story('Alice is a user who starts a new game')
        self.browser.get(self.server_url)
        page = game.Homepage(self.browser)
        page.start_button.click()
        self.assertRegex(self.browser.current_url, r'/game/([^/]+)$')

        self.story('There is a log section, the first entry displays a new'
                   ' game started message')
        gamepage = game.GamePage(self.browser)
        self.assertRegex(gamepage.log[0].text,
            r'\[\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}\] New game started')
