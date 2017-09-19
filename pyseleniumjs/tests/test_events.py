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

    @property
    def add_user_button(self):
        """
        :Description: Returns the counter increment button.
        :return: WebElement
        """
        return self.browser.find_element_by_css_selector('button[ng-click="addUser()"]')

    @property
    def user_cards(self):
        """
        :Description: Returns a list of user cards.
        :return [WebElement, ...]
        """
        return self.browser.find_elements_by_css_selector('li[ng-repeat="user in ctrl.users"]')


class EventTest(TestCase):

    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.page = MyPage(browser=webdriver.Chrome(chrome_options=chrome_options))
        self.page.browser.get('http://localhost:3000')

    def test_trigger_single_event(self):
        """Test: Trigger click event on button, validate dispatched"""
        regex = '([0-9]{1,3})'
        self.page.browser.save_screenshot('jas2.png')
        original = eval(re.findall(regex, self.page.counter_label.text)[0])
        self.page.js.trigger_event(
            element=self.page.add_counter_button,
            event='click'
        )
        for i in range(10):
            if (original == eval(re.findall(regex, self.page.counter_label.text)[0])):
                time.sleep(1)
            else:
                break
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
            else:
                break
        modified = eval(re.findall(regex, self.page.counter_label.text)[0])
        self.assertEqual(
            modified, original+2,
            'Counter label was not modified as expected; %s clicks' % modified
        )

    def test_trigger_multiple_events_multiple_elements(self):
        """Test: Trigger click event on two buttons twice, validate dispatched"""
        regex = '([0-9]{1,3})'
        num_counter_original = eval(re.findall(regex, self.page.counter_label.text)[0])
        num_users_original = len(self.page.user_cards)
        self.page.js.trigger_event(
            element=(self.page.add_counter_button, self.page.add_user_button),
            event=('click', 'click')
        )
        for i in range(10):
            if (num_counter_original == eval(re.findall(regex, self.page.counter_label.text)[0])):
                time.sleep(1)
            else:
                break
        num_counter_modified = eval(re.findall(regex, self.page.counter_label.text)[0])
        self.assertEqual(
            num_counter_modified, num_counter_original+2,
            'Counter label was not modified as expected; %s clicks' % num_counter_modified
        )
        self.assertEqual(
            len(self.page.user_cards), num_users_original+2,
            'Expected %s user cards found %s' % (
                num_users_original+2, len(self.page.user_cards)
            )
        )

    def tearDown(self):
        self.page.exit()                 
