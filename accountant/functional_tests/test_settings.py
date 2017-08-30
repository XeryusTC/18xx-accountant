# -*- coding: utf-8 -*-
from .base import FunctionalTestCase
from .pages import game

class SettingsTests(FunctionalTestCase):
    def test_default_settings(self):
        self.story('Alice is a user who creates a game')
        self.browser.get(self.server_url)
        homepage = game.Homepage(self.browser)
        homepage.start_button.click()

        self.story('The game page loads, check the defaults')
        game_page = game.GamePage(self.browser)
        self.assertFalse(game_page.pool_shares_pay.is_selected())
        self.assertFalse(game_page.ipo_shares_pay.is_selected())

    def test_create_game_with_pool_shares_paying_to_company(self):
        self.story('Alice is a user who visits the homepage')
        self.browser.get(self.server_url)

        self.story('She sees a checkbox for pool shares paying to the company'
            'and enables it (it is disabled by default)')
        homepage = game.Homepage(self.browser)
        self.assertFalse(homepage.pool_shares_pay.is_selected())
        homepage.pool_shares_pay.click()
        self.assertTrue(homepage.pool_shares_pay.is_selected())
        self.story('She starts the game')
        homepage.start_button.click()

        self.story('She lands on the game page')
        self.assertRegex(self.browser.current_url, r'/game/([^/]+)$')
        game_page = game.GamePage(self.browser)
        self.assertTrue(game_page.pool_shares_pay.is_selected())

        self.story('Create a company for the game')
        game_uuid = self.browser.current_url[-36:]
        self.create_company(game_uuid, 'B&O', cash=0, bank_shares=3)
        self.browser.refresh()

        self.story('The company operates, and receives some money')
        company = game_page.get_companies()[0]
        company['elem'].click()
        operate_form = game.OperateForm(self.browser)
        operate_form.revenue(company['detail']).clear()
        operate_form.revenue(company['detail']).send_keys('10')
        operate_form.full(company['detail']).click()

        self.story('The page updates and the company has received some money')
        self.verify_company(game_page.get_companies()[0], cash=3)

    def test_create_game_with_ipo_shares_paying_to_company(self):
        self.story('Alice is a user who visits the homepage')
        self.browser.get(self.server_url)

        self.story('She sees a checkbox for ipo shares paying to the company'
            'and enables it (it is disabled by default)')
        homepage = game.Homepage(self.browser)
        self.assertFalse(homepage.ipo_shares_pay.is_selected())
        homepage.ipo_shares_pay.click()
        self.assertTrue(homepage.ipo_shares_pay.is_selected())
        self.story('She starts the game')
        homepage.start_button.click()

        self.story('She lands on the game page')
        self.assertRegex(self.browser.current_url, r'/game/([^/]+)$')
        game_page = game.GamePage(self.browser)
        self.assertTrue(game_page.ipo_shares_pay.is_selected())

        self.story('Create a company for the game')
        game_uuid = self.browser.current_url[-36:]
        self.create_company(game_uuid, 'PRR', cash=0, ipo_shares=7)
        self.browser.refresh()

        self.story('The company operates, and receives some money')
        company = game_page.get_companies()[0]
        company['elem'].click()
        operate_form = game.OperateForm(self.browser)
        operate_form.revenue(company['detail']).clear()
        operate_form.revenue(company['detail']).send_keys('20')
        operate_form.full(company['detail']).click()

        self.story('The page updates and the company has received some money')
        self.verify_company(game_page.get_companies()[0], cash=14)
