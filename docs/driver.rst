======
Driver
======

About
=====

The pyselenium-js driver is **just** a utility that exercises the existing selenium webdriver api *execute_script*.
This project was originally created for convenience sake, but has been shaped into a reusable module to help alleviate some of the terrible burdings experienced while relying on the official selenium bindings for more modern websites and web applications.

Best Practices
==============

pyselenium-js was designed to be a lightweight, and easily accessible all-purpose javascript driver to cover any functionality the official selenium bindings either don't support or don't cover well.
To truly exercise the javascript driver, we suggest leveraging page objects and or page factories to simplify integration into your project or test suite.

Asynchronous Javascript Wait
============================

One of the more unique and powerful features of pyselenium-js, is the ability to create an asynchronous wait using javascript.
This wait request is farmed out to your target web browser, and it's condition can be checked by a globally defined handle.

.. code-block:: python

    # create wait on a 250ms interval for button to be enabled and class to include 'danger'
    # this example is passing the the element as a WebElement instance
    # the element can be referenced in the condition by the alias $el
    page.js.wait(
        '$el.disabled == false && \
         $el.getAttribute("class").includes("danger")',
        250, page.button)
    >> string

    # the wait method also consumes selectors
    # if a selector is passed, the browser will query for the element
    # this is especially helpful for creating waits for elements that may not yet be available
    page.js.wait(
        '$el.disabled == false && \
         $el.getAttribute("class").includes("danger")',
        250, 'button[ng-click="login()"]')
    >> string

    # the wait method also has the capability to consume multiple elements
    # the elements can be referenced in the condition with the alias $el[x]
    page.js.wait(
        '$el[0].disabled == false && \
         $el[1].getAttribute("class").includes("active")',
        250, page.button, 'input[ng-bind="username"]')
    >> string

To check the wait status of your dispatched asynchronous wait, refer to the api method *wait_status*:

.. code-block:: python

    handle = page.js.wait(
        '$el.disabled == false && \
         $el.getAttribute("class").includes("danger")',
        250, 'button[ng-click="login()"]')
    ...
    page.js.wait_status(handle)
    >> True, False

Browser Console Logging
=======================

Another very helpful feature of the pyselenium-js driver, is the ability to store and retrieve console browser logs.
This functionality is **not** supported by the official selenium bindings.

To enable logging, use the api method **console_logger**:

.. code-block:: python

    page.js.console_logger()

To retrieve your browser's logs, refer to **console_dump**:

.. code-block:: python

    page.js.console_dump()
    >> string

The string returned will be in JSON format.

Checking Element Visibility
===========================

The javascript driver allows you to check for the visibility of a WebElement instance like so:

.. code-block:: python

    page.js.is_visible(page.element)
    >> True, False

Clicking and Double Clicking Elements
=====================================

The official selenium bindings attempt to click on an element based on it’s coordinate position, to emulate a natural click event on a given element.
The problem with this, is more modern websites rely on z-index styling rules for pop ups and raised panels; making it impossible to locate the correct coordinates otherwise raising a WebDriverException exception.
This behavior has also shown to be especially problematic in nested iframes.

The javascript driver's click method will dispatch a click event directly to the target element.
Additionally, the driver provides an api method *dbl_click* to double click on a given element – this feature is **not** supported by the official selenium bindings.

.. code-block:: python

    page.js.click(page.button)

    # double click on an element
    page.js.dbl_click(page.button)

Selecting Options From Select Elements
======================================

...

Getting and Setting Element Attributes
======================================

...

Getting and Setting Element Properties
======================================

...

Getting Element Text
======================================

...


Getting Element Value
======================================

...

Dispatching Events
==================

...

Scrolling an Element Into View
==============================

...

Get Page Scrolling Offsets
==========================

...

Angular.js
==========

Enable Debugging
----------------

...

Get Element Text
----------------

...

Set Element Text
----------------

...

Toggle Element Class
--------------------

...

Trigger Event Handler
---------------------

...

Get and Set Scope Property
--------------------------

...

Call Scope Function
-------------------

...

Get and Set Controller Property
-------------------------------

...

Call Controller Function
------------------------

...

Angular (2-5)
=============

Get and Set Component Property
------------------------------

...

Call Component Function
-----------------------

...
