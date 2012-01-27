# -*- coding: utf-8 -*-

from five import grok

from zope.component import getMultiAdapter

from Products.ATContentTypes.interfaces.link import IATLink
from Products.Archetypes.interfaces import IObjectInitializedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from zope.annotation.interfaces import IAnnotations

from OFS.Image import Image

import urllib2


class LinkApi(grok.View):
    grok.context(IATLink)
    grok.name("link_api")
    grok.require("zope2.View")

    def get(self, element):
        annotations = IAnnotations(self.context)
        return annotations.get(element, None)

    def is_video(self):
        return self.get('archivo_url') and True or False

    def render(self):
        return self


class LinkPreviewThumbnailView(grok.View):
    grok.context(IATLink)
    grok.name("thumbnail_pequeno")
    grok.require("zope2.View")

    def render(self):
        link_api = getMultiAdapter((self.context, self.request),
                                       name="link_api")
        thumb = link_api.get('thumbnail_pequeno')

        if thumb:
            return thumb.index_html(self.request, self.request.RESPONSE)
        else:
            return ''


class UpdateLinkView(grok.View):
    grok.context(IATLink)
    grok.name("update-link")
    grok.require("cmf.ModifyPortalContent")

    def __call__(self):
        request = self.request
        link_control = getMultiAdapter((self.context, request),
                                       name="link-control")
        link_control.update_local_data(self.context)
        view_url = self.context.absolute_url()
        self.request.response.redirect(view_url)

    def render(self):
        return "update-link"


class LinkControl(grok.View):
    grok.context(IATLink)
    grok.name("link-control")
    grok.require("cmf.ModifyPortalContent")

    def update_local_data(self, element):
        annotations = IAnnotations(element)
        video_api = getMultiAdapter((element, self.request), name="video_api")
        json = video_api.get_json(element.remoteUrl)

        if json:
            thumb = json.get('thumbnail_pequeno', None)
            archivo_url = json.get('archivo_url', None)
            titulo = json.get('titulo', None)
            descripcion = json.get('descripcion', None)
            slug = json.get('slug', None)

            if thumb:
                data = urllib2.urlopen(thumb)
                img = Image('thumbnail_pequeno', 'Thumbnail', data.read())
                annotations['thumbnail_pequeno'] = img
            else:
                try:
                    del(annotations['thumbnail_pequeno'])
                except KeyError:
                    pass

            if archivo_url:
                annotations['archivo_url'] = archivo_url
            else:
                try:
                    del(annotations['archivo_url'])
                except KeyError:
                    pass

            if titulo:
                annotations['titulo'] = titulo
                element.setTitle(titulo)
            else:
                try:
                    del(annotations['titulo'])
                except KeyError:
                    pass

            if descripcion:
                annotations['descripcion'] = descripcion
                element.setDescription(descripcion)
            else:
                try:
                    del(annotations['descripcion'])
                except KeyError:
                    pass

            if slug:
                annotations['slug'] = slug
            else:
                try:
                    del(annotations['slug'])
                except KeyError:
                    pass

    def render(self):
        return self


@grok.subscribe(IATLink, IObjectInitializedEvent)
@grok.subscribe(IATLink, IObjectModifiedEvent)
def update_local_data(obj, event):
    request = obj.REQUEST
    link_control = getMultiAdapter((obj, request), name="link-control")
    link_control.update_local_data(obj)
