# -*- coding: utf-8 -*-

import transaction

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting


class TelesurPolicyFixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import telesur.policy
        self.loadZCML(package=telesur.api)

    def setUpPloneSite(self, portal):
        # Set default workflow chains for tests
        wf = getattr(portal, 'portal_workflow')
        types = ('Folder', 'Topic')
        wf.setChainForPortalTypes(types, 'simple_publication_workflow')


FIXTURE = TelesurPolicyFixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='telesur.policy:Integration',
    )
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='telesur.policy:Functional',
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
                 check_for_first=False, **kwargs):
    if delete_first and id in context.objectIds():
        context.manage_delObjects([id])
    if not check_for_first or id not in context.objectIds():
        return context[context.invokeFactory(_type, id, **kwargs)]

    return context[id]

def setupTestContent(test):
    createObject(test.portal, 'Folder', 'folder',
            title='News Folder')
    test.folder = test.portal['folder']
    createObject(test.folder, 'collective.nitf.content', 'news-1',
            title='News Test 1')
    test.news1 = test.folder['news-1']
    test.news1.section = u'General'
    test.news1.setEffectiveDate('2011/09/11')
    createObject(test.folder, 'collective.nitf.content', 'news-2',
            title='News Test 2')
    test.news2 = test.folder['news-2']
    test.news2.section = u'Avances'
    test.news2.setEffectiveDate('2011/10/31')
    createObject(test.folder, 'collective.nitf.content', 'news-3',
            title='News Test 3')
    test.news3 = test.folder['news-3']
    #import pdb; pdb.set_trace();
    test.news3.section = u'Latinoamérica'
    test.news3.setEffectiveDate('2011/10/31')
    test.news1.reindexObject()
    test.news2.reindexObject()
    test.news3.reindexObject()
    transaction.commit()
