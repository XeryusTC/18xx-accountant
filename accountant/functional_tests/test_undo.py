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
