# -*- coding: utf-8 -*-

from plone import api

from plone.restapi.services import Service

from kitconcept.glossary.interfaces import IGlossarySettings

SERVICE_NAME = "@glossary_terms"


class GetGlossaryTerms(Service):
    def _error(self, status, type, message):
        self.request.response.setStatus(status)
        return {"error": {"type": type, "message": message}}

    def reply(self):
        brains = api.content.find(portal_type="GlossaryTerm")

        terms = [
            {
                "id": brain["id"],
                "title": brain["Title"],
                "terms": [brain["Title"]] + list(brain["variants"]),
                "definition": brain["definition"] or "",
                "url": brain.getURL(),
            }
            for brain in brains
        ]
        settings = {
            "enabled": api.portal.get_registry_record(
                name="enable_tooltip", interface=IGlossarySettings, default=False,
            ),
            "enabled_types": api.portal.get_registry_record(
                name="enabled_content_types", interface=IGlossarySettings, default=[],
            ),
        }

        return {
            "terms": terms,
            "settings": settings,
        }
