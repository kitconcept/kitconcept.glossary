# -*- coding: utf-8 -*-
from kitconcept.glossary.testing import INTEGRATION_TESTING
from plone import api
from plone.app.textfield.value import RichTextValue

import unittest


class BaseViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]

        with api.env.adopt_roles(["Manager"]):
            self.g1 = api.content.create(
                self.portal,
                "Glossary",
                "g1",
                title="Glossary",
                description="Glossary Description",
            )
            self.t1 = api.content.create(
                self.g1,
                "GlossaryTerm",
                "t1",
                title="First Term",
                definition=RichTextValue(
                    "First Term Description", "text/html", "text/html"
                ),
            )
            self.t2 = api.content.create(
                self.g1,
                "GlossaryTerm",
                "t2",
                title="Second Term",
                definition=RichTextValue(
                    "Second Term Description", "text/html", "text/html"
                ),
            )
            self.d1 = api.content.create(
                self.portal,
                "Document",
                "d1",
                title="Document",
                description="Document Description",
            )


class TermViewTestCase(BaseViewTestCase):
    def setUp(self):
        super(TermViewTestCase, self).setUp()
        self.view = api.content.get_view(u"view", self.t1, self.request)

    def test_get_entry(self):
        expected = {
            "definition": "First Term Description",
            "variants": None,
            "term": "First Term",
        }
        self.assertEqual(self.view.get_entry(), expected)


class GlossaryViewTestCase(BaseViewTestCase):
    def setUp(self):
        super(GlossaryViewTestCase, self).setUp()
        self.view = api.content.get_view(u"view", self.g1, self.request)
