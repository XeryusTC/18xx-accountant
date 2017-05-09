# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import inspect
import signal
from pytractor import webdriver
from unipath import Path

try:
    from . import remote
except ImportError:
    pass # Ignore error, we're most likely testing locally/running CI
from core import factories
from core import models

DEFAULT_WAIT = 3
SCREEN_DUMP_LOCATION = Path('screendumps')

class FunctionalTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.against_staging = False
        cls._get_options()

        if not cls.against_staging:
            super(FunctionalTestCase, cls).setUpClass()
            cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if not cls.against_staging:
            super(FunctionalTestCase, cls).tearDownClass()

    def setUp(self):
        self.webdriver = webdriver.Chrome
        self.browser = self.webdriver(test_timeout=DEFAULT_WAIT)
        self.browser.implicitly_wait(DEFAULT_WAIT)
        self.browser.set_script_timeout(DEFAULT_WAIT)

        if self.against_staging:
            from . import remote
            remote.flushdb(self.ansible_dir, self.inventory)

        if self.verbosity >= 2:
            print() # Start stories on a fresh line

    def tearDown(self):
        if self._test_has_failed(): # pragma: no cover
            SCREEN_DUMP_LOCATION.mkdir()
            for ix, handle in enumerate(self.browser.window_handles):
                self.browser.switch_to_window(handle)
                filename = self._get_filename(ix)
                self._take_screenshot(filename + '.png')
                self._dump_html(filename + '.html')
        self.browser.quit()

    def story(self, text):
        if self.verbosity >= 2:
            print('-', text)

    def create_game(self, **kwargs):
        if self.against_staging:
            return remote.creategame(self.ansible_dir, self.inventory,
                **kwargs)[1]
        else:
            game = factories.GameFactory.create(**kwargs)
            return str(game.pk)

    def create_player(self, game_uuid, name, **kwargs):
        if self.against_staging:
            return remote.createplayer(self.ansible_dir, self.inventory,
                game_uuid, name, **kwargs)[1]
        else:
            game = models.Game.objects.get(pk=game_uuid)
            company = factories.PlayerFactory.create(game=game, name=name,
                **kwargs)
            return str(company.pk)

    def create_company(self, game_uuid, name, **kwargs):
        if 'text' in kwargs:
            kwargs['text_color'] = kwargs['text']
            del kwargs['text']
        if 'background' in kwargs:
            kwargs['background_color'] = kwargs['background']
            del kwargs['background']
        if self.against_staging:
            return remote.createcompany(self.ansible_dir, self.inventory,
                game=game_uuid, name=name, **kwargs)[1]
        else:
            game = models.Game.objects.get(pk=game_uuid)
            company = factories.CompanyFactory.create(game=game, name=name,
                **kwargs)
            return str(company.pk)

    def create_player_share(self, owner, company, **kwargs):
        if self.against_staging:
            return remote.createplayershare(self.ansible_dir, self.inventory,
                owner=owner, company=company, **kwargs)[1]
        else:
            owner = models.Player.objects.get(pk=owner)
            company = models.Company.objects.get(pk=company)
            share = factories.PlayerShareFactory.create(owner=owner,
                company=company, **kwargs)
            return str(share.pk)

    def create_company_share(self, owner, company, **kwargs):
        if self.against_staging:
            return remote.createcompanyshare(self.ansible_dir, self.inventory,
                owner=owner, company=company, **kwargs)[1]
        else:
            owner = models.Company.objects.get(pk=owner)
            company = models.Company.objects.get(pk=company)
            share = factories.CompanyShareFactory.create(owner=owner,
                company=company, **kwargs)
            return str(share.pk)

    def verify_player(self, player, name=None, cash=None,
                      shares=None): # pragma: no cover
        if name is not None:
            self.assertEqual(player['name'].text, name)
        if cash is not None:
            self.assertEqual(player['cash'].text, str(cash))
        if shares is not None:
            self.assertSequenceEqual(shares,
                [s.text for s in player['shares']])

    def verify_company(self, company, name=None, cash=None, share_count=None,
                       ipo_shares=None, bank_shares=None, shares=None,
                       text=None, background=None): # pragma: no cover
        if name is not None:
            self.assertEqual(company['name'].text, name)
        if cash is not None:
            self.assertEqual(company['cash'].text, str(cash))
        if share_count is not None:
            self.assertEqual(company['share_count'].text, str(share_count))
        if ipo_shares is not None:
            self.assertEqual(company['ipo_shares'].text, str(ipo_shares))
        if bank_shares is not None:
            self.assertEqual(company['bank_shares'].text, str(bank_shares))
        if shares is not None:
            self.assertSequenceEqual(shares,
                [s.text for s in company['shares']])
        if text is not None:
            self.assertin('fg-' + text, company['elem'].get_attribute('class'))
        if background is not None:
            self.assertin('bg-' + background,
                company['elem'].get_attribute('class'))

    def _test_has_failed(self): # pragma: no cover
        for method, error in self._outcome.errors:
            if error:
                return True
        return False

    def _take_screenshot(self, filename): # pragma: no cover
        print('Screenshot to', filename)
        self.browser.get_screenshot_as_file(filename)

    def _dump_html(self, filename): # pragma: no cover
        print('Dumping HTML to', filename)
        filename.write_file(self.browser.page_source)

    def _get_filename(self, windowid): # pragma: no cover
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return Path(SCREEN_DUMP_LOCATION, \
            '{cls}.{method}-window{windowid}-{timestamp}'.format(
                cls=self.__class__.__name__, method=self._testMethodName,
                windowid=windowid, timestamp=timestamp))

    @classmethod
    def _get_options(cls): # pragma: no cover
        """Get value of verbosity level argument given to manage.py"""
        # Code taken from http://stackoverflow.com/questions/27456881/
        for s in reversed(inspect.stack()):
            options = s[0].f_locals.get('options')
            if isinstance(options, dict):
                cls.verbosity = int(options['verbosity'])
                if options['staging']:
                    cls.server_url = 'http://' + options['staging'][0]
                    cls.inventory = Path(options['staging'][1])
                    cls.ansible_dir = Path(options['ansible_directory'])
                    cls.against_staging = True
