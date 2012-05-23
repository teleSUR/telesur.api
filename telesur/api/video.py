# -*- coding: utf-8 -*-

import re
import json
import urllib

from AccessControl import ClassSecurityInfo

from five import grok
from zope.interface import Interface

from zope.component import getUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer

from zope.event import notify
from Products.Archetypes.event import ObjectInitializedEvent


URL_BASE = u"http://multimedia.tlsur.net/api/"
VIDEO_API = "%s%s/?" % (URL_BASE, 'clip')

VIDEO_API_REGEX_STRING = u"^http:\/\/.+\/api\/(?P<url>clip\/.+?)$"
VIDEO_WIDGET_URL_BASE = u"http://multimedia.telesurtv.net/player/insertar.js?archivo="
VIDEO_REGEX_STRING = u"^http:\/\/.+\/(?P<url>clips\/.+\.mp4?)$"
AUDIO_REGEX_STRING = u"^http:\/\/.+\/(?P<url>clips\/.+\.mp3?)$"

VIDEO_API_REGEX = re.compile(VIDEO_API_REGEX_STRING)
VIDEO_REGEX = re.compile(VIDEO_REGEX_STRING)
AUDIO_REGEX = re.compile(AUDIO_REGEX_STRING)

"""
Más vistos del día:
http://multimedia.telesurtv.net/media/video/cmswidgets/cmswidgets.html?widget=mas_vistos&tiempo=dia
Más vistos de la semana:
http://multimedia.telesurtv.net/media/video/cmswidgets/cmswidgets.html?widget=mas_vistos&tiempo=semana
Más vistos del mes:
http://multimedia.telesurtv.net/media/video/cmswidgets/cmswidgets.html?widget=mas_vistos&tiempo=mes
Más vistos del año:
http://multimedia.telesurtv.net/media/video/cmswidgets/cmswidgets.html?widget=mas_vistos&tiempo=ano
"""

WIDGET_URLS = [
                {'title': u"Más vistos del día",
                 'url': 'http://multimedia.telesurtv.net/media/video/' +
                 'cmswidgets/videos.html?widget=mas_vistos&tiempo=dia',
                },
                {'title': u"Más vistos de la semana",
                 'url': 'http://multimedia.telesurtv.net/media/video/' +
                 'cmswidgets/videos.html?widget=mas_vistos&tiempo=semana'
                 },
                {'title': u"Más vistos del mes",
                 'url': 'http://multimedia.telesurtv.net/media/video/' +
                 'cmswidgets/videos.html?widget=mas_vistos&tiempo=mes'
                 },
               ]


class Video_API(grok.View):
    grok.context(Interface)
    grok.name("video_api")
    grok.require("zope2.View")

    security = ClassSecurityInfo()

    def __init__(self, *args, **kwargs):
        super(Video_API, self).__init__(*args, **kwargs)

    def render(self):
        return u"video_api"

    def get_widgets(self):
        return WIDGET_URLS

    security.declarePublic('query')
    def query(self, **kwargs):
        """
        """
        if kwargs:
            query_url = VIDEO_API + urllib.urlencode(kwargs)
            return self.get_json(query_url)

        raise ValueError("No arguments supplied")


    def get_json(self, url):
        """
        Método que, dado una url, crea un JSON como resultado.
        En caso que la url no sea contenido apropiado para crear un JSON,
        devuelve None
        """
        result = None
        if url:
            try:
                result = json.load(urllib.urlopen(url))
            except ValueError:
                result = None

            if result and 'Error' in result:
                result = None

        return result

    def get_video_widget_url(self, url, width=400, json=None):
        """
        Método que se encarga de obtener el Javascript utilizado para
        embeber el player con el video. De la forma:
        http://[url]insertar.js?archivo=[archivo]&amp;width=[width]
        """
        if json:
            video_info = json
        else:
            video_info = self.get_json(url)

        widget_width = u"&amp;width=%s" % width
        if video_info:
            if 'archivo_url' in video_info:
                video_url = video_info['archivo_url']
                match = VIDEO_REGEX.search(video_url)
                if match:
                    clip_url = match.groups()[0]
                    return VIDEO_WIDGET_URL_BASE + clip_url + widget_width

    def get_audio_widget_url(self, url, width=400, json=None):
        """
        Método que se encarga de obtener el Javascript utilizado para
        embeber el player con el adio. De la forma:
        http://[url]insertar.js?archivo=[archivo]&amp;width=[width]&solo_audio=true
        """
        result = self.get_video_widget_url(url, width, json)
        if result:
            return result + "&solo_audio=true"

    def get_video_thumb(self, url, thumb_size='pequeno', json=None):
        """da el thumb image de un video, los posibles tamanios son pequeno,
        mediano, grande"""

        if json:
            json_data = json
        else:
            json_data = self.get_json(url)

        thumb_url = ''
        thumb = 'thumbnail_' + thumb_size
        if json_data:
            if thumb in json_data:
                thumb_url = json_data[thumb]
        return thumb_url

    

    def get_section_last_videos(self, section_name):
        #check the slug id in the api
        categories_list = ['latinoamerica', 'vuelta-al-mundo', 'deportes',
                           'ciencia', 'cultura', 'salud', 'tecnologia']
        #category = self.get_json(URL_BASE + '/categoria')

        section_id = ''
        if section_name in categories_list:
            section_id = 'http://multimedia.telesurtv.net/media/video/cmswidgets/videos.html?widget=ultimos_seccion&seccion_plone=' + section_name
        return section_id


class AddVideoToContext(grok.View):
    grok.context(Interface)
    grok.name("add-video-to-context")
    grok.require("zope2.View")

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, title, url):
        title = title.strip()
        url = url.strip()
        normalizer = getUtility(IIDNormalizer)
        id = normalizer.normalize(title)
        if id not in self.context:
            self.context.invokeFactory('Link', id, title=title, remoteUrl=url)
        link = self.context[id]
        notify(ObjectInitializedEvent(link))

    def render(self):
        return u"add-video-to-context"
