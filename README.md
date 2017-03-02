# pyselenium-js
Lightweight, Python module to execute frequently used javascript functionality on a Selenium webdriver.

### About
**pyselenium-js** is a very simple, lightweight module that helps relieve some of the burden of E2E testing with the official Selenium bindings.
The official Selenium bindings operate in the most natural way a user would operate against a given web page.
The problem with this, is with more advanced and modern websites, these bindings may not always work as expected on custom DOMs.

### Usage
Simply place `e2ejs.py` in your prefered directory and import it into your project.
A very clean, and simply approach to referencing this library is instantiating it in your page object or factory, so it may be referenced with your active webdriver instance.

===
Copyright (c) 2017 John Nolette Licensed under the Apache License, Version 2.0.
