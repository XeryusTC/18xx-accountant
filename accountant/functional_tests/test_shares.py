# -*- coding: utf-8 -*-
from .base import FunctionalTestCase
from .pages import game

class BuyShareTests(FunctionalTestCase):
    def test_player_can_buy_shares_from_company_ipo(self):
        self.story('Start a game with a player and a company')
        game_uuid = self.create_game()
        self.create_player(game_uuid, 'Alice', cash=1000)
        self.create_company(game_uuid, 'NYC', text='amber-200',
            background='brown-300')
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

        self.story('Confirm cash and share amounts')
        player = game_page.get_players()[0]
        company = game_page.get_companies()[0]
        self.assertEqual(game_page.bank_cash.text, '12000')
        self.assertEqual(player['cash'].text, '1000')
        self.assertEqual(company['cash'].text, '0')
        self.assertEqual(len(player['shares']), 0)
        self.assertEqual(company['ipo_shares'].text, '10')

        self.story('Set the value of the NYC')
        company['value'].clear()
        company['value'].send_keys('90')

        self.story("Open Alice's detail section, there is a buy share form")
        player['row'].click()
        player = game_page.get_players()[0]
        share_form = game.ShareForm(self.browser)
        self.assertEqual('1',
            share_form.shares(player['detail']).get_attribute('value'))
        share_form.shares(player['detail']).clear()
        share_form.shares(player['detail']).send_keys('3')
        for label in share_form.company(player['detail']):
            if label.get_attribute('for') == 'company-NYC':
                self.assertIn('fg-amber-200', label.get_attribute('class'))
                self.assertIn('bg-brown-300', label.get_attribute('class'))
                label.click()
                break
        else: # pragma: no cover
            self.fail('No company called NYC found in share list')

        self.story('Buy the share from the IPO')
        for label in share_form.source(player['detail']):
            if label.get_attribute('for') == 'source-ipo':
                label.click()
                break
        else: # pragma: no cover
            self.fail('There are no shares in the IPO')
        share_form.transfer_button(player['detail']).click()

        self.story('The page reloads and money and shares have changed hands')
        player = game_page.get_players()[0]
        company = game_page.get_companies()[-1]
        self.assertEqual(game_page.bank_cash.text, '12270')
        self.assertEqual(player['cash'].text, '730')
        self.assertEqual(company['cash'].text, '0')
        self.assertEqual(len(player['shares']), 1)
        self.assertEqual(player['shares'][0].text, 'NYC 30%')
        self.assertIn('fg-amber-200',
            player['shares'][0].get_attribute('class'))
        self.assertIn('bg-brown-300',
            player['shares'][0].get_attribute('class'))
        self.assertEqual(company['ipo_shares'].text, '7')

    def test_player_can_buy_shares_from_bank_pool(self):
        self.story('Start a game with a player and a company')
        game_uuid = self.create_game()
        self.create_player(game_uuid, 'Alice', cash=1000)
        self.create_company(game_uuid, 'RDR', text='yellow-800',
            background='green-600', bank_shares=5)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

        self.story('Confirm cash and share amounts')
        player = game_page.get_players()[0]
        company = game_page.get_companies()[0]
        self.assertEqual(game_page.bank_cash.text, '12000')
        self.assertEqual(player['cash'].text, '1000')
        self.assertEqual(company['cash'].text, '0')
        self.assertEqual(len(player['shares']), 0)
        self.assertEqual(company['bank_shares'].text, '5')

        self.story('Set the value of the RDR')
        company['value'].clear()
        company['value'].send_keys(60)

        self.story("Open Alice's detail section, there is a buy share form")
        player['row'].click()
        player = game_page.get_players()[0]
        share_form = game.ShareForm(self.browser)
        share_form.shares(player['detail']).clear()
        share_form.shares(player['detail']).send_keys('4')
        for label in share_form.company(player['detail']):
            if label.get_attribute('for') == 'company-RDR':
                self.assertIn('fg-yellow-800', label.get_attribute('class'))
                self.assertIn('bg-green-600', label.get_attribute('class'))
                label.click()
                break
        else: # pragma: no cover
            self.fail('No company called PMQ found in share list')

        self.story('Select the bank as a source')
        for label in share_form.source(player['detail']):
            if label.get_attribute('for') == 'source-bank':
                label.click()
                break
        else: # pragma: no cover
            self.fail('There is no option to set the bank as the source')
        share_form.transfer_button(player['detail']).click()

        self.story('The page reloads and money and shares have changed hands')
        player = game_page.get_players()[0]
        company = game_page.get_companies()[0]
        self.assertEqual(game_page.bank_cash.text, '12240')
        self.assertEqual(player['cash'].text, '760')
        self.assertEqual(company['cash'].text, '0')
        self.assertEqual(len(player['shares']), 1)
        self.assertEqual(player['shares'][0].text, 'RDR 40%')
        self.assertIn('fg-yellow-800',
            player['shares'][0].get_attribute('class'))
        self.assertIn('bg-green-600',
            player['shares'][0].get_attribute('class'))
        self.assertEqual(company['bank_shares'].text, '1')

    def test_player_can_buy_shares_from_company_treasury(self):
        self.story('Start with a player and a company with treasury shares')
        game_uuid = self.create_game()
        self.create_player(game_uuid, 'Alice', cash=1500)
        company_uuid = self.create_company(game_uuid, 'C&O',
            text='blue-300', background='yellow-300', ipo_shares=0, cash=100)
        self.create_company_share(company_uuid, company_uuid, shares=10)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

        self.story('Confirm cash and share amounts')
        player = game_page.get_players()[0]
        company = game_page.get_companies()[0]
        self.assertEqual(game_page.bank_cash.text, '12000')
        self.assertEqual(player['cash'].text, '1500')
        self.assertEqual(company['cash'].text, '100')
        self.assertEqual(len(player['shares']), 0)
        self.assertEqual(len(company['shares']), 1)
        self.assertEqual(company['shares'][0].text, 'C&O 100%')

        self.story('Set the value of the C&O')
        company = game_page.get_companies()[0]
        company['value'].clear()
        company['value'].send_keys(20)

        self.story("Open Alice's detail section, buy shares C&O from the C&O")
        player = game_page.get_players()[0]
        player['row'].click()
        player = game_page.get_players()[0] # Get DOM updates
        share_form = game.ShareForm(self.browser)
        share_form.shares(player['detail']).clear()
        share_form.shares(player['detail']).send_keys('2')
        for label in share_form.company(player['detail']):
            if label.get_attribute('for') == 'company-C&O':
                label.click()
                break
        else: # pragma: no cover
            self.fail('No company called C&O found in share list')

        self.story('Select the C&O as the source')
        for label in share_form.source(player['detail']):
            if label.get_attribute('for') == 'source-C&O':
                self.assertIn('fg-blue-300', label.get_attribute('class'))
                self.assertIn('bg-yellow-300', label.get_attribute('class'))
                label.click()
                break
        else: # pragma: no cover
            self.fail('There is no option to set the C&O as the source')
        share_form.transfer_button(player['detail']).click()

        self.story('The page reloads and money and shares have changed hands')
        player = game_page.get_players()[0]
        company = game_page.get_companies()[0]
        self.assertEqual(game_page.bank_cash.text, '12000')
        self.assertEqual(player['cash'].text, '1460')
        self.assertEqual(company['cash'].text, '140')
        self.assertEqual(len(player['shares']), 1)
        self.assertEqual(player['shares'][0].text, 'C&O 20%')
        self.assertIn('fg-blue-300',
            player['shares'][0].get_attribute('class'))
        self.assertIn('bg-yellow-300',
            player['shares'][0].get_attribute('class'))
        self.assertEqual(len(company['shares']), 1)
        self.assertEqual(company['shares'][0].text, 'C&O 80%')

    def test_company_can_buy_shares_from_own_ipo(self):
        self.story('Create a game with a company')
        game_uuid = self.create_game()
        self.create_company(game_uuid, 'CPR', cash=100,
        text='red-500', background='black', ipo_shares=10)
        self.browser.get(self.server_url + '/game/' + game_uuid)

        game_page = game.GamePage(self.browser)
        share_form = game.ShareForm(self.browser)

        self.story('Set the value of the CPR')
        company = game_page.get_companies()[0]
        company['value'].clear()
        company['value'].send_keys(20)

        self.story('The CPR buys a share from its own IPO')
        company['elem'].click()
        company = game_page.get_companies()[0]
        share_form.shares(company['detail']).clear()
        share_form.shares(company['detail']).send_keys('3')
        for label in share_form.company(company['detail']):
            if label.get_attribute('for') == 'company-CPR':
                self.assertIn('fg-red-500', label.get_attribute('class'))
                self.assertIn('bg-black', label.get_attribute('class'))
                label.click()
                break
        else: # pragma: no cover
            self.fail('Cannot find the CPR in the list of companies')

        self.story('Select the IPO as the source')
        for label in share_form.source(company['detail']):
            if label.get_attribute('for') == 'source-ipo':
                label.click()
                break
        else: # pragma: no cover
            self.fail('There are no shares in the IPO?')
        share_form.transfer_button(company['detail']).click()

        self.story('The page reloads and shares have been bought')
        company = game_page.get_companies()[0]
        self.assertEqual(game_page.bank_cash.text, '12060')
        self.assertEqual(company['cash'].text, '40')
        self.assertEqual(len(company['shares']), 1)
        self.assertEqual(company['shares'][0].text, 'CPR 30%')
        self.assertIn('fg-red-500',
            company['shares'][0].get_attribute('class'))
        self.assertIn('bg-black', company['shares'][0].get_attribute('class'))

    def test_company_can_buy_own_shares_from_bank_pool(self):
        self.story('Create a game with a company with shares in the pool')
        game_uuid = self.create_game()
        self.create_company(game_uuid, 'B&M', text='red-900',
            background='amber-400', bank_shares=5, cash=500)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)
        share_form = game.ShareForm(self.browser)

        self.story('Set the value of the B&M')
        company = game_page.get_companies()[0]
        company['value'].clear()
        company['value'].send_keys(40)

        self.story("Open the B&M's detail section, buy the pool shares")
        company['elem'].click()
        company = game_page.get_companies()[0]
        share_form.shares(company['detail']).clear()
        share_form.shares(company['detail']).send_keys('5')
        for label in share_form.company(company['detail']):
            if label.get_attribute('for') == 'company-B&M':
                self.assertIn('fg-red-900', label.get_attribute('class'))
                self.assertIn('bg-amber-400', label.get_attribute('class'))
                label.click()
                break
        else: # pragma: no cover
            self.fail('Could not find the B&M in the list of shares')
        for label in share_form.source(company['detail']):
            if label.get_attribute('for') == 'source-bank':
                label.click()
                break
        else: # pragma: no cover
            self.fail('There is no option to buy from the bank')
        share_form.transfer_button(company['detail']).click()

        self.story('The page updates and money and shares have moved')
        company = game_page.get_companies()[0]
        self.assertEqual(game_page.bank_cash.text, '12200')
        self.assertEqual(company['cash'].text, '300')
        self.assertEqual(len(company['shares']), 1)
        self.assertEqual(company['shares'][0].text, 'B&M 50%')
        self.assertIn('fg-red-900',
            company['shares'][0].get_attribute('class'))
        self.assertIn('bg-amber-400',
            company['shares'][0].get_attribute('class'))

    def test_company_can_buy_shares_from_other_company_ipo(self):
        self.story('Create a game with two companies')
        game_uuid = self.create_game()
        self.create_company(game_uuid, 'buy', cash=1000)
        self.create_company(game_uuid, 'share', text='red-500',
            background='green-500', ipo_shares=10, cash=0)
        self.browser.get(self.server_url + '/game/' + game_uuid)

        game_page = game.GamePage(self.browser)
        share_form = game.ShareForm(self.browser)
        buy_company, share_company = game_page.get_companies()

        self.story('Set the value of share company')
        share_company['value'].clear()
        share_company['value'].send_keys(10)

        self.story('The buy company buys a share of the other company')
        buy_company['elem'].click()
        buy_company = game_page.get_companies()[0]
        share_form.shares(buy_company['detail']).clear()
        share_form.shares(buy_company['detail']).send_keys('2')
        for label in share_form.company(buy_company['detail']):
            if label.get_attribute('for') == 'company-share':
                self.assertIn('fg-red-500', label.get_attribute('class'))
                self.assertIn('bg-green-500', label.get_attribute('class'))
                label.click()
                break
        else: # pragma: no cover
            self.fail('Cannot find the share company in available shares list')

        self.story('Select the IPO as the source')
        for label in share_form.source(buy_company['detail']):
            if label.get_attribute('for') == 'source-ipo':
                label.click()
                break
        else: # pragma: no cover
            self.fail('There are no shares in the IPO')
        share_form.transfer_button(buy_company['detail']).click()

        self.story('The page reloads and money and shares have changed hands')
        buy_company, share_company = game_page.get_companies()
        self.assertEqual(game_page.bank_cash.text, '12020')
        self.assertEqual(buy_company['cash'].text, '980')
        self.assertEqual(share_company['cash'].text, '0')
        self.assertEqual(len(buy_company['shares']), 1)
        self.assertEqual(len(share_company['shares']), 0)
        self.assertEqual(buy_company['shares'][0].text, 'share 20%')
        self.assertIn('fg-red-500',
            buy_company['shares'][0].get_attribute('class'))
        self.assertIn('bg-green-500',
            buy_company['shares'][0].get_attribute('class'))

    def test_company_can_buy_other_company_shares_from_pool(self):
        self.story('Create a game with two companies')
        game_uuid = self.create_game()
        self.create_company(game_uuid, 'buy', cash=1000)
        self.create_company(game_uuid, 'share', text='red-500',
            background='green-500', bank_shares=10, cash=0)
        self.browser.get(self.server_url + '/game/' + game_uuid)

        game_page = game.GamePage(self.browser)
        share_form = game.ShareForm(self.browser)
        buy_company, share_company = game_page.get_companies()

        self.story('Set the value of the share company')
        share_company['value'].clear()
        share_company['value'].send_keys('60')

        self.story('Buy company buys shares of the other company from pool')
        buy_company['elem'].click()
        buy_company = game_page.get_companies()[0] # Get DOM updates
        for label in share_form.company(buy_company['detail']):
            if label.get_attribute('for') == 'company-share':
                label.click()
                break
        else: # pragma: no cover
            self.fail('Cannot find the share company in available shares list')
        for label in share_form.source(buy_company['detail']):
            if label.get_attribute('for') == 'source-bank':
                label.click()
                break
        else: # pragma: no cover
            self.fail('There are no shares in the pool')
        share_form.shares(buy_company['detail']).clear()
        share_form.shares(buy_company['detail']).send_keys('3\n')


        self.story('The page updates and shares have changed hands')
        buy_company, share_company = game_page.get_companies()
        self.assertEqual(game_page.bank_cash.text, '12180')
        self.assertEqual(buy_company['cash'].text, '820')
        self.assertEqual(share_company['cash'].text, '0')
        self.assertEqual(len(buy_company['shares']), 1)
        self.assertEqual(len(share_company['shares']), 0)
        self.assertEqual(buy_company['shares'][0].text, 'share 30%')
        self.assertIn('fg-red-500',
            buy_company['shares'][0].get_attribute('class'))
        self.assertIn('bg-green-500',
            buy_company['shares'][0].get_attribute('class'))

    def test_company_can_buy_shares_from_other_company_treasury(self):
        self.story('Create a game with two companies holding shares')
        game_uuid = self.create_game(cash=12000)
        buy_uuid = self.create_company(game_uuid, 'buy', cash=1000)
        share_uuid = self.create_company(game_uuid, 'share', text='red-50',
            background='yellow-900', cash=500)
        self.create_company_share(share_uuid, buy_uuid, shares=5)
        self.create_company_share(share_uuid, share_uuid, shares=7)
        self.browser.get(self.server_url + '/game/' + game_uuid)

        game_page = game.GamePage(self.browser)
        share_form = game.ShareForm(self.browser)
        buy_company, share_company = game_page.get_companies()

        self.story('Set the value of the share company')
        share_company['value'].clear()
        share_company['value'].send_keys('70')

        self.story('Buy company buys a share of the other company from its '
            'treasury')
        buy_company['elem'].click()
        buy_company = game_page.get_companies()[0] # Get DOM updates
        for label in share_form.source(buy_company['detail']):
            if label.get_attribute('for') == 'source-share':
                label.click()
                break
        else: # pragma: no cover
            self.fail('Share company has no treasury shares')
        for label in share_form.company(buy_company['detail']):
            if label.get_attribute('for') == 'company-share':
                label.click()
                break
        else: # pragma: no cover
            self.fail('Cannot find the share company in available shares list')
        share_form.shares(buy_company['detail']).clear()
        share_form.shares(buy_company['detail']).send_keys('4\n')

        self.story('The page updates and shares have changed hands')
        buy_company, share_company = game_page.get_companies()
        self.assertEqual(game_page.bank_cash.text, '12000')
        self.assertEqual(buy_company['cash'].text, '720')
        self.assertEqual(share_company['cash'].text, '780')
        self.assertEqual(len(buy_company['shares']), 1)
        self.assertEqual(buy_company['shares'][0].text, 'share 40%')
        self.assertEqual(len(share_company['shares']), 2)
        self.assertEqual(share_company['shares'][0].text, 'buy 50%')
        self.assertEqual(share_company['shares'][1].text, 'share 30%')

        self.story('Set the value of the share company')
        buy_company['value'].clear()
        buy_company['value'].send_keys('80')

        self.story('Buy company buys one of its own shares back from the '
            'share company')
        buy_company['elem'].click()
        buy_company = game_page.get_companies()[0] # Get DOM updates
        for label in share_form.source(buy_company['detail']):
            if label.get_attribute('for') == 'source-share':
                label.click()
                break
        else: # pragma: no cover
            self.fail('Share company has no treasury shares')
        for label in share_form.company(buy_company['detail']):
            if label.get_attribute('for') == 'company-buy':
                label.click()
                break
        else: # pragma: no cover
            self.fail('Cannot find the buy company in available shares list')
        share_form.shares(buy_company['detail']).clear()
        share_form.shares(buy_company['detail']).send_keys('5\n')

        self.story('The page updates and shares have changed hands')
        buy_company, share_company = game_page.get_companies()
        self.assertEqual(game_page.bank_cash.text, '12000')
        self.assertEqual(buy_company['cash'].text, '320')
        self.assertEqual(share_company['cash'].text, '1180')
        self.assertEqual(len(buy_company['shares']), 2)
        self.assertEqual(buy_company['shares'][0].text, 'buy 50%')
        self.assertEqual(buy_company['shares'][1].text, 'share 40%')
        self.assertEqual(len(share_company['shares']), 1)
        self.assertEqual(share_company['shares'][0].text, 'share 30%')
