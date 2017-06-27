# Licensed to the Software Freedom Conservancy (SFC) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import uuid, re

class E2EJS(object):
    """
    :Description: Packaged library for javascript operations.
    :Info: This library includes convenient vanilla, jquery, and angular operations.
    :param browser: This driver instance is used to execute javascript.
    :type browser: webdriver
    """
    def __init__(self, browser):
        self.browser = browser

    def wait(self, condition, element=None, interval=500):
        """
        :Description: Create an interval in js engine window, will clear interval after condition met.
        :param condition: Condition in javascript to pass to interval.
        :example: '$el.innerText = "cheesecake"'
        :type condition: basestring
        :element: Optional element to target in condition -- will be aliased to '$el' in conditional.
        :type element: WebElement
        :param interval: Time in milliseconds to execute interval.
        :type interval: int or float
        :return: basestring
        """
        id = lambda: str(uuid.uuid1())[:8]
        handle = id()
        if element:
            dom = id()
            self.browser.execute_script(
                'window["$%s"]=arguments[0];window["$%s"]=window.setInterval(function(){if(%s){(window.clearInterval(window["$%s"])||true)&&(window["$%s"]=-1); delete window["$%s"];}}, %s)' % (
                    dom, handle, condition.replace('$el', 'window["$%s"]' % dom), handle, handle, dom, interval
                ), element
            )
        else:
            self.browser.execute_script(
                'window["$%s"]=window.setInterval(function(){if(%s){(window.clearInterval(window["$%s"])||true)&&(window["$%s"]=-1);}}, %s)' % (
                    handle, condition, handle, handle, interval
                )
            )
        return handle

    def wait_status(self, handle):
        """
        :Description: Check the status of browser wait.
        :param handle: Interval handle returned from `self.wait`.
        :type handle: basestring
        :return: bool
        """
        return self.browser.execute_script('return window["$%s"] == -1' % handle)

    def console_logger(self):
        """
        :Description: Override browser console for log and error store.
        :Source: https://github.com/neetVeritas/pyselenium-js/issues/9#issuecomment-304284471
        :Warning: This will only enable console logging per session.
        """
        self.browser.execute_script('var _0xeb7a=["\x24\x63\x6F\x6E\x73\x6F\x6C\x65","\x24\x6C\x6F\x67\x73","\x24\x65\x72\x72\x6F\x72\x73","\x24\x77\x61\x72\x6E\x69\x6E\x67\x73","\x61\x73\x73\x65\x72\x74","\x63\x6C\x65\x61\x72","\x67\x72\x6F\x75\x70","\x67\x72\x6F\x75\x70\x43\x6F\x6C\x6C\x61\x70\x73\x65\x64","\x67\x72\x6F\x75\x70\x45\x6E\x64","\x69\x6E\x66\x6F","\x74\x61\x62\x6C\x65","\x74\x69\x6D\x65","\x74\x69\x6D\x65\x45\x6E\x64","\x6C\x6F\x67","\x70\x72\x6F\x74\x6F\x74\x79\x70\x65","\x70\x75\x73\x68","\x65\x72\x72\x6F\x72","\x65\x78\x63\x65\x70\x74\x69\x6F\x6E","\x74\x72\x61\x63\x65","\x77\x61\x72\x6E","\x64\x75\x6D\x70","\x73\x74\x72\x69\x6E\x67\x69\x66\x79","\x61\x6A\x61\x78\x45\x72\x72\x6F\x72","\x75\x72\x6C","\x74\x79\x70\x65","\x73\x74\x61\x74\x75\x73","\x72\x65\x73\x70\x6F\x6E\x73\x65\x54\x65\x78\x74","\x63\x6F\x6E\x73\x6F\x6C\x65"];function Logger(){this[_0xeb7a[0]]= console;this[_0xeb7a[1]]= [];this[_0xeb7a[2]]= [];this[_0xeb7a[3]]= [];this[_0xeb7a[4]]= this[_0xeb7a[0]][_0xeb7a[4]];this[_0xeb7a[5]]= this[_0xeb7a[0]][_0xeb7a[5]];this[_0xeb7a[6]]= this[_0xeb7a[0]][_0xeb7a[6]];this[_0xeb7a[7]]= this[_0xeb7a[0]][_0xeb7a[7]];this[_0xeb7a[8]]= this[_0xeb7a[0]][_0xeb7a[8]];this[_0xeb7a[9]]= this[_0xeb7a[0]][_0xeb7a[9]];this[_0xeb7a[10]]= this[_0xeb7a[0]][_0xeb7a[10]];this[_0xeb7a[11]]= this[_0xeb7a[0]][_0xeb7a[11]];this[_0xeb7a[12]]= this[_0xeb7a[0]][_0xeb7a[12]]}Logger[_0xeb7a[14]][_0xeb7a[13]]= function(){this[_0xeb7a[1]][_0xeb7a[15]](arguments[0]);this[_0xeb7a[0]][_0xeb7a[13]](arguments[0])};Logger[_0xeb7a[14]][_0xeb7a[16]]= function(){this[_0xeb7a[2]][_0xeb7a[15]](arguments[0]);this[_0xeb7a[0]][_0xeb7a[16]](arguments[0])};Logger[_0xeb7a[14]][_0xeb7a[17]]= function(){this[_0xeb7a[2]][_0xeb7a[15]](arguments[0]);this[_0xeb7a[0]][_0xeb7a[17]](arguments[0])};Logger[_0xeb7a[14]][_0xeb7a[18]]= function(){this[_0xeb7a[2]][_0xeb7a[15]](arguments[0]);this[_0xeb7a[0]][_0xeb7a[18]](arguments[0])};Logger[_0xeb7a[14]][_0xeb7a[19]]= function(){this[_0xeb7a[3]][_0xeb7a[15]](arguments[0]);this[_0xeb7a[0]][_0xeb7a[19]](arguments[0])};Logger[_0xeb7a[14]][_0xeb7a[20]]= function(){return JSON[_0xeb7a[21]]({logs:this[_0xeb7a[1]],errors:this[_0xeb7a[2]],warnings:this[_0xeb7a[3]]})};($?($(document)?($(document)[_0xeb7a[22]]?true:false):false):false)&& $(document)[_0xeb7a[22]](function(){console[_0xeb7a[16]]({location:arguments[2][_0xeb7a[23]],method:arguments[2][_0xeb7a[24]],status:arguments[1][_0xeb7a[25]],error:arguments[3],response:arguments[1][_0xeb7a[26]]})});window[_0xeb7a[27]]=  new Logger()')

    def console_dump(self):
        """
        :Description: Return console logs as stringified JSON structure.
        :Warning: This will only work once `console_logger` is executed.
        """
        return self.browser.execute_script('return console.dump()')

    def is_visible(self, element):
        """
        :Description: Get's the visibility of the provided target element.
        :param element: Element for browser instance to target.
        :return: bool
        """
        return self.browser.execute_script(
            'return !!(arguments[0].offsetWidth || arguments[0].offsetHeight || arguments[0].getClientRects().length);',
            element
        )

    def click(self, element):
        """
        :Description: Execute the `click` event on the target element.
        :param element: Element for browser instance to target.
        """
        self.browser.execute_script('arguments[0].click();', element)

    def dbl_click(self, element):
        """
        :Description: Execute the `dbclick` event on the target element.
        :param element: Element for browser instance to target.
        """
        self.browser.execute_script(
            'var e = document.createEvent("mouseEvent"); e.initEvent("dblclick", true, true); arguments[0].dispatchEvent(e);',
            element
        )

    def select(self, element):
        """
        :Description: Sets the attribute `selected` to true on target element and triggers `change` event.
        :param element: Element for browser instance to target.
        """
        self.browser.execute_script(
            'arguments[0].selected = "selected"; arguments[0].dispatchEvent(new Event("change"));',
            element
        )

    def deselect(self, element):
        """
        :Description: Sets the attribute `selected` to true on target element and triggers `change` event.
        :param element: Element for browser instance to target.
        """
        self.browser.execute_script(
            'arguments[0].selected = null; arguments[0].dispatchEvent(new Event("change"));',
            element
        )

    def get_attribute(self, element, attribute):
        """
        :Description: Return the given attribute of the target element.
        :param element: Element for browser instance to target.
        :param attribute: Attribute of target element to return.
        :return: basestring
        """
        return self.browser.execute_script(
            'return arguments[0].getAttribute("%s");' % attribute,
            element
        )

    def set_attribute(self, element, attribute, value):
        """
        :Description: Modify the given attribute of the target element.
        :param element: Element for browser instance to target.
        :param attribute: Attribute of target element to modify.
        :param value: Value of target element's attribute to modify.
        """
        if value is None:
            exec_string = 'arguments[0].setAttribute("%s", null);' % attribute
        elif isinstance(value, bool):
            exec_string = 'arguments[0].setAttribute("%s", %s);' % (attribute, 'false' if not value else 'true')
        elif isinstance(value, (int, float)):
            exec_string = 'arguments[0].setAttribute("%s", %s);' % (attribute, value)
        else:
            exec_string = 'arguments[0].setAttribute("%s", "%s");' % (attribute, value)
        self.browser.execute_script(
            exec_string,
            element
        )

    def remove_attribute(self, element, attribute):
        """
        :Description: Remove the given attribute from the target element.
        :param element: Element for browser instance to target.
        :param attribute: Attribute of target element to remove.
        """
        self.browser.execute_script(
            'arguments[0].removeAttribute("%s");' % attribute,
            element
        )

    def get_property(self, element, property):
        """
        :Description: Return the given attribute of the target element.
        :Warning: This method relies on JQuery.
        :param element: Element for browser instance to target.
        :param property: Property of target element to return.
        """
        return self.browser.execute_script('return arguments[0]["%s"];' % property, element)

    def set_property(self, element, property, value):
        """
        :Description: Modify the given attribute of the target element.
        :Warning: This method relies on JQuery.
        :param element: Element for browser instance to target.
        :param property: Property of target element to modify.
        :param value: Value of target element's property to modify.
        """
        if value is None:
            exec_string = 'arguments[0]["%s"] = null;' % property
        elif isinstance(value, bool):
            exec_string = 'arguments[0]["%s"] = %s;' % (property, 'false' if not value else 'true')
        elif isinstance(value, (int, float)):
            exec_string = 'arguments[0]["%s"] = %s;' % (property, value)
        else:
            exec_string = 'arguments[0]["%s"] = "%s";' % (property, value)
        self.browser.execute_script(
            exec_string,
            element
        )

    def get_value(self, element):
        """
        :Description: Return the value of the given element.
        :param element: Element for browser instance to target.
        :return: basestring
        """
        return self.get_property(
            element=element,
            property='value'
        )

    def get_text(self, element):
        """
        :Description: Return the text content between the tags of the given element.
        :Info: This may be helpful for reading text from elements that do not support the `value` property.
        :param element: Element for browser instance to target.
        :return: basestring
        """
        return self.get_property(
            element=element,
            property='innerText'
        )

    def get_raw_text(self, element):
        """
        :Description: Return the text content between the tags of the given element.
        :Info: This may be helpful for reading text from elements that do not support the `value` property.
        :Warning: This will return the raw text content of the DOM's child scope.
        :param element: Element for browser instance to target.
        :return: basestring
        """
        return self.get_property(
            element=element,
            property='innerHTML'
        )

    def trigger_event(self, element, event):
        """
        :Description: Trigger specified event of the given element.
        :Warning: This method relies on JQuery.
        :param element: Element for browser instance to target.
        :param event: Event to trigger from target element.
        """
        self.browser.execute_script('arguments[0].dispatchEvent(new Event("%s"));' % event, element)

    def trigger_mouse_event(self, element, event):
        """
        :Description: Trigger specified mouse related event of the given element.
        :param element: Element for browser instance to target.
        :param event: Event to trigger from target element.
        """
        self.browser.execute_script('arguments[0].dispatchEvent(new MouseEvent("%s"));' % event, element)

    def trigger_keyboard_event(self, element, event):
        """
        :Description: Trigger specified keyboard related event of the given element.
        :param element: Element for browser instance to target.
        :param event: Event to trigger from target element.
        """
        self.browser.execute_script('arguments[0].dispatchEvent(new KeyboardEvent("%s"));' % event, element)

    def trigger_enter_key(self, element):
        """
        :Description: Trigger enter key keypress on given event.
        :param element: Element for browser instance to target.
        """
        self.browser.execute_script(
            'var e = new Event("KeyboardEvent"); e.initEvent("keydown", true, true); e.which=13; arguments[0].dispatchEvent(e);',
            element
        )

    def scroll_into_view(self, element):
        """
        :Description: Scroll the target element into view.
        :Warning: This method relies on JQuery.
        :param element: Element for browser instance to target.
        """
        self.browser.execute_script('arguments[0].scrollIntoView();', element)

    def ng_enable_debugging(self):
        """
        :Description: Enables angular debugging on given webpage.
        """
        self.browser.execute_script(
            'angular.reloadWithDebugInfo()'
        )

    def ng_get_text(self, element):
        """
        :Description: Will return the DOM's value, if not found will default to `innerHTML`.
        :Warning: This will only work for angular elements.
        :param element: Element for browser instance to target.
        :return: basestring
        """
        return self.browser.execute_script('return angular.element(arguments[0]).text();', element)

    def ng_set_text(self, element, text):
        """
        :Description: Will set a DOM's value, if not found will default to `innerHTML`.
        :Warning: This will only work for angular elements.
        :param element: Element for browser instance to target.
        :param text: Text used for related operation.
        """
        self.browser.execute_script('angular.element(arguments[0]).text("%s");' % text, element)

    def ng_toggle_class(self, element, target):
        """
        :Description: Toggle DOM class.
        :Warning: This will only work for angular elements.
        :param element: Element for browser instance to target.
        :param target: Class to toggle.
        """
        self.browser.execute_script('angular.element(arguments[0]).toggleClass("%s");' % target, element)

    def ng_trigger_event_handler(self, element, event):
        """
        :Description: Trigger angular event handler of element.
        :Warning: This will only work for angular elements.
        :param element: Element for browser instance to target.
        :param event: Event to trigger.
        """
        self.browser.execute_script(
            'angular.element(arguments[0]).triggerHandler("%s");' % event,
            element
        )

    def __property(self, property):
        """
        :Description: Turn nested properties into object tree.
        :param property: Property to clean.
        :type property: basestring
        :return: basestring
        """
        pat = re.compile('[a-z]{0,}.')
        results = pat.findall(property)
        for i in range(0, len(results)):
            results[i] = ("['%s']" % results[i]).replace('.', '')
        return ''.join(results)

    def ng_get_scope_property(self, element, property):
        """
        :Description: Will return value of property of element's scope.
        :Warning: Requires angular debugging to be enabled.
        :param element: Element for browser instance to target.
        :param property: Property of element's angular scope to target.
        :return: basestring
        """
        return self.browser.execute_script(
            'return angular.element(arguments[0]).scope()%s;' % self.__property(property=property),
            element
        )

    def ng_set_scope_property(self, element, property, value):
        """
        :Description: Will set value of property of element's scope.
        :Warning: Requires angular debugging to be enabled.
        :param element: Element for browser instance to target.
        :param property: Property of element's angular scope to target.
        :param value: Value to specify to angular element's scope's property.
        """
        self.browser.execute_script(
            'angular.element(arguments[0]).scope()%s = "%s";' % (self.__property(property=property), value),
            element
        )

    def ng_call_scope_function(self, element, func, params=[]):
        """
        :Description: Will execute scope function with provided parameters.
        :Warning: Requires angular debugging to be enabled.
        :param element: Element for browser instance to target.
        :param func: Function to execute from angular element scope.
        :type func: basestring
        :param params: List of parameters to pass to target function.
        :type params: list
        """
        param_str = ''
        numeric = (int, float)
        for param in params:
            if isinstance(param, basestring):
                param_str += '"%s",' % param
            elif isinstance(param, numeric):
                param_str += '%s,' % param
            elif isinstance(param, bool):
                param_str += '%s,' % 'true' if param else 'false'
        if param_str.endswith(','):
            param_str = param_str.replace(param_str[-1], '')
        self.browser.execute_script(
            'angular.element(arguments[0]).scope().%s(%s);' % (func, param_str),
            element
        )

    def ng_get_ctrl_property(self, element, property):
        """
        :Description: Will return value of property of element's controller.
        :Warning: Requires angular debugging to be enabled.
        :param element: Element for browser instance to target.
        :param property: Property of element's angular controller to target.
        :return: basestring
        """
        return self.browser.execute_script(
            'return angular.element(arguments[0]).controller()%s;' % self.__property(property=property),
            element
        )

    def ng_set_ctrl_property(self, element, property, value):
        """
        :Description: Will set value of property of element's controller.
        :Warning: Requires angular debugging to be enabled.
        :param element: Element for browser instance to target.
        :param property: Property of element's angular scope to target.
        :param value: Value to specify to angular element's controller's property.
        """
        self.browser.execute_script(
            'angular.element(arguments[0]).controller()%s = "%s";' % (self.__property(property=property), value),
            element
        )

    def ng_call_ctrl_function(self, element, func, params):
        """
        :Description: Will execute controller function with provided parameters.
        :Warning: Requires angular debugging to be enabled.
        :param element: Element for browser instance to target.
        :param func: Function to execute from angular element controller.
        :type func: basestring
        :param params: List of parameters to pass to target function.
        :type params: list
        """
        param_str = ''
        numeric = (int, float)
        for param in params:
            if isinstance(param, basestring):
                param_str += '"%s",' % param
            elif isinstance(param, numeric):
                param_str += '%s,' % param
            elif isinstance(param, bool):
                param_str += '%s,' % 'true' if param else 'false'
        if param_str.endswith(','):
            param_str = param_str.replace(param_str[-1], '')
        self.browser.execute_script(
            'angular.element(arguments[0]).controller().%s(%s);' % (func, param_str),
            element
        )
