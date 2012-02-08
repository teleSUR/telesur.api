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

from telesur.api.video import WIDGET_URLS

class BrowserLayerTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.pc = getToolByName(self.portal, 'portal_catalog')
        
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        
        self.video_api = getMultiAdapter((self.portal, self.request),
                                          name='video_api')
            
        #setupTestContent(self)
        #self.brains = self.pc(portal_type='collective.nitf.content',
                              #sort_on='created')

    def test_get_widgets(self):
        results = self.video_api.get_widgets()
        
        self.failUnlessEqual(results, WIDGET_URLS)

    def test_render(self):
        results = self.video_api.render()

        self.failUnlessEqual(results, u"video_api")
                              
    def test_get_video_widget_url(self):

        url = ("http://multimedia.tlsur.net/api/clip/vallejo-"
               "el-conflicto-debe-resolverse-con-los-"
               "estudiantes/?detalle=completo")

        results = self.video_api.get_video_widget_url(url)
        self.failUnlessEqual(results, (u"http://multimedia.telesurtv.net/"
                                        "player/insertar.js?archivo=clips/"
                                        "telesur-video-2011-10-14-201605224901"
                                        ".mp4&amp;width=400"))

    def test_get_video_thumb(self):

        url = ("http://multimedia.tlsur.net/api/clip/vallejo-"
               "el-conflicto-debe-resolverse-con-los-"
               "estudiantes/?detalle=completo")

        results = self.video_api.get_video_thumb(url)
        self.failUnlessEqual(results, (u"http://media.tlsur.net/cache/10/f9/"
                                        "10f910a49e6a261276f90d920063eede.jpg"))

    def test_get_section_last_videos(self):
        
        url = ("http://multimedia.telesurtv.net/media/video/cmswidgets/videos"
               ".html?widget=ultimos_seccion&seccion_plone=")
        categories_list = ['latinoamerica', 'vuelta-al-mundo', 'deportes',
                           'ciencia', 'cultura', 'salud', 'tecnologia']

        for i in categories_list:
            result = self.video_api.get_section_last_videos(i)
            self.failUnlessEqual(result, url+i)
            

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
