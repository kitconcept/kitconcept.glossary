# -*- coding: utf-8 -*-
from kitconcept.glossary.testing import INTEGRATION_TESTING
from kitconcept.glossary.transform import GlossaryTransform
from plone import api

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
        portal = self.layer['portal']
        request = self.layer['request']
        request.response.setHeader('Content-Type', 'text/html')
        self.transformer = GlossaryTransform(None, request)

        with api.env.adopt_roles(['Manager']):
            document = api.content.create(
                container=portal,
                type='Document',
                title='Document',
            )
            glossary = api.content.create(
                container=portal,
                type='Glossary',
                title=u'Glossary',
            )

        api.content.create(
            container=glossary,
            type='Term',
            title=u'Term',
        )
        api.content.create(
            container=glossary,
            type='Term',
            title=u'Universität',
        )
        api.content.create(
            container=glossary,
            type='Term',
            title=u'CASE Insensitive',
        )

        request.environ['PATH_INFO'] = '/'.join(
            document.getPhysicalPath())

    def test_glossary_applied(self):
        html = HTML.format(text=u'Glossary Term')
        result = self.transformer.transformIterable(html, 'utf-8')
        self.assertTrue(
            result.tree.xpath('//*[@class="highlightedGlossaryTerm"]'))

    def test_accents(self):
        html = HTML.format(text=u'Plone Universität')
        result = self.transformer.transformIterable(html, 'utf-8')
        self.assertTrue(
            result.tree.xpath('//*[@class="highlightedGlossaryTerm"]'))

    def test_case_insensitive(self):
        html = HTML.format(text=u'case insensitive')
        result = self.transformer.transformIterable(html, 'utf-8')
        self.assertTrue(
            result.tree.xpath('//*[@class="highlightedGlossaryTerm"]'))
