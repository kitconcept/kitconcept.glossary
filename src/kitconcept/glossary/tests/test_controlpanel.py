# -*- coding: utf-8 -*-
from kitconcept.glossary.controlpanel import IGlossarySettings
from kitconcept.glossary.interfaces import IGlossaryLayer
from kitconcept.glossary.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import logout
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import alsoProvides
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

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


class ControlPanelTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        alsoProvides(self.request, IGlossaryLayer)
        self.controlpanel = self.portal["portal_controlpanel"]

    def test_controlpanel_has_view(self):
        view = api.content.get_view(u"glossary-settings", self.portal, self.request)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized

        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse("@@glossary-settings")

    def test_controlpanel_installed(self):
        actions = [a.getAction(self)["id"] for a in self.controlpanel.listActions()]
        self.assertIn("glossary", actions)

    # def test_controlpanel_removed_on_uninstall(self):
    #     qi = self.portal["portal_quickinstaller"]

    #     with api.env.adopt_roles(["Manager"]):
    #         qi.uninstallProducts(products=[PROJECTNAME])

    #     actions = [a.getAction(self)["id"] for a in self.controlpanel.listActions()]
    #     self.assertNotIn("glossary", actions)


class RegistryTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(IGlossarySettings)  # noqa: P001

    def test_enable_tooltip_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, "enable_tooltip"))
        self.assertEqual(self.settings.enable_tooltip, True)

    def test_enabled_content_types_record_in_registry(self):
        from kitconcept.glossary.config import DEFAULT_ENABLED_CONTENT_TYPES

        self.assertTrue(hasattr(self.settings, "enabled_content_types"))
        self.assertEqual(
            self.settings.enabled_content_types, DEFAULT_ENABLED_CONTENT_TYPES
        )

    def test_records_removed_on_uninstall(self):
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstallProducts(["kitconcept.glossary"])

        records = [
            IGlossarySettings.__identifier__ + ".enable_tooltip",
            IGlossarySettings.__identifier__ + ".enabled_content_types",
        ]

        for r in records:
            self.assertNotIn(r, self.registry)
