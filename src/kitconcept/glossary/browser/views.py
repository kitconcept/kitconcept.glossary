# -*- coding: utf-8 -*-
from plone import api
from plone.app.layout.viewlets import ViewletBase
from plone.i18n.normalizer.base import baseNormalize
from plone.memoize.instance import memoize
from Products.CMFPlone.PloneBatch import Batch
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from zExceptions import Redirect

import string

from kitconcept.glossary.interfaces import IGlossarySettings

BATCH_SIZE = 30


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
            results = api.content.find(letter=self.search_letter.upper(), **common)
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

        max_length = api.portal.get_registry_record(
                name='description_length',
                interface=IGlossarySettings,
                )
        ellipsis = api.portal.get_registry_record(
                name='description_limiter',
                interface=IGlossarySettings,
                )

        text = safe_unicode(text).strip()

        if max_length > 0 and len(text) > max_length:
            text = text[:max_length]
            text = text.strip()
            text = u'{0}{1}'.format(text, ellipsis)

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


class ResourcesViewlet(ViewletBase):
    """This viewlet inserts static resources on page header."""
