# -*- coding: utf-8 -*-
from kitconcept.glossary.interfaces import IGlossaryTerm
from kitconcept.glossary.testing import INTEGRATION_TESTING
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class GlossaryTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        with api.env.adopt_roles(['Manager']):
            self.g1 = api.content.create(self.portal, 'Glossary', 'g1')

        self.t1 = api.content.create(self.g1, 'GlossaryTerm', 't1')

    def test_adding(self):
        self.assertTrue(IGlossaryTerm.providedBy(self.t1))

    def test_adding_outside_glossary(self):
        from plone.api.exc import InvalidParameterError
        with self.assertRaises(InvalidParameterError):
            api.content.create(self.portal, 'GlossaryTerm', 'test')

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='GlossaryTerm')
        self.assertIsNotNone(fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='GlossaryTerm')
        schema = fti.lookupSchema()
        self.assertEqual(IGlossaryTerm, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='GlossaryTerm')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IGlossaryTerm.providedBy(new_object))
