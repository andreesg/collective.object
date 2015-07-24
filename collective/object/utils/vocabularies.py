#!/usr/bin/python
# -*- coding: utf-8 -*-

#atvm = getToolByName(context, 'portal_vocabularies')
#categories = atvm.getVocabularyByName('object-categories-vocabulary')
#terms = []
#for term in categories:
#    terms.append(SimpleVocabulary.createTerm(
#        term, term.encode('utf-8'), categories[term].title))
#return SimpleVocabulary(terms)

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

def _createNameTypeVocabulary():
    # [person, family, institution, regiment/service]
    names = {
        "person": _(u"person"),
        "family": _(u"family"),
        "institution": _(u"institution"),
        "regiment/service": _(u"regiment/service")
    }
    for key, name in names.items():
        term = SimpleTerm(value=key, token=str(key), title=name)
        yield term

def _createSubjectTypeVocabulary():
    # [object name, animal, plant, activity, event, subject, geography, concept, people, cultural affinity]
    names = {
        "object name": _(u"object name"),
        "animal": _(u"animal"),
        "plant": _(u"plant"),
        "activity": _(u"activity"),
        "event": _(u"event"),
        "subject": _(u"subject"),
        "geography": _(u"geography"),
        "concept": _(u"concept"),
        "people": _(u"people"),
        "geography": _(u"geography"),
        "cultural affinity": _(u"cultural affinity"),
    }

    for key, name in names.items():
        term = SimpleTerm(value=key, token=str(key), title=name)
        yield term

def _createTaxonomyRankVocabulary():
    taxonomies = ["kingdom", "subkingdom", "phylum/division", "subphylum/subdivision", "superclass", "class", "subclass", "infraclass", "superorder", "order", "suborder", "infraorder", "superfamily", "family", "subfamily", "tribe", "subtribe", "genus", "subgenus", "section", "subsection", "species", "subspecies", "variety", "subvariety", "form", "subform"]
    names = {}

    for tax in taxonomies:
        names[tax] = _(u'%s'%(tax))

    for key, name in names.items():
        term = SimpleTerm(value=key, token=str(key), title=name)
        yield term

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


class RoleVocabulary(object):
    """Vocabulary factory listing all catalog keywords from the "productionDating_production_productionRole" index
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        self.context = context
        portal = api.portal.get()
        self.catalog = getToolByName(portal, "portal_catalog")
        if self.catalog is None:
            return SimpleVocabulary([])
        index = self.catalog._catalog.getIndex('productionDating_production_productionRole')
        items = [SimpleTerm(i, i, i) for i in index._index]

        return SimpleVocabulary(items)

class PlaceVocabulary(object):
    """Vocabulary factory listing all catalog keywords from the "productionDating_production_productionPlace" index
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        self.context = context
        portal = api.portal.get()
        self.catalog = getToolByName(portal, "portal_catalog")
        if self.catalog is None:
            return SimpleVocabulary([])
        index = self.catalog._catalog.getIndex('productionDating_production_productionPlace')
        items = [SimpleTerm(i, i, i) for i in index._index]

        return SimpleVocabulary(items)

class SchoolStyleVocabulary(object):
    """Vocabulary factory listing all catalog keywords from the "productionDating_production_schoolStyle" index
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        self.context = context
        portal = api.portal.get()
        self.catalog = getToolByName(portal, "portal_catalog")
        if self.catalog is None:
            return SimpleVocabulary([])
        index = self.catalog._catalog.getIndex('productionDating_production_schoolStyle')
        items = [SimpleTerm(i, i, i) for i in index._index]

        return SimpleVocabulary(items)

class ObjectVocabulary(object):

    implements(IVocabularyFactory)

    def __init__(self, index):
        self.index = index

    def __call__(self, context):
        self.context = context
        portal = api.portal.get()
        self.catalog = getToolByName(portal, "portal_catalog")
        if self.catalog is None:
            return SimpleVocabulary([])
        index = self.catalog._catalog.getIndex(self.index)

        items = [SimpleTerm(value=i, token=i.encode('ascii', 'ignore'), title=i) for i in index._index]

        return SimpleVocabulary(items)


# TODO: Update vocabularies to use general ObjectVocabulary
CategoryVocabularyFactory = CategoryVocabulary()
ObjectNameVocabularyFactory = ObjectNameVocabulary()
RoleVocabularyFactory = RoleVocabulary()
PlaceVocabularyFactory = PlaceVocabulary()
SchoolStyleVocabularyFactory = SchoolStyleVocabulary()

# Updated vocabularies
TechniqueVocabularyFactory = ObjectVocabulary('physicalCharacteristics_technique')
MaterialVocabularyFactory = ObjectVocabulary('physicalCharacteristics_material')
DimensionVocabularyFactory = ObjectVocabulary('physicalCharacteristics_dimension')
GeneralThemesVocabularyFactory = ObjectVocabulary('iconography_generalSearchCriteria_generalThemes')
SpecificThemesVocabularyFactory = ObjectVocabulary('iconography_generalSearchCriteria_specificThemes')
ContentSubjectsVocabularyFactory = ObjectVocabulary('iconography_contentSubjects')
InscriptionsTypeVocabularyFactory = ObjectVocabulary('inscriptionsMarkings_inscriptionsAndMarkings_type')
InscriptionsRoleVocabularyFactory = ObjectVocabulary('inscriptionsMarkings_inscriptionsAndMarkings_role')
InscriptionsScriptVocabularyFactory = ObjectVocabulary('inscriptionsMarkings_inscriptionsAndMarkings_script')
AssociatedSubjectVocabularyFactory = ObjectVocabulary('associations_associatedSubjects_subject')
AssociatedPeriodVocabularyFactory = ObjectVocabulary('associations_associatedSubjects_period')
CurrencyVocabularyFactory = ObjectVocabulary('valueInsurance_valuations_currency')
ConditionVocabularyFactory = ObjectVocabulary('conditionConservation_conditions_condition')
PreservationFormVocabularyFactory = ObjectVocabulary('conditionConservation_preservationForm')
AquisitionMethodVocabularyFactory = ObjectVocabulary('acquisition_methods')
AquisitionPlaceVocabularyFactory = ObjectVocabulary('acquisition_places')
ExchangeMethodVocabularyFactory = ObjectVocabulary('ownershipHistory_history_exchangeMethod')
HistoryPlaceVocabularyFactory = ObjectVocabulary("ownershipHistory_history_place")


priority_vocabulary = SimpleVocabulary(list(_createPriorityVocabulary()))
insurance_type_vocabulary = SimpleVocabulary(list(_createInsuranceTypeVocabulary()))
objectstatus_vocabulary = SimpleVocabulary(list(_createObjectStatusVocabulary()))
nametype_vocabulary = SimpleVocabulary(list(_createNameTypeVocabulary()))
subjecttype_vocabulary = SimpleVocabulary(list(_createSubjectTypeVocabulary()))
taxonomyrank_vocabulary = SimpleVocabulary(list(_createTaxonomyRankVocabulary()))
