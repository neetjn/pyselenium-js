"""
Test example web app events.
"""

from unittest import TestCase
from warnings import warn

import time
import re

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

    @property
    def counter_label(self):
        """
        :Description: Returns the counter label.
        :return: WebElement
        """
        return self.browser.find_element_by_css_selector('h1.logo.ng-binding')


class EventTest(TestCase):

    def setUp(self):
        self.page = MyPage(browser=webdriver.PhantomJS())
        self.page.browser.get('http://localhost:3000')

    def test_trigger_single_event(self):
        """Test: Trigger click event on button, validate dispatched"""
        regex = '([0-9]{1,3})'
        original = eval(re.findall(regex, self.page.counter_label.text)[0])
        self.page.js.trigger_event(
            element=self.page.add_counter_button,
            event='click'
        )
        for i in range(10):
            if (original == eval(re.findall(regex, self.page.counter_label.text)[0])):
                time.sleep(1)
        modified = eval(re.findall(regex, self.page.counter_label.text)[0])
        self.assertEqual(
            modified, original+1,
            'Counter label was not modified as expected; %s clicks' % modified
        )

    def test_trigger_multiple_events(self):
        """Test: Trigger click event on button twice, validate dispatched"""
        regex = '([0-9]{1,3})'
        original = eval(re.findall(regex, self.page.counter_label.text)[0])
        self.page.js.trigger_event(
            element=self.page.add_counter_button,
            event=('click', 'click')
        )
        for i in range(10):
            if (original == eval(re.findall(regex, self.page.counter_label.text)[0])):
                time.sleep(1)
        modified = eval(re.findall(regex, self.page.counter_label.text)[0])
        self.assertEqual(
            modified, original+2,
            'Counter label was not modified as expected; %s clicks' % modified
        )

    def tearDown(self):
        self.page.exit()                 
