# -*- coding: utf-8 -*-

import json
import unittest2 as unittest
import urllib

from StringIO import StringIO

from zope.app.file.tests.test_image import zptlogo
from zope.interface import directlyProvides
from zope.interface import Interface

from Products.CMFCore.utils import getToolByName
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.testing.z2 import Browser

from telesur.policy.api import Video_API
from telesur.policy.interfaces import ITelesurLayer
from telesur.policy.testing import FUNCTIONAL_TESTING
from telesur.policy.testing import browserLogin
from telesur.policy.testing import createObject
from telesur.policy.testing import setupTestContent

from zope.component import getMultiAdapter


class BrowserLayerTest(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        workflow_tool = getToolByName(self.portal, 'portal_workflow')
        workflow_tool.setDefaultChain('one_state_workflow')
        workflow_tool.updateRoleMappings()
        setupTestContent(self)
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False
        browserLogin(self.portal, self.browser)
        directlyProvides(self.request, ITelesurLayer)

    def test_portal_api_no_query(self):
        name = "/@@portal_api"
        api_query = { 'secciones': (u"Latinoamérica".encode("utf-8"),
                                    u"Vuelta al mundo".encode("utf-8")),
                      'texto': u'Tema útil'.encode("utf-8"),
                      }
        query = urllib.urlencode(api_query)
        # Si no se especifica 'api'
        self.browser.open(self.portal.absolute_url() + name + "?" + query )
        self.assertNotEquals(self.browser.contents, json.dumps(api_query))
        self.assertEquals(u'No hay resultados', self.browser.contents)
        # Si se especifica 'api' inexistente
        query = urllib.urlencode({ 'api': 'noexiste'})
        self.browser.open(self.portal.absolute_url() + name + "?" + query )
        self.assertEquals(u'No hay resultados', self.browser.contents)
        print u"\nNO QUERY:\nquery: %s\nbrowser: %s\njson dump: %s" % (query, self.browser.contents, json.dumps(api_query))

    def test_portal_api_query_good(self):
        name = "/@@portal_api"
        api_query = { 'api': 'portal',
                      'secciones': [u"Latinoamérica".encode("utf-8"),
                                    u"Vuelta al mundo".encode("utf-8")],
                      'texto': u'Tema útil'.encode("utf-8"),
                      }
        query = urllib.urlencode(api_query)
        self.browser.open(self.portal.absolute_url() + name + "?" + query )
        self.assertIn(json.dumps(api_query), self.browser.contents)
        print u"\nGOOD QUERY:\nquery: %s\nbrowser: %s\njson dump: %s" % (query,
                                                                   self.browser.contents,
                                                                   json.dumps(api_query))

    def test_portal_api_query_good_with_widgets(self):
        name = "/@@portal_api"
        api_query = { 'api': 'portal',
                      'secciones': [u"Latinoamérica".encode("utf-8"),
                                    u"Vuelta al mundo".encode("utf-8")],
                      'texto': u'Tema útil'.encode("utf-8"),
                      'widgets': [u'telesur.policy.mas_titulares'.encode("utf-8"),
                                  u'telesur.policy.related_contents'.encode("utf-8"),
                                  u'telesur.policy.videosporseccion'.encode("utf-8")],
                      }
        query = urllib.urlencode(api_query)
        self.browser.open(self.portal.absolute_url() + name + "?" + query )
        self.assertIn('<div id="telesur-titulares"', self.browser.contents)
        self.assertIn('<div id="related-contents" class="row">',
                      self.browser.contents)
        self.assertIn('<div id="videos-por-seccion" class="row">',
                      self.browser.contents)

    def test_portal_api_query_bad(self):
        name = "/@@portal_api"
        api_query = { 'api': 'portal',
                      'secciones': (u"Latinoamérica".encode("utf-8"),
                                    u"Vuelta al mundo".encode("utf-8")),
                      'texto': u'Tema útil'.encode("utf-8"),
                      }
        query = urllib.urlencode(api_query)
        self.browser.open(self.portal.absolute_url() + name + "?" + query )
        self.assertIn('api', self.browser.contents)
        self.assertIn('texto', self.browser.contents)
        self.assertNotIn('\"secciones\"', self.browser.contents)
        print u"\nBAD QUERY:\nquery: %s\nbrowser: %s\njson dump: %s" % (query,
                                                                   self.browser.contents,
                                                                   json.dumps(api_query))


    def test_video_api_exists(self):
        try:
            view = getMultiAdapter((self.portal, self.request),
                                   name='video_api')
        except ComponentLookupError:
            view = None

        self.failUnless(isinstance(view, Video_API))


    def test_video_api_valid_url(self):
        view = getMultiAdapter((self.portal, self.request),
                                name='video_api')

        url = ("http://multimedia.tlsur.net/api/clip/vallejo-el-conflicto"
               "-debe-resolverse-con-los-estudiantes?detalle=completo")
               

        self.assertIsNotNone(view.get_json(url))
        
        widget = view.get_video_widget_url(url, width=600)

        self.failUnlessEqual(widget, 'http://multimedia.telesurtv.net/player/'
                                     'insertar.js?archivo=clips/telesur-video'
                                     '-2011-10-14-201605224901.mp4&amp;'
                                     'width=600')

    def test_video_api_invalid_url(self):
        view = getMultiAdapter((self.portal, self.request),
                                name='video_api')

        url = ("http://multimedia.telesurtv.net/14/10/2011/53803/vallejo-el-"
               "conflicto-debe-resolverse-con-los-estudiantes/")


        self.assertIsNone(view.get_json(url))

        widget = view.get_video_widget_url(url, width=600)
        self.assertIsNone(widget)
        

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
