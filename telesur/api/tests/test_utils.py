# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory

from telesur.api.interfaces import IPortalAPI
from telesur.api.testing import INTEGRATION_TESTING

IAPIViewlet = ['telesur.policy.videosporseccion',
               'telesur.policy.related_contents',
               'telesur.policy.related_videos',
               'telesur.policy.mas_titulares']


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


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
