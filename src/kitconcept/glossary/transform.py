# -*- coding: utf-8 -*-
from AccessControl.unauthorized import Unauthorized
from cgi import escape
from kitconcept.glossary.interfaces import IGlossarySettings
from kitconcept.glossary.logger import logger
from lxml import etree
from plone import api
from plone.transformchain.interfaces import ITransform
from repoze.xmliter.utils import getHTMLSerializer
from zExceptions import NotFound
from zope.interface import implementer
from zope.interface import Interface


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

# search for element text
TEXT_SELECTOR = u'{0}//*[contains(concat(" ", normalize-space(text()), " "), " {1} ")]'

GLOSSARY_TAG = u"""
<spam class="highlightedGlossaryTerm"
   data-term="{0}"
   data-definition="{1}"
   data-url="{2}">
    {0}
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

    def _apply_glossary(self, element, term, definition, url):
        """Inject attributes needed by lazysizes to lazy load elements.
        For more information, see: https://afarkas.github.io/lazysizes
        """
        # https://stackoverflow.com/a/6208001/2116850
        term = term.decode('utf-8').encode('ascii', 'xmlcharrefreplace')
        definition = definition.decode(
            'utf-8').encode('ascii', 'xmlcharrefreplace')
        definition = escape(definition, quote=True)
        html = etree.tostring(element)
        new_html = html.replace(
            term, GLOSSARY_TAG.format(term, definition, url))
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
        except (NotFound, Unauthorized):
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
            xpath = TEXT_SELECTOR.format(ROOT_SELECTOR, brain.Title)
            for el in result.tree.xpath(xpath):
                self._apply_glossary(el, brain.Title, brain.definition, brain.getURL())
            for variant in brain.variants:
                xpath = TEXT_SELECTOR.format(ROOT_SELECTOR, variant)
                for el in result.tree.xpath(xpath):
                    self._apply_glossary(el, variant, brain.definition, brain.getURL())

        return result
