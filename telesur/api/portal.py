# -*- coding: utf-8 -*-

from five import grok
from zope.component import queryMultiAdapter
from zope.component import queryUtility
from zope.interface import Interface
from zope.schema.interfaces import IVocabularyFactory

from Products.CMFCore.utils import getToolByName

from telesur.api.interfaces import IPortalAPI
from telesur.api.interfaces import IAPIViewlet


class Portal_API(grok.View):
    grok.context(Interface)
    grok.name("portal_api")
    grok.require("zope2.View")
    
    def __init__(self, *args, **kwargs):
        super(Portal_API, self).__init__(*args, **kwargs)
        self.api_query = None
        self.catalog = getToolByName(self.context, 'portal_catalog')
        self.util = queryUtility(IPortalAPI, name=u"portal")
        if self.util:
            self.api_query = self.util.getAPIQuery(self.request)
        self.vocab = queryUtility(IVocabularyFactory,
                                  name=u"telesur.api.Widgets")
        self.list_viewlets = self.getViewletsVocabulary(IAPIViewlet)

    def getViewletsVocabulary(self, interface=IAPIViewlet):
        if self.vocab:
            return self.vocab(interface)


    def render(self, query=None):
        if query is not None:
            self.api_query = query
        if self.api_query:
            if 'widgets' in self.api_query and self.vocab is not None:
                rendering = u""
                for widget_name in self.api_query['widgets']:
                    if widget_name in self.list_viewlets.by_token:
                        term = self.list_viewlets.by_token[widget_name]
                        viewlet = term.value
                        widget = viewlet(self.context,
                                         self.request,
                                         self, None)
                        widget.update()
                        rendering += u"\n%s" % widget.render()
                return rendering
            results = {}
            results['search_query'] = self.api_query
            return self.util.dumps(results)
        return u"No hay resultados"

    def get_nitf_view_for_brain(self, brain):
        item_obj = brain.getObject()
        if brain["portal_type"] == "collective.nitf.content":
            nitf_api = queryMultiAdapter((item_obj, self.request),
                                         name=u"view")
            if nitf_api:
                return nitf_api

    def get_first_image_for_brain(self, brain):
        item_obj = brain.getObject()
        if hasattr(item_obj, 'image'):
            return item_obj.image
        if brain["portal_type"] == "collective.nitf.content":
            nitf_api = queryMultiAdapter((item_obj, self.request),
                                         name=u"view")
            if nitf_api:
                img = nitf_api.image()
                if img:
                    return img

    def get_first_video_for_brain(self, brain):
        #folder_int = "Products.ATContentTypes.interfaces.folder.IATFolder"
        #dexter_int = "plone.dexterity.interfaces.IDexterityContainer"
        #obj_provides = brain["object_provides"]
        #if folder_int in obj_provides or dexter_int in obj_provides:
        ##if brain["portal_type"] == "collective.nitf.content":
        if brain["is_folderish"]:
            item_obj = brain.getObject()
            return self.get_first_video_for_container(item_obj)

    def get_first_video_for_container(self, container):
        if container.portal_type == "collective.nitf.content":
            item_obj = container
            query = {'Type': ('Link',)}
            brains = self.query_container(item_obj, query)
            for brain in brains:
                brain_obj = brain.getObject()
                match = VIDEO_API_REGEX.search(brain_obj.remoteUrl)
                if match:
                    return brain_obj.remoteUrl
            return False

    def query_container(self, container, query, limit=None,
                        depth=1, sort_on="getObjPositionInParent"):
        context_path = '/'.join(container.getPhysicalPath())
        if 'path' not in query.keys():
            query['path'] = {'query': context_path,
                             'depth': 1}
        brains = self.catalog.searchResults(query,
                                            sort_on=sort_on,
                                            limit=limit)
        return brains

    def get_section_names(self):
        return self.catalog.uniqueValuesFor("section")

    def get_first_of_sections(self, section_names=None, query=None, limit=1):
        if section_names is None:
            section_names = self.get_section_names()
        if query is None:
            query = {
                     'portal_type': 'collective.nitf.content',
                     'sort_on': 'effective',
                     'sort_order': 'reverse',
                     }
        firsts = []
        if len(section_names) > 0:
            for section in section_names:
                query['section'] = section
                results = self.catalog(query)
                if len(results) > 0:
                    firsts.append({'section_name': section,
                        'brains': results[:limit],
                                   })
        return firsts                    