# -*- coding: utf-8 -*-
from .base import FunctionalTestCase
from .pages import game

class CreatePlayerTests(FunctionalTestCase):
    """Tests for creating players at the start of a game"""
    def test_can_create_player(self):
        self.story('Alice is a user who starts a new game')
        self.browser.get(self.server_url)
        page = game.Homepage(self.browser)
        page.start_button.click()
        self.assertRegex(self.browser.current_url, r'/game/([^/]+)$')

        self.story('She sees an add player button')
        game_page = game.GamePage(self.browser)
        game_page.add_player_link.click()

        self.story('She lands on a add player page')
        add_player = game.AddPlayerPage(self.browser)
        self.assertRegex(self.browser.current_url,
            r'/game/([^/]+)/add-player$')
        self.assertEqual(add_player.header.text, 'Add player')
        self.assertEqual(self.browser.title, 'Add player')

        self.story('She enters her name and a starting amount of cash')
        add_player.name.clear()
        add_player.name.send_keys('Alice')
        add_player.cash.clear()
        add_player.cash.send_keys('700')
        add_player.add_button.click()

        self.story('Her name appears in the player list on the game page')
        self.assertRegex(self.browser.current_url, r'/game/([^/]+)$')

        player_list = game_page.get_players()
        self.assertEqual(len(player_list), 1)
        self.assertEqual(player_list[0]['name'].text, 'Alice')
        self.assertEqual(player_list[0]['cash'].text, '700')

    def test_cannot_create_duplicate_player(self):
        self.story('Alice is a user who starts a new game')
        self.browser.get(self.server_url)
        page = game.Homepage(self.browser)
        page.start_button.click()

        self.story('She goes to add a player')
        game_page = game.GamePage(self.browser)
        game_page.add_player_link.click()
        add_player = game.AddPlayerPage(self.browser)
        add_player.name.clear()
        add_player.cash.clear()
        add_player.name.send_keys('Alice')
        add_player.cash.send_keys('700\n')
        self.story('The new player is added to the game')
        player_list = game_page.get_players()
        self.assertEqual(len(player_list), 1)
        self.assertEqual(player_list[0]['name'].text, 'Alice')
        self.assertEqual(player_list[0]['cash'].text, '700')

        self.story('She goes to add another player')
        game_page.add_player_link.click()
        add_player.name.clear()
        add_player.cash.clear()
        add_player.name.send_keys('Alice')
        add_player.cash.send_keys('100\n')
        self.story('She stays on the same page and sees an error message')
        self.assertRegex(self.browser.current_url,
            r'/game/([^/]+)/add-player$')
        self.assertIn('There is already a player with this name in your game',
            add_player.error_list.text)

    def test_can_return_to_game_page_from_add_player_page(self):
        self.story('Alice is a user who starts a new game')
        self.browser.get(self.server_url)
        page = game.Homepage(self.browser)
        page.start_button.click()

        self.story('She goes to the add player screen')
        game_page = game.GamePage(self.browser)
        game_page.add_player_link.click()
        self.assertRegex(self.browser.current_url,
            r'/game/([^/]+)/add-player$')

        self.story("She doesn't want to add a player and clicks the back "
            "button")
        add_player = game.AddPlayerPage(self.browser)
        add_player.back.click()
        self.assertEqual(self.browser.title, '18xx Accountant')
        self.assertRegex(self.browser.current_url, r'/game/([^/]+)$')
        self.assertEqual(game_page.get_players(), [])

    def test_creating_player_with_cash_decreases_bank_cash(self):
        self.story('Alice is a user who starts a new game')
        self.browser.get(self.server_url)
        page = game.Homepage(self.browser)
        page.bank_cash.clear()
        page.bank_cash.send_keys('1000\n')

        self.story('She goes to add a player')
        game_page = game.GamePage(self.browser)
        game_page.add_player_link.click()

        add_player = game.AddPlayerPage(self.browser)
        add_player.name.clear()
        add_player.cash.clear()
        add_player.name.send_keys('Alice')
        add_player.cash.send_keys('400\n')

        self.story('On the game page she sees that the bank size has reduced')
        self.assertEqual(game_page.bank_cash.text, '600')

    def test_players_are_sorted_alphabetically(self):
        self.story('Alice is a user who starts a new game')
        self.browser.get(self.server_url)
        page = game.Homepage(self.browser)
        page.start_button.click()

        self.story('She goes to add two players')
        game_page = game.GamePage(self.browser)
        add_player = game.AddPlayerPage(self.browser)
        game_page.add_player_link.click()
        add_player.name.send_keys('Alice\n')
        game_page.add_player_link.click()
        add_player.name.send_keys('Charlie\n')

        self.story('The players should be listed as Alice, Charlie')
        players = game_page.get_players()
        self.assertEqual(['Alice', 'Charlie'],
            [player['name'].text for player in players])

        self.story('She adds a third player')
        game_page.add_player_link.click()
        add_player.name.send_keys('Bob\n')

        self.story('The players should be listed as Alice, Bob, Charlie')
        players = game_page.get_players()
        self.assertEqual(['Alice', 'Bob', 'Charlie'],
            [player['name'].text for player in players])

        self.story('She adds a fourth player')
        game_page.add_player_link.click()
        add_player.name.send_keys('Bert\n')

        self.story('The players should be listed as Alice, Bert, Bob, Charlie')
        players = game_page.get_players()
        self.assertEqual(['Alice', 'Bert', 'Bob', 'Charlie'],
            [player['name'].text for player in players])

        self.story('She adds a fifthplayer')
        game_page.add_player_link.click()
        add_player.name.send_keys('Dave\n')

        self.story('Players are listed as Alice, Bert, Bob, Charlie, Dave')
        players = game_page.get_players()
        self.assertEqual(['Alice', 'Bert', 'Bob', 'Charlie', 'Dave'],
            [player['name'].text for player in players])


class ManagePlayerTests(FunctionalTestCase):
    """Tests for managing player actions during a game"""
    def test_clicking_player_opens_player_detail_section(self):
        self.story('Alice is a user who starts a new game with two players')
        game_uuid = self.create_game()
        self.create_player(game_uuid, 'Alice')
        self.create_player(game_uuid, 'Bob')
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

        self.story('Check that the two players are in the list')
        self.assertCountEqual(['Alice', 'Bob'],
            list(player.text for player in game_page.player_name_list))

        self.story('The player detail sections are both hidden')
        players = game_page.get_players()
        for player in players:
            with self.subTest(player=player['name'].text):
                self.assertIsNone(player['detail'])

        self.story('She clicks the first player and the details appear')
        players[0]['row'].click()
        players = game_page.get_players()  # Get DOM updates
        self.assertIsNotNone(players[0]['detail'])
        self.assertIsNone(players[1]['detail'])

        self.story("She clicks the second player, the first player's details"
            "disappear and the second player's appear")
        players[1]['row'].click()
        players = game_page.get_players()  # Get DOM updates
        self.assertIsNone(players[0]['detail'])
        self.assertIsNotNone(players[1]['detail'])

    def test_clicking_player_closes_company_detail_section(self):
        self.story('Alice is a user who starts a new game')
        game_uuid = self.create_game()
        self.create_player(game_uuid, 'Alice')
        self.create_company(game_uuid, 'PRR')
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

        self.story('She clicks the company to open its detail section')
        player = game_page.get_players()[0]
        company = game_page.get_companies()[0]
        company['elem'].click()

        # Need to retrieve DOM updates first
        company = game_page.get_companies()[0]
        player = game_page.get_players()[0]
        self.assertIsNone(player['detail'])
        self.assertIsNotNone(company['detail'])

        self.story('When she clicks the player the company detail closes')
        player['row'].click()
        player = game_page.get_players()[0]
        company = game_page.get_companies()[0]
        self.assertIsNotNone(player['detail'])
        self.assertIsNone(company['detail'])

    def test_player_can_transfer_money_to_bank(self):
        self.story('Alice is a user who starts a new game')
        game_uuid = self.create_game(cash=11000)
        self.create_player(game_uuid, 'Alice', cash=1000)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

        self.story('Confirm cash amounts')
        player = game_page.get_players()[0]
        self.assertEqual(player['cash'].text, '1000')
        self.assertEqual(game_page.bank_cash.text, '11000')

        self.story("She opens the player's detail view")
        player['row'].click()
        player = game_page.get_players()[0]

        self.story('There is a form that allows her to send money')
        transfer_form = game.TransferForm(self.browser)
        transfer_form.amount(player['detail']).clear()
        transfer_form.amount(player['detail']).send_keys('100')
        for radio in transfer_form.target(player['detail']):
            if radio.get_attribute('value') == 'bank':
                radio.click()
                break
        transfer_form.transfer_button(player['detail']).click()

        self.story("The page reloads and the player's cash amount has lowered")
        player = game_page.get_players()[0]
        self.assertEqual(player['cash'].text, '900')
        self.assertEqual(game_page.bank_cash.text, '11100')

        self.story('Alice goes to transfer money again')
        player['row'].click()
        player = game_page.get_players()[0]  # Get DOM updates
        transfer_form.amount(player['detail']).clear()
        transfer_form.amount(player['detail']).send_keys('10')
        self.story("This time she doesn't select a target, the bank should be"
            ' default')
        transfer_form.transfer_button(player['detail']).click()

        self.story('After the page reloads she has found that the amount has'
            'changed again')
        player = game_page.get_players()[0]
        self.assertEqual(player['cash'].text, '890')
        self.assertEqual(game_page.bank_cash.text, '11110')

    def test_player_can_transfer_money_to_company(self):
        self.story('Alice is a user who starts a new game')
        game_uuid = self.create_game(cash=10500)
        self.create_player(game_uuid, 'Alice', cash=1000)
        self.create_company(game_uuid, 'CPR', cash=500, text='white',
            background='red-700')
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

        self.story('Confirm cash amounts')
        player = game_page.get_players()[0]
        company = game_page.get_companies()[0]
        self.assertEqual(player['cash'].text, '1000')
        self.assertEqual(company['cash'].text, '500')

        self.story("She opens the player's detail view")
        player['row'].click()
        player = game_page.get_players()[0]

        self.story('The form allows her to transfer funds to the CPR')
        transfer_form = game.TransferForm(self.browser)
        transfer_form.amount(player['detail']).clear()
        transfer_form.amount(player['detail']).send_keys('19')
        for label in transfer_form.labels(player['detail']):
            if label.get_attribute('for') == 'target-CPR':
                self.story('She sees that the label is in company colors')
                self.assertIn('fg-white', label.get_attribute('class'))
                self.assertIn('bg-red-700', label.get_attribute('class'))
                self.story('She then selects the company')
                transfer_form.target(label)[0].click()
                break
        else:  # pragma: no cover
            self.fail('No company called CPR found in transfer form')
        transfer_form.transfer_button(player['detail']).click()

        self.story('The Page reloads and money has changed hands')
        player = game_page.get_players()[0]
        company = game_page.get_companies()[0]
        self.assertEqual(player['cash'].text, '981')
        self.assertEqual(company['cash'].text, '519')

    def test_player_can_transfer_money_to_other_player(self):
        self.story('Alice is a user who starts a new game with two players')
        game_uuid = self.create_game()
        self.create_player(game_uuid, 'Alice', cash=530)
        self.create_player(game_uuid, 'Bob', cash=290)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

        self.story('She moves some money from Alice to Bob')
        alice, bob = game_page.get_players()
        alice['row'].click()

        transfer_form = game.TransferForm(self.browser)
        alice, bob = game_page.get_players()
        transfer_form.amount(alice['detail']).clear()
        transfer_form.amount(alice['detail']).send_keys(67)
        for radio in transfer_form.target(alice['detail']):
            if radio.get_attribute('id') == 'target-Bob':
                radio.click()
                break
        else:  # pragma: no cover
            self.fail('Could not find Bob in the transfer form')
        transfer_form.transfer_button(alice['detail']).click()

        self.story('Money has been transfered between the players')
        players = game_page.get_players()
        for player in players:
            with self.subTest(player=player['name'].text):
                if player['name'].text == 'Alice':
                    self.assertEqual(player['cash'].text, '463')
                elif player['name'].text == 'Bob':
                    self.assertEqual(player['cash'].text, '357')

    def test_player_cannot_transfer_money_to_self(self):
        self.story('Alice is a user who starts a new game')
        game_uuid = self.create_game()
        self.create_player(game_uuid, 'Alice')
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

        self.story("There is no option for Alice on Alice's transfer section")
        alice = game_page.get_players()[0]
        alice['row'].click()

        transfer_form = game.TransferForm(self.browser)
        alice = game_page.get_players()[0]
        self.assertEqual(['Bank'],
            [label.text for label in transfer_form.labels(alice['detail'])])

    def test_after_player_transfers_money_detail_section_is_still_open(self):
        self.story('Alice is a user who starts a new game')
        game_uuid = self.create_game(cash=11983)
        self.create_player(game_uuid, 'Alice', cash=17)
        self.browser.get(self.server_url + '/game/' + game_uuid)
        game_page = game.GamePage(self.browser)

        self.story('She transfers some money to the bank')
        player = game_page.get_players()[0]
        player['row'].click()

        transfer_form = game.TransferForm(self.browser)
        player = game_page.get_players()[0]
        transfer_form.amount(player['detail']).send_keys('3\n')

        self.story('Money has been transfered')
        player = game_page.get_players()[0]
        self.assertEqual(game_page.bank_cash.text, '11986')
        self.assertEqual(player['cash'].text, '14')

        self.story('The detail section is still visible')
        self.assertIsNotNone(player['detail'])
