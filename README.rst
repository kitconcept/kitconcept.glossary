.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

==============================================================================
kitconcept.glossary
==============================================================================

.. image:: http://img.shields.io/pypi/v/kitconcept.glossary.svg
    :target: https://pypi.python.org/pypi/kitconcept.glossary

.. image:: https://img.shields.io/travis/kitconcept/kitconcept.glossary/master.svg
    :target: http://travis-ci.org/kitconcept/kitconcept.glossary

.. image:: https://img.shields.io/coveralls/kitconcept/kitconcept.glossary/master.svg
    :target: https://coveralls.io/r/kitconcept/kitconcept.glossary

|

.. image:: https://raw.githubusercontent.com/collective/kitconcept.glossary/master/kitconcept.png
   :alt: kitconcept
   :target: https://kitconcept.com/

Introduction
------------

A Dexterity-based content type to define a glossary and its terms.

This package is inspired by `PloneGlossary`_.

.. _`PloneGlossary`: https://pypi.python.org/pypi/Products.PloneGlossary

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


Installation
------------

Install kitconcept.glossary by adding it to your buildout::

   [buildout]

    ...

    eggs =
        kitconcept.glossary


and then run "bin/buildout".


Contribute
----------

- `Source code at Github <https://github.com/collective/kitconcept.glossary>`_
- `Issue tracker at Github <https://github.com/collective/kitconcept.glossary/issues>`_ or same


Support
-------

If you are having issues, `please let us know <https://github.com/collective/kitconcept.glossary/issues>`_.


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


Credits
-------

.. image:: https://www.hu-berlin.de/++resource++humboldt.logo.Logo.png
   :height: 97px
   :width: 434px
   :scale: 100 %
   :alt: HU Berlin
   :target: https://www.hu-berlin.de

|

The development of this plugin has been kindly sponsored by `Humboldt-Universität zu Berlin`_.

|

.. image:: https://raw.githubusercontent.com/collective/kitconcept.glossary/master/kitconcept.png
   :alt: kitconcept
   :target: https://kitconcept.com/

Developed by `kitconcept`_.


License
-------

The project is licensed under the GPLv2.


.. _Humboldt-Universität zu Berlin: https://www.hu-berlin.de
.. _kitconcept: http://www.kitconcept.com/

