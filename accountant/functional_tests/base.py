# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import inspect
import signal
from pytractor import webdriver
from unipath import Path

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
        self.browser = self.webdriver()
        self.browser.implicitly_wait(DEFAULT_WAIT)

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
                    cls.inventory = options['staging'][1]
                    cls.ansible_dir = options['ansible_directory']
                    cls.against_staging = True
