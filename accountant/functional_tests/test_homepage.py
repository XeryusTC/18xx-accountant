# -*- coding: utf-8 -*-
from .base import FunctionalTestCase
from .pages import game

class HomePageTest(FunctionalTestCase):
    def test_loads_angular_app(self):
        self.story('Alice is a user who visits the website')
        self.browser.get(self.server_url)

        self.story('There is an angular root element in the DOM')
        page = game.Homepage(self.browser)
        self.assertIsNotNone(page.app_root)
        self.assertTrue(
            page.app_root.get_attribute('ng-version').startswith('4.4'))

    def test_create_game(self):
        self.story('Alice is a user who visits the website')
        self.browser.get(self.server_url)
        self.story('She sees that the title of the browser contains "18xx '
            'Accountant"')
        self.assertEqual(self.browser.title, '18xx Accountant')

        self.story('There is a button that says "Start new game", she clicks '
            'it')
        page = game.Homepage(self.browser)
        self.assertEqual(page.start_button.text.lower(), 'start new game')
        page.start_button.click()

        self.story('She lands on a new page')
        self.assertRegex(self.browser.current_url, r'/game/([^/]+)$')
        self.assertEqual(self.browser.title, '18xx Accountant')

    def test_create_game_with_bank_size(self):
        self.story('Alice is a user who visits the website')
        self.browser.get(self.server_url)

        self.story('She wants to start a new game with a bank of 9000')
        page = game.Homepage(self.browser)
        page.bank_cash.clear()
        page.bank_cash.send_keys('9000\n')

        self.story('She lands on the game page, it says that the bank size is '
            '9000')
        self.assertRegex(self.browser.current_url, r'/game/([^/]+)$')
        game_page = game.GamePage(self.browser)
        self.assertEqual(game_page.bank_cash.text, '9000')

    def test_gives_error_on_non_existent_game(self):
        self.story('Alice is a user who requests a non existing game')
        self.browser.get(self.server_url + \
                '/game/000000000000-0000-0000-0000-00000000')

        self.story('There is a box overlaying the page that shows an error')
        error_page = game.ErrorPage(self.browser)
        self.assertGreater(len(error_page.errors), 0)
        self.assertEqual(error_page.errors[0].text,
            'Game not found. Return to home page.')

        self.story('Clicking the close button closes the error display')
        error_page.close.click()
        self.assertEqual(error_page.errors, [])
