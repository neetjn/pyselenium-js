# pyselenium-js
Lightweight, Python module to execute frequently used javascript functionality on a Selenium webdriver.

### About
**pyselenium-js** is a very simple, lightweight module that helps relieve some of the burden of E2E testing with the official Selenium bindings.
The official Selenium bindings operate in the most natural way a user would operate against a given web page.
The problem with this, is with more advanced and modern websites, these bindings may not always work as expected on custom DOMs.

### Usage
This project was created using Python 2.7.x and Selenium 3.0.0b3.

Simply place `e2ejs.py` in your prefered directory and import it into your project.
A very clean, and simply approach to referencing this library is instantiating it in your page object or factory, so it may be referenced with your active webdriver instance.

```python
from selenium import webdriver
from warnings import warn
from e2ejs import E2EJS


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


MyPage(Page):

  @property
  def div_with_text(self):
    return self.browser.find_element_by_css_selector('div.something')
    
  @property
  def ng_elements(self):
    return self.browser.find_elements_by_css_selector('[ng-repeat]')
    
page = Page(browser=webdriver.Firefox())
print page.div_with_text.text  # bindings cannot pull text from divs
print page.js.get_text(element=page.div_with_text)

for el in page.ng_elements:
  page.js.ng_set_scope_property(
    element=el,
    property='searchText',
    value='pls halp'
  )
  page.js.ng_trigger_handler(
    element=el,
    event='change'
  )
  page.js.ng_call_scope_function(
    element=el,
    func='updateSearch',
    params=[True, 40]
  )
  
page.exit()
```

===
Copyright (c) 2017 John Nolette Licensed under the Apache License, Version 2.0.
