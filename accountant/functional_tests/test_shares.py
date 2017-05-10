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
        self.verify_player(player, cash=1000, shares=[])
        self.verify_company(company, cash=0, ipo_shares=10)

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
        self.verify_player(player, cash=730, shares=['NYC 30%'])
        self.verify_company(company, cash=0, ipo_shares=7, bank_shares=0)
        self.assertIn('fg-amber-200',
            player['shares'][0].get_attribute('class'))
        self.assertIn('bg-brown-300',
            player['shares'][0].get_attribute('class'))

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
        self.verify_player(player, cash=1000, shares=[])
        self.verify_company(company, cash=0, bank_shares=5, ipo_shares=10)
        self.assertEqual(game_page.bank_cash.text, '12000')

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
        self.verify_player(player, cash=760, shares=['RDR 40%'])
        self.assertIn('fg-yellow-800',
            player['shares'][0].get_attribute('class'))
        self.assertIn('bg-green-600',
            player['shares'][0].get_attribute('class'))
        self.verify_company(company, cash=0, ipo_shares=10, bank_shares=1)

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
        self.verify_player(player, cash=1500, shares=[])
        self.verify_company(company, cash=100, shares=['C&O 100%'])

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
        self.verify_player(player, cash=1460, shares=['C&O 20%'])
        self.assertIn('fg-blue-300',
            player['shares'][0].get_attribute('class'))
        self.assertIn('bg-yellow-300',
            player['shares'][0].get_attribute('class'))
        self.verify_company(company, cash=140, ipo_shares=0, bank_shares=0,
            shares=['C&O 80%'])

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
        self.verify_company(company, cash=40, shares=['CPR 30%'], ipo_shares=7,
            bank_shares=0)
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
        self.verify_company(company, cash=300, shares=['B&M 50%'],
            ipo_shares=10, bank_shares=0)
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
        self.verify_company(buy_company, cash=980, shares=['share 20%'],
            ipo_shares=10, bank_shares=0)
        self.verify_company(share_company, cash=0, shares=[], ipo_shares=8,
            bank_shares=0)
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
        self.verify_company(buy_company, cash=820, shares=['share 30%'],
            ipo_shares=10, bank_shares=0)
        self.verify_company(share_company, cash=0, shares=[],
            ipo_shares=10, bank_shares=7)
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
        self.verify_company(buy_company, cash=720, shares=['share 40%'])
        self.verify_company(share_company, cash=780,
            shares=['buy 50%', 'share 30%'])

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
        self.verify_company(buy_company, cash=320,
            shares=['buy 50%', 'share 40%'])
        self.verify_company(share_company, cash=1180, shares=['share 30%'])


class SellShareTests(FunctionalTestCase):
    def test_player_can_sell_shares_to_bank_pool(self):
        self.story('Create a game with a player owning some shares')
        game_uuid = self.create_game()
        player_uuid = self.create_player(game_uuid, 'Alice', cash=0)
        company_uuid = self.create_company(game_uuid, 'CPR', text='red-500',
            background='black', cash=0, ipo_shares=0, bank_shares=0)
        self.create_player_share(player_uuid, company_uuid, shares=5)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

        self.story('The player should be the only one owning shares')
        player = game_page.get_players()[0]
        company = game_page.get_companies()[0]
        self.verify_player(player, cash=0, shares=['CPR 50%'])
        self.verify_company(company, cash=0, ipo_shares=0, bank_shares=0,
            shares=[])

        self.story('Set the value of the CPR')
        company['value'].clear()
        company['value'].send_keys('10')

        self.story('The player sells some shares')
        player['row'].click()
        player = game_page.get_players()[0]
        share_form = game.ShareForm(self.browser)
        self.assertTrue(share_form.buy_share(player['detail']).is_selected())
        share_form.sell_share(player['detail']).click()
        share_form.shares(player['detail']).clear()
        share_form.shares(player['detail']).send_keys('3')

        self.story('Select the CPR to sell it')
        for label in share_form.company(player['detail']):
            if label.get_attribute('for') == 'company-CPR':
                self.assertIn('fg-red-500', label.get_attribute('class'))
                self.assertIn('bg-black', label.get_attribute('class'))
                label.click()
                break
        else: # pragma: no cover
            self.fail('CPR is not in the owned shares list')

        self.story('Select the bank so the shares end up in there')
        for label in share_form.source(player['detail']):
            if label.get_attribute('for') == 'source-bank':
                label.click()
                break
        else: # pragma: no cover
            self.fail('Cannot select the bank to sell to')
        share_form.transfer_button(player['detail']).click()

        self.story('The page updates and shares and money have changed hands')
        player = game_page.get_players()[0]
        company = game_page.get_companies()[0]
        self.assertEqual(game_page.bank_cash.text, '11970')
        self.assertEqual(len(game_page.bank_pool), 1)
        self.assertEqual(game_page.bank_pool[0].text, 'CPR 30%')
        self.verify_player(player, cash=30, shares=['CPR 20%'])
        self.verify_company(company, ipo_shares=0, bank_shares=3, cash=0,
            shares=[])

    def test_player_can_sell_shares_to_ipo(self):
        self.story('Create a game with a player owning some shares')
        game_uuid = self.create_game()
        player_uuid = self.create_player(game_uuid, 'Bob', cash=0)
        company_uuid = self.create_company(game_uuid, 'NNH', cash=0,
            text='orange-400', background='black', ipo_shares=0,
            bank_shares=0)
        self.create_player_share(player_uuid, company_uuid, shares=9)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

        self.story('The player should be the only one owning shares')
        player = game_page.get_players()[0]
        company = game_page.get_companies()[0]
        self.verify_player(player, cash=0, shares=['NNH 90%'])
        self.verify_company(company, cash=0, ipo_shares=0, bank_shares=0,
            shares=[])

        self.story('Set the value of the NNH')
        company['value'].clear()
        company['value'].send_keys('20')

        self.story('The player sells some shares')
        player['row'].click()
        player = game_page.get_players()[0]
        share_form = game.ShareForm(self.browser)
        share_form.sell_share(player['detail']).click()
        share_form.shares(player['detail']).clear()
        share_form.shares(player['detail']).send_keys('5')

        self.story('Select the NNH to sell it')
        for label in share_form.company(player['detail']):
            if label.get_attribute('for') == 'company-NNH':
                self.assertIn('fg-orange-400', label.get_attribute('class'))
                self.assertIn('bg-black', label.get_attribute('class'))
                label.click()
                break
        else: # pragma: no cover
            self.fail('NNH is not in the owned shares list')

        self.story('Select the IPO to sell the shares to')
        for label in share_form.source(player['detail']):
            if label.get_attribute('for') == 'source-ipo':
                label.click()
                break
        else: # pragma: no cover
            self.fail('Cannot select the IPO to sell to')
        share_form.transfer_button(player['detail']).click()

        self.story('The page updates and shares and money have changed hands')
        player = game_page.get_players()[0]
        company = game_page.get_companies()[0]
        self.assertEqual(game_page.bank_cash.text, '11900')
        self.assertEqual(len(game_page.bank_pool), 0)
        self.verify_player(player, cash=100, shares=['NNH 40%'])
        self.verify_company(company, cash=0, ipo_shares=5, bank_shares=0,
            shares=[])

    def test_player_can_short_sell_shares_to_pool(self):
        self.story('Create a game with a player owning some shares')
        game_uuid = self.create_game()
        player_uuid = self.create_player(game_uuid, 'Charlie', cash=0)
        company_uuid = self.create_company(game_uuid, 'Erie', cash=0,
            ipo_shares=0, bank_shares=0)
        self.create_player_share(player_uuid, company_uuid, shares=2)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

        self.story('The player should be the only one owning shares')
        player = game_page.get_players()[0]
        company = game_page.get_companies()[0]
        self.verify_player(player, shares=['Erie 20%'])
        self.verify_company(company, ipo_shares=0, bank_shares=0, shares=[])

        self.story('Set the value of the Erie')
        company['value'].clear()
        company['value'].send_keys('50')

        self.story('The player sells some shares')
        player['row'].click()
        player = game_page.get_players()[0]
        share_form = game.ShareForm(self.browser)
        share_form.sell_share(player['detail']).click()
        share_form.shares(player['detail']).clear()
        share_form.shares(player['detail']).send_keys('3')

        self.story('Select the Erie to sell it')
        for label in share_form.company(player['detail']):
            if label.get_attribute('for') == 'company-Erie':
                label.click()
                break
        else: # pragma: no cover
            self.fail('Erie is not in the owned shares list')

        self.story('Select the bank pool to sell the shares to')
        for label in share_form.source(player['detail']):
            if label.get_attribute('for') == 'source-bank':
                label.click()
                break
        else: # pragma: no cover
            self.fail('Cannot select the bank pool to sell to')
        share_form.transfer_button(player['detail']).click()

        self.story('The page updates and shares and money have changed hands')
        player = game_page.get_players()[0]
        company = game_page.get_companies()[0]
        self.assertEqual(game_page.bank_cash.text, '11850')
        self.assertEqual(len(game_page.bank_pool), 1)
        self.assertEqual(game_page.bank_pool[0].text, 'Erie 30%')
        self.verify_player(player, cash=150, shares=['Erie -10%'])
        self.verify_company(company, cash=0, ipo_shares=0, bank_shares=3,
            shares=[])

    def test_company_can_sell_shares_to_bank_pool(self):
        self.story('Create a game with a company owning some shares')
        game_uuid = self.create_game()
        sell_uuid = self.create_company(game_uuid, 'sell', cash=0)
        share_uuid = self.create_company(game_uuid, 'share', cash=0,
            ipo_shares=0, bank_shares=0)
        self.create_company_share(sell_uuid, share_uuid, shares=10)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

        self.story('The sell company should be the only one owning shares')
        sell, share = game_page.get_companies()
        self.verify_company(sell, shares=['share 100%'])
        self.verify_company(share, shares=[])

        self.story('Set the value of the share company')
        share['value'].clear()
        share['value'].send_keys('30')

        self.story('The sell company sells some shares')
        sell['elem'].click()
        sell, share = game_page.get_companies()
        share_form = game.ShareForm(self.browser)
        share_form.sell_share(sell['detail']).click()
        share_form.shares(sell['detail']).clear()
        share_form.shares(sell['detail']).send_keys(7)

        self.story('Select the share company to sell it')
        for label in share_form.company(sell['detail']):
            if label.get_attribute('for') == 'company-share':
                label.click()
                break
        else: # pragma: no cover
            self.fail('Cannot select the share company to sell to')

        self.story('Select the bank to sell to it')
        for label in share_form.source(sell['detail']):
            if label.get_attribute('for') == 'source-bank':
                label.click()
                break
        else: # pragma: no cover
            self.fail('Cannot select the bank to sell to')
        share_form.transfer_button(sell['detail']).click()

        self.story('The page updates and shares and money have changed hands')
        sell, share = game_page.get_companies()
        self.assertEqual(game_page.bank_cash.text, '11790')
        self.assertEqual(len(game_page.bank_pool), 1)
        self.assertEqual(game_page.bank_pool[0].text, 'share 70%')
        self.verify_company(sell, cash=210, shares=['share 30%'])
        self.verify_company(share, ipo_shares=0, bank_shares=7, shares=[],
            cash=0)

    def test_company_can_sell_shares_to_ipo(self):
        self.story('Create a game with a company owning some shares')
        game_uuid = self.create_game()
        sell_uuid = self.create_company(game_uuid, 'sell', cash=0)
        share_uuid = self.create_company(game_uuid, 'share', cash=0,
            ipo_shares=0, bank_shares=0)
        self.create_company_share(sell_uuid, share_uuid, shares=10)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

        self.story('The sell company should be the only one owning shares')
        sell, share = game_page.get_companies()
        self.verify_company(sell, shares=['share 100%'])
        self.verify_company(share, ipo_shares=0, bank_shares=0, shares=[])

        self.story('Set the value of the share company')
        share['value'].clear()
        share['value'].send_keys('40')

        self.story('The sell company sells some shares')
        sell['elem'].click()
        sell, share = game_page.get_companies()
        share_form = game.ShareForm(self.browser)
        share_form.sell_share(sell['detail']).click()
        share_form.shares(sell['detail']).clear()
        share_form.shares(sell['detail']).send_keys(4)

        self.story('Select the share company to sell it')
        for label in share_form.company(sell['detail']):
            if label.get_attribute('for') == 'company-share':
                label.click()
                break
        else: # pragma: no cover
            self.fail('Cannot select the share company to sell to')

        self.story('Select the IPO to sell to it')
        for label in share_form.source(sell['detail']):
            if label.get_attribute('for') == 'source-ipo':
                label.click()
                break
        else: # pragma: no cover
            self.fail('Cannot select the IPO to sell to')
        share_form.transfer_button(sell['detail']).click()

        self.story('The page updates and shares and money have changed hands')
        sell, share = game_page.get_companies()
        self.assertEqual(game_page.bank_cash.text, '11840')
        self.assertEqual(len(game_page.bank_pool), 0)
        self.verify_company(sell, cash=160, shares=['share 60%'])
        self.verify_company(share, cash=0, ipo_shares=4, bank_shares=0,
            shares=[])


class MiscellaneousShareTests(FunctionalTestCase):
    def test_shares_in_pool_appear_in_bank_section(self):
        self.story('Create game with a company with shares in the pool')
        game_uuid = self.create_game()
        self.create_company(game_uuid, 'NYC', text='white', background='black',
            ipo_shares=5, bank_shares=5)
        self.create_company(game_uuid, 'N&W', text='yellow-400',
            background='red-700', ipo_shares=7, bank_shares=3)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

        self.story('There is a bank pool in the bank section holding the bank '
            'pool shares')
        self.assertEqual(len(game_page.bank_pool), 2)
        self.assertEqual(game_page.bank_pool[0].text, 'N&W 30%')
        self.assertIn('fg-yellow-400',
            game_page.bank_pool[0].get_attribute('class'))
        self.assertIn('bg-red-700',
            game_page.bank_pool[0].get_attribute('class'))
        self.assertEqual(game_page.bank_pool[1].text, 'NYC 50%')
        self.assertIn('fg-white',
            game_page.bank_pool[1].get_attribute('class'))
        self.assertIn('bg-black',
            game_page.bank_pool[1].get_attribute('class'))

    def test_shares_not_in_pool_dont_appear_in_bank_section(self):
        self.story('Create a game with two companies, one having pool shares')
        game_uuid = self.create_game()
        self.create_company(game_uuid, 'NKP', text='grey-50',
            background='black', ipo_shares=5, bank_shares=5)
        self.create_company(game_uuid, 'B&M', text='yellow-400',
            background='red-900', bank_shares=0)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

        self.story('Only the NKP shares are in the pool')
        self.assertEqual(len(game_page.bank_pool), 1)
        self.assertEqual(game_page.bank_pool[0].text, 'NKP 50%')
        self.assertIn('fg-grey-50',
            game_page.bank_pool[0].get_attribute('class'))
        self.assertIn('bg-black',
            game_page.bank_pool[0].get_attribute('class'))

    def test_text_on_confirm_button_changes_with_action(self):
        self.story('Create a game with a company')
        game_uuid = self.create_game()
        self.create_company(game_uuid, 'B&O')
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

        self.story("Open the company's detail section")
        company = game_page.get_companies()[0]
        company['elem'].click()
        company = game_page.get_companies()[0]

        self.story('The share form confirm button should read Buy')
        share_form = game.ShareForm(self.browser)
        self.assertEqual('Buy', share_form.transfer_button(company['detail'])
            .get_attribute('value'))
        self.assertEqual('from', share_form.action(company['detail']).text)

        self.story('Selecting sell changes the text to Sell')
        share_form.sell_share(company['detail']).click()
        self.assertEqual('Sell', share_form.transfer_button(company['detail'])
            .get_attribute('value'))
        self.assertEqual('to', share_form.action(company['detail']).text)

        self.story('Changing back again updates the text to Buy')
        share_form.buy_share(company['detail']).click()
        self.assertEqual('Buy', share_form.transfer_button(company['detail'])
            .get_attribute('value'))
        self.assertEqual('from', share_form.action(company['detail']).text)

    def test_company_value_remains_the_same_after_buying_a_share(self):
        """Fix bug where the value field is empty after buying a share"""
        self.story('Create a game with a company')
        game_uuid = self.create_game()
        self.create_company(game_uuid, 'C&O', cash=1000)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

        self.story('Set the value of the C&O')
        company = game_page.get_companies()[0]
        company['value'].clear()
        company['value'].send_keys('67')
        self.assertEqual(company['value'].get_attribute('value'), '67')

        self.story('Let the C&O buy one of its own shares')
        company['elem'].click()
        company = game_page.get_companies()[0] # Get DOM updates
        share_form = game.ShareForm(self.browser)
        for label in share_form.company(company['detail']):
            if label.get_attribute('for') == 'company-C&O':
                label.click()
                break
        else: # pragma: no cover
            self.fail('The C&O is not in the list of available companies')
        for label in share_form.source(company['detail']):
            if label.get_attribute('for') == 'source-ipo':
                label.click()
                break
        else: # pragma: no cover
            self.fail('Cannot buy form the IPO')
        share_form.shares(company['detail']).clear()
        share_form.shares(company['detail']).send_keys('3\n')

        self.story('The page updates, but the value of the C&O is the same')
        company = game_page.get_companies()[0] # Get DOM updates
        self.assertEqual(company['value'].get_attribute('value'), '67')
