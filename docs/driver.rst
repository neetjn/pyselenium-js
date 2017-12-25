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

To enable logging, use the api method *console_logger*:

.. code-block:: python

    page.js.console_logger()

To retrieve your browser's logs, refer to *console_dump*:

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

The official selenium bindings provide a very round about method of selecting select element options.
This method also does not work for the Safari webdriver.

The pyselenium-js driver offers an api method *select* that will work across any webdriver on any platform without the use of action chains.

.. code-block:: python

    page.country_selection.click()
    page.country_option('United States').click()
    # trigger event "select" to notify the browser this element value has been modified
    page.js.select(page.country_selection)

Getting and Setting Element Attributes
======================================

Using the pyselenium-js driver, an element’s attribute can be fetched like so:

.. code-block:: python

    page.js.get_attribute(page.checkbox, 'aria-toggled')

Additionally, an element’s attribute can be set using the *set_attribute* api method:

.. code-block:: python

    page.js.set_attribute(page.checkbox, 'aria-toggled', True)

Under the hood, pyselenium-js will automatically convert javascript types into pythonic types and inverse.

Getting and Setting Element Properties
======================================

**This feature is not supported by the official selenium bindings (or remote api).**

Using the pyselenium-js driver, an element’s property can be fetched like so:

.. code-block:: python

    page.js.get_property(page.checkbox, 'disabled')

Additionally, an element’s property can be set using the *set_property* api method:

.. code-block:: python

    page.js.set_property(page.checkbox, 'disabled', True)

Under the hood, pyselenium-js will automatically convert javascript types into pythonic types and inverse.

Getting Element Text
======================================

To scrape text from an element, refer to the api method `get_text`:

.. code-block:: python

    # pulls the innerText property value from a given element
    page.js.get_text(page.element)
    >> 'foobar'

You may alternatively use the api method `get_raw_text` for elements that do not support the `innerText` property.

.. code-block:: python

    # pulls the innerHTML property value from a given element
    page.js.get_raw_text(page.element)
    >> '<span>foobar</span>'

Getting Element Value
======================================

Input elements provide a property, value, which selenium does **not** provide explicit bindings for.
Using the api method *get_value* you may pull the value from any input element (including select, button, radiobutton).

.. code-block:: python

    page.js.get_value(page.username_field)
    >> string

Dispatching Events
==================

The pyselenium-js driver allows developers the ability to dispatch configuragle events to a given element.
Refer to the api method *trigger_event*, which can be used like so:

.. code-block:: python

    # dispatch a naked event 'click'
    page.js.trigger_event(page.button, event='click')

    # dispatch an event 'click' of type MouseEvent
    # pass the event options 'bubbles' and 'cancelable'
    page.js.trigger_event(page.button, event='click', event_type='MouseEvent', options={
        'bubbles': True,
        'cancelable': False
    })

Scrolling an Element Into View
==============================

To scroll an element into view, use the api method *scroll_into_view*:

.. code-block:: python

    page.js.scroll_into_view(page.button)

Get Page Scrolling Offsets
==========================

The driver provides a property *get_scrolling_offsets* to pull the webdriver's current scrolling coordinates.
This can be especially helpful when testing fragment identifiers and continuously scrolling content.

.. code-block:: python

    coords = page.js.get_scrolling_offsets
    page.scroll_to_bottom.click()
    assert coords['y'] < page.js.get_scrolling_offsets['y']

Angular.js
==========

**These methods shouldn't be a go-to for many test cases, but they can certainly helpful for more advanced web applications.**

Enable Debugging
----------------

To enable angular debugging for access to angular element scropes and controllers, refer to the api method *ng_enable_debugging*.
This method *will* reload the driver's current location.

.. code-block:: python

    page.js.ng_enable_debugging()

To verify angular debugging is enabled, a well regarded trick is to search for any existing elements with the class *ng-binding*.

Get and Set Element Text
----------------

To pull the inner text of a given angular element, the javascript driver provides an api method *ng_get_text*

.. code-block:: python

    page.js.ng_get_text(page.username_field)

Additionally, the driver provides another api method *ng_set_text* to modify the text of a given angular element.

.. code-block:: python

    page.js.ng_set_text(page.username_field, 'john_doe')

Toggle Element Class
--------------------

Toggling the class of an angular element can be done using the api method *ng_toggle_class*:

.. code-block:: python

    page.js.ng_toggle_class(page.button, 'active')

Trigger Event Handler
---------------------

Angular.js provides a relatively simple interface for triggering angular element event handlers.
You may trigger an angular.js element event handler like so:

.. code-block:: python

    page.js.ng_trigger_event_handler(page.button, 'click')

Get and Set Scope Property
--------------------------

The pyselenium-js driver enables angular element scope manipulation, and allows for the extraction of scope property values.
Refer to the api methods *ng_get_scope_property* and *ng_set_scope_property*:

.. code-block:: python

    # angular.element('#someSelector').scope().data.username = 'foobar'
    page.js.ng_set_scope_property(page.user_tile, 'data.username', 'foobar')

    assert page.js.ng_get_scope_property(
        page.user_tile, 'data.username') == 'foobar'

Though this shouldn't be a go-to for many test cases, it's certainly helpful for more advanced web applications.

Call Scope Function
-------------------

A more advanced feature of the angular.js utilities for pyselenium-js, is the ability to directly invoke scope functions.
Take for example the following angular.js controller,

.. code-block:: javascript

    angular.controller('homeCtrl', ['$scope', ($scope) => {
        $scope.addUser(username, email, age) {
            ...
        }
    }])

Using the api method *ng_call_scope_function* you may call the scope method directly like so:

.. code-block:: python

    # angular.element('#someSelector').scope().addUser('john', 'john@neetgroup.net', 22)
    page.js.ng_call_scope_function(
        page.username_field, 'addUser', ['john', 'john@neetgroup.net', 22])

Get and Set Controller Property
-------------------------------

The pyselenium-js driver enables angular element controller manipulation, and allows for the extraction of controller property values.
Refer to the api methods *ng_get_ctrl_property* and *ng_set_ctrl_property*:

.. code-block:: python

    # angular.element('#someSelector').controller().UserService.username = 'foobar'
    page.js.ng_ctrl_scope_property(page.user_tile, 'UserService.username', 'foobar')

    assert page.js.ng_ctrl_scope_property(
        page.user_tile, 'UserService.username') == 'foobar'

Call Controller Function
------------------------

A more advanced feature of the angular.js utilities for pyselenium-js, is the ability to directly invoke controller functions.
Take for example the following angular.js controller,

.. code-block:: javascript

    angular.controller('homeCtrl', () => {
        this.deleteUser(userId) {
            ...
        }
    })

Using the api method *ng_call_ctrl_function* you may call the controller method directly like so:

.. code-block:: python

    # angular.element('#someSelector').controller().deleteUser(100100)
    page.js.ng_call_ctrl_function(page.username_field, 'deleteUser', [100100])

Angular (2-5)
=============

**These methods shouldn't be a go-to for many test cases, but they can certainly helpful for more advanced web applications.**

Get and Set Component Property
------------------------------

The pyselenium-js driver provides a simple and easy to use interface for Angular applications to get and set component properties.
Refer to the api methods *ng2_get_component_property* and *ng2_set_component_property*.

.. code-block:: python

    # ng.probe('#someSelector').componentInstance.username = 'jack'
    page.js.ng2_set_component_property(page.profile_username, 'username', 'jack')

    assert page.js.ng2_get_component_property(
        page.profile_username, 'username') == 'jack'

Call Component Function
-----------------------

To invoke an Angular application component function, refer to the *ng2_call_component_function* api method.

.. code-block:: python

    # ng.probe('#someSelector').componentInstance.logout()
    page.js.ng2_call_component_function(page.profile_username, 'logout', [])

    # ng.probe('#someSelector').componentInstance.login('username', 'password')
    page.js.ng2_call_component_function(page.username_field, 'login', ['username', 'password'])
