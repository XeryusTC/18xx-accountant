# -*- coding: utf-8 -*-
import unittest
from .base import FunctionalTestCase
from .pages import game

class CreatePlayerTests(FunctionalTestCase):
    """Tests for creating players at the start of a game"""
    def test_can_create_player(self):
        self.story('Alice is a user who starts a new game')
        self.browser.get(self.live_server_url)
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

        self.story('The game field is not visible')
        #self.assertEqual(add_player.game.get_attribute('type'), 'hidden')
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
        self.browser.get(self.live_server_url)
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
        self.browser.get(self.live_server_url)
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
        self.browser.get(self.live_server_url)
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


class ManagePlayerTests(FunctionalTestCase):
    """Tests for managing player actions during a game"""
    def test_clicking_player_opens_player_detail_section(self):
        self.story('Alice is a user who starts a new game')
        self.browser.get(self.live_server_url)
        homepage = game.Homepage(self.browser)
        homepage.start_button.click()

        self.story('She adds two players')
        game_page = game.GamePage(self.browser)
        game_page.add_player_link.click()
        add_player = game.AddPlayerPage(self.browser)
        add_player.name.clear()
        add_player.name.send_keys('Alice\n')

        game_page.add_player_link.click()
        add_player.name.clear()
        add_player.name.send_keys('Bob\n')

        self.story('Check that the two players are in the list')
        self.assertSequenceEqual(['Alice', 'Bob'],
            list(player.text for player in game_page.player_name_list))

        self.story('The player detail sections are both hidden')
        players = game_page.get_players()
        for player in players:
            with self.subTest(player=player['name'].text):
                self.assertIsNone(player['detail'])

        self.story('She clicks the first player and the details appear')
        players[0]['row'].click()
        players = game_page.get_players() # Get DOM updates
        self.assertIsNotNone(players[0]['detail'])
        self.assertIsNone(players[1]['detail'])

        self.story("She clicks the second player, the first player's details"
            "disappear and the second player's appear")
        players[1]['row'].click()
        players = game_page.get_players() # Get DOM updates
        self.assertIsNone(players[0]['detail'])
        self.assertIsNotNone(players[1]['detail'])

    def test_clicking_player_closes_company_detail_section(self):
        self.story('Alice is a user who starts a new game')
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
        add_company.name.send_keys('PRR\n')

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
