# -*- coding: utf-8 -*-
from kitconcept.glossary.testing import INTEGRATION_TESTING
from kitconcept.glossary.transform import GlossaryTransform
from plone import api

import lxml
import unittest


HTML = u"""<html>
  <body>
    <div id="content">
      <p>{text}</p>
    </div>
  </body>
</html>
"""


class TransformerTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.request.response.setHeader('Content-Type', 'text/html')
        self.transformer = GlossaryTransform(None, self.request)

        with api.env.adopt_roles(['Manager']):
            self.glossary = api.content.create(
                container=self.portal,
                type='Glossary',
                title='Glossary',
            )

        api.content.create(
            container=self.glossary,
            type='Term',
            title='Term',
        )
        api.content.create(
            container=self.glossary,
            type='Term',
            title='Universität',
        )
        api.content.create(
            container=self.glossary,
            type='Term',
            title='CASE Insensitive',
        )

    def test_glossary_applied(self):
        with api.env.adopt_roles(['Manager']):
            document = api.content.create(
                container=self.portal,
                type='Document',
                title='Document',
            )
        self.request.environ['PATH_INFO'] = '/'.join(
            document.getPhysicalPath())
        html = HTML.format(text='Glossary Term')
        result = self.transformer.transformIterable(html, 'utf-8')
        self.assertTrue(
            result.tree.xpath('//*[@class="highlightedGlossaryTerm"]'))

    def test_accents(self):
        with api.env.adopt_roles(['Manager']):
            document = api.content.create(
                container=self.portal,
                type='Document',
                title='Document',
            )
        self.request.environ['PATH_INFO'] = '/'.join(
            document.getPhysicalPath())
        html = HTML.format(text='Plone Universität')
        result = self.transformer.transformIterable(html, 'utf-8')
        self.assertTrue(
            result.tree.xpath('//*[@class="highlightedGlossaryTerm"]'))

    def test_case_insensitive(self):
        with api.env.adopt_roles(['Manager']):
            document = api.content.create(
                container=self.portal,
                type='Document',
                title='Document',
            )
        self.request.environ['PATH_INFO'] = '/'.join(
            document.getPhysicalPath())
        html = HTML.format(text='case insensitive')
        result = self.transformer.transformIterable(html, 'utf-8')
        self.assertTrue(
            result.tree.xpath('//*[@class="highlightedGlossaryTerm"]'))
