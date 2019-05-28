# -*- coding: utf-8 -*-
from kitconcept.glossary import _
from kitconcept.glossary.config import DEFAULT_ENABLED_CONTENT_TYPES
from plone.app.textfield import RichText
from plone.autoform import directives as form
from plone.supermodel import model
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IEditForm
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
        description=_(
            u'Only objects of these content types will display glossary terms.'),
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

    model.fieldset(
        'settings',
        label=_(u"Settings"),
        fields=['exclude_from_nav']
    )

    # https://community.plone.org/t/how-to-change-existing-dexterity-types-and-behaviors/219/6
    exclude_from_nav = schema.Bool(
        title=_(
            u'label_exclude_from_nav',
            default=u'Exclude from navigation'
        ),
        description=_(
            u'help_exclude_from_nav',
            default=u'If selected, this item will not appear in the '
                    u'navigation tree'
        ),
        default=True,  # Need to be True
    )

    form.omitted('exclude_from_nav')
    form.no_omit(IEditForm, 'exclude_from_nav')
    form.no_omit(IAddForm, 'exclude_from_nav')
