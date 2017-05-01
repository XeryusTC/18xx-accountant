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
