# -*- coding: utf-8 -*-
import unittest
from .base import FunctionalTestCase
from .pages import game

class CompanyTests(FunctionalTestCase):
    def test_can_create_company(self):
        self.story('Alice is a user who starts a game')
        self.browser.get(self.live_server_url)
        homepage = game.Homepage(self.browser)
        homepage.start_button.click()

        self.story('She sees a button that says "Add company" and clicks it')
        game_page = game.GamePage(self.browser)
        self.assertEqual(game_page.add_company_link.text.lower(),
            'add company')
        game_page.add_company_link.click()

        self.story('She lands on a add company page')
        add_company = game.AddCompanyPage(self.browser)
        self.assertRegex(self.browser.current_url,
            r'/game/([^/]+)/add-company$')
        self.assertEqual(self.browser.title, 'Add company')
        self.assertEqual(add_company.header.text, 'Add company')

        self.story('She enters a name, an amount of starting cash and a share '
            'split')
        add_company.name.clear()
        add_company.name.send_keys('B&O')
        add_company.cash.clear()
        add_company.cash.send_keys('100')
        add_company.shares.clear()
        add_company.shares.send_keys('10')
        add_company.add_button.click()

        self.story('The company appears in the company list on the game page')
        self.assertRegex(self.browser.current_url, r'/game/([^/]+)$')

        company_list = game_page.get_companies()
        self.assertEqual(len(company_list), 1)
        self.assertEqual(company_list[0]['name'].text, 'B&O')
        self.assertEqual(company_list[0]['cash'].text, '100')
        self.assertEqual(company_list[0]['share_count'].text, '10')
        self.assertEqual(company_list[0]['ipo_shares'].text, '10')
        self.assertEqual(company_list[0]['bank_shares'].text, '0')

    def test_cannot_create_duplicate_company(self):
        self.story('Alice is a user who starts a game')
        self.browser.get(self.live_server_url)
        homepage = game.Homepage(self.browser)
        homepage.start_button.click()

        self.story('She adds a company')
        game_page = game.GamePage(self.browser)
        game_page.add_company_link.click()

        add_company = game.AddCompanyPage(self.browser)
        add_company.name.clear()
        add_company.name.send_keys('NYC\n')
        self.story('The company has been added to the game')
        company_list = game_page.get_companies()
        self.assertEqual(len(company_list), 1)
        self.assertEqual(company_list[0]['name'].text, 'NYC')

        self.story('Alice goes to add another company')
        game_page.add_company_link.click()
        add_company.name.clear()
        add_company.name.send_keys('NYC\n')
        self.story('She stays on the page and sees an error message')
        self.assertRegex(self.browser.current_url,
            r'/game/([^/]+)/add-company$')
        self.assertIn('There is already a company with this name in your game',
            add_company.error_list.text)

    def test_can_return_to_game_page_from_add_company_page(self):
        self.story('Alice is a user who starts a new game')
        self.browser.get(self.live_server_url)
        page = game.Homepage(self.browser)
        page.start_button.click()

        self.story('She goes to the add company screen')
        game_page = game.GamePage(self.browser)
        game_page.add_company_link.click()
        self.assertRegex(self.browser.current_url,
            r'/game/([^/]+)/add-company$')

        self.story("She realises she doesn't want to create a company and "
            "clicks the back button")
        add_company = game.AddCompanyPage(self.browser)
        add_company.back.click()
        self.assertRegex(self.browser.current_url, r'/game/([^/]+)$')
        self.assertEqual(game_page.get_companies(), [])

    def test_can_set_company_colors(self):
        self.story('Alice is a user who starts a new game')
        self.browser.get(self.live_server_url)
        page = game.Homepage(self.browser)
        page.start_button.click()

        self.story('She goes to the add company screen')
        game_page = game.GamePage(self.browser)
        game_page.add_company_link.click()

        self.story('She enters some details')
        add_company = game.AddCompanyPage(self.browser)
        add_company.name.clear()
        add_company.name.send_keys('C&O')

        self.story('She sees two color selectors, one is for the'
            'background color, she picks the color blue')
        self.assertGreater(len(add_company.background_color), 0)
        self.assertGreater(len(add_company.text_color), 0)
        # For some reason the test fails when the first color is selected
        # only once, so do it twice to prevent that
        for radio in add_company.background_color:
            if radio.get_attribute('value') == 'blue-500':
                radio.click()
                break
        for radio in add_company.background_color:
            if radio.get_attribute('value') == 'blue-500':
                radio.click()
                break

        self.story('She picks yellow for the text color')
        for radio in add_company.text_color:
            if radio.get_attribute('value') == 'yellow-300':
                radio.click()
                break

        self.story('She adds the company and is returned to the game page')
        add_company.add_button.click()
        self.assertRegex(self.browser.current_url, r'/game/([^/]+)$')

        self.story('She sees that the company row has the correct colors')
        company_list = game_page.get_companies()
        self.assertEqual(len(company_list), 1)
        self.assertEqual(company_list[0]['name'].text, 'C&O')
        self.assertIn('bg-blue-500',
            company_list[0]['elem'].get_attribute('class'))
        self.assertIn('fg-yellow-300',
            company_list[0]['elem'].get_attribute('class'))

    def test_company_colors_preview(self):
        self.story('Alice is a user who starts a new game')
        self.browser.get(self.live_server_url)
        page = game.Homepage(self.browser)
        page.start_button.click()

        self.story('She goes to the add company screen')
        game_page = game.GamePage(self.browser)
        game_page.add_company_link.click()

        self.story('The preview is empty and has default colors')
        add_company = game.AddCompanyPage(self.browser)
        self.assertEqual(add_company.preview.text, '')
        self.assertIn('fg-black', add_company.preview.get_attribute('class'))
        self.assertIn('bg-white', add_company.preview.get_attribute('class'))

        self.story('She enters a name and selects some colors')
        add_company.name.clear()
        add_company.name.send_keys('PRR')
        for radio in add_company.background_color:
            if radio.get_attribute('value') == 'green-700':
                radio.click()
                break
        for radio in add_company.background_color:
            if radio.get_attribute('value') == 'green-700':
                radio.click()
                break
        for radio in add_company.text_color:
            if radio.get_attribute('value') == 'red-500':
                radio.click()
                break

        self.story('The preview has updated to the selected options')
        self.assertEqual(add_company.preview.text, 'PRR')
        self.assertIn('bg-green-700',
            add_company.preview.get_attribute('class'))
        self.assertIn('fg-red-500', add_company.preview.get_attribute('class'))

    def test_creating_company_with_cash_decreases_bank_cash(self):
        self.story('Alice is a user who starts a new game')
        self.browser.get(self.live_server_url)
        page = game.Homepage(self.browser)
        page.bank_cash.clear()
        page.bank_cash.send_keys('1000\n')

        self.story('She goes to add a company')
        game_page = game.GamePage(self.browser)
        game_page.add_company_link.click()

        add_company = game.AddCompanyPage(self.browser)
        add_company.name.clear()
        add_company.cash.clear()
        add_company.name.send_keys('B&O')
        add_company.cash.send_keys('300\n')

        self.story('On the game page she sees that the bank size has reduced')
        self.assertEqual(game_page.bank_cash.text, '700')

class ManageCompanyTests(FunctionalTestCase):
    def test_clicking_company_opens_company_detail_section(self):
        self.story('Alice is a user who starts a new game')
        self.browser.get(self.live_server_url)
        homepage = game.Homepage(self.browser)
        homepage.start_button.click()

        self.story('She adds two companies')
        game_page = game.GamePage(self.browser)
        game_page.add_company_link.click()
        add_company = game.AddCompanyPage(self.browser)
        add_company.name.clear()
        add_company.name.send_keys('B&O\n')

        game_page.add_company_link.click()
        add_company.name.clear()
        add_company.name.send_keys('C&O\n')

        self.story('The company detail sections are both hidden')
        companies = game_page.get_companies()
        for company in companies:
            with self.subTest(company=company['name'].text):
                self.assertIsNone(company['detail'])

        self.story('She clicks the first company and the detail appear')
        companies[0]['elem'].click()
        companies = game_page.get_companies() # Need to retrieve DOM updates
        self.assertIsNotNone(companies[0]['detail'])
        self.assertIsNone(companies[1]['detail'])

        self.story("She clicks the second company, the first company's"
            "details disappear and the second company's details appear")
        companies[1]['elem'].click()
        companies = game_page.get_companies() # Need to retrieve DOM updates
        self.assertIsNone(companies[0]['detail'])
        self.assertIsNotNone(companies[1]['detail'])

    def test_clicking_company_closes_opened_player_detail_section(self):
        self.browser.get(self.live_server_url)
        homepage = game.Homepage(self.browser)
        homepage.start_button.click()

        self.story('She adds a player')
        game_page = game.GamePage(self.browser)
        game_page.add_player_link.click()
        add_player = game.AddPlayerPage(self.browser)
        add_player.name.send_keys('Alice\n')

        self.story('She also adds a company')
        game_page.add_company_link.click()
        add_company = game.AddCompanyPage(self.browser)
        add_company.name.send_keys('NYC\n')

        self.story("She clicks the player to open the player's detail section")
        player = game_page.get_players()[0]
        company = game_page.get_companies()[0]
        player['row'].click()

        # Retrieve DOM updates before testing visibility
        player = game_page.get_players()[0]
        company = game_page.get_companies()[0]
        self.assertIsNotNone(player['detail'])
        self.assertIsNone(company['detail'])

        self.story('When she clicks the company the player detail closes')
        company['elem'].click()
        player = game_page.get_players()[0]
        company = game_page.get_companies()[0]
        self.assertIsNone(player['detail'])
        self.assertIsNotNone(company['detail'])
