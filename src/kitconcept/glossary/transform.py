# -*- coding: utf-8 -*-
from AccessControl.unauthorized import Unauthorized
from cgi import escape
from kitconcept.glossary.interfaces import IGlossarySettings
from kitconcept.glossary.logger import logger
from lxml import etree
from plone import api
from plone.transformchain.interfaces import ITransform
from Products.CMFPlone.utils import safe_unicode
from repoze.xmliter.utils import getHTMLSerializer
from zExceptions import NotFound
from zope.interface import implementer
from zope.interface import Interface

import re


try:
    # Python 2.6-2.7 
    from HTMLParser import HTMLParser
except ImportError:
    # Python 3
    from html.parser import HTMLParser


try:
    from Products.Archetypes.interfaces import IBaseObject
except ImportError:
    class IBaseObject(Interface):
        pass


try:
    from plone.dexterity.interfaces import IDexterityContent
except ImportError:
    class IDexterityContent(Interface):
        pass


# to avoid additional network round trips to render content above the fold
# we only process elements inside the "content" element
ROOT_SELECTOR = u'//*[@id="content"]'

# search for element text: https://stackoverflow.com/a/2756994/2116850
TEXT_SELECTOR = u'{0}//*[re:match(text(), "{1}", "gi")]'

GLOSSARY_TAG = u"""
<spam class="highlightedGlossaryTerm"
   data-term="{0}"
   data-definition="{2}"
   data-url="{3}">
    {1}
</spam>
"""


@implementer(ITransform)
class GlossaryTransform(object):

    """Transform a response to lazy load <img> and <iframe> elements."""

    order = 8888

    def __init__(self, published, request):
        self.published = published
        self.request = request

    def _parse(self, result):
        """Create an XMLSerializer from an HTML string, if needed."""
        content_type = self.request.response.getHeader('Content-Type')
        if not content_type or not content_type.startswith('text/html'):
            return

        try:
            return getHTMLSerializer(result)
        except (AttributeError, TypeError, etree.ParseError):
            return

    def _apply_glossary_tag(self, term, definition, url):
        """This method is needed just to keep the original case of term
        """
        def currying(match):
            before = match.group(1)
            matched_term = match.group(2)
            after = match.group(3)
            return '{0}{1}{2}'.format(
                before,
                GLOSSARY_TAG.format(term, matched_term, definition, url),
                after
            )
        return currying

    def _apply_glossary(self, element, term, definition, url):
        """Inject attributes needed by lazysizes to lazy load elements.
        For more information, see: https://afarkas.github.io/lazysizes
        """
        term = safe_unicode(term)
        definition = escape(safe_unicode(definition), quote=True)
        parser = HTMLParser()
        html = etree.tostring(element)
        html = parser.unescape(html)
        pattern = re.compile(
            u'(.*)({0})(.*)'.format(term),
            flags=re.IGNORECASE|re.DOTALL|re.UNICODE,
        )
        new_html = pattern.sub(
            self._apply_glossary_tag(term, definition, url), html)
        new_element = etree.fromstring(new_html)
        parent = element.getparent()
        parent.replace(element, new_element)
        logger.debug(u'Find glossary for term "{0}".'.format(term))

    def transformBytes(self, result, encoding):
        return

    def transformUnicode(self, result, encoding):
        return

    def transformIterable(self, result, encoding):
        # user is authenticated, check if transform is enabled
        enabled = api.portal.get_registry_record(
            name='enable_tooltip',
            interface=IGlossarySettings,
            default=False,
        )
        if not enabled:
            return  # no need to transform

        # don't run for types not enabled
        enabled_types = api.portal.get_registry_record(
            name='enabled_content_types',
            interface=IGlossarySettings,
            default=[],
        )
        path = self.request.environ['PATH_INFO']
        try:
            context = api.content.get(path=path)
        except (IndexError, NotFound, Unauthorized):
            return  # no need to transform
        if context is None:
            return  # no need to transform
        if not IBaseObject.providedBy(context) and \
           not IDexterityContent.providedBy(context):
            return  # no need to transform
        if context.portal_type not in enabled_types:
            return  # no need to transform
        if not result:
            return  # no need to transform
        result = self._parse(result)
        if result is None:
            return  # no need to transform

        for brain in api.content.find(portal_type='Term'):
            xpath = TEXT_SELECTOR.format(ROOT_SELECTOR, brain.Title.lower())
            for el in result.tree.xpath(
                xpath, namespaces={"re": "http://exslt.org/regular-expressions"}):
                self._apply_glossary(el, brain.Title, brain.definition, brain.getURL())
            for variant in brain.variants:
                xpath = TEXT_SELECTOR.format(ROOT_SELECTOR, variant.lower())
                for el in result.tree.xpath(
                    xpath, namespaces={"re": "http://exslt.org/regular-expressions"}):
                    self._apply_glossary(el, variant, brain.definition, brain.getURL())

        return result
