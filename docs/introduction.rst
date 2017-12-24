============
Introduction
============

About
=====

pyselenium-js is a very simple, lightweight module that helps relieve some of the burden of e2e testing with the official Selenium bindings.
The official Selenium bindings operate in the most natural way a user would operate against a given web page.
The problem with this, is with more advanced and modern websites, these bindings may not always work as expected on custom elements and components.

An example of this being a div tag taking keyboard input, where div tags do not support the onfocus event listener by design -- and the selenium bindings invoke this before attempting to send input to the target DOM.
