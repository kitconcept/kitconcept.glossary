# -*- coding: utf-8 -*-
from kitconcept.glossary.interfaces import IGlossaryTerm
from plone.app.textfield.interfaces import ITransformer
from plone.i18n.normalizer.base import baseNormalize
from plone.indexer import indexer
from Products.CMFPlone.utils import safe_unicode


@indexer(IGlossaryTerm)
def textIndexer(context):
    """SearchableText contains id, title, variants and definition
    text as plain text.
    """
    transformer = ITransformer(context)

    try:
        definition = transformer(context.definition, "text/plain")
    except AttributeError:
        definition = u""
    try:
        variants = u" ".join(context.variants)
    except TypeError:
        variants = u""

    return u" ".join(
        (
            safe_unicode(context.id),
            safe_unicode(context.title) or u"",
            safe_unicode(variants),
            safe_unicode(definition),
        )
    )


@indexer(IGlossaryTerm)
def variantsIndexer(context):
    if not context.variants:
        return []
    return context.variants


@indexer(IGlossaryTerm)
def definitionIndexer(context):
    return context.definition.raw


@indexer(IGlossaryTerm)
def letterIndexer(context):
    if not context.title:
        return u""
    return baseNormalize(context.title)[0].upper()
