# -*- coding: utf-8 -*-

import transaction

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

class TelesurPolicyFixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.formwidget.relationfield
        self.loadZCML(package=collective.formwidget.relationfield)
        import telesur.policy
        self.loadZCML(package=telesur.policy)
        import telesur.api
        self.loadZCML(package=telesur.api)
        
        # Install product and call its initialize() function
        z2.installProduct(app, 'Products.CMFPlacefulWorkflow')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'telesur.policy:initial')
        self.applyProfile(portal, 'telesur.policy:default')
        self.applyProfile(portal, 'telesur.api:default')
        # Set default workflow chains for tests
        wf = getattr(portal, 'portal_workflow')
        types = ('Folder', 'Topic')
        wf.setChainForPortalTypes(types, 'simple_publication_workflow')


FIXTURE = TelesurPolicyFixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='telesur.api:Integration',
    )
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='telesur.api:Functional',
    )


def browserLogin(portal, browser, username=None, password=None):
    handleErrors = browser.handleErrors
    try:
        browser.handleErrors = False
        browser.open(portal.absolute_url() + '/login_form')
        if username is None:
            username = TEST_USER_NAME
        if password is None:
            password = TEST_USER_PASSWORD
        browser.getControl(name='__ac_name').value = username
        browser.getControl(name='__ac_password').value = password
        browser.getControl(name='submit').click()
    finally:
        browser.handleErrors = handleErrors


def createObject(context, _type, id, delete_first=False,
                 check_for_first=True, **kwargs):
    if delete_first and id in context.objectIds():
        context.manage_delObjects([id])
    if check_for_first and id not in context.objectIds():
        return context[context.invokeFactory(_type, id, **kwargs)]

    return context[id]


def setupTestContent(test):
    createObject(test.portal, 'Folder', 'folder',
            title='News Folder')
    test.folder = test.portal['folder']
    createObject(test.folder, 'collective.nitf.content', 'news-1',
            title='News Test 1')
    test.news1 = test.folder['news-1']
    test.news1.genre = 'Current'
    test.news1.section = u'General'
    test.news1.setEffectiveDate('2011/09/11')
    createObject(test.news1,
                 'Link',
                 'video-1',
                 title='Video 1',
                 remoteUrl="http://multimedia.tlsur.net/api/clip/vallejo-el-"
                           "conflicto-debe-resolverse-con-los-estudiantes/?"
                           "detalle=completo")
    test.video1 = test.news1['video-1']
    createObject(test.folder, 'collective.nitf.content', 'news-2',
            title='News Test 2')
    test.news2 = test.folder['news-2']
    test.news2.genre = 'Current'
    test.news2.section = u'Avances'
    test.news2.setEffectiveDate('2011/10/31')
    createObject(test.folder, 'collective.nitf.content', 'news-3',
            title='News Test 3')
    test.news3 = test.folder['news-3']
    test.news3.genre = 'Current'
    test.news3.section = u'Latinoamérica'
    test.news3.setEffectiveDate('2011/10/31')
    createObject(test.folder, 'collective.nitf.content', 'news-4',
            title='News Test 4')
    test.news4 = test.folder['news-4']
    test.news4.genre = 'Current'
    test.news4.section = u'Latinoamérica'
    test.news4.setEffectiveDate('2011/10/30')
    createObject(test.folder, 'collective.nitf.content', 'news-5',
            title='News Test 5')
    test.news5 = test.folder['news-5']
    test.news5.genre = 'Current'
    test.news5.section = u'Latinoamérica'
    test.news5.setEffectiveDate('2011/10/29')
    createObject(test.folder, 'collective.nitf.content', 'news-6',
            title='News Test 6')
    test.news6 = test.folder['news-6']
    test.news6.genre = 'Current'
    test.news6.section = u'Avances'
    test.news6.setEffectiveDate('2011/10/25')
    test.news1.reindexObject()
    test.news2.reindexObject()
    test.news3.reindexObject()
    test.news4.reindexObject()
    test.news5.reindexObject()
    test.news6.reindexObject()
    transaction.commit()
