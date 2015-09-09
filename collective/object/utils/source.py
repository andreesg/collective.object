#!/usr/bin/python
# -*- coding: utf-8 -*-
from plone.formwidget.contenttree.source import PathSourceBinder, PathSource, ObjPathSource
from zope.schema.vocabulary import SimpleTerm


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Extended function that generates SimpleTerm for each related item   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 



class ObjExtendedPathSource(ObjPathSource):

    def _getBrainByValue(self, value):
        try:
            if type(value) != str and type(value) != unicode:
                if not value.absolute_url():
                    portal_catalog = self.context.portal_catalog
                    brains = portal_catalog(UID=value.UID())
                    if brains:
                        brain = brains[0]
                        return brain

                return self._getBrainByToken('/'.join(value.getPhysicalPath()))
        except:
            pass

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Extended function that uses custom ObjPathSource class    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class ObjPathSourceBinder(PathSourceBinder):
    path_source = ObjExtendedPathSource


