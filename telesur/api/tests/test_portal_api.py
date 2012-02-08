# -*- coding: utf-8 -*-

import json
import unittest2 as unittest
import urllib

from copy import deepcopy

from zope.interface import alsoProvides
from telesur.api.interfaces import ITelesurAPILayer

from Products.CMFCore.utils import getToolByName
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.testing.z2 import Browser

from telesur.api.video import Video_API
from telesur.api.testing import INTEGRATION_TESTING
from telesur.api.testing import setupTestContent

from zope.component import getMultiAdapter


class BrowserLayerTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.pc = getToolByName(self.portal, 'portal_catalog')
        
        alsoProvides(self.request, ITelesurAPILayer)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        
        self.portal_api = getMultiAdapter((self.portal, self.request),
                                          name='portal_api')
            
        setupTestContent(self)
        self.brains = self.pc(portal_type='collective.nitf.content',
                              sort_on='created')


    def test_get_first_video_for_brain(self):
        results = []
        for i in self.brains:
            results.append(self.portal_api.get_first_video_for_brain(i))

        self.failUnlessEqual(results,
                             [("http://multimedia.tlsur.net/api/clip/vallejo-"
                               "el-conflicto-debe-resolverse-con-los-"
                               "estudiantes/?detalle=completo"),
                               False,
                               False,
                               False,
                               False,
                               False,
                               ])

    def test_get_nitf_view_for_brain(self):

        for i in self.brains:
            api_view = self.portal_api.get_nitf_view_for_brain(i)
            
            obj = i.getObject()
            view = getMultiAdapter((obj, self.request), name="view")

            self.failUnlessEqual(api_view.__class__, view.__class__)
            

    def test_get_first_video_for_container(self):
        result = self.portal_api.get_first_video_for_container(self.news1)
        self.failUnlessEqual(result,
                             ("http://multimedia.tlsur.net/api/clip/vallejo-"
                              "el-conflicto-debe-resolverse-con-los-"
                              "estudiantes/?detalle=completo"))

        result = self.portal_api.get_first_video_for_container(self.news2)
        self.failUnlessEqual(result, False)

        result = self.portal_api.get_first_video_for_container(self.news3)
        self.failUnlessEqual(result, False)


    def test_get_first_of_sections(self):
        results = self.portal_api.get_first_of_sections()
        results.sort(key=lambda x:x['section_name'])

        self.failUnlessEqual(results[0]['brains'][0].getObject(), self.news2)
        self.failUnlessEqual(results[0]['section_name'], u'Avances')

        self.failUnlessEqual(results[1]['brains'][0].getObject(), self.news1)
        self.failUnlessEqual(results[1]['section_name'], u'General')

        self.failUnlessEqual(results[2]['brains'][0].getObject(), self.news3)
        self.failUnlessEqual(results[2]['section_name'], "Latinoamérica".decode("utf-8"))


    def test_portal_api_no_query(self):
        api_query = {'secciones': (u"Latinoamérica".encode("utf-8"),
                                   u"Vuelta al mundo".encode("utf-8")),
                      'texto': u'Tema útil'.encode("utf-8")}

        for key in api_query.keys():
            self.request.set(key, api_query[key])
                     
        portal_api = getMultiAdapter((self.portal, self.request),
                                     name='portal_api')
                     
        results = portal_api.render()
        
        self.assertNotEquals(results, json.dumps(api_query))
        self.assertEquals(u'No hay resultados', results)
        
        # Si se especifica 'api' inexistente
        api_query.update({'api': 'noexiste'})

        for key in api_query.keys():
            self.request.set(key, api_query[key])
                
        portal_api = getMultiAdapter((self.portal, self.request),
                                     name='portal_api')

        results = portal_api.render()

        self.assertEquals(u'No hay resultados', results)

        

    # XXX: El método "render" de portal_api no es usado en ningún lugar, como
    #      así tampoco el codigo de IPortalAPIQuerySchema. El test anterior,
    #      "test_portal_api_no_query", se mantiene como remanente, pero
    #      testea funcionalidad sin uso


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
