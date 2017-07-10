"""
Test example web app angularjs bindings.
"""

from unittest import TestCase
from warnings import warn
from uuid import uuid4 as uuid

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
    def add_user_button(self):
        """
        :Description: Returns the user creation button.
        :return: WebElement
        """
        return self.browser.find_element_by_css_selector('button[ng-click="addUser()"]')

    @property
    def user_name_field(self):
        """
        :Description: Returns the user name field.
        :return: WebElement
        """
        return self.browser.find_element_by_css_selector('input[ng-model="name"]')

    @property
    def user_profession_field(self):
        """
        :Description: Returns the user profession field.
        :return: WebElement
        """
        return self.browser.find_element_by_css_selector('input[ng-model="field"]')

    @property
    def user_list(self):
        """
        :Description: Returns the list of available users.
        :return: [WebElement, ...]
        """
        return self.browser.find_elements_by_css_selector('li[ng-repeat="user in ctrl.users"]')

    def user_remove_button(self, user):
        """
        :Description: Returns the removal button of the specified user.
        :param user: User with remove button.
        :type user: WebElement
        :return: WebElement
        """
        return user.find_element_by_css_selector('button[ng-click="removeUser($index)"]')


class AngularTest(TestCase):

    def setUp(self):
        self.page = MyPage(browser=webdriver.PhantomJS())
        self.page.browser.get('http://localhost:3000')

    @staticmethod
    @property
    def rand_id():
        """
        :Description: 
        :return: basestring
        """
        return str(uuid4()).replace('-', '')

    def test_scope_get_val(self):
        """Test: Set and read from scope model manipulated by DOM."""
        check = self.rand_id
        self.page.user_name_field.send_keys(name)
        self.assertEqual(
            self.page.js.ng_get_scope_property(
                element=self.page.user_name_field,
                prop='name'
            ), check, 'Expected "%s" found "%s"' %  self.page.js.ng_get_scope_property(
                element=self.page.user_name_field,
                prop='name'
            )
        )

    def test_scope_set_val(self):
        """Test: ..."""
        self.assertEqual(
            self.page.js.ng_get_scope_property(
                element=self.page.user_name_field,
                prop='name'
            ), ''
        )
        self.assert

    def test_scope_func_call(self):
        """Test: Remove user from list of users by invoking scope function directly."""
        remove_button = self.page.user_remove_button(
            user=self.page.user_list[0]
        )  # get removal button of first user in list
        self.page.js.ng_call_scope_function(
            element=remove_button,
            func='$parent.removeUser',
            params=[0]
        )  # remove user from list
        self.page.js.ng_call_scope_function(
            element=remove_button,
            func='$apply',
            params=[]
        )  # apply changes and trigger digest
        self.assertEqual(
            len(self.page.user_list), 0,
            'Expected no users found "%s"' % len(self.page.user_list)
        )

    def test_ctrl_prop_get_set(self):
        pass

    def tearDown(self):
        self.page.exit()                 
