********
Glossary
********

.. contents:: Table of Contents

Life, the Universe, and Everything
==================================

A Dexterity-based content type to define a glossary and its terms.

This package is inspired in `PloneGlossary`_.

.. _`PloneGlossary`: https://pypi.python.org/pypi/Products.PloneGlossary

Mostly Harmless
===============

.. image:: http://img.shields.io/pypi/v/kitconcept.glossary.svg
    :target: https://pypi.python.org/pypi/kitconcept.glossary

.. image:: https://img.shields.io/travis/kitconcept/kitconcept.glossary/master.svg
    :target: http://travis-ci.org/kitconcept/kitconcept.glossary

.. image:: https://img.shields.io/coveralls/kitconcept/kitconcept.glossary/master.svg
    :target: https://coveralls.io/r/kitconcept/kitconcept.glossary

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

.. _`opening a support ticket`: https://github.com/kitconcept/kitconcept.glossary/issues

Known issues
------------

See the `complete list of bugs on GitHub <https://github.com/kitconcept/kitconcept.glossary/labels/bug>`_.

Don't Panic
===========

Installation
------------

To enable this package in a buildout-based installation:

#. Edit your buildout.cfg and add ``kitconcept.glossary`` to the list of eggs to install:

.. code-block:: ini

    [buildout]
    ...
    eggs =
        kitconcept.glossary

After updating the configuration you need to run ''bin/buildout'', which will take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``kitconcept.glossary`` and click the 'Activate' button.

Usage
-----

TBD.


Screenshots
-----------

.. figure:: https://raw.github.com/kitconcept/kitconcept.glossary/master/docs/glossary.png
    :align: center
    :height: 640px
    :width: 768px

    Create a Glossary.

.. figure:: https://raw.github.com/kitconcept/kitconcept.glossary/master/docs/usage.png
    :align: center
    :height: 640px
    :width: 768px

    Use it!

.. figure:: https://raw.github.com/kitconcept/kitconcept.glossary/master/docs/controlpanel.png
    :align: center
    :height: 400px
    :width: 768px

    The tooltip can be disabled in the control panel configlet.


How does it work
----------------

The terms are loaded in a page using an AJAX call to a browser view that returns them as a JSON object.

The tooltips will only be available in the default view of a content type instance.


Look Ma! No Resource Registries
-------------------------------
This add-on uses a very opinionated approach on how to handle static resources in Plone.
We just deprecated resource registries in favor of a simpler approach: a viewlet in ``plone.htmlhead``.
This simplifies maintainance among multiple Plone versions and avoids bundling of unrelated resources.


Development
-----------

Requirements:

- Python 2.7
- Virtualenv

Setup::

  make

Run Static Code Analysis::

  make code-Analysis

Run Unit / Integration Tests::

  make test

Run Robot Framework based acceptance tests::

  make test-acceptance
