"""
Test example web app scrolling.
"""

from unittest import TestCase
from warnings import warn

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
    def header(self):
        """
        :Description: Returns the header of the web app.
        :return: WebElement
        """
        return self.browser.find_element_by_css_selector('header')

    @property
    def footer(self):
        """
        :Description: Returns the footer of the web app.
        :return: WebElement
        """
        return self.browser.find_element_by_css_selector('footer')

    @property
    def user_cards(self):
        """
        :Description: Returns a list of user cards.
        :return [WebElement, ...]
        """
        return self.browser.find_elements_by_css_selector('li[ng-repeat="user in ctrl.users"]')


class ScrollingTest(TestCase):

    def setUp(self):
        self.page = MyPage(browser=webdriver.PhantomJS())
        self.page.browser.get('http://localhost:3000')
        self.page.browser.set_window_size(800, 600)

    def test_scroll_offset(self):
        """Test: Scroll to bottom of page and ensure page y offset has been incremented"""
        initial_offsets = self.page.js.get_scrolling_offsets()
        self.assertEqual(
            initial_offsets['y'], 0,
            'Expected an initial Y offset of 0 found {}'.format(
                initial_offsets['y']
            )
        )
        for i in range(10):
            self.page.add_counter_button.click()  # add components to increase page height
        self.page.js.scroll_into_view(element=self.page.user_cards[-1])
        updated_offsets = self.page.js.get_scrolling_offsets()
        self.assertGreater(
            updated_offsets['y'], 0,
            'Expected Y to be greater than 0 found {}'.format(
                updated_offsets['y']
            )
        )

    def tearDown(self):
        self.page.exit()                 
