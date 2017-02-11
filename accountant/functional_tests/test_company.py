# -*- coding: utf-8 -*-
from .base import FunctionalTestCase
from .pages import game

class CompanyTests(FunctionalTestCase):
    def test_can_create_company(self):
        # Alice is a user who starts a game
        self.browser.get(self.live_server_url)
        homepage = game.Homepage(self.browser)
        homepage.start_button.click()

        # She sees a button that says 'Add company' and clicks it
        game_page = game.GamePage(self.browser)
        self.assertEqual(game_page.add_company_link.text, 'Add company')
        game_page.add_company_link.click()

        # She lands on a add company page
        add_company = game.AddCompanyPage(self.browser)
        self.assertRegex(self.browser.current_url,
            r'/en/game/([^/]+)/add-company/$')
        self.assertEqual(self.browser.title, 'Add company')
        self.assertEqual(add_company.header.text, 'Add company')

        # The game field is hidden
        self.assertEqual(add_company.game.get_attribute('type'), 'hidden')
        # She enters a name, an amount of starting cash and a share split
        add_company.name.clear()
        add_company.name.send_keys('B&O')
        add_company.cash.clear()
        add_company.cash.send_keys('100')
        add_company.shares.clear()
        add_company.shares.send_keys('10')
        add_company.add_button.click()

        # The company appears in the company list on the game page
        self.assertRegex(self.browser.current_url, r'/en/game/([^/]+)/$')

        company_list = game_page.get_companies()
        self.assertEqual(len(company_list), 1)
        self.assertEqual(company_list[0]['name'].text, 'B&O')
        self.assertEqual(company_list[0]['cash'].text, '100')
        self.assertEqual(company_list[0]['share_count'].text, '10')
        self.assertEqual(company_list[0]['ipo_shares'].text, '10')
        self.assertEqual(company_list[0]['bank_shares'].text, '0')
