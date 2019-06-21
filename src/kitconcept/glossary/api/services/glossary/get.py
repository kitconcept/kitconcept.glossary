# -*- coding: utf-8 -*-

from plone import api

from plone.restapi.services import Service

SERVICE_NAME = "@glossary_terms"


class GetGlossaryTerms(Service):
    def _error(self, status, type, message):
        self.request.response.setStatus(status)
        return {"error": {"type": type, "message": message}}

    def reply(self):
        brains = api.content.find(portal_type='Term')

        return [{'id': brain['id'],
                 'title': brain['Title'],
                 'terms': [brain['Title']] + list(brain['variants']),
                 'definition': brain['definition'],
                 'url': brain.getURL(),
                 }
                for brain in brains]
