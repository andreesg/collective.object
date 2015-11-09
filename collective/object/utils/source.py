#!/usr/bin/python
# -*- coding: utf-8 -*-
from plone.formwidget.contenttree.source import PathSourceBinder, PathSource, ObjPathSource, UUIDSource
from zope.schema.vocabulary import SimpleTerm
from plone.app.uuid.utils import uuidToCatalogBrain

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Extended function that generates SimpleTerm for each related item   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class ObjExtendedPathSource(ObjPathSource):

    def _getBrainByValue(self, value):
        try:
            if type(value) != str and type(value) != unicode:
                try:
                    if not value.absolute_url():
                        uuid = value.UID()
                        brains = uuidToCatalogBrain(uuid)
                        if brains:
                            return brains
                except:
                    raise

                return self._getBrainByToken('/'.join(value.getPhysicalPath()))
        except:
            raise

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Extended function that uses custom ObjPathSource class    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class ObjPathSourceBinder(PathSourceBinder):
    path_source = ObjExtendedPathSource


