# -*- coding: utf-8 -*-
from kitconcept.glossary.interfaces import IGlossarySettings
from plone import api
from plone.app.layout.viewlets import ViewletBase
from plone.i18n.normalizer.base import baseNormalize
from plone.memoize import ram
from plone.memoize.instance import memoize
from Products.CMFPlone.PloneBatch import Batch
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from zExceptions import Redirect

import json
import string


BATCH_SIZE = 30
DESCRIPTION_LENGTH = 0


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

    def title(self):
        """Title of our glossary"""

        return self.context.title_or_id()

    def first_letters(self):
        """Users with non latin chars (cyrillic, arabic, ...) should override
        this with a better suited dataset."""
        out = []
        glossary_url = self.context.absolute_url()
        for letter in tuple(string.ascii_uppercase):
            exists = any([
                brain.letter
                for brain in api.content.find(
                    context=self.context,
                    depth=1,
                    portal_type='Term',
                    letter=letter,
                    sort_limit=1,
                )
            ])
            letter_map = {
                'glyph': letter,
                'has_no_term': not exists,
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
        common = {
            'context': self.context,
            'depth': 1,
            'portal_type': 'Term',
        }

        if self.search_letter:
            results = api.content.find(letter=self.search_letter, **common)
        elif self.search_text:
            results = api.content.find(SearchableText=self.search_text, **common)
            # We redirect to the result if unique
            if len(results) == 1:
                target = results[0].getURL()
                raise Redirect(target)
        else:
            # Viewing all terms
            results = api.content.find(**common)
        results = list(results)
        results.sort(lambda x, y: cmp(baseNormalize(x.Title),
                                      baseNormalize(y.Title)))
        return tuple(results)

    def truncateDescription(self, text):
        """Truncate definition using tool properties"""

        max_length = DESCRIPTION_LENGTH
        text = safe_unicode(text).strip()

        if max_length > 0 and len(text) > max_length:
            ellipsis = self.description_ellipsis
            text = text[:max_length]
            text = text.strip()
            text = '{0} {1}'.format(text, ellipsis)

        text = text.encode('utf-8', 'replace')

        return text

    def result_features(self, result):
        """TAL friendly properties of each feature"""

        description = self.truncateDescription(result.Description)
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
