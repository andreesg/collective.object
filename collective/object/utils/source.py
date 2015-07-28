#!/usr/bin/python
# -*- coding: utf-8 -*-
from plone.formwidget.contenttree.source import PathSourceBinder, PathSource
from zope.schema.vocabulary import SimpleTerm


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Extended function that generates SimpleTerm for each related item   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class ObjPathSource(PathSource):

    def _getBrainByValue(self, value):
        if type(value) != str and type(value) != unicode:
            if not value.absolute_url():
                portal_catalog = self.context.portal_catalog
                brains = portal_catalog(UID=value.UID())
                if len(brains) > 0:
                    brain = brains[0]
                    return brain

            return self._getBrainByToken('/'.join(value.getPhysicalPath()))

    def getTermByBrain(self, brain, real_value=True):
    	item = brain.getObject()

        if real_value:
            value = brain._unrestrictedGetObject()
        else:
            value = brain.getPath()[len(self.portal_path):]

        title = brain.Title
        if hasattr(item, 'identification_identification_objectNumber'):
            title = "%s - %s" %(item.identification_identification_objectNumber, brain.Title)

        return SimpleTerm(value, token=brain.getPath(), title=title or
                          brain.id)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Extended function that uses custom ObjPathSource class    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class ObjPathSourceBinder(PathSourceBinder):
    path_source = ObjPathSource


