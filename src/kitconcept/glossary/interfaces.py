# -*- coding: utf-8 -*-
from kitconcept.glossary import _
from kitconcept.glossary.config import DEFAULT_ENABLED_CONTENT_TYPES
from plone.app.textfield import RichText
from plone.app.textfield.interfaces import ITransformer
from plone.autoform import directives as form
from plone.indexer import indexer
from Products.CMFPlone.utils import safe_unicode
from zope import schema
from zope.interface import Interface


class IGlossaryLayer(Interface):

    """A layer specific for this add-on product."""


class IGlossarySettings(Interface):

    """Schema for the control panel form."""

    enable_tooltip = schema.Bool(
        title=_(u'Enable tooltip?'),
        description=_(u'Enable tooltip.'),
        default=True,
    )

    enabled_content_types = schema.List(
        title=_(u'Enabled Content Types'),
        description=_(u'Only objects of these content types will display glossary terms.'),
        required=False,
        default=DEFAULT_ENABLED_CONTENT_TYPES,
        # we are going to list only the main content types in the widget
        value_type=schema.Choice(
            vocabulary=u'kitconcept.glossary.PortalTypes'),
    )


class IGlossary(Interface):

    """A Glossary is a container for Terms."""

    text = RichText(
        title=_(u'Body text'),
        description=_(u'Enter the body text.'),
        required=False,
    )


class ITerm(Interface):

    """A Term."""

    title = schema.TextLine(
        title=_(u'Term'),
        description=_(u'Enter the term to be defined.'),
        required=True,
    )

    form.widget('variants', cols=25, rows=10)
    variants = schema.Tuple(
        title=_(u'Variants'),
        description=_(u'Enter the variants of the term, one per line.'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=(),
    )

    definition = RichText(
        title=_(u'Body text'),
        description=_(u'Enter the body text.'),
        required=False,
    )


@indexer(ITerm)
def textIndexer(obj):
    """SearchableText contains id, title, variants and definition
    text as plain text.
    """
    transformer = ITransformer(obj)

    try:
        definition = transformer(obj.definition, 'text/plain')
    except AttributeError:
        definition = u''
    try:
        variants = u' '.join(obj.variants)
    except TypeError:
        variants = u''

    return u' '.join((
        safe_unicode(obj.id),
        safe_unicode(obj.title) or u'',
        safe_unicode(variants),
        safe_unicode(definition),
    ))
