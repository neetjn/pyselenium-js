# pyselenium-js
[![build](https://travis-ci.org/neetVeritas/pyselenium-js.svg?branch=master)](https://travis-ci.org/neetVeritas/pyselenium-js)
[![PyPI version](https://badge.fury.io/py/pyseleniumjs.svg)](https://badge.fury.io/py/pyseleniumjs)

Lightweight python module to execute frequently used javascript functionality on a Selenium webdriver.

### About
**pyselenium-js** is a very simple, lightweight module that helps relieve some of the burden of E2E testing with the official Selenium bindings.
The official Selenium bindings operate in the most natural way a user would operate against a given web page.
The problem with this, is with more advanced and modern websites, these bindings may not always work as expected on certain/custom DOMs.

An example of this being a div tag taking keyboard input, where div tags do not support the `onfocus` event listener by design -- and the selenium bindings invoke this before attempting to send input to the target DOM.

### Usage
This project was created using Python 2.7.x and Selenium 3.0.0b3. **pyselenium-js** can be installed using pip like so,

```bash
pip install pyseleniumjs
```

Simply import `E2EJS` from `pyselenium-js`.
If you're using page objects or factories, you can instantiate a new instance in your object's sontructor passing your target web driver.

```python
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from warnings import warn
from pyseleniumjs import E2EJS


class Page(object):

  def __init__(self, browser):
    self.browser = browser  # specify reference to browser instance
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
  def div_with_text(self):
    return self.browser.find_element_by_css_selector('div.something')

page = MyPage(browser=webdriver.Firefox())

print page.div_with_text.text  # bindings cannot pull text from divs
print page.js.get_text(element=page.div_with_text)
page.exit()
```

**pyselenium-js** also contains angular.js (1.x) and Angular support, including scope and controller access for angular debugging.

```python
class MyPage(Page):

  @property
  def ng_elements(self):
    return self.browser.find_elements_by_css_selector('li[ng-repeat]')

  @property
  def ng2_elements(self):
    return self.browser.find_elements_by_css_selector('li.ng2[ng-repeat]')

page = Page(browser=webdriver.Firefox())

for el in page.ng_elements:
  page.js.ng_toggle_class(element=el, target='active')
  page.js.ng_set_scope_property(element=el, prop='data.views', value=None)
  page.js.ng_set_scope_property(element=el, prop='data.viewed', value=False)

for el in page.ng2_elements:
  page.js.ng2_set_component_property(element=el, prop='data.likes', value=0)
  page.js.ng2_set_component_property(element=el, prop='data.viewed', value=False)
```

### Testing

All module related e2e tests are in the `pyselenium/tests` subdirectory. To setup your environment run `make setup`. To stand up the mock application, run `make app`. This will serve the application on `localhost:3000`. To run the test suite, use `make tests`.

*Note as of this time, tests for the Angular 2 bindings are not yet available.*

Requirements:
* Chromium 60
* ChromeDriver 2.32.3
* Node.js 6
* Python 2.7
* Pip

### Contributing

* Make sure your code passes our lint and e2e tests.
* Any new features added must also be tested in the `pyseleniumjs/tests` subdirectory.
---

Copyright (c) 2017 John Nolette Licensed under the Apache License, Version 2.0.
