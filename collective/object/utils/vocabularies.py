#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from collective.object import MessageFactory as _
from zope.schema.interfaces import ISource, IContextSourceBinder, IVocabularyFactory
from zope.interface import implements, classProvides
from Products.CMFCore.utils import getToolByName
from plone import api
# # # # # # # # # # # # # #
# Vocabularies            #
# # # # # # # # # # # # # #

def _createInsuranceTypeVocabulary():
    insurance_types = {
        "commercial": _(u"Commercial"),
        "indemnity": _(u"Indemnity"),
    }

    for key, name in insurance_types.items():
        term = SimpleTerm(value=key, token=str(key), title=name)
        yield term

def _createObjectStatusVocabulary():
    # holotype, lectotype, neotype, paralectotype, paratype, syntype
    status_types = {
        "holotype": _(u"holotype"),
        "neotype": _(u"neotype"),
        "paralectotype": _(u"paralectotype"),
        "paratype": _(u"paratype"),
        "syntype": _(u"syntype"),
    }

    for key, name in status_types.items():
        term = SimpleTerm(value=key, token=str(key), title=name)
        yield term

def _createPriorityVocabulary():
    priorities = {
        "low": _(u"low"),
        "medium": _(u"medium"),
        "high": _(u"high"),
        "urgent": _(u"urgent")
    }

    for key, name in priorities.items():
        term = SimpleTerm(value=key, token=str(key), title=name)
        yield term

#atvm = getToolByName(context, 'portal_vocabularies')
#categories = atvm.getVocabularyByName('object-categories-vocabulary')
#terms = []
#for term in categories:
#    terms.append(SimpleVocabulary.createTerm(
#        term, term.encode('utf-8'), categories[term].title))
#return SimpleVocabulary(terms)

class CategoryVocabulary(object):
    """Vocabulary factory listing all catalog keywords from the "identification_objectName_category" index
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        self.context = context
        portal = api.portal.get()
        self.catalog = getToolByName(portal, "portal_catalog")
        if self.catalog is None:
            return SimpleVocabulary([])
        index = self.catalog._catalog.getIndex('identification_objectName_category')
        items = [SimpleTerm(i, i, i) for i in index._index]
        return SimpleVocabulary(items)

class ObjectNameVocabulary(object):
    """Vocabulary factory listing all catalog keywords from the "identification_objectName_category" index
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        self.context = context
        portal = api.portal.get()
        self.catalog = getToolByName(portal, "portal_catalog")
        if self.catalog is None:
            return SimpleVocabulary([])
        index = self.catalog._catalog.getIndex('identification_objectName_objectname')
        items = [SimpleTerm(i, i, i) for i in index._index]

        return SimpleVocabulary(items)

CategoryVocabularyFactory = CategoryVocabulary()
ObjectNameVocabularyFactory = ObjectNameVocabulary()

priority_vocabulary = SimpleVocabulary(list(_createPriorityVocabulary()))
insurance_type_vocabulary = SimpleVocabulary(list(_createInsuranceTypeVocabulary()))
objectstatus_vocabulary = SimpleVocabulary(list(_createObjectStatusVocabulary()))


