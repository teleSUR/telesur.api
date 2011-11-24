# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles

from telesur.policy.api import IPortalAPI
from telesur.policy.testing import INTEGRATION_TESTING
from telesur.policy.viewlets import IListViewlet


class UtilitesTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_portal_api_utility(self):
        util = queryUtility(IPortalAPI, name=u"portal")
        self.failUnless(util, 'Portal API Utility not installed')

    def test_video_api_utility(self):
        util = queryUtility(IPortalAPI, name=u"video")
        self.failUnless(util, 'Video API Utility not installed')

    def test_api_vocabulary(self):
        util = queryUtility(IVocabularyFactory, name=u"telesur.api.Utilities")
        self.failUnless(util, 'API Vocabulary not installed')
        self.assertIn(u'portal', util().by_token.keys())
        self.assertIn(u'video', util().by_token.keys())

    def test_viewlets_vocabulary_no_interface(self):
        util = queryUtility(IVocabularyFactory, name=u"telesur.api.Widgets")
        self.failUnless(util, 'Widgets Vocabulary not installed')
        vocab = util()
        self.assertEquals([], vocab.by_token.keys())

    def test_viewlets_vocabulary_list_interface(self):
        util = queryUtility(IVocabularyFactory, name=u"telesur.api.Widgets")
        self.failUnless(util, 'Widgets Vocabulary not installed')
        vocab = util(IListViewlet)
        self.assertIn(u'telesur.policy.firstofsections', vocab.by_token.keys())
        self.assertIn(u'telesur.policy.videos_busqueda', vocab.by_token.keys())
        self.assertIn(u'telesur.policy.videosporseccion', vocab.by_token.keys())
        self.assertEquals(len(vocab.by_token.keys()), 3)

    def test_viewlets_names_vocabulary_list_interface(self):
        util = queryUtility(IVocabularyFactory, name=u"telesur.api.WidgetsNames")
        self.failUnless(util, 'Widgets Names Vocabulary not installed')
        vocab = util(IListViewlet)
        self.assertIn(u'telesur.policy.firstofsections', vocab.by_token.keys())
        self.assertIn(u'telesur.policy.videos_busqueda', vocab.by_token.keys())
        self.assertIn(u'telesur.policy.videosporseccion', vocab.by_token.keys())
        self.assertEquals(len(vocab.by_token.keys()), 3)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
