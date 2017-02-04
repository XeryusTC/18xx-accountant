# -*- coding: utf-8 -*-
import unittest
from .base import FunctionalTestCase
from .pages import game

class HomePageTest(FunctionalTestCase):
    def test_create_game(self):
        # Alice is a user who visits the website
        self.browser.get(self.live_server_url)
        # She sees that the title of the browser contains '18xx Accountant'
        self.assertEqual(self.browser.title, '18xx Accountant')

        # There is a button that says "Start new game", she clicks it
        page = game.Homepage(self.browser)
        self.assertEqual(page.start_button.text, 'Start new game')
        page.start_button.click()

        # She lands on a new page, it lists a code for the game name
        self.assertIn('/en/game/', self.browser.current_url)

    def test_create_game_with_bank_size(self):
        # Alice is a user who visits the website
        self.browser.get(self.live_server_url)

        # She wants to start a new game with a bank of 9000
        page = game.Homepage(self.browser)
        page.bank_cash.clear()
        page.bank_cash.send_keys('9000\n')

        # She lands on the game page, it says that the bank size is 9000
        self.assertIn('/en/game/', self.browser.current_url)
        game_page = game.GamePage(self.browser)
        self.assertEqual(game_page.bank_cash.text, '9000')
