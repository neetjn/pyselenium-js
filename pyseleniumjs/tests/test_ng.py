"""
Test example web app angularjs bindings.
"""

from unittest import TestCase
from warnings import warn
from uuid import uuid4

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
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
    def binded_elements(self):
        """
        :Description: Returns all elements binded to a scope or controller property.
        :return: [WebElement, ...]
        """
        return self.browser.find_elements_by_css_selector('.ng-binding')

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

    @property
    def rand_id(self):
        """
        :Description: 
        :return: basestring
        """
        return str(uuid4())

    def test_ng_debugging(self):
        """Test: Enable angular debugging and verify binded elements"""
        self.page.js.ng_enable_debugging()
        WebDriverWait(self.page.browser, 5).until(EC.presence_of_element_located((By.ID, 'app')))
        self.page.js.trigger_event(
            element=self.page.user_name_field,
            event='focus'
        )  # wait for page reload
        self.assertGreater(
            len(self.page.binded_elements), 0,
            'Expected at least one binded element found none'
        )

    def test_toggle_class(self):
        """Test: Toggle blass on DOM and verify changes"""
        check = self.rand_id
        self.page.js.ng_toggle_class(
            element=self.page.add_user_button,
            target=check
        )
        self.assertIn(
            check, self.page.js.get_attribute(
                element=self.page.add_user_button,
                attribute='class'
            ), 'Expected class to contain "%s" found "%s"' % (
                check, self.page.js.get_attribute(
                    element=self.page.add_user_button,
                    attribute='class'
                )
            )
        )

    def test_scope_get_prop(self):
        """Test: Modify DOM binded to scope and observe changes"""
        check = self.rand_id
        self.page.user_name_field.send_keys(check)
        self.assertEqual(
            self.page.js.ng_get_scope_property(
                element=self.page.user_name_field,
                prop='name'
            ), check, 'Expected "%s" found "%s"' % (check, self.page.js.ng_get_scope_property(
                element=self.page.user_name_field,
                prop='name'
            ))
        )

    def test_scope_set_prop(self):
        """Test: Modify angular scope and observe changes in binded DOM"""
        self.assertEqual(
            self.page.js.ng_get_scope_property(
                element=self.page.user_name_field,
                prop='name'
            ), '', 'Expected scope value to be "", found "%s"' % self.page.js.ng_get_scope_property(
                element=self.page.user_name_field,
                prop='name'
            )
        )
        check = self.rand_id
        self.page.js.ng_set_scope_property(
            element=self.page.user_name_field,
            prop='name',
            value=check
        )  # set scope property
        self.assertEqual(
            self.page.js.ng_get_scope_property(
                element=self.page.user_name_field,
                prop='name'
            ), check, 'Expected scope value to be "%s" found "%s"' % (
                check, self.page.js.ng_get_scope_property(
                    element=self.page.user_name_field,
                    prop='name'
                )
            )
        )

    def test_scope_func_call(self):
        """Test: Invoke `removeUser` from scope and observe changes on page"""
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

    def tearDown(self):
        self.page.exit()                 
