"""
Test example web app property manipulation.
"""

from unittest import TestCase
from warnings import warn

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from pyseleniumjs import E2EJS


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
    def add_user_button(self):
        """
        :Description: Returns the user creation button.
        :return: WebElement
        """
        return self.browser.find_element_by_css_selector('button[ng-click="addUser()"]')


class PropertyTest(TestCase):

    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        self.page = MyPage(browser=webdriver.Chrome(chrome_options=chrome_options))
        self.page.browser.get('http://localhost:3000')

    def test_set_get_property(self):
        """Test: Set disabled property of button, ensure property set correctly"""
        self.page.js.set_property(
            element=self.page.add_user_button,
            prop='disabled',
            value=True
        )
        self.assertTrue(
            self.page.js.get_property(
                element=self.page.add_user_button,
                prop='disabled'
            ),
            'DOM disabled property was not set as expected'
        )
        self.assertEqual(
            self.page.js.get_attribute(
                element=self.page.add_user_button,
                attribute='disabled'
            ), '', 'DOM attribute disabled not created after setting property disabled'
        )

    def tearDown(self):
        self.page.exit()
