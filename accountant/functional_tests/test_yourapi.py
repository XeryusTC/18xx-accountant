# -*- coding: utf-8 -*-
import requests

from .base import FunctionalTestCase
from .pages import game

class YourapiTests(FunctionalTestCase):
    def test_creates_game_on_yourapi(self):
        self.browser.get(self.server_url)
        page = game.Homepage(self.browser)
        page.start_button.click()
        self.assertRegex(self.browser.current_url, r'/game/([^/]+)$')
        uuid = self.browser.current_url.split('/')[-1]
        url = 'https://accountant-18xx.draft.yourapi.io/18xx/accountant/' \
            'game/' + uuid
        response = requests.get(url, headers={'Authorization': self.auth_token})
        self.assertEqual(200, response.status_code, response.text)
