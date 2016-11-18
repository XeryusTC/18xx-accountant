# -*- coding: utf-8 -*-
from .base import FunctionalTestCase

class HomePageTest(FunctionalTestCase):
    def test_create_game(self):
        # Alice is a user who visits the website
        self.browser.get(self.live_server_url)
        # She sees that the title of the browser contains '18xx Accountant'
        self.assertEqual(self.browser.title, '18xx Accountant')

        self.fail ('Finish test')
