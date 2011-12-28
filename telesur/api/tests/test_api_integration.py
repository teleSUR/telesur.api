# -*- coding: utf-8 -*-

import unittest2 as unittest

from StringIO import StringIO

from zope.app.file.tests.test_image import zptlogo
from zope.interface import directlyProvides
from zope.interface import Interface

from plone.app.customerize import registration

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from telesur.policy.interfaces import ITelesurLayer as IAPILayer
from telesur.policy.testing import INTEGRATION_TESTING


class BrowserLayerTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        directlyProvides(self.request, IAPILayer)

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('collective.nitf.content', 'n1')
        self.n1 = self.folder['n1']

    def getViewByName(self, context, name):
        try:
            return context.restrictedTraverse(name)
        except AttributeError:
            return None

    def test_views_registered(self):
        views = ['portal_api', 'video_api']
        registered = [v.name for v in registration.getViews(IAPILayer)]
        # empty set only if all 'views' are 'registered'
        self.assertEquals(set(views) - set(registered), set([]))

    def test_portal_api(self):
        name = "@@portal_api"
        view = self.getViewByName(self.portal, name)
        self.failUnless(view, u"%s has no view %s" % (self.portal, name))
        view.update()

    def test_portal_api_viewlet(self):
        name = "@@portal_api"
        view = self.getViewByName(self.portal, name)
        self.failUnless(view, u"%s has no view %s" % (self.portal, name))
        view.update()
        vocab = view.getViewletsVocabulary()
        self.failUnless(vocab, u"API Widgets Vocabulary is not present")
        viewlet_keys = [u'telesur.policy.mas_titulares',
                        u'telesur.policy.related_contents',
                        u'telesur.policy.related_videos',
                        u'telesur.policy.videosporseccion']
        self.assertEquals(set(vocab.by_token.keys()) - set(viewlet_keys), set([]))

    def test_viewlets_registered(self):
        # TODO: implement test
        pass


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
