# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = "1.0.0a1.dev0"
description = "Plone add-on product to define a glossary."
long_description = (
    open("README.rst").read()
    + "\n\n"
    + open("CHANGES.rst").read()
)

setup(
    name="kitconcept.glossary",
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.1",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="plone glossary",
    author="kitconcept GmbH",
    author_email="info@kitconcept.com",
    url="https://github.com/kitconcept/kitconcept.glossary",
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages=["kitconcept"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "plone.api",
        "plone.app.dexterity",
        "plone.app.registry",
        "plone.dexterity",
        "plone.namedfile",
        "Products.CMFPlone >=4.3",
        "Products.GenericSetup",
        "setuptools",
        "zope.globalrequest",
        "zope.i18nmessageid",
        "zope.interface",
        "zope.schema",
    ],
    extras_require={
        "test": [
            "AccessControl",
            "plone.app.robotframework",
            "plone.app.testing [robot]",
            "plone.browserlayer",
            "plone.registry",
            "plone.testing",
            "robotsuite",
            "zope.component",
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
