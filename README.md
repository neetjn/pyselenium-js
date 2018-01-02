# pyselenium-js

[![build](https://travis-ci.org/neetjn/pyselenium-js.svg?branch=master)](https://travis-ci.org/neetjn/pyselenium-js)
[![Documentation Status](https://readthedocs.org/projects/pyselenium-js/badge/?version=latest)](http://pyselenium-js.readthedocs.io/en/latest/?badge=latest)
[![Code Health](https://landscape.io/github/neetjn/pyselenium-js/master/landscape.svg?style=flat)](https://landscape.io/github/neetjn/pyselenium-js/master)
[![codecov](https://codecov.io/gh/neetjn/pyselenium-js/branch/master/graph/badge.svg)](https://codecov.io/gh/neetjn/pyselenium-js)

[![PyPI version](https://badge.fury.io/py/pyseleniumjs.svg)](https://badge.fury.io/py/pyseleniumjs)
[![Join the chat at https://gitter.im/riot-view-router/Lobby](https://badges.gitter.im/riot-view-router/Lobby.svg)](https://gitter.im/riot-view-router/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Lightweight python module to execute frequently used javascript functionality on a Selenium webdriver.

For an all inclusive selenium framework check out [py-component-controller](https://github.com/neetjn/py-component-controller)!

Official documentation be be read [here](http://pyselenium-js.readthedocs.io).

### About

**pyselenium-js** is a very simple, lightweight module that helps relieve some of the burden of e2e testing with the official Selenium bindings.
The official Selenium bindings operate in the most natural way a user would operate against a given web page.
The problem with this, is with more advanced and modern websites, these bindings may not always work as expected on custom elements or components.

An example of this being a div tag taking keyboard input, where div tags do not support the `onfocus` event listener by design -- and the selenium bindings invoke this before attempting to send input to the target DOM.

### Usage

This project was created using selenium `3.6.0`.

Support is available for both Python 2.7 and 3.6.

**pyselenium-js** and can be installed using pip like so,

```bash
pip install pyseleniumjs
```

For more information refer to the official documentation [here](http://pyselenium-js.readthedocs.io).

### Testing

All module related e2e tests are in the `pyselenium/tests` subdirectory. To setup your environment run `make setup`. To stand up the mock site, run `make app`. This will serve the site on `localhost:3000`. To run the test suite, use `make tests`.

The mock website was created using angular.js 1.6, bulmacss, and webpack 3. It was designed to represent a common website layout with responsive capabilities. To add new features for unit tests, refer to [pyjs-mock-site](https://github.com/neetjn/pysjs-mock-site) and be sure to update the submodule commit accordingly.

*Note as of this time, tests for the Angular 2 bindings are not yet available.*

Requirements:
* Python 2.7, 3.6 (with pip)
* Chrome or Chromium (*last confirmed test used version 63*)
* ChromeDriver (*last confirmed test used version 2.33*)
* Node.js 6+ (with npm)

### Contributors

* **John Nolette** (john@neetgroup.net)

Contributing guidelines are as follows,

* Any new features added must also be unit tested in the `pyseleniumjs/tests` subdirectory.
  * Branches for bugs and features should be structured like so, `issue-x-username`.
* Include your name and email in the contributors list.

---

Copyright (c) 2017 John Nolette Licensed under the Apache License, Version 2.0.
