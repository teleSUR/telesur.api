# -*- coding: utf-8 -*-

from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder

from plone.directives import form
from plone.autoform.interfaces import IFormFieldProvider

from collective.nitf.content import INITF
from zope.interface import implements, alsoProvides
from zope.component import adapts
from rwproperty import getproperty, setproperty

from telesur.widgets.videos import AddVideosFieldWidget

from z3c.form.interfaces import IDisplayForm


class IAddableVideos(form.Schema):
    """
    """

    form.omitted('relatedVideos')
    form.no_omit(IDisplayForm, 'relatedVideos')
    form.widget(relatedVideos=AddVideosFieldWidget)
    relatedVideos = RelationList(
        title=u'Videos relacionados',
        default=[],
        value_type=RelationChoice(title=u"Videos relacionados",
                      source=ObjPathSourceBinder()),
        required=False,
        )

alsoProvides(IAddableVideos, IFormFieldProvider)


class AddableVideos(object):
    """Store tags in the Dublin Core metadata Subject field. This makes
    tags easy to search for.
    """
    implements(IAddableVideos)
    adapts(INITF)

    def __init__(self, context):
        self.context = context

    @getproperty
    def relatedVideos(self):
        # Codigo para listar videos ya agregados
        return []

    @setproperty
    def relatedVideos(self, value):
        # Codigo para agregar videos al nitf
        return []
