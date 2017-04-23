# -*- coding: utf-8 -*-
import unittest
from .base import FunctionalTestCase
from .pages import game

class CompanyTests(FunctionalTestCase):
    def test_can_create_company(self):
        self.story('Alice is a user who starts a game')
        self.browser.get(self.server_url)
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
        self.browser.get(self.server_url)
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
        self.browser.get(self.server_url)
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
        self.browser.get(self.server_url)
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
        self.browser.get(self.server_url)
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
        self.browser.get(self.server_url)
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

    def test_companies_are_sorted_alphabetically(self):
        self.story('Alice is a user who starts a new game')
        self.browser.get(self.server_url)
        homepage = game.Homepage(self.browser)
        homepage.start_button.click()

        self.story('She goes to add two companies')
        game_page = game.GamePage(self.browser)
        add_company = game.AddCompanyPage(self.browser)
        game_page.add_company_link.click()
        add_company.name.send_keys('B&O\n')
        game_page.add_company_link.click()
        add_company.name.send_keys('Erie\n')

        self.story('The companies should be listed as B&O, Erie')
        self.assertEqual(['B&O', 'Erie'],
            [company['name'].text for company in game_page.get_companies()])

        self.story('She adds a third company')
        game_page.add_company_link.click()
        add_company.name.send_keys('C&O\n')

        self.story('The companies should be listed as B&O, C&O, Erie')
        self.assertEqual(['B&O', 'C&O', 'Erie'],
            [company['name'].text for company in game_page.get_companies()])

        self.story('She adds a fourth company')
        game_page.add_company_link.click()
        add_company.name.send_keys('PRR\n')

        self.story('The companies should be listed as B&O, C&O, Erie, PRR')
        self.assertEqual(['B&O', 'C&O', 'Erie', 'PRR'],
            [company['name'].text for company in game_page.get_companies()])

        self.story('She adds a fifth company')
        game_page.add_company_link.click()
        add_company.name.send_keys('CPR\n')

        self.story('The companies are listed as B&O, C&O, CPR, Erie, PRR')
        self.assertEqual(['B&O', 'C&O', 'CPR', 'Erie', 'PRR'],
            [company['name'].text for company in game_page.get_companies()])

class ManageCompanyTests(FunctionalTestCase):
    def test_clicking_company_opens_company_detail_section(self):
        self.story('Alice is a user who starts a new game')
        game_uuid = self.create_game()
        self.create_company(game_uuid, 'B&O')
        self.create_company(game_uuid, 'C&O')
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

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
        self.story('Alice is a user who starts a game')
        game_uuid = self.create_game()
        self.create_player(game_uuid, 'Alice')
        self.create_company(game_uuid, 'NYC')
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

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

    def test_company_can_transfer_money_to_bank(self):
        self.story('Alice is a user who starts a new game')
        game_uuid = self.create_game(cash=11600)
        self.create_company(game_uuid, 'B&O', cash=400)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

        self.story('Confirm cash amounts')
        company = game_page.get_companies()[0]
        self.assertEqual(company['cash'].text, '400')
        self.assertEqual(game_page.bank_cash.text, '11600')
        self.story("She opens the company's detail view")
        company['elem'].click()
        company = game_page.get_companies()[0] # get DOM updates

        self.story('There is a form that allows her to send money')
        transfer_form = game.TransferForm(self.browser)
        transfer_form.amount(company['detail']).clear()
        transfer_form.amount(company['detail']).send_keys('100')
        for radio in transfer_form.target(company['detail']):
            if radio.get_attribute('value') == 'bank':
                radio.click()
                break
        transfer_form.transfer_button(company['detail']).click()

        self.story("The page updates and the company's cash amount is lower")
        company = game_page.get_companies()[0] # get DOM updates
        self.assertEqual(company['cash'].text, '300')
        self.assertEqual(game_page.bank_cash.text, '11700')

        self.story('Alice goes to transfer money again')
        company['elem'].click()
        company = game_page.get_companies()[0]
        transfer_form.amount(company['detail']).clear()
        transfer_form.amount(company['detail']).send_keys('50')
        self.story("This time she doesn't select a target, the bank is the"
            "default target")
        transfer_form.transfer_button(company['detail']).click()

        self.story('After the page updates the sees the amounts have changed')
        company = game_page.get_companies()[0] # get DOM updates
        self.assertEqual(company['cash'].text, '250')
        self.assertEqual(game_page.bank_cash.text, '11750')

    def test_company_can_transfer_money_to_player(self):
        self.story('Alice is a user who starts a new game')
        game_uuid = self.create_game(cash=11500)
        self.create_player(game_uuid, 'Alice', cash=100)
        self.create_company(game_uuid, 'B&O', cash=400)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

        self.story('Confirm cash amounts')
        player = game_page.get_players()[0]
        company = game_page.get_companies()[0]
        self.assertEqual(player['cash'].text, '100')
        self.assertEqual(company['cash'].text, '400')
        self.assertEqual(game_page.bank_cash.text, '11500')

        self.story("She opens the company's detail view")
        company['elem'].click()
        company = game_page.get_companies()[0]

        self.story('The form allows her to transfer funds to Alice')
        transfer_form = game.TransferForm(self.browser)
        transfer_form.amount(company['detail']).send_keys('15')
        for radio in transfer_form.target(company['detail']):
            if radio.get_attribute('id') == 'target-Alice':
                radio.click()
                break
        else: # pragma: no cover
            self.fail('Could not find Alice in the transfer form')
        transfer_form.transfer_button(company['detail']).click()

        self.story('Check final cash amounts')
        player = game_page.get_players()[0]
        company = game_page.get_companies()[0]
        self.assertEqual(player['cash'].text, '115')
        self.assertEqual(company['cash'].text, '385')
        self.assertEqual(game_page.bank_cash.text, '11500')

    def test_company_can_transfer_money_to_other_company(self):
        self.story('Alice is a user who starts a new game with companies')
        game_uuid = self.create_game(cash=11800)
        self.create_company(game_uuid, 'CPR', cash=100)
        self.create_company(game_uuid, 'NYC', cash=100, text='amber-200',
            background='black')
        self.browser.get(self.server_url + '/game/' + game_uuid)

        self.story('She adds a company')
        game_page = game.GamePage(self.browser)

        self.story('She transfers some money from the CPR to the NYC')
        cpr, nyc = game_page.get_companies()
        cpr['elem'].click()
        cpr, nyc = game_page.get_companies()
        transfer_form = game.TransferForm(self.browser)
        transfer_form.amount(cpr['detail']).send_keys(42)
        for label in transfer_form.labels(cpr['detail']):
            if label.get_attribute('for') == 'target-NYC':
                self.story('She sees that the label is in company colors')
                self.assertIn('bg-black', label.get_attribute('class'))
                self.assertIn('fg-amber-200', label.get_attribute('class'))
                label.click()
                break
        else: # pragma: no cover
            self.fail('Could not find the NYC in the transfer form')
        transfer_form.transfer_button(cpr['detail']).click()

        self.story('Money has been transfered between the players')
        cpr, nyc = game_page.get_companies()
        self.assertEqual(cpr['cash'].text, '58')
        self.assertEqual(nyc['cash'].text, '142')
        self.assertEqual(game_page.bank_cash.text, '11800')

    def test_company_cannot_transfer_money_to_self(self):
        self.story('Alice is a user who starts a new game with a company')
        game_uuid = self.create_game()
        self.create_company(game_uuid, 'B&O', cash=23)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

        self.story("There is no option for B&O on the B&O's transfer section")
        bno = game_page.get_companies()[0]
        bno['elem'].click()

        transfer_form = game.TransferForm(self.browser)
        bno = game_page.get_companies()[0] # Get DOM updates
        self.assertEqual(['Bank'],
            [label.text for label in transfer_form.labels(bno['detail'])])

    def test_after_company_transfers_money_detail_section_remains_open(self):
        self.story('Alice is a user who starts a new game with a company')
        game_uuid = self.create_game(cash=11977)
        self.create_company(game_uuid, 'B&O', cash=23)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

        self.story('She transfers some money to the bank')
        company = game_page.get_companies()[0]
        company['elem'].click()

        transfer_form = game.TransferForm(self.browser)
        company = game_page.get_companies()[0]
        transfer_form.amount(company['detail']).send_keys('3\n')

        self.story('Money has been transfered')
        company = game_page.get_companies()[0]
        self.assertEqual(game_page.bank_cash.text, '11980')
        self.assertEqual(company['cash'].text, '20')

        self.story('The detail section is still visible')
        self.assertIsNotNone(company['detail'])
