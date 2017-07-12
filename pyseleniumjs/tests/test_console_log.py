"""
Test example web app console logging.
"""

from unittest import TestCase
from warnings import warn
import json

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from .. import E2EJS


class Page(object):

    def __init__(self, browser):
        self.browser = browser  # specify reference to browser instance
        self.browser.implicitly_wait(10)  # poll for 10 seconds
        self.js = E2EJS(browser=browser)  # instantiate instance of jslib

    def exit(self):
        try:
            self.browser.stop_client()
        except (WebDriverException, AttributeError):
            warn('Assumed use of a local webdriver')
        finally:
            self.browser.quit()


class MyPage(Page):

    @property
    def add_counter_button(self):
        """
        :Description: Returns the counter increment button.
        :return: WebElement
        """
        return self.browser.find_element_by_css_selector('button[ng-click="incrementClicked()"]')


class ConsoleTest(TestCase):

    def setUp(self):
        self.page = MyPage(browser=webdriver.PhantomJS())
        self.page.browser.get('http://localhost:3000')

    def test_set_get_property(self):
        """Test: Enable browser logging, invoke a console log, verify store"""
        self.page.js.console_logger()  # enable console logging
        self.page.add_counter_button.click()  # increment counter
        logs = json.loads(self.page.js.console_dump())
        self.assertEqual(
            len(logs['logs']), 1,
            'Expected one log found "%s"' % json.dumps(logs['logs'])
        )

    def tearDown(self):
        self.page.exit()                 