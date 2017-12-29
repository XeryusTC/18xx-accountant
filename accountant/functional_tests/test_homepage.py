# -*- coding: utf-8 -*-
from .base import FunctionalTestCase
from .pages import game

DATE_REGEX = r'\[\d{1,2}-\d{1,2} \d{2}:\d{2}\] '

class HomePageTest(FunctionalTestCase):
    def test_loads_angular_app(self):
        self.story('Alice is a user who visits the website')
        self.browser.get(self.server_url)

        self.story('There is an angular root element in the DOM')
        page = game.Homepage(self.browser)
        self.assertIsNotNone(page.app_root)
        self.assertTrue(
            page.app_root.get_attribute('ng-version').startswith('5.1'))

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
        self.browser.get(self.server_url +
                '/game/000000000000-0000-0000-0000-00000000')

        self.story('There is a box overlaying the page that shows an error')
        error_page = game.ErrorPage(self.browser)
        self.assertGreater(len(error_page.errors), 0)
        self.assertEqual(error_page.errors[0].text,
            'Game not found. Return to home page.')

        self.story('Clicking the close button closes the error display')
        error_page.close.click()
        self.assertEqual(error_page.errors, [])

    def test_can_soft_reload_game(self):
        self.story('Alice is a user who has a game')
        game_uuid = self.create_game()
        self.browser.get(self.server_url + '/game/' + game_uuid)
        alice_window = self.browser.current_window_handle

        self.story("Bob is another user who joins Alice's game")
        self.browser.execute_script(
            'window.open("{}/game/{}")'.format(self.server_url, game_uuid))
        bob_window = self.browser.window_handles[-1]

        self.story('Alice adds herself to the game')
        gamepage = game.GamePage(self.browser)
        add_player = game.AddPlayerPage(self.browser)
        gamepage.add_player_link.click()
        add_player.name.send_keys('Alice\n')

        self.story("Alice's game page shows her, but Bob's doesn't")
        self.assertEqual(['Alice'],
            [player.text for player in gamepage.player_name_list])
        # Bob's window
        self.browser.switch_to.window(bob_window)
        self.assertEqual(gamepage.player_name_list, [])

        self.story('Bob clicks a Reload button at the top of the page, '
            'Alice appears in the player list')
        gamepage.reload_game.click()
        self.assertRegex(gamepage.log[0].text,
            DATE_REGEX + 'Added player Alice with 0 starting cash')
        # Alice's window
        self.browser.switch_to_window(alice_window)
        self.assertEqual(['Alice'],
            [player.text for player in gamepage.player_name_list])

        self.story('Bob adds a company to the game')
        # Bob's window
        self.browser.switch_to.window(bob_window)
        gamepage.add_company_link.click()
        add_company = game.AddCompanyPage(self.browser)
        add_company.name.send_keys('NNH\n')

        self.story("Bob's game page shows the NNH, but Alice's doesn't")
        self.assertEqual(len(gamepage.get_companies()), 1)
        self.assertEqual(gamepage.get_companies()[0]['name'].text, 'NNH')
        # Alice's window
        self.browser.switch_to_window(alice_window)
        self.assertEqual(len(gamepage.get_companies()), 0)

        self.story('When Alice clicks her reload button the NNH shows up')
        gamepage.reload_game.click()
        self.assertEqual(len(gamepage.get_companies()), 1)
        self.assertEqual(gamepage.get_companies()[0]['name'].text, 'NNH')
        self.assertRegex(gamepage.log[0].text,
            DATE_REGEX + 'Added 10-share company NNH with 0 starting cash')
