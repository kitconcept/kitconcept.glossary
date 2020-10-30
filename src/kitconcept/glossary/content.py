# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import safe_unicode
from kitconcept.glossary.interfaces import IGlossary
from kitconcept.glossary.interfaces import IGlossaryTerm
from plone.dexterity.content import Container
from plone.dexterity.content import Item
from zope.interface import implementer

import lxml


@implementer(IGlossary)
class Glossary(Container):

    """A Glossary is a container for Terms."""


@implementer(IGlossaryTerm)
class GlossaryTerm(Item):
    def Description(self):
        if not self.definition:
            return ""
        tree = lxml.html.fromstring(u"<div>%s</div>" % self.definition.output)
        text = tree.text_content()
        # Remove lxml ElementUnicodeResult which is a subclass of unicode
        text = safe_unicode(text.encode("utf-8"))
        return text
