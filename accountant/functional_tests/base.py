# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from unipath import Path

DEFAULT_WAIT = 3
SCREEN_DUMP_LOCATION = Path('screendumps')

class FunctionalTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.webdriver = webdriver.PhantomJS
        self.browser = self.webdriver()
        self.browser.implicitly_wait(DEFAULT_WAIT)

    def tearDown(self):
        if self._test_has_failed(): # pragma: no cover
            SCREEN_DUMP_LOCATION.mkdir()
            for ix, handle in enumerate(self.browser.window_handles):
                self.browser.switch_to_window(handle)
                filename = self._get_filename(ix)
                self._take_screenshot(filename + '.png')
                self._dump_html(filename + '.html')
        self.browser.quit()

    def _test_has_failed(self):
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
