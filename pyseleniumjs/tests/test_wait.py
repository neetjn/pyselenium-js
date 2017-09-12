"""
Test example web app wait status.
"""

from unittest import TestCase
from warnings import warn
import json
import re
import time

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

    @property
    def counter_label_selector(self):
        return 'h1.logo.ng-binding'


class WaitTest(TestCase):

    def setUp(self):
        self.page = MyPage(browser=webdriver.PhantomJS())
        self.page.browser.get('http://localhost:3000')

    def test_wait_single_element(self):
        """Test: Enable wait, trigger condition, verify watcher status"""
        handle = self.page.js.wait(
            '$el.innerText.match(/([0-9]{1,3})/g)[0] == 1', 500,
            self.page.counter_label
        )
        self.page.add_counter_button.click()  # increment counter label
        for i in range(10):
            if not self.page.js.wait_status(handle=handle):
                time.sleep(1)
        self.assertTrue(
            self.page.js.wait_status(handle=handle),
            'Wait status was not updated as expected "%s"' % (
                self.page.counter_label.text
            )
        )

    def test_wait_multi_elements(self):
        """Test: Enable wait, trigger condition, verify watcher status"""
        handle = self.page.js.wait(
            '$el[0].innerText.match(/([0-9]{1,3})/g)[0] == 1 && \
             $el[1].innerText.match(/([0-9]{1,3})/g)[0] == 1', 500,
            self.page.counter_label, self.page.counter_label_selector
        )
        self.page.add_counter_button.click()  # increment counter label
        for i in range(10):
            if not self.page.js.wait_status(handle=handle):
                time.sleep(1)
        self.assertTrue(
            self.page.js.wait_status(handle=handle),
            'Wait status was not updated as expected "%s"' % (
                self.page.counter_label.text
            )
        )

    def tearDown(self):
        self.page.exit()                 