# -*- coding: utf-8 -*-
from kitconcept.glossary.testing import INTEGRATION_TESTING
from plone.browserlayer.utils import registered_layers
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone import api

import unittest

try:
    from Products.CMFPlone.factory import _IMREALLYPLONE5

    _IMREALLYPLONE5  # noqa
except ImportError:
    PLONE_5 = False
else:
    PLONE_5 = True

try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.installProducts(['kitconcept.glossary'])

    def test_product_installed(self):
        self.assertTrue(self.installer.isProductInstalled(
            'kitconcept.glossary'))

    def test_addon_layer(self):
        layers = [layer.getName() for layer in registered_layers()]
        self.assertIn("IGlossaryLayer", layers)

    def test_add_glossary_permission(self):
        permission = "kitconcept.glossary: Add Glossary"
        roles = self.portal.rolesOfPermission(permission)
        roles = [r["name"] for r in roles if r["selected"]]
        expected = ["Contributor", "Manager", "Owner", "Site Administrator"]
        self.assertListEqual(roles, expected)

    def test_add_term_permission(self):
        permission = "kitconcept.glossary: Add Glossary Term"
        roles = self.portal.rolesOfPermission(permission)
        roles = [r["name"] for r in roles if r["selected"]]
        expected = ["Contributor", "Manager", "Owner", "Site Administrator"]
        self.assertListEqual(roles, expected)


class UninstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['kitconcept.glossary'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        self.assertFalse(
            self.installer.isProductInstalled('kitconcept.glossary')
        )

    # def test_browserlayer_removed(self):
    #     from kitconcept.glossary.interfaces import IGlossaryLayer
    #     from plone.browserlayer import utils

    #     self.assertNotIn(IGlossaryLayer, utils.registered_layers())
