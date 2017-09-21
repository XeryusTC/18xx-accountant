# -*- coding: utf-8 -*-
from .base import FunctionalTestCase
from .pages import game

DATE_REGEX = r'\[\d{1,2}-\d{1,2} \d{2}:\d{2}\] '

class UndoTests(FunctionalTestCase):
    def test_can_undo_player_transfering_money_to_bank(self):
        self.story('Alice is a user who has a game with a player')
        self.browser.get(self.server_url)
        homepage = game.Homepage(self.browser)
        homepage.bank_cash.clear()
        homepage.bank_cash.send_keys('1000\n')
        game_uuid = self.browser.current_url[-36:]
        self.create_player(game_uuid, 'Alice', cash=100)

        self.story('Alice transfers some money to the bank')
        game_page = game.GamePage(self.browser)
        game_page.reload_game.click()
        transfer_form = game.TransferForm(self.browser)
        alice = game_page.get_players()[0]
        alice['row'].click()
        transfer_form.amount(alice['detail']).send_keys('50\n')

        alice = game_page.get_players()[0]
        self.assertEqual(game_page.bank_cash.text, '1050')
        self.assertEqual(alice['cash'].text, '50')
        self.assertEqual(len(game_page.log), 2)
        self.assertRegex(game_page.log[1].text,
            DATE_REGEX + 'Alice transfered 50 to the bank')

        self.story('There is an undo button, once it is clicked the game is '
            'reverted to the previous state')
        game_page.undo.click()
        alice = game_page.get_players()[0]  # Get DOM updates
        self.assertEqual(game_page.bank_cash.text, '1000')
        self.assertEqual(alice['cash'].text, '100')
        self.assertEqual(len(game_page.log), 1)

        self.story('There is also a redo button, when that is clicked the '
            'transfer happens again')
        game_page.redo.click()
        alice = game_page.get_players()[0]  # Get DOM updates
        self.assertEqual(game_page.bank_cash.text, '1050')
        self.assertEqual(alice['cash'].text, '50')
        self.assertEqual(len(game_page.log), 2)
        self.assertRegex(game_page.log[1].text,
            DATE_REGEX + 'Alice transfered 50 to the bank')

    def test_can_undo_company_transfering_money_to_bank(self):
        self.story('Alice is a user who has a game with a company')
        self.browser.get(self.server_url)
        homepage = game.Homepage(self.browser)
        homepage.start_button.click()
        game_uuid = self.browser.current_url[-36:]
        self.create_company(game_uuid, 'B&O', cash=1000)

        self.story('The B&O transfers some money to the bank')
        game_page = game.GamePage(self.browser)
        game_page.reload_game.click()
        transfer_form = game.TransferForm(self.browser)
        bno = game_page.get_companies()[0]
        bno['elem'].click()
        transfer_form.amount(bno['detail']).send_keys('30\n')

        bno = game_page.get_companies()[0]
        self.assertEqual(game_page.bank_cash.text, '12030')
        self.assertEqual(bno['cash'].text, '970')
        self.assertEqual(len(game_page.log), 2)
        self.assertRegex(game_page.log[-1].text,
            DATE_REGEX + 'B&O transfered 30 to the bank')

        self.story('Click the undo button, the game state is reverted')
        game_page.undo.click()
        bno = game_page.get_companies()[0]
        self.assertEqual(game_page.bank_cash.text, '12000')
        self.assertEqual(bno['cash'].text, '1000'),
        self.assertEqual(len(game_page.log), 1)

        self.story('Click the redo button, the transfer is done again')
        game_page.redo.click()
        bno = game_page.get_companies()[0]
        self.assertEqual(game_page.bank_cash.text, '12030')
        self.assertEqual(bno['cash'].text, '970')
        self.assertEqual(len(game_page.log), 2)
        self.assertRegex(game_page.log[-1].text,
            DATE_REGEX + 'B&O transfered 30 to the bank')

    def test_log_does_not_show_undone_log_actions(self):
        self.story('Alice is a user who has a game with a player')
        self.browser.get(self.server_url)
        homepage = game.Homepage(self.browser)
        homepage.start_button.click()
        game_uuid = self.browser.current_url[-36:]
        self.create_player(game_uuid, 'Alice', cash=100)

        self.story('Alice transfers some money to the bank')
        game_page = game.GamePage(self.browser)
        game_page.reload_game.click()
        transfer_form = game.TransferForm(self.browser)
        alice = game_page.get_players()[0]
        alice['row'].click()
        transfer_form.amount(alice['detail']).send_keys('50\n')

        self.assertEqual(len(game_page.log), 2)
        self.assertRegex(game_page.log[-1].text,
            DATE_REGEX + 'Alice transfered 50 to the bank')

        self.story('Click the undo button, an item is removed from the log')
        game_page.undo.click()
        self.assertEqual(len(game_page.log), 1)
        self.assertRegex(game_page.log[-1].text,
            DATE_REGEX + 'New game started')

        self.story('Soft reload the page, the undone item is still not shown')
        game_page.reload_game.click()
        self.assertEqual(len(game_page.log), 1)
        self.assertRegex(game_page.log[-1].text,
            DATE_REGEX + 'New game started')

        self.story('Hard refresh the page, the undone item is still not shown')
        self.browser.refresh()
        self.assertEqual(len(game_page.log), 1)
        self.assertRegex(game_page.log[-1].text,
            DATE_REGEX + 'New game started')

        self.story('Click the redo button, the undone item is shown again')
        game_page.redo.click()
        self.assertEqual(len(game_page.log), 2)
        self.assertRegex(game_page.log[-1].text,
            DATE_REGEX + 'Alice transfered 50 to the bank')

        self.story('Soft reload the page, the item is still there')
        game_page.reload_game.click()
        self.assertEqual(len(game_page.log), 2)
        self.assertRegex(game_page.log[-1].text,
            DATE_REGEX + 'Alice transfered 50 to the bank')

        self.story('Hard refresh the page, the item is still visible')
        self.browser.refresh()
        self.assertEqual(len(game_page.log), 2)
        self.assertRegex(game_page.log[-1].text,
            DATE_REGEX + 'Alice transfered 50 to the bank')
