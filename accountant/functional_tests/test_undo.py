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

    def test_can_undo_player_transfering_money_to_company(self):
        self.story('Alice is a user who has a game')
        self.browser.get(self.server_url)
        homepage = game.Homepage(self.browser)
        homepage.start_button.click()
        game_uuid = self.browser.current_url[-36:]
        self.create_player(game_uuid, 'Alice', cash=100)
        self.create_company(game_uuid, 'B&O', cash=1000)

        self.story('Alice transfers some money to the B&O')
        game_page = game.GamePage(self.browser)
        transfer_form = game.TransferForm(self.browser)
        game_page.reload_game.click()
        alice = game_page.get_players()[0]
        alice['row'].click()
        transfer_form.select_target('B&O', alice['detail'])
        transfer_form.amount(alice['detail']).send_keys('40\n')

        self.story('Verify transfer happened')
        alice = game_page.get_players()[0]
        bno = game_page.get_companies()[0]
        self.verify_player(alice, cash=60)
        self.verify_company(bno, cash=1040)
        self.assertEqual(len(game_page.log), 2)

        self.story('Click the undo button, the game state is reverted')
        game_page.undo.click()
        alice = game_page.get_players()[0]
        bno = game_page.get_companies()[0]
        self.verify_player(alice, cash=100)
        self.verify_company(bno, cash=1000)
        self.assertEqual(len(game_page.log), 1)

        self.story('Click the redo button, the transfer is done again')
        game_page.redo.click()
        alice = game_page.get_players()[0]
        bno = game_page.get_companies()[0]
        self.verify_player(alice, cash=60)
        self.verify_company(bno, cash=1040)
        self.assertEqual(len(game_page.log), 2)

    def test_can_undo_company_transfering_money_to_player(self):
        self.story('Alice is a user who has a game')
        self.browser.get(self.server_url)
        homepage = game.Homepage(self.browser)
        homepage.start_button.click()
        game_uuid = self.browser.current_url[-36:]
        self.create_player(game_uuid, 'Alice', cash=100)
        self.create_company(game_uuid, 'B&O', cash=1000)

        self.story('Alice transfers some money to the B&O')
        game_page = game.GamePage(self.browser)
        transfer_form = game.TransferForm(self.browser)
        game_page.reload_game.click()
        bno = game_page.get_companies()[0]
        bno['elem'].click()
        transfer_form.select_target('Alice', bno['detail'])
        transfer_form.amount(bno['detail']).send_keys('20\n')

        self.story('Verify transfer happened')
        alice = game_page.get_players()[0]
        bno = game_page.get_companies()[0]
        self.verify_player(alice, cash=120)
        self.verify_company(bno, cash=980)
        self.assertEqual(len(game_page.log), 2)

        self.story('Click the undo button, the game state is reverted')
        game_page.undo.click()
        alice = game_page.get_players()[0]
        bno = game_page.get_companies()[0]
        self.verify_player(alice, cash=100)
        self.verify_company(bno, cash=1000)
        self.assertEqual(len(game_page.log), 1)

        self.story('Click the redo button, the transfer is done again')
        game_page.redo.click()
        alice = game_page.get_players()[0]
        bno = game_page.get_companies()[0]
        self.verify_player(alice, cash=120)
        self.verify_company(bno, cash=980)

    def test_can_undo_player_buying_share_from_ipo(self):
        self.story('Alice is a user who has a game')
        self.browser.get(self.server_url)
        homepage = game.Homepage(self.browser)
        homepage.start_button.click()
        game_uuid = self.browser.current_url[-36:]
        self.create_player(game_uuid, 'Alice', cash=100)
        self.create_company(game_uuid, 'B&O', cash=0, ipo_shares=3)

        self.story('Alice buys a share from the B&Os IPO')
        game_page = game.GamePage(self.browser)
        share_form = game.ShareForm(self.browser)
        game_page.reload_game.click()
        bno = game_page.get_companies()[0]
        bno.set_value(10)
        alice = game_page.get_players()[0]
        alice['row'].click()
        share_form.select_company('B&O', alice['detail'])
        share_form.select_source('ipo', alice['detail'])
        share_form.shares(alice['detail']).clear()
        share_form.shares(alice['detail']).send_keys('2\n')

        self.story('Verify that Alice bought the share')
        bno = game_page.get_companies()[0]
        alice = game_page.get_players()[0]
        self.verify_player(alice, cash=80, shares=['B&O 20%'])
        self.verify_company(bno, cash=0, ipo_shares=1, bank_shares=0)
        self.assertEqual(game_page.bank_cash.text, '12020')
        self.assertEqual(len(game_page.log), 2)

        self.story('Click the undo button, the game state is reverted')
        game_page.undo.click()
        bno = game_page.get_companies()[0]
        alice = game_page.get_players()[0]
        self.verify_player(alice, cash=100, shares=[])
        self.verify_company(bno, cash=0, ipo_shares=3, bank_shares=0)
        self.assertEqual(game_page.bank_cash.text, '12000')
        self.assertEqual(len(game_page.log), 1)

        self.story('Click the redo button, the transfer is done again')
        game_page.redo.click()
        bno = game_page.get_companies()[0]
        alice = game_page.get_players()[0]
        self.verify_player(alice, cash=80, shares=['B&O 20%'])
        self.verify_company(bno, cash=0, ipo_shares=1, bank_shares=0)
        self.assertEqual(game_page.bank_cash.text, '12020')
        self.assertEqual(len(game_page.log), 2)

    def test_can_undo_company_buying_share_from_bank(self):
        self.story('Alice is a user who has a game')
        self.browser.get(self.server_url)
        homepage = game.Homepage(self.browser)
        homepage.start_button.click()
        game_uuid = self.browser.current_url[-36:]
        self.create_company(game_uuid, 'CPR', cash=0, bank_shares=5,
            ipo_shares=5)
        self.create_company(game_uuid, 'B&M', cash=100)

        self.story('B&M buys a share of CPR from the bank')
        game_page = game.GamePage(self.browser)
        share_form = game.ShareForm(self.browser)
        game_page.reload_game.click()
        bm, cpr = game_page.get_companies()
        cpr.set_value(20)
        bm['elem'].click()
        share_form.select_company('CPR', bm['detail'])
        share_form.select_source('bank', bm['detail'])
        share_form.shares(bm['detail']).clear()
        share_form.shares(bm['detail']).send_keys('4\n')

        self.story('Verify that shares have been bought')
        bm, cpr = game_page.get_companies()
        self.verify_company(cpr, cash=0, ipo_shares=5, bank_shares=1)
        self.verify_company(bm, cash=20, shares=['CPR 40%'])
        self.assertEqual(game_page.bank_cash.text, '12080')
        self.assertEqual(len(game_page.log), 2)

        self.story('Click the undo button, the game state is reverted')
        game_page.undo.click()
        bm, cpr = game_page.get_companies()
        self.verify_company(cpr, cash=0, ipo_shares=5, bank_shares=5)
        self.verify_company(bm, cash=100, shares=[])
        self.assertEqual(game_page.bank_cash.text, '12000')

        self.story('Click the redo button, the transfer is done again')
        game_page.redo.click()
        bm, cpr = game_page.get_companies()
        self.verify_company(cpr, cash=0, ipo_shares=5, bank_shares=1)
        self.verify_company(bm, cash=20, shares=['CPR 40%'])
        self.assertEqual(game_page.bank_cash.text, '12080')
        self.assertEqual(len(game_page.log), 2)

    def test_can_undo_player_buying_share_from_company_treasury(self):
        self.story('Alice is a user who has a game')
        self.browser.get(self.server_url)
        homepage = game.Homepage(self.browser)
        homepage.start_button.click()
        game_uuid = self.browser.current_url[-36:]
        self.create_player(game_uuid, 'Alice', cash=300)
        co_uuid = self.create_company(game_uuid, 'C&O', cash=0, bank_shares=0,
            ipo_shares=0)
        self.create_company_share(co_uuid, co_uuid, shares=10)

        self.story('Alice buys a share C&O from the C&O')
        game_page = game.GamePage(self.browser)
        share_form = game.ShareForm(self.browser)
        game_page.reload_game.click()
        alice = game_page.get_players()[0]
        co = game_page.get_companies()[0]
        co.set_value(30)
        alice['row'].click()
        share_form.select_company('C&O', alice['detail'])
        share_form.select_source('C&O', alice['detail'])
        share_form.shares(alice['detail']).clear()
        share_form.shares(alice['detail']).send_keys('6\n')

        self.story('Verify that shares have been bought')
        alice = game_page.get_players()[0]
        co = game_page.get_companies()[0]
        self.verify_player(alice, cash=120, shares=['C&O 60%'])
        self.verify_company(co, cash=180, shares=['C&O 40%'])

        self.story('Click the undo button, the game state is reverted')
        game_page.undo.click()
        alice = game_page.get_players()[0]
        co = game_page.get_companies()[0]
        self.verify_player(alice, cash=300, shares=[])
        self.verify_company(co, cash=0, shares=['C&O 100%'])

        self.story('Click the redo button, the transfer is done again')
        game_page.redo.click()
        alice = game_page.get_players()[0]
        co = game_page.get_companies()[0]
        self.verify_player(alice, cash=120, shares=['C&O 60%'])
        self.verify_company(co, cash=180, shares=['C&O 40%'])

    def test_can_undo_company_paying_dividends(self):
        self.story('Alice is a user who has a game')
        self.browser.get(self.server_url)
        homepage = game.Homepage(self.browser)
        homepage.start_button.click()
        game_uuid = self.browser.current_url[-36:]
        alice_uuid = self.create_player(game_uuid, 'Alice', cash=0)
        bob_uuid = self.create_player(game_uuid, 'Bob', cash=0)
        bo_uuid = self.create_company(game_uuid, 'B&O', cash=0, bank_shares=0,
            ipo_shares=2)
        self.create_company_share(bo_uuid, bo_uuid, shares=1)
        self.create_player_share(alice_uuid, bo_uuid, shares=4)
        self.create_player_share(bob_uuid, bo_uuid, shares=3)

        self.story('The B&O operates and pays dividends')
        game_page = game.GamePage(self.browser)
        operate_form = game.OperateForm(self.browser)
        game_page.reload_game.click()
        bo = game_page.get_companies()[0]
        bo['elem'].click()
        operate_form.revenue(bo['detail']).clear()
        operate_form.revenue(bo['detail']).send_keys('80')
        operate_form.full(bo['detail']).click()

        self.story('Verify that everyone has received money')
        alice, bob = game_page.get_players()
        bo = game_page.get_companies()[0]
        self.verify_player(alice, cash=32)
        self.verify_player(bob, cash=24)
        self.verify_company(bo, cash=8)
        self.assertEqual(game_page.bank_cash.text, '11936')

        self.story('Click the undo button, the game state is reverted')
        game_page.undo.click()
        alice, bob = game_page.get_players()
        bo = game_page.get_companies()[0]
        self.verify_player(alice, cash=0)
        self.verify_player(bob, cash=0)
        self.verify_company(bo, cash=0)
        self.assertEqual(game_page.bank_cash.text, '12000')

        self.story('Click the redo button, the operation is done again')
        game_page.redo.click()
        alice, bob = game_page.get_players()
        bo = game_page.get_companies()[0]
        self.verify_player(alice, cash=32)
        self.verify_player(bob, cash=24)
        self.verify_company(bo, cash=8)
        self.assertEqual(game_page.bank_cash.text, '11936')

    def test_can_undo_company_withholding_dividends(self):
        self.story('Alice is a user who has a game')
        self.browser.get(self.server_url)
        homepage = game.Homepage(self.browser)
        homepage.start_button.click()
        game_uuid = self.browser.current_url[-36:]
        alice_uuid = self.create_player(game_uuid, 'Alice', cash=0)
        bob_uuid = self.create_player(game_uuid, 'Bob', cash=0)
        bo_uuid = self.create_company(game_uuid, 'B&O', cash=0, bank_shares=0,
            ipo_shares=2)
        self.create_company_share(bo_uuid, bo_uuid, shares=1)
        self.create_player_share(alice_uuid, bo_uuid, shares=4)
        self.create_player_share(bob_uuid, bo_uuid, shares=3)

        self.story('The B&O operates and withholds dividends')
        game_page = game.GamePage(self.browser)
        operate_form = game.OperateForm(self.browser)
        game_page.reload_game.click()
        bo = game_page.get_companies()[0]
        bo['elem'].click()
        operate_form.revenue(bo['detail']).clear()
        operate_form.revenue(bo['detail']).send_keys('90')
        operate_form.withhold(bo['detail']).click()

        self.story('Verify that only the B&O has received money')
        alice, bob = game_page.get_players()
        bo = game_page.get_companies()[0]
        self.verify_player(alice, cash=0)
        self.verify_player(bob, cash=0)
        self.verify_company(bo, cash=90)
        self.assertEqual(game_page.bank_cash.text, '11910')

        self.story('Click the undo button, the game state is reverted')
        game_page.undo.click()
        alice, bob = game_page.get_players()
        bo = game_page.get_companies()[0]
        self.verify_player(alice, cash=0)
        self.verify_player(bob, cash=0)
        self.verify_company(bo, cash=0)
        self.assertEqual(game_page.bank_cash.text, '12000')

        self.story('Click the redo button, the withholding is done again')
        game_page.redo.click()
        alice, bob = game_page.get_players()
        bo = game_page.get_companies()[0]
        self.verify_player(alice, cash=0)
        self.verify_player(bob, cash=0)
        self.verify_company(bo, cash=90)
        self.assertEqual(game_page.bank_cash.text, '11910')

    def test_can_undo_company_paying_half_dividends(self):
        self.story('Alice is a user who has a game')
        self.browser.get(self.server_url)
        homepage = game.Homepage(self.browser)
        homepage.start_button.click()
        game_uuid = self.browser.current_url[-36:]
        alice_uuid = self.create_player(game_uuid, 'Alice', cash=0)
        bob_uuid = self.create_player(game_uuid, 'Bob', cash=0)
        bo_uuid = self.create_company(game_uuid, 'B&O', cash=0, bank_shares=0,
            ipo_shares=2)
        self.create_company_share(bo_uuid, bo_uuid, shares=1)
        self.create_player_share(alice_uuid, bo_uuid, shares=4)
        self.create_player_share(bob_uuid, bo_uuid, shares=3)

        self.story('The B&O operates and pays half dividends')
        game_page = game.GamePage(self.browser)
        operate_form = game.OperateForm(self.browser)
        game_page.reload_game.click()
        bo = game_page.get_companies()[0]
        bo['elem'].click()
        operate_form.revenue(bo['detail']).clear()
        operate_form.revenue(bo['detail']).send_keys('100')
        operate_form.half(bo['detail']).click()

        self.story('Verify that everyone received the correct amounts')
        alice, bob = game_page.get_players()
        bo = game_page.get_companies()[0]
        self.verify_player(alice, cash=20)
        self.verify_player(bob, cash=15)
        self.verify_company(bo, cash=55)
        self.assertEqual(game_page.bank_cash.text, '11910')

        self.story('Click the undo button, the game state is reverted')
        game_page.undo.click()
        alice, bob = game_page.get_players()
        bo = game_page.get_companies()[0]
        self.verify_player(alice, cash=0)
        self.verify_player(bob, cash=0)
        self.verify_company(bo, cash=0)
        self.assertEqual(game_page.bank_cash.text, '12000')

        self.story('Click the redo button, the split payment is done again')
        game_page.redo.click()
        alice, bob = game_page.get_players()
        bo = game_page.get_companies()[0]
        self.verify_player(alice, cash=20)
        self.verify_player(bob, cash=15)
        self.verify_company(bo, cash=55)
        self.assertEqual(game_page.bank_cash.text, '11910')

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

    def test_undo_button_disabled_when_action_cant_be_undone(self):
        self.story('Alice is a user who has a game')
        self.browser.get(self.server_url)
        homepage = game.Homepage(self.browser)
        homepage.start_button.click()

        self.story("The game creating can't be undone")
        game_page = game.GamePage(self.browser)
        self.assertFalse(game_page.undo.is_enabled())

        self.story("Can't undo player creation")
        game_page.add_player_link.click()
        add_player = game.AddPlayerPage(self.browser)
        add_player.name.send_keys('Alice\n')
        self.assertFalse(game_page.undo.is_enabled())

        self.story("Can't undo company creation")
        game_page.add_company_link.click()
        add_company = game.AddCompanyPage(self.browser)
        add_company.name.send_keys('B&M\n')
        self.assertFalse(game_page.undo.is_enabled())

        self.story("Can't undo editing a company")
        bm = game_page.get_companies()[0]
        bm['elem'].click()
        bm['edit'].click()
        edit_company = game.EditCompanyPage(self.browser)
        edit_company.name.clear()
        edit_company.name.send_keys('CPR\n')
        self.assertFalse(game_page.undo.is_enabled())
