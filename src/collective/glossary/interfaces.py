# -*- coding: utf-8 -*-
from collective.glossary import _
from collective.glossary.config import DEFAULT_ENABLED_CONTENT_TYPES
from plone.directives import form
from plone.namedfile.field import NamedBlobImage
from zope import schema
from zope.interface import Interface


class IGlossaryLayer(Interface):

    """A layer specific for this add-on product."""


class IGlossarySettings(form.Schema):

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
            vocabulary=u'collective.glossary.PortalTypes'),
    )


class IGlossary(form.Schema):

    """A Glossary is a container for Terms."""


class ITerm(form.Schema):

    """A Term."""

    image = NamedBlobImage(
        title=_(u'Image'),
        description=_(u''),
        required=False,
    )
