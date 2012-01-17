# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.browserlayer.utils import registered_layers

from telesur.api.config import PROJECTNAME
from telesur.api.testing import INTEGRATION_TESTING


class InstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = getattr(self.portal, 'portal_quickinstaller')

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer_installed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertTrue('ITelesurAPILayer' in layers,
                        'browser layer not installed')


class UninstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer_removed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertFalse('ITelesurAPILayer' in layers,
                         'browser layer not removed')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
