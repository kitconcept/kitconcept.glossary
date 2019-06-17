# -*- coding: utf-8 -*-
from kitconcept.glossary.interfaces import IGlossary
from kitconcept.glossary.interfaces import ITerm
from plone.dexterity.content import Container
from plone.dexterity.content import Item
from zope.interface import implementer

import lxml


@implementer(IGlossary)
class Glossary(Container):

    """A Glossary is a container for Terms."""


@implementer(ITerm)
class Term(Item):

    """A Term."""

    def Description(self):
        if not self.definition:
            return ''
        tree = lxml.html.fromstring(u'<div>%s</div>' %
                                    self.definition.output)
        text = tree.text_content()
        return text
