===============
Getting Started
===============

Sample Usage
============

The following code example features a simple implementation using page objects:

.. code-block:: python

    from selenium import webdriver
    from pyseleniumjs import E2EJS


    class Page(object):

        def __init__(self, browser):
            self.browser = browser  # specify reference to browser instance
            self.js = E2EJS(browser=browser)  # instantiate instance of js driver

        def exit(self):
            self.browser.quit()


    class MyPage(Page):

        @property
        def div_with_text(self):
            return self.browser.find_element_by_css_selector('div.withText')


    page = MyPage(browser=webdriver.Firefox())

    # selenium bindings cannot pull text from divs
    # selenium bindings try to pull the text element property
    print page.div_with_text.text
    >> ''

    # js driver will try to extract the innerText property
    print page.js.get_text(element=page.div_with_text)
    >> 'foobar'

    # alternatively can pull innerHTML
    print page.js.get_raw_text(element=page.div_with_text)
    >> '<span>foobar</span>'

    page.exit()

Example Explained
=================

...
