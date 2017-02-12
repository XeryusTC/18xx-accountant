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

    def test_cannot_create_duplicate_company(self):
        # Alice is a user who starts a game
        self.browser.get(self.live_server_url)
        homepage = game.Homepage(self.browser)
        homepage.start_button.click()

        # She adds a company
        game_page = game.GamePage(self.browser)
        game_page.add_company_link.click()

        add_company = game.AddCompanyPage(self.browser)
        add_company.name.clear()
        add_company.name.send_keys('NYC\n')
        # The company has been added to the game
        company_list = game_page.get_companies()
        self.assertEqual(len(company_list), 1)
        self.assertEqual(company_list[0]['name'].text, 'NYC')

        # Alice goes to add another company
        game_page.add_company_link.click()
        add_company.name.clear()
        add_company.name.send_keys('NYC\n')
        # She stays on the page and sees an error message
        self.assertRegex(self.browser.current_url,
            r'/en/game/([^/]+)/add-company/$')
        self.assertIn('There is already a company with this name in your game',
            add_company.error_list.text)

    def test_can_return_to_game_page_from_add_player_page(self):
        # Alice is a user who starts a new game
        self.browser.get(self.live_server_url)
        page = game.Homepage(self.browser)
        page.start_button.click()

        # She goes to the add company screen
        game_page = game.GamePage(self.browser)
        game_page.add_company_link.click()
        self.assertRegex(self.browser.current_url,
            r'/en/game/([^/]+)/add-company/$')

        # She realises she doesn't want to create a company and clicks
        # the back button
        add_company = game.AddCompanyPage(self.browser)
        add_company.back.click()
        self.assertRegex(self.browser.current_url, r'/en/game/([^/]+)/$')
        self.assertEqual(game_page.get_companies(), [])

    def test_can_set_company_colors(self):
        # Alice is a user who starts a new game
        self.browser.get(self.live_server_url)
        page = game.Homepage(self.browser)
        page.start_button.click()

        # She goes to the add company screen
        game_page = game.GamePage(self.browser)
        game_page.add_company_link.click()

        # She enters some details
        add_company = game.AddCompanyPage(self.browser)
        add_company.name.clear()
        add_company.name.send_keys('C&O')

        # She sees two color selectors, the first is for the background
        # color, she picks the color blue
        for radio in add_company.background_color:
            if radio.get_attribute('value') == 'blue-500':
                radio.click()
                break

        # She picks yellow for the text color
        for radio in add_company.text_color:
            if radio.get_attribute('value') == 'yellow-300':
                radio.click()
                break

        # She adds the company and is returned to the game page
        add_company.add_button.click()
        self.assertRegex(self.browser.current_url, r'/en/game/([^/]+)/$')

        # She sees that the company row has the correct colors
        company_list = game_page.get_companies()
        self.assertEqual(len(company_list), 1)
        self.assertEqual(company_list[0]['name'].text, 'C&O')
        self.assertIn('bg-blue-500',
            company_list[0]['elem'].get_attribute('class'))
        self.assertIn('fg-yellow-300',
            company_list[0]['elem'].get_attribute('class'))
