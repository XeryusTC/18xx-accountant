#! -*- coding: utf-8 -*-
from .base import FunctionalTestCase
from .pages import game

class OperateTests(FunctionalTestCase):
    def test_company_can_operate_and_pays_dividends(self):
        self.story('Start a game with two players and two companies')
        game_uuid = self.create_game()
        player1_uuid = self.create_player(game_uuid, 'Alice', cash=0)
        player2_uuid = self.create_player(game_uuid, 'Bob', cash=0)
        company1_uuid = self.create_company(game_uuid, 'B&O', cash=0,
            ipo_shares=2, bank_shares=1)
        company2_uuid = self.create_company(game_uuid, 'NYC', cash=0)
        self.create_player_share(player1_uuid, company1_uuid, shares=3)
        self.create_player_share(player2_uuid, company1_uuid, shares=1)
        self.create_company_share(company1_uuid, company1_uuid, shares=2)
        self.create_company_share(company2_uuid, company1_uuid, shares=1)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

        self.story('Open B&O detail section, there is an operate form')
        bno, nyc = game_page.get_companies()
        bno['elem'].click()
        bno = game_page.get_companies()[0] # Get DOM updates
        operate_form = game.OperateForm(self.browser)
        self.assertEqual('0',
            operate_form.revenue(bno['detail']).get_attribute('value'))

        self.story('The B&O operates for 140, pays full dividends')
        operate_form.revenue(bno['detail']).clear()
        operate_form.revenue(bno['detail']).send_keys('140')
        operate_form.full(bno['detail']).click()

        self.story('The page updates and everyone receives their dividends')
        alice, bob = game_page.get_players()
        bno, nyc = game_page.get_companies()
        self.assertEqual(game_page.bank_cash.text, '11902')
        self.verify_player(alice, cash=42)
        self.verify_player(bob, cash=14)
        self.verify_company(bno, cash=28)
        self.verify_company(nyc, cash=14)

    def test_company_can_operate_and_pay_half_dividends(self):
        self.story('start a game with two players and two companies')
        game_uuid = self.create_game(cash=100)
        player1_uuid = self.create_player(game_uuid, 'Alice', cash=0)
        player2_uuid = self.create_player(game_uuid, 'Bob', cash=0)
        company1_uuid = self.create_company(game_uuid, 'C&O', cash=0,
            ipo_shares=2, bank_shares=1)
        company2_uuid = self.create_company(game_uuid, 'NNH', cash=0)
        self.create_player_share(player1_uuid, company1_uuid, shares=3)
        self.create_player_share(player2_uuid, company1_uuid, shares=1)
        self.create_company_share(company1_uuid, company1_uuid, shares=2)
        self.create_company_share(company2_uuid, company1_uuid, shares=1)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

        self.story('Open C&O detail section, and fill in the operate form')
        cno = game_page.get_companies()[0]
        cno['elem'].click()
        cno = game_page.get_companies()[0] # Get DOM updates
        operate_form = game.OperateForm(self.browser)
        operate_form.revenue(cno['detail']).clear()
        operate_form.revenue(cno['detail']).send_keys('90')
        operate_form.half(cno['detail']).click()

        self.story('The page updates and dividends have been paid out')
        alice, bob = game_page.get_players()
        cno, nnh = game_page.get_companies()
        self.assertEqual(game_page.bank_cash.text, '25')
        self.verify_player(alice, cash=15)
        self.verify_player(bob, cash=5)
        self.verify_company(cno, cash=50) # 40 + 2 * 5
        self.verify_company(nnh, cash=5)

    def test_company_can_withhold_revenue(self):
        self.story('start a game with two players and two companies')
        game_uuid = self.create_game(cash=100)
        player1_uuid = self.create_player(game_uuid, 'Alice', cash=0)
        player2_uuid = self.create_player(game_uuid, 'Bob', cash=0)
        company1_uuid = self.create_company(game_uuid, 'Erie', cash=0,
            ipo_shares=2, bank_shares=1)
        company2_uuid = self.create_company(game_uuid, 'PRR', cash=0)
        self.create_player_share(player1_uuid, company1_uuid, shares=4)
        self.create_player_share(player2_uuid, company1_uuid, shares=2)
        self.create_company_share(company1_uuid, company1_uuid, shares=0)
        self.create_company_share(company2_uuid, company1_uuid, shares=1)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

        self.story('Open the Erie detail section, withhold some revenue')
        erie = game_page.get_companies()[0]
        erie['elem'].click()
        erie = game_page.get_companies()[0] # Get DOM updates
        operate_form = game.OperateForm(self.browser)
        operate_form.revenue(erie['detail']).clear()
        operate_form.revenue(erie['detail']).send_keys('40')
        operate_form.withhold(erie['detail']).click()

        self.story('The page updates and revenue has been withheld')
        alice, bob = game_page.get_players()
        erie, prr = game_page.get_companies()
        self.assertEqual(game_page.bank_cash.text, '60')
        self.verify_player(alice, cash=0)
        self.verify_player(bob, cash=0)
        self.verify_company(erie, cash=40)
        self.verify_company(prr, cash=0)
