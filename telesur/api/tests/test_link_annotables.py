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

from telesur.api.browser import LinkControl

from zope.annotation.interfaces import IAnnotations

from zope.event import notify
from Products.Archetypes.event import ObjectInitializedEvent

class BrowserLayerTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.pc = getToolByName(self.portal, 'portal_catalog')
        
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        setupTestContent(self)
    
        self.link_control_api = getMultiAdapter((self.video1, self.request),
                                                name='link-control')

    def test_link_control_render(self):
        render = self.link_control_api.render()

        self.failUnless(isinstance(render, LinkControl))

    def test_update_local_data(self):
        annotations = IAnnotations(self.video1)

        self.failUnlessEqual(annotations, {})
        
        self.link_control_api.update_local_data(self.video1)

        keys = ['archivo_url', 'audio_url', 'descripcion', 'slug',
                'thumbnail_grande', 'thumbnail_mediano', 'thumbnail_pequeno',
                'titulo']

        for key in keys:
            self.failUnless(key in annotations)


    def test_notify_creation(self):
        annotations = IAnnotations(self.video1)

        self.failUnlessEqual(annotations, {})
        
        notify(ObjectInitializedEvent(self.video1))

        keys = ['archivo_url', 'audio_url', 'descripcion', 'slug',
                'thumbnail_grande', 'thumbnail_mediano', 'thumbnail_pequeno',
                'titulo']

        for key in keys:
            self.failUnless(key in annotations)

    def test_thumbnail_sizes(self):

        pequeno = getMultiAdapter((self.video1, self.request),
                                  name="thumbnail_pequeno")
        self.failIf(pequeno.render())
        mediano = getMultiAdapter((self.video1, self.request),
                                  name="thumbnail_mediano")
        self.failIf(mediano.render())
        grande = getMultiAdapter((self.video1, self.request),
                                 name="thumbnail_grande")
        self.failIf(grande.render())

        notify(ObjectInitializedEvent(self.video1))

        pequeno = getMultiAdapter((self.video1, self.request),
                                  name="thumbnail_pequeno")
        self.failUnless(pequeno.render())
        mediano = getMultiAdapter((self.video1, self.request),
                                  name="thumbnail_mediano")
        self.failUnless(mediano.render())
        grande = getMultiAdapter((self.video1, self.request),
                                 name="thumbnail_grande")
        self.failUnless(grande.render())

    def test_link_api(self):
        
        api = getMultiAdapter((self.video1, self.request), name="link_api")

        keys = ['archivo_url', 'audio_url', 'descripcion', 'slug',
                'thumbnail_grande', 'thumbnail_mediano', 'thumbnail_pequeno',
                'titulo']

        for key in keys:
            self.failIf(api.get(key))

        notify(ObjectInitializedEvent(self.video1))

        for key in keys:
            self.failUnless(api.get(key))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
