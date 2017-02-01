# -*- coding: utf-8 -*-
import unittest
from .base import FunctionalTestCase
from .pages import game

class CreatePlayerTests(FunctionalTestCase):
    def test_can_create_player(self):
        # Alice is a user who starts a new game
        self.browser.get(self.live_server_url)
        page = game.Homepage(self.browser)
        page.start_button.click()
        self.assertRegex(self.browser.current_url, r'/en/game/([^/]+)/$')

        # She sees an add player button
        menu = game.MenuSection(self.browser)
        menu.add_player.click()

        # She lands on a add player page
        add_player = game.AddPlayerPage(self.browser)
        self.assertRegex(self.browser.current_url,
            r'/en/game/([^/]+)/add-player/$')
        self.assertEqual(add_player.header.text, 'Add player')

        # She enters her name and a starting amount of cash
        add_player.name.clear()
        add_player.name.send_keys('Alice')
        add_player.cash.clear()
        add_player.cash.send_keys('700')
        add_player.add_button.click()

        # Her name appears in the player list on the game page
        players = game.PlayerSection(self.browser)
        self.assertRegex(self.browser.current_url, r'/en/game/([^/]+)/$')

        player_list = players.get_players()
        self.assertEqual(len(player_list), 1)
        self.assertEqual(player_list[0]['name'].text, 'Alice')
        self.assertEqual(player_list[0]['cash'].text, '700')
