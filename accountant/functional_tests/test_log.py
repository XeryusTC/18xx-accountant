# -*- coding: utf-8 -*-
from .base import FunctionalTestCase
from .pages import game

DATE_REGEX = r'\[\d{1,2}-\d{1,2} \d{2}:\d{2}\] '

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
            DATE_REGEX + 'New game started')

    def test_creating_player_adds_entry_to_log(self):
        self.story('Alice is a user who starts a new game')
        self.browser.get(self.server_url)
        homepage = game.Homepage(self.browser)
        homepage.start_button.click()

        self.story('She continues to create a new player')
        game_page = game.GamePage(self.browser)
        game_page.add_player_link.click()
        add_player = game.AddPlayerPage(self.browser)
        add_player.name.send_keys('Alice')
        add_player.cash.send_keys('250\n')

        self.story('She returns to the game page and sees that an extra item '
                   'has been added to the log')
        self.assertEqual(len(game_page.log), 2)
        self.assertRegex(game_page.log[-1].text,
            DATE_REGEX + 'Added player Alice with 250 starting cash')

    def test_creating_company_adds_entry_to_log(self):
        self.story('Alice is a user who starts a new game')
        self.browser.get(self.server_url)
        homepage = game.Homepage(self.browser)
        homepage.start_button.click()

        self.story('She continues to create a new company')
        game_page = game.GamePage(self.browser)
        game_page.add_company_link.click()
        add_company = game.AddCompanyPage(self.browser)
        add_company.name.send_keys('B&O')
        add_company.cash.send_keys('820')
        add_company.shares.clear()
        add_company.shares.send_keys('4\n')

        self.story('She returns to the game page and sees that an extra item '
                   'has been added to the log')
        self.assertEqual(len(game_page.log), 2)
        self.assertRegex(game_page.log[-1].text,
            DATE_REGEX + 'Added 4-share company B&O with 820 starting cash')

    def test_transfering_money_from_player_to_bank_adds_log_entry(self):
        self.story('Alice is a user who starts a new game')
        game_uuid = self.create_game(cash=1000)
        self.create_player(game_uuid, 'Alice', cash=1000)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)
        self.assertEqual(len(game_page.log), 0)

        self.story('Alice opens her player section and transfers money to '
                   'the bank (which is the default)')
        transfer_form = game.TransferForm(self.browser)
        player = game_page.get_players()[0]
        player['row'].click()
        transfer_form.amount(player['detail']).clear()
        transfer_form.amount(player['detail']).send_keys('50\n')

        self.story('The page reloads and she sees money has changed hands')
        player = game_page.get_players()[0]
        self.assertEqual(player['cash'].text, '950')

        self.story('There is also a new entry in the log (no initial entry)')
        self.assertEqual(len(game_page.log), 1)
        self.assertRegex(game_page.log[0].text,
            DATE_REGEX + 'Alice transfered 50 to the bank')

    def test_transfering_money_from_player_to_player_adds_log_entry(self):
        self.story('Alice is a user who starts a new game')
        game_uuid = self.create_game()
        self.create_player(game_uuid, 'Alice', cash=1000)
        self.create_player(game_uuid, 'Bob', cash=1000)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)
        self.assertEqual(len(game_page.log), 0)

        self.story('Alice opens her player section and transfers money to Bob')
        transfer_form = game.TransferForm(self.browser)
        alice = game_page.get_players()[0]
        alice['row'].click()
        transfer_form.select_target('Bob', alice['detail'])
        transfer_form.amount(alice['detail']).send_keys('60\n')

        self.story('There is an entry in the log')
        self.assertEqual(len(game_page.log), 1)
        self.assertRegex(game_page.log[0].text,
            DATE_REGEX + 'Alice transfered 60 to Bob')

    def test_transfering_money_from_player_to_company_adds_log_entry(self):
        self.story('Alice is a user who starts a new game')
        game_uuid = self.create_game()
        self.create_player(game_uuid, 'Alice', cash=1000)
        self.create_company(game_uuid, 'NNH', cash=0)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)
        self.assertEqual(len(game_page.log), 0)

        self.story('Alice opens her player section and transfers money to NNH')
        transfer_form = game.TransferForm(self.browser)
        alice = game_page.get_players()[0]
        alice['row'].click()
        transfer_form.select_target('NNH', alice['detail'])
        transfer_form.amount(alice['detail']).send_keys('70\n')

        self.story('The page updates and there is an entry in the log')
        self.assertEqual(len(game_page.log), 1)
        self.assertRegex(game_page.log[0].text,
            DATE_REGEX + 'Alice transfered 70 to NNH')

    def test_transfering_money_from_company_to_bank_adds_log_entry(self):
        self.story('Alice is a user who starts a new game')
        game_uuid = self.create_game()
        self.create_company(game_uuid, 'B&M', cash=1000)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)
        self.assertEqual(len(game_page.log), 0)

        self.story('Alice opens the B&M and transfers money to the bank')
        transfer_form = game.TransferForm(self.browser)
        company = game_page.get_companies()[0]
        company['elem'].click()
        transfer_form.amount(company['detail']).send_keys('80\n')

        self.story('The page reloads and there is a new log entry')
        self.assertEqual(len(game_page.log), 1)
        self.assertRegex(game_page.log[0].text,
            DATE_REGEX + 'B&M transfered 80 to the bank')

    def test_transfering_money_from_company_to_company_adds_log_entry(self):
        self.story('Alice is a user who starts a new game')
        game_uuid = self.create_game()
        self.create_company(game_uuid, 'NNH', cash=1000)
        self.create_company(game_uuid, 'NYC', cash=1000)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)
        self.assertEqual(len(game_page.log), 0)

        self.story('Alice opens the NNH and transfers money to the bank')
        transfer_form = game.TransferForm(self.browser)
        company = game_page.get_companies()[0]
        company['elem'].click()
        transfer_form.select_target('NYC', company['detail'])
        transfer_form.amount(company['detail']).send_keys('90\n')

        self.story('The page updates and there is an entry in the log')
        self.assertEqual(len(game_page.log), 1)
        self.assertRegex(game_page.log[0].text,
            DATE_REGEX + 'NNH transfered 90 to NYC')

    def test_transfering_money_from_company_to_player_adds_log_entry(self):
        self.story('Alice is a user who starts a new game')
        game_uuid = self.create_game()
        self.create_player(game_uuid, 'Alice', cash=1000)
        self.create_company(game_uuid, 'PRR', cash=0)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)
        self.assertEqual(len(game_page.log), 0)

        self.story('Alice opens PRR section and transfers money to herself')
        transfer_form = game.TransferForm(self.browser)
        company = game_page.get_companies()[0]
        company['elem'].click()
        transfer_form.select_target('Alice', company['detail'])
        transfer_form.amount(company['detail']).send_keys('100\n')

        self.story('The page updates and there is an entry in the log')
        self.assertEqual(len(game_page.log), 1)
        self.assertRegex(game_page.log[0].text,
            DATE_REGEX + 'PRR transfered 100 to Alice')

    def test_player_buying_share_from_IPO_adds_log_entry(self):
        self.story('Alice is a user who starts a new game')
        game_uuid = self.create_game()
        self.create_player(game_uuid, 'Alice', cash=1000)
        self.create_company(game_uuid, 'C&O', cash=1000)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)
        self.assertEqual(len(game_page.log), 0)

        self.story('Set the value of the C&O')
        company = game_page.get_companies()[0]
        company['value'].send_keys('10')

        self.story('Open Alices detail section, buy a share C&O')
        player = game_page.get_players()[0]
        player['row'].click()
        share_form = game.ShareForm(self.browser)
        share_form.shares(player['detail']).clear()
        share_form.shares(player['detail']).send_keys('2')
        share_form.select_company('C&O', player['detail'])
        share_form.transfer_button(player['detail']).click()

        self.story('The page updates and there is an entry in the log')
        self.assertEqual(len(game_page.log), 1)
        self.assertRegex(game_page.log[0].text,
            DATE_REGEX + 'Alice bought 2 shares C&O from the IPO for 10 each')

    def test_company_buying_share_from_pool_adds_log_entry(self):
        self.story('Alice is a user who starts a new game')
        game_uuid = self.create_game()
        self.create_company(game_uuid, 'NYC', bank_shares=5)
        self.create_company(game_uuid, 'PRR', cash=1000)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)
        self.assertEqual(len(game_page.log), 0)


        self.story('Set the value of the NYC')
        nyc, prr = game_page.get_companies()
        self.assertEqual(nyc['name'].text, 'NYC')
        nyc['value'].send_keys('20')

        self.story('Alice opens the PRRs detail section and buys NYC')
        prr['row'].click()
        share_form = game.ShareForm(self.browser)
        share_form.shares(prr['detail']).clear()
        share_form.shares(prr['detail']).send_keys('3')
        share_form.select_company('NYC', prr['detail'])
        share_form.select_source('bank', prr['detail'])
        share_form.transfer_button(prr['detail']).click()

        self.story('The page updates and there is an entry in the log')
        self.assertEqual(len(game_page.log), 1)
        self.assertRegex(game_page.log[0].text,
            DATE_REGEX + 'PRR bought 3 shares NYC from the bank for 20 each')

    def test_player_buying_share_from_company_treasury_adds_log_entry(self):
        self.story('Alice is a user who starts a new game')
        game_uuid = self.create_game()
        self.create_player(game_uuid, 'Alice', cash=1000)
        company_uuid = self.create_company(game_uuid, 'B&O', ipo_shares=0)
        self.create_company_share(company_uuid, company_uuid, shares=10)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)
        self.assertEqual(len(game_page.log), 0)

        self.story('Set the value of the B&O')
        company = game_page.get_companies()[0]
        company['value'].send_keys('30')

        self.story('Open Alices detail section, buy a share B&O')
        player = game_page.get_players()[0]
        player['row'].click()
        share_form = game.ShareForm(self.browser)
        share_form.shares(player['detail']).clear()
        share_form.shares(player['detail']).send_keys('6')
        share_form.select_company('B&O', player['detail'])
        share_form.select_source('B&O', player['detail'])
        share_form.transfer_button(player['detail']).click()

        self.story('The page updates and t here is an entry in the log')
        self.assertEqual(len(game_page.log), 1)
        self.assertRegex(game_page.log[0].text,
            DATE_REGEX + 'Alice bought 6 shares B&O from B&O for 30 each')
