# -*- coding: utf-8 -*-

from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer


class IPortalAPI(Interface):
    """ Interfaz genérica para APis """


class ITelesurAPILayer(IDefaultPloneLayer):
    """ Default browser layer for telesur.api """


class IPortalAPIQuerySchema(Interface):
    """ Interfaz para describir los campos de búsqueda """


class IVideoAPIQuerySchema(Interface):
    """ Interfaz para describir los campos de búsqueda """


class IAPIViewlet(Interface):
    """ Interfaz para viewlets del API """
