# -*- coding: utf-8 -*-

import json
import urllib

from five import grok
from zope.component import getUtilitiesFor
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.viewlet.interfaces import IViewlet

from plone.app.customerize import registration

from telesur.api.interfaces import IPortalAPI
from telesur.api.interfaces import IPortalAPIQuerySchema
from telesur.api.interfaces import IVideoAPIQuerySchema
from telesur.api.interfaces import ITelesurAPILayer
from telesur.api.interfaces import IAPIViewlet


class ApiUtilitiesVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self):
        utilities = getUtilitiesFor(IPortalAPI)
        terms = []
        for name, instance in utilities:
            terms.append(SimpleVocabulary.createTerm(instance, name, name))
        return SimpleVocabulary(terms)

grok.global_utility(ApiUtilitiesVocabulary, name=u"telesur.api.Utilities")


class APIWidgetsVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, interface=IAPIViewlet, layer=ITelesurAPILayer):
        #views = registration.getViews(IBrowserRequest)
        views = registration.getViews(layer)

        terms = []
        if interface is not None:
            for v in views:
                if v.provided == IViewlet:
                    if interface.providedBy(v.factory):
                        terms.append(SimpleVocabulary.createTerm(v.factory,
                            u"%s" % v.name, v.name))
        return SimpleVocabulary(terms)

grok.global_utility(APIWidgetsVocabulary, name=u"telesur.api.Widgets")


class APIWidgetsNamesVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, interface=None):
        viewlets_vocab = queryUtility(IVocabularyFactory,
                                      name=u"telesur.api.Widgets")
        terms = []
        if viewlets_vocab and interface is not None:
            vocab = viewlets_vocab(interface)
            for token in vocab.by_token.keys():
                term = vocab.by_token[token]
                terms.append(SimpleVocabulary.createTerm(term.token,
                                    u"%s" % term.token, term.title))
        return SimpleVocabulary(terms)

grok.global_utility(APIWidgetsNamesVocabulary,
                    name=u"telesur.api.WidgetsNames")


class APIUtility(object):
    grok.implements(IPortalAPI)

    def __init__(self, api=None, query_interface=None):
        self.api = api
        self.query_interface = query_interface

    def getAPIQuery(self, request):

        if len(request.form.keys()) > 0:
            form = request.form
            query = {}
            if 'api' in form and self.query_interface is not None:
                for name in self.query_interface.names():
                    if name in form:
                        value = self.getValueFrom(form[name])
                        if isinstance(value, list):
                            tmp = []
                            for item in value:
                                item_val = self.getValueFrom(item)
                                tmp.append(item_val)
                            query[name] = tmp
                        if isinstance(value, basestring):
                            query[name] = value.decode("utf-8")
                if queryUtility(IPortalAPI, name=query['api']) is None:
                    query = {}
            return query

    def getValueFrom(self, value=None):
        try:
            value = eval(value)
            if isinstance(value, list):
                tmp = []
                for val in value:
                    tmp.append(self.getValueFrom((val)))
                value = tmp
        except:
            if isinstance(value, basestring):
                value = urllib.unquote_plus(value)
            if isinstance(value, list):
                tmp = []
                for val in value:
                    tmp.append(self.getValueFrom((val)))
                value = tmp
        return value

    def dumps(self, text=None):
        if text is None:
            text = u""
        return json.dumps(text)


portal_api = APIUtility("portal", IPortalAPIQuerySchema)
video_api = APIUtility("video", IVideoAPIQuerySchema)

grok.global_utility(portal_api, provides=IPortalAPI, name="portal", direct=True)
grok.global_utility(video_api, provides=IPortalAPI, name="video", direct=True)
