# -*- coding: utf-8 -*-
from kitconcept.glossary.interfaces import IGlossarySettings
from plone import api
from plone.app.layout.viewlets import ViewletBase
from plone.memoize import ram
from plone.memoize.instance import memoize
from Products.CMFPlone.PloneBatch import Batch
from Products.Five.browser import BrowserView
from Products.PloneGlossary.utils import encode_ascii
from zExceptions import Redirect

import json
import string


BATCH_SIZE = 30
PLONEGLOSSARY_TOOL = 'portal_glossary'


def _catalog_counter_cachekey(method, self):
    """Return a cachekey based on catalog updates."""

    catalog = api.portal.get_tool('portal_catalog')
    return str(catalog.getCounter())


class TermView(BrowserView):

    """Default view for Term type"""

    def get_entry(self):
        """Get term in the desired format"""

        item = {
            'term': self.context.title,
            'variants': self.context.variants,
            'definition': self.context.definition.raw,
        }
        return item


class GlossaryView(BrowserView):

    """Default view of Glossary type"""

    def __init__(self, context, request):
        super(GlossaryView, self).__init__(context, request)
        self.search_letter = request.get('search_letter', '')
        self.search_text = request.get('search_text')
        self.batch_start = request.get('b_start', 0)
        self.uid = context.UID()
        # self.gtool = get Tool By Name(context, PLONEGLOSSARY_TOOL)

    def title(self):
        """Title of our glossary"""

        return self.context.title_or_id()

    def first_letters(self):
        """Users with non latin chars (cyrillic, arabic, ...) should override
        this with a better suited dataset."""

        out = []
        existing = self.gtool.getAbcedaire([self.uid])
        glossary_url = self.context.absolute_url()
        for letter in tuple(string.ascii_uppercase):
            letter_map = {
                'glyph': letter,
                'has_no_term': letter.lower() not in existing,
                'zoom_link': glossary_url + '?search_letter=' + letter.lower(),
                'css_class': (letter.lower() == self.search_letter.lower() and
                              'selected' or None),
            }
            out.append(letter_map)
        return out

    def has_results(self):
        """Something to show ?"""

        return len(self._list_results()) > 0

    def batch_results(self):
        """Wrap all results in a batch"""

        results = self._list_results()
        batch = Batch(results, BATCH_SIZE, int(self.batch_start), orphan=1)
        return batch

    @memoize
    def _list_results(self):
        """Terms list (brains) depending on the request"""

        gtool = self.gtool
        if self.search_letter:
            # User clicked a letter
            results = gtool.getAbcedaireBrains([self.uid],
                                               letters=[self.search_letter])
        elif self.search_text:
            # User searches for text
            # results = gtool.search Results([self.uid],
            #                              SearchableText=self.search_text)
            # We redirect to the result if unique
            if len(results) == 1:
                target = results[0].getURL()
                raise Redirect(target)
        # else:
        #     # Viewing all terms
        #     results = gtool.search Results([self.uid])
        results = list(results)
        results.sort(lambda x, y: cmp(encode_ascii(x.Title),
                                      encode_ascii(y.Title)))
        return tuple(results)

    def result_features(self, result):
        """TAL friendly properties of each feature"""

        description = self.gtool.truncateDescription(result.Description)
        return {
            'url': result.getURL(),
            'title': result.Title or result.getId,
            'description': description.replace('\n', '<br />'),
        }


class GlossaryStateView(BrowserView):
    """Glossary State view used to enable or disable resources

    This is called by JS and CSS resources registry
    """

    @property
    def tooltip_is_enabled(self):
        """Check if term tooltip is enabled."""
        return api.portal.get_registry_record(
            IGlossarySettings.__identifier__ + '.enable_tooltip')

    @property
    def content_type_is_enabled(self):
        """Check if we must show the tooltip in this context."""
        context = self.context
        if getattr(context, 'default_page', False) and context.id != context.default_page:
            context = context.get(context.default_page)
        portal_type = getattr(context, 'portal_type', None)
        enabled_content_types = api.portal.get_registry_record(
            IGlossarySettings.__identifier__ + '.enabled_content_types')
        return portal_type in enabled_content_types

    def __call__(self):
        response = self.request.response
        response.setHeader('content-type', 'application/json')

        data = {
            'enabled': self.tooltip_is_enabled and self.content_type_is_enabled,
        }
        return response.setBody(json.dumps(data))


class JsonView(BrowserView):
    """Json view that return all glossary items in json format

    This view is used into an ajax call for
    """

    @ram.cache(_catalog_counter_cachekey)
    def get_json_entries(self):
        """Get all itens and prepare in the desired format.
        Note: do not name it get_entries, otherwise caching is broken. """

        catalog = api.portal.get_tool('portal_catalog')

        items = []
        for brain in catalog(portal_type='Term'):
            items.append({
                'term': brain.Title,
                'definition': brain.definition,
            })
            if brain.variants is None:
                continue
            for variant in brain.variants:
                items.append({
                    'term': variant,
                    'definition': brain.definition,
                })

        return items

    def __call__(self):
        response = self.request.response
        response.setHeader('content-type', 'application/json')

        return response.setBody(json.dumps(self.get_json_entries()))


class ResourcesViewlet(ViewletBase):
    """This viewlet inserts static resources on page header."""
