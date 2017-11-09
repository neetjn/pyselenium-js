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

import uuid
import re
import json
import warnings

class E2EJS(object):
    """
    :Description: Packaged library for javascript operations.
    :Info: This library includes convenient vanilla, jquery, and angular operations.
    :param browser: This driver instance is used to execute javascript.
    :type browser: webdriver
    """
    def __init__(self, browser):
        self.browser = browser

    @classmethod
    def __type2js(cls, value):
        """
        :Description: Convert python value to executable javascript value by type.
        :param value: Value to transform.
        :type value: None, bool, int, float, basestring
        :return: basestring
        """
        if value is None:
            return 'null'
        elif isinstance(value, bool):
            return 'false' if not value else 'true'
        elif isinstance(value, (int, float)):
            return '%s' % value
        return '"%s"' % value

    @classmethod
    def __type2python(cls, value):
        """
        :Description: Convert javascript value to python value by type.
        :param value: Value to transform.
        :type value: None, bool, int, float, basestring
        :return: None, bool, int, float, basestring
        """
        if isinstance(value, basestring):
            if value is 'null':
                return None
            elif value in ('true', 'false'):
                return False if value is 'false' else True
            elif value.replace('.', '', 1).isdigit():
                return eval(value)
        return value

    def wait(self, condition, interval, *args):
        """
        :Description: Create an interval in vm.window, will clear interval after condition met.
        :param condition: Condition in javascript to pass to interval.
        :example: '$el.innerText == "cheesecake"'
        :example: '$el[0].disabled && $el[1].disabled'
        :type condition: basestring
        :param interval: Time in milliseconds to execute interval.
        :type interval: int or float
        :param *args: WebElement or selector of condition element.
        :type *args: tuple
        :return: basestring
        """
        hid = lambda: '$' + str(uuid.uuid1())[:8]
        handle = hid()
        if len(args):
            element_handle = hid()
            self.browser.execute_script(
                'window["{}"] = [];'.format(element_handle)
            )  # create element container in window scope
            for el in args:
                if isinstance(el, basestring):
                    # assume selector
                    self.browser.execute_script('window["{}"].push({});'.format(
                        element_handle, 'function() { return document.querySelector("%s") }' % el))
                else:
                    # assume web element
                    self.browser.execute_script(
                        'window["{}"].push(arguments[0]);'.format(element_handle), el)
            if len(args) == 1:
                condition = condition.replace('$el', 'window["{}"][0]{}'.format(
                    element_handle, '()' if isinstance(args[0], basestring) else ''))
            else:
                regex = r'(\$el\[([0-9]{0,3})\])'
                results = re.findall(regex, condition)  # [('$el[0]', '0'), ('$el[1]', '1'), ...]
                for result in results:
                    pos = eval(result[1])
                    if pos + 1 <= len(args):
                        condition = condition.replace(result[0], 'window["{}"][{}]{}'.format(
                            element_handle, pos, '()' if isinstance(args[pos], basestring) else ''))

            self.browser.execute_script(
                'window["%s"]=window.setInterval(function(){if(%s){ \
                (window.clearInterval(window["%s"])||true)&&(window["%s"]=-1); \
                delete window["%s"];}}, %s)' % (handle, condition, handle, handle, \
                element_handle, interval))  # create interval
        else:
            self.browser.execute_script(
                'window["%s"]=window.setInterval(function(){if(%s){ \
                (window.clearInterval(window["%s"])||true)&&(window["%s"]=-1);}}, %s)' % (
                handle, condition, handle, handle, interval))  # create interval

        return handle

    def wait_status(self, handle):
        """
        :Description: Check the status of browser wait.
        :param handle: Interval handle returned from `self.wait`.
        :type handle: basestring
        :return: bool
        """
        return self.browser.execute_script('return window["%s"] == -1' % handle)

    def console_logger(self):
        """
        :Description: Override browser console for log and error store.
        :Source: https://github.com/neetVeritas/pyselenium-js/issues/9#issuecomment-304284471
        :Warning: This will only enable console logging per session.
        """
        self.browser.execute_script('var _0x4f63=["\x24\x63\x6F\x6E\x73\x6F\x6C\x65","\x24\x6C\x6F\x67\x73","\x24\x65\x72\x72\x6F\x72\x73","\x24\x77\x61\x72\x6E\x69\x6E\x67\x73","\x61\x73\x73\x65\x72\x74","\x63\x6C\x65\x61\x72","\x67\x72\x6F\x75\x70","\x67\x72\x6F\x75\x70\x43\x6F\x6C\x6C\x61\x70\x73\x65\x64","\x67\x72\x6F\x75\x70\x45\x6E\x64","\x69\x6E\x66\x6F","\x74\x61\x62\x6C\x65","\x74\x69\x6D\x65","\x74\x69\x6D\x65\x45\x6E\x64","\x6C\x6F\x67","\x70\x72\x6F\x74\x6F\x74\x79\x70\x65","\x70\x75\x73\x68","\x65\x72\x72\x6F\x72","\x65\x78\x63\x65\x70\x74\x69\x6F\x6E","\x74\x72\x61\x63\x65","\x77\x61\x72\x6E","\x64\x75\x6D\x70","\x73\x74\x72\x69\x6E\x67\x69\x66\x79","\x24","\x61\x6A\x61\x78\x45\x72\x72\x6F\x72","\x75\x72\x6C","\x74\x79\x70\x65","\x73\x74\x61\x74\x75\x73","\x72\x65\x73\x70\x6F\x6E\x73\x65\x54\x65\x78\x74","\x63\x6F\x6E\x73\x6F\x6C\x65"];function Logger(){this[_0x4f63[0]]= console,this[_0x4f63[1]]= [],this[_0x4f63[2]]= [],this[_0x4f63[3]]= [],this[_0x4f63[4]]= this[_0x4f63[0]][_0x4f63[4]],this[_0x4f63[5]]= this[_0x4f63[0]][_0x4f63[5]],this[_0x4f63[6]]= this[_0x4f63[0]][_0x4f63[6]],this[_0x4f63[7]]= this[_0x4f63[0]][_0x4f63[7]],this[_0x4f63[8]]= this[_0x4f63[0]][_0x4f63[8]],this[_0x4f63[9]]= this[_0x4f63[0]][_0x4f63[9]],this[_0x4f63[10]]= this[_0x4f63[0]][_0x4f63[10]],this[_0x4f63[11]]= this[_0x4f63[0]][_0x4f63[11]],this[_0x4f63[12]]= this[_0x4f63[0]][_0x4f63[12]]}Logger[_0x4f63[14]][_0x4f63[13]]= function(){this[_0x4f63[1]][_0x4f63[15]](arguments[0]),this[_0x4f63[0]][_0x4f63[13]](arguments[0])},Logger[_0x4f63[14]][_0x4f63[16]]= function(){this[_0x4f63[2]][_0x4f63[15]](arguments[0]),this[_0x4f63[0]][_0x4f63[16]](arguments[0])},Logger[_0x4f63[14]][_0x4f63[17]]= function(){this[_0x4f63[2]][_0x4f63[15]](arguments[0]),this[_0x4f63[0]][_0x4f63[17]](arguments[0])},Logger[_0x4f63[14]][_0x4f63[18]]= function(){this[_0x4f63[2]][_0x4f63[15]](arguments[0]),this[_0x4f63[0]][_0x4f63[18]](arguments[0])},Logger[_0x4f63[14]][_0x4f63[19]]= function(){this[_0x4f63[3]][_0x4f63[15]](arguments[0]),this[_0x4f63[0]][_0x4f63[19]](arguments[0])},Logger[_0x4f63[14]][_0x4f63[20]]= function(){return JSON[_0x4f63[21]]({logs:this[_0x4f63[1]],errors:this[_0x4f63[2]],warnings:this[_0x4f63[3]]})},(window[_0x4f63[22]]&& $(document)&& $(document)[_0x4f63[23]]?!0:!1)&& $(document)[_0x4f63[23]](function(){console[_0x4f63[16]]({location:arguments[2][_0x4f63[24]],method:arguments[2][_0x4f63[25]],status:arguments[1][_0x4f63[26]],error:arguments[3],response:arguments[1][_0x4f63[27]]})}),window[_0x4f63[28]]=  new Logger')

    def console_dump(self):
        """
        :Description: Return console logs as stringified JSON structure.
        :Warning: This will only work once `console_logger` is executed.
        :return: basestring
        """
        return self.browser.execute_script('return console.dump()')

    def is_visible(self, element):
        """
        :Description: Get's the visibility of the provided target element.
        :param element: Element for browser instance to target.
        :type element: WebElement
        :return: bool
        """
        return bool(self.browser.execute_script(
            'return !!(arguments[0].offsetWidth || arguments[0].offsetHeight || \
            arguments[0].getBoundingClientRect().height || \
            arguments[0].getBoundingClientRect().width) && \
            (arguments[0].style.visibility == "" || arguments[0].style.visibility == "visible");',
            element))

    def click(self, element):
        """
        :Description: Execute the `click` event on the target element.
        :param element: Element for browser instance to target.
        :type element: WebElement
        """
        self.browser.execute_script('arguments[0].click()', element)

    def dbl_click(self, element):
        """
        :Description: Execute the `dbclick` event on the target element.
        :param element: Element for browser instance to target.
        :type element: WebElement
        """
        self.browser.execute_script(
            'var e = document.createEvent("mouseEvent"); \
            e.initEvent("dblclick", true, true); \
            arguments[0].dispatchEvent(e);', element)

    def select(self, element):
        """
        :Description: Sets the attribute `selected` to true and triggers `change` event.
        :param element: Element for browser instance to target.
        :type element: WebElement
        """
        self.browser.execute_script(
            'arguments[0].selected = "selected"; \
             arguments[0].dispatchEvent(new Event("change"));', element)

    def deselect(self, element):
        """
        :Description: Sets the attribute `selected` to null and triggers `change` event.
        :param element: Element for browser instance to target.
        :type element: WebElement
        """
        self.browser.execute_script(
            'arguments[0].selected = null; \
             arguments[0].dispatchEvent(new Event("change"));', element)

    def get_attribute(self, element, attribute, convert_type=True):
        """
        :Description: Return the given attribute of the target element.
        :param element: Element for browser instance to target.
        :type element: WebElement
        :param attribute: Attribute of target element to return.
        :type attribute: basestring
        :param convert_type: If enabled, will return pythonic type.
        :type convert_type: bool
        :return: None, bool, int, float, basestring
        """
        attribute = self.browser.execute_script(
            'return arguments[0].getAttribute("%s");' % attribute, element)

        return self.__type2python(attribute) if convert_type else attribute

    def set_attribute(self, element, attribute, value):
        """
        :Description: Modify the given attribute of the target element.
        :param element: Element for browser instance to target.
        :type element: WebElement
        :param attribute: Attribute of target element to modify.
        :type attribute: basestring
        :param value: Value of target element's attribute to modify.
        :type value: None, bool, int, float, basestring
        """
        self.browser.execute_script('arguments[0].setAttribute("%s", %s);' % (
            attribute, self.__type2js(value=value)), element)

    def remove_attribute(self, element, attribute):
        """
        :Description: Remove the given attribute from the target element.
        :param element: Element for browser instance to target.
        :type element: WebElement
        :param attribute: Attribute of target element to remove.
        :type attribute: basestring
        """
        self.browser.execute_script('arguments[0].removeAttribute("%s");' % attribute, element)

    def get_property(self, element, prop):
        """
        :Description: Return the given attribute of the target element.
        :param element: Element for browser instance to target.
        :type element: WebElement
        :param prop: Property of target element to return.
        :type prop: basestring
        :return: None, bool, int, float, basestring
        """
        return self.browser.execute_script('return arguments[0]["%s"];' % prop, element)

    def set_property(self, element, prop, value):
        """
        :Description: Modify the given attribute of the target element.
        :param element: Element for browser instance to target.
        :type element: WebElement
        :param prop: Property of target element to modify.
        :type prop: basestring
        :param value: Value of target element's property to modify.
        :type value: None, bool, int float, basestring
        """
        self.browser.execute_script(
            'arguments[0]["%s"] = %s' % (prop, self.__type2js(value=value)), element)

    def get_value(self, element):
        """
        :Description: Return the value of the given element.
        :param element: Element for browser instance to target.
        :type element: WebElement
        :return: basestring
        """
        return self.get_property(element=element, prop='value')

    def get_text(self, element):
        """
        :Description: Return the text content between the tags of the given element.
        :Info: Helpful for reading text from elements that do not support the `value` property.
        :param element: Element for browser instance to target.
        :return: basestring
        """
        return self.get_property(element=element, prop='innerText')

    def get_raw_text(self, element):
        """
        :Description: Return the text content between the tags of the given element.
        :Info: Helpful for reading text from elements that do not support the `value` property.
        :Warning: This will return the raw text content of the DOM's child scope.
        :param element: Element for browser instance to target.
        :type element: WebElement
        :return: basestring
        """
        return self.get_property(element=element, prop='innerHTML')

    def trigger_event(self, element, event, event_type=None, options=None):
        """
        :Description: Trigger specified event of the given element.
        :param element: Element for browser instance to target.
        :type element: WebElement, (WebElement, ...)
        :param event: Event to trigger from target element.
        :type event: basestring, (basestring, ...)
        :param event_type: Event type.
        :type event_type: basestring
        :example: 'KeyboardEvent'
        :param options: Event options.
        :example: { 'bubbles': True, 'cancelable': False }
        :type options: dict
        """
        if not isinstance(element, (tuple, list)):
            element = [element]
        if not isinstance(event, (tuple, list)):
            event = [event]
        for el in element:
            for e in event:
                self.browser.execute_script(
                    'e = new %s("%s"); ops = %s; if (ops) {for(key in ops) { \
                        Object.defineProperty(e, key, { value: ops[key], configurable: true }) \
                    }} arguments[0].dispatchEvent(e)' % (
                        event_type if event_type else 'Event',
                        e, json.dumps(options) if options else 'undefined'
                    ), el)

    def trigger_keypress(self, element, key_code):
        """
        :Description: Trigger specific key "keypress" event on given element.
        :Warning: This method will be deprecated in version 2, use trigger_event.
        :param element: Element for browser instance to target.
        :type element: WebElement
        :param key_code: Code of key to invoke event.
        :type key_code: int
        """
        warnings.warn('Deprecated in version 2 switch to `trigger_event`', UserWarning)
        self.browser.execute_script(
            'var e = new Event("KeyboardEvent"); \
            e.initEvent("keypress", true, true); \
            e.which=%s; arguments[0].dispatchEvent(e);' % key_code,
            element)

    def scroll_into_view(self, element):
        """
        :Description: Scroll the target element into view.
        :Warning: This method relies on JQuery.
        :param element: Element for browser instance to target.
        :type element: WebElement
        """
        self.browser.execute_script('arguments[0].scrollIntoView();', element)

    @property
    def get_scrolling_offsets(self):
        """
        :Description: Returns the page scrolling x and y offsets.
        :return: dict
        """
        return {
            'x': self.browser.execute_script('return window.pageXOffset'),
            'y': self.browser.execute_script('return window.pageYOffset')
        }

    def ng_enable_debugging(self):
        """
        :Description: Enables angular debugging on given webpage.
        :Warning: This will only work for angular.js 1.x.
        """
        self.browser.execute_script('angular.reloadWithDebugInfo()')

    def ng_get_text(self, element):
        """
        :Description: Will return the DOM's value, if not found will default to `innerHTML`.
        :Warning: This will only work for angular.js 1.x.
        :Warning: This will only work for angular elements.
        :param element: Element for browser instance to target.
        :type element: WebElement
        :return: basestring
        """
        return self.browser.execute_script('return angular.element(arguments[0]).text();', element)

    def ng_set_text(self, element, text):
        """
        :Description: Will set a DOM's value, if not found will default to `innerHTML`.
        :Warning: This will only work for angular.js 1.x.
        :Warning: This will only work for angular elements.
        :param element: Element for browser instance to target.
        :type element: WebElement
        :param text: Text used for related operation.
        :type text: basestring
        """
        self.browser.execute_script('angular.element(arguments[0]).text("%s");' % text, element)

    def ng_toggle_class(self, element, target):
        """
        :Description: Toggle DOM class.
        :Warning: This will only work for angular.js 1.x.
        :Warning: This will only work for angular elements.
        :param element: Element for browser instance to target.
        :param target: Class to toggle.
        """
        self.browser.execute_script(
            'angular.element(arguments[0]).toggleClass("%s");' % target, element)

    def ng_trigger_event_handler(self, element, event):
        """
        :Description: Trigger angular event handler of element.
        :Warning: This will only work for angular.js 1.x.
        :Warning: This will only work for angular elements.
        :param element: Element for browser instance to target.
        :param event: Event to trigger.
        """
        self.browser.execute_script(
            'angular.element(arguments[0]).triggerHandler("%s");' % event, element)

    @staticmethod
    def __d2b_notation(prop):
        """
        :Description: Transform javascript dot notation to bracket notation.
        :param prop: Property to transform.
        :type prop: basestring
        :example: 'messages.total' >> someObject['messages']['total']
        :return: basestring
        """
        results = re.compile('[[$a-zA-Z]{0,}.').findall(prop)
        for i in range(0, len(results)):
            results[i] = ("['%s']" % results[i]).replace('.', '')
        return ''.join(results)

    @classmethod
    def __serialize_params(cls, params):
        param_str = ''
        for param in params:
            param_str += '%s,' % cls.__type2js(value=param)
        if param_str.endswith(','):
            param_str = param_str.replace(param_str[-1], '')
        return param_str

    def ng_get_scope_property(self, element, prop):
        """
        :Description: Will return value of property of element's scope.
        :Warning: This will only work for angular.js 1.x.
        :Warning: Requires angular debugging to be enabled.
        :param element: Element for browser instance to target.
        :param prop: Property of element's angular scope to target.
        :type prop: basestring
        :example: 'messages.total'
        :return: basestring
        """
        return self.browser.execute_script(
            'return angular.element(arguments[0]).scope()%s;' % self.__d2b_notation(
                prop=prop
            ), element)

    def ng_set_scope_property(self, element, prop, value):
        """
        :Description: Will set value of property of angular element's scope.
        :Warning: This will only work for angular.js 1.x.
        :Warning: Requires angular debugging to be enabled.
        :param element: Element for browser instance to target.
        :param prop: Property of element's angular scope to target.
        :type prop: basestring
        :example: 'messages.total'
        :param value: Value to specify to angular element's scope's property.
        :type value: None, bool, int, float, basestring
        """
        self.browser.execute_script(
            'angular.element(arguments[0]).scope()%s = %s;' % (
                self.__d2b_notation(prop=prop), self.__type2js(value=value)
            ), element)

    def ng_call_scope_function(self, element, func, params='', return_out=False):
        """
        :Description: Will execute scope function with provided parameters.
        :Warning: This will only work for angular.js 1.x.
        :Warning: Requires angular debugging to be enabled.
        :param element: Element for browser instance to target.
        :param func: Function to execute from angular element scope.
        :type func: basestring
        :param params: String (naked) args, or list of parameters to pass to target function.
        :type params: basestring, tuple, list
        :param return_out: Return output of function call otherwise None
        :type return_out: bool
        """
        if isinstance(params, basestring):
            param_str = params
        elif isinstance(params, (tuple, list)):
            param_str = self.__serialize_params(params)
        else:
            raise ValueError('Invalid type specified for function parameters')
        exec_str = 'angular.element(arguments[0]).scope().%s(%s);' % (func, param_str)
        if return_out:
            return self.__type2python(
                self.browser.execute_script('return {}'.format(exec_str), element))
        else:
            self.browser.execute_script(exec_str, element)

    def ng_get_ctrl_property(self, element, prop):
        """
        :Description: Will return value of property of element's controller.
        :Warning: This will only work for angular.js 1.x.
        :Warning: Requires angular debugging to be enabled.
        :param element: Element for browser instance to target.
        :type element: WebElement
        :param prop: Property of element's angular controller to target.
        :type prop: basestring
        :example: 'messages.total'
        :return: basestring
        """
        return self.browser.execute_script(
            'return angular.element(arguments[0]).controller()%s;' % self.__d2b_notation(prop=prop),
            element)

    def ng_set_ctrl_property(self, element, prop, value):
        """
        :Description: Will set value of property of element's controller.
        :Warning: This will only work for angular.js 1.x.
        :Warning: Requires angular debugging to be enabled.
        :param element: Element for browser instance to target.
        :type element: WebElement
        :param prop: Property of element's angular scope to target.
        :type prop: basestring
        :example: 'messages.total'
        :param value: Value to specify to angular element's controller's property.
        :type value: None, bool, int, float, basestring
        """
        self.browser.execute_script(
            'angular.element(arguments[0]).controller()%s = %s;' % (
                self.__d2b_notation(prop=prop), self.__type2js(value=value)
            ), element)

    def ng_call_ctrl_function(self, element, func, params='', return_out=False):
        """
        :Description: Will execute controller function with provided parameters.
        :Warning: This will only work for angular.js 1.x.
        :Warning: Requires angular debugging to be enabled.
        :param element: Element for browser instance to target.
        :param func: Function to execute from angular element controller.
        :type func: basestring
        :param params: String (naked) args, or list of parameters to pass to target function.
        :type params: basestring, tuple, list
        :param return_out: Return output of function call otherwise None
        :type return_out: bool
        """
        if isinstance(params, basestring):
            param_str = params
        elif isinstance(params, (tuple, list)):
            param_str = self.__serialize_params(params)
        else:
            raise ValueError('Invalid type specified for function parameters')
        exec_str = 'angular.element(arguments[0]).controller().%s(%s);' % (func, param_str)
        if return_out:
            return self.__type2python(
                self.browser.execute_script('return {}'.format(exec_str), element))
        else:
            self.browser.execute_script(exec_str, element)

    def ng2_get_component_property(self, element, prop):
        """
        :Description: Will get value of property of element's component instance.
        :Warning: This will only work for Angular components.
        :param element: Element for browser instance to target.
        :type element: WebElement
        :param prop: Property of element's component to target.
        :type prop: basestring
        :example: 'messages.total'
        :return: basestring
        """
        return self.browser.execute_script(
            'return ng.probe(arguments[0]).componentInstance%s;' % self.__d2b_notation(prop=prop),
            element)

    def ng2_set_component_property(self, element, prop, value):
        """
        :Description: Will set value of property of element's component instance.
        :Warning: This will only work for Angular components.
        :param element: Element for browser instance to target.
        :type element: WebElement
        :param prop: Property of element's component to target.
        :type prop: basestring
        :example: 'messages.total'
        :param value: Value to specify to component's property.
        :type value: None, bool, int, float, basestring
        """
        self.browser.execute_script(
            'ng.probe(arguments[0]).componentInstance%s = %s;' % (
                self.__d2b_notation(prop=prop), self.__type2js(value=value)
            ), element)

    def ng2_call_component_function(self, element, func, params='', return_out=False):
        """
        :Description: Will execute the component instance function with provided parameters.
        :Warning: This will only work for Angular components.
        :param element: Element for browser instance to target.
        :param func: Function to execute from component instance.
        :type func: basestring
        :param params: String (naked) args, or list of parameters to pass to target function.
        :type params: basestring, tuple, list
        :param return_out: Return output of function call otherwise None
        :type return_out: bool
        """
        if isinstance(params, basestring):
            param_str = params
        elif isinstance(params, (tuple, list)):
            param_str = self.__serialize_params(params)
        else:
            raise ValueError('Invalid type specified for function parameters')
        exec_str = 'ng.probe(arguments[0]).componentInstance.%s(%s);' % (func, param_str)
        if return_out:
            return self.__type2python(
                self.browser.execute_script('return {}'.format(exec_str), element))
        else:
            self.browser.execute_script(exec_str, element)
