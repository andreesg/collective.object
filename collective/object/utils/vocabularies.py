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
from zope.component.hooks import getSite
from binascii import b2a_qp
from Products.CMFPlone.utils import safe_unicode
from plone.app.vocabularies.catalog import CatalogVocabulary
from plone.app.querystring import queryparser

# # # # # # # # # # # # # #
# Vocabularies            #
# # # # # # # # # # # # # #

def _createInsuranceTypeVocabulary():
    insurance_types = {
        "commercial": _(u"Commercial"),
        "indemnity": _(u"Indemnity"),
        "": ""
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
        "":""
    }

    for key, name in status_types.items():
        term = SimpleTerm(value=key, token=str(key), title=name)
        yield term

def _createPriorityVocabulary():
    priorities = {
        "low": _(u"low"),
        "medium": _(u"medium"),
        "high": _(u"high"),
        "urgent": _(u"urgent"),
        "No value":" "
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
        "regiment/service": _(u"regiment/service"),
        "No value":u" "
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
        "cultural affinity": _(u"cultural affinity"),
        "No value":u" "
    }

    for key, name in names.items():
        term = SimpleTerm(value=key, token=str(key), title=name)
        yield term

def _createTaxonomyRankVocabulary():
    taxonomies = ["kingdom", "subkingdom", "phylum/division", "subphylum/subdivision", "superclass", "class", "subclass", "infraclass", "superorder", "order", "suborder", "infraorder", "superfamily", "family", "subfamily", "tribe", "subtribe", "genus", "subgenus", "section", "subsection", "species", "subspecies", "variety", "subvariety", "form", "subform", "No value"]
    names = {}

    for tax in taxonomies:
        names[tax] = _(u'%s'%(tax))

    for key, name in names.items():
        if key == "No value":
            name = " "
        term = SimpleTerm(value=key, token=str(key), title=name)
        yield term


class ObjectVocabulary(object):

    implements(IVocabularyFactory)

    def __init__(self, index):
        self.index = index

    def __call__(self, context, query=None):
        self.context = context
        
        site = getSite()
        self.catalog = getToolByName(site, "portal_catalog")
        if self.catalog is None:
            return SimpleVocabulary([])
        index = self.catalog._catalog.getIndex(self.index)
        
        def safe_encode(term):
            if isinstance(term, unicode):
                # no need to use portal encoding for transitional encoding from
                # unicode to ascii. utf-8 should be fine.
                term = term.encode('utf-8')
            return term

        items = [
            SimpleTerm(i, b2a_qp(safe_encode(i)), safe_unicode(i))
            for i in index._index
            if type(i) != list and (query is None or safe_encode(query) in safe_encode(i))
        ]

        return SimpleVocabulary(items)

class ATVMVocabulary(object):
    implements(IVocabularyFactory)
    def __init__(self, name):
        self.name = name

    def __call__(self, context):
        portal = getSite()
        atvm = getToolByName(portal, 'portal_vocabularies')
        units = atvm.getVocabularyByName(self.name)
        terms = []

        if units:
            for term in units:
                if units[term]:
                    terms.append(SimpleVocabulary.createTerm(
                        term, term.encode('utf-8'), _(units[term].title)))
        else:
            return SimpleVocabulary(terms)
        return SimpleVocabulary(terms)


class RelatedItemsVocabulary(object):
    
    implements(IVocabularyFactory)

    def __init__(self, sort_on=None):
        self.sort_on = sort_on

    def __call__(self, context, query=None):
        parsed = {}
        if query:
            self.sort_on = 'sortable_title'
            for c in query['criteria']:
                if c['i'] == 'Type':
                    self.sort_on = "getObjPositionInParent"
                    break
                if c['i'] == 'path':
                    if c['v'] == "/zm/nl/bibliotheek" and len(query['criteria']) > 1:
                        query['criteria'] = query['criteria'][1:]
                        break
                    if c['v'] == "/zm/nl/intern/bruiklenen" and len(query['criteria']) > 1:
                        query['criteria'] = query['criteria'][1:]
                        break

            parsed = queryparser.parseFormquery(context, query['criteria'])
            if 'sort_on' in query:
                parsed['sort_on'] = query['sort_on']
            if 'sort_order' in query:
                parsed['sort_order'] = str(query['sort_order'])

            parsed['sort_on'] = self.sort_on
                
        try:
            catalog = getToolByName(context, 'portal_catalog')
        except AttributeError:
            catalog = getToolByName(getSite(), 'portal_catalog')
        brains = catalog(**parsed)

        return CatalogVocabulary.fromItems(brains, context)


class InstitutioRelatedItemsVocabulary(object):
    
    implements(IVocabularyFactory)

    def __init__(self, sort_on=None):
        self.sort_on = sort_on

    def __call__(self, context, query=None):
        parsed = {}
        if query:
            index_choice = "institution"
            catalog_index = "nameInformation_name_nameType_type"

            self.sort_on = 'sortable_title'
            for c in query['criteria']:
                if c['i'] == 'Type':
                    self.sort_on = "getObjPositionInParent"
                    break

            parsed = queryparser.parseFormquery(context, query['criteria'])
            if 'sort_on' in query:
                parsed['sort_on'] = query['sort_on']
            if 'sort_order' in query:
                parsed['sort_order'] = str(query['sort_order'])

            ### Search for index
            parsed['sort_on'] = self.sort_on
            parsed[catalog_index] = index_choice
                
        try:
            catalog = getToolByName(context, 'portal_catalog')
        except AttributeError:
            catalog = getToolByName(getSite(), 'portal_catalog')
        brains = catalog(**parsed)

        return CatalogVocabulary.fromItems(brains, context)

class TaxonomicRelatedItemsVocabulary(object):
    
    implements(IVocabularyFactory)

    def __init__(self, sort_on=None):
        self.sort_on = sort_on

    def __call__(self, context, query=None):
        parsed = {}
        if query:
            self.sort_on = 'sortable_title'

            parsed = queryparser.parseFormquery(context, query['criteria'])
            if 'sort_on' in query:
                parsed['sort_on'] = query['sort_on']
            if 'sort_order' in query:
                parsed['sort_order'] = str(query['sort_order'])

            parsed['sort_on'] = self.sort_on

            if 'taxonomic_rank' in query:
                if query['taxonomic_rank'] != "" and query['taxonomic_rank'] != " ":
                    parsed['taxonomicTermDetails_term_rank'] = query['taxonomic_rank']
                parsed['sort_on'] = self.sort_on
                
        try:
            catalog = getToolByName(context, 'portal_catalog')
        except AttributeError:
            catalog = getToolByName(getSite(), 'portal_catalog')
        
        brains = catalog(**parsed)

        return CatalogVocabulary.fromItems(brains, context)


RelatedItemsVocabularyFactory = RelatedItemsVocabulary('sortable_title')
TaxonomicRelatedItemsVocabularyFactory = TaxonomicRelatedItemsVocabulary()
InstitutioRelatedItemsVocabularyFactory = InstitutioRelatedItemsVocabulary()


# Updated vocabularies
CategoryVocabularyFactory = ObjectVocabulary('identification_objectName_category')
ObjectNameVocabularyFactory = ObjectVocabulary('identification_objectName_objectname')
RoleVocabularyFactory = ObjectVocabulary('productionDating__production_productionRole')
PlaceVocabularyFactory = ObjectVocabulary('productionDating__production_productionPlace')
SchoolStyleVocabularyFactory = ObjectVocabulary('productionDating__production_schoolStyle')

ObjectNameTypeVocabularyFactory = ObjectVocabulary('identification__objectName_objectname_type')
TechniqueVocabularyFactory = ObjectVocabulary('physicalCharacteristics__technique')
MaterialVocabularyFactory = ObjectVocabulary('physicalCharacteristics__material')
DimensionVocabularyFactory = ObjectVocabulary('physicalCharacteristics__dimension')
GeneralThemesVocabularyFactory = ObjectVocabulary('iconography__generalSearchCriteria_generalThemes')
SpecificThemesVocabularyFactory = ObjectVocabulary('iconography__generalSearchCriteria_specificThemes')
ContentSubjectsVocabularyFactory = ObjectVocabulary('iconography__contentSubjects')
InscriptionsTypeVocabularyFactory = ObjectVocabulary('inscriptionsMarkings__inscriptionsAndMarkings_type')
InscriptionsRoleVocabularyFactory = ObjectVocabulary('inscriptionsMarkings__inscriptionsAndMarkings_role')
InscriptionsScriptVocabularyFactory = ObjectVocabulary('inscriptionsMarkings__inscriptionsAndMarkings_script')
AssociatedSubjectVocabularyFactory = ObjectVocabulary('associations__associatedSubjects_subject')
AssociatedPeriodVocabularyFactory = ObjectVocabulary('associations__associatedSubjects_period')
CurrencyVocabularyFactory = ObjectVocabulary('valueInsurance__valuations_currency')
ConditionVocabularyFactory = ObjectVocabulary('conditionConservation__conditions_condition')
PreservationFormVocabularyFactory = ObjectVocabulary('conditionConservation__preservationForm')
AquisitionMethodVocabularyFactory = ObjectVocabulary('acquisition__methods')
AquisitionPlaceVocabularyFactory = ObjectVocabulary('acquisition__places')
ExchangeMethodVocabularyFactory = ObjectVocabulary('ownershipHistory__history_exchangeMethod')
HistoryPlaceVocabularyFactory = ObjectVocabulary("ownershipHistory__history_place")
LocationVocabularyFactory = ObjectVocabulary('location__normalLocation_normalLocation')
CurrentLocationVocabularyFactory = ObjectVocabulary('location__currentLocation')
CollectorRoleVocabularyFactory = ObjectVocabulary('fieldCollection__fieldCollection_collector_role')
CollectorNameVocabularyFactory = ObjectVocabulary('fieldCollection__fieldCollection_collector_name')
FieldCollectionMethodVocabularyFactory = ObjectVocabulary('fieldCollection__fieldCollection_method')
FieldCollectionPlaceVocabularyFactory = ObjectVocabulary('fieldCollection__fieldCollection_place')
PlaceFeatureVocabularyFactory = ObjectVocabulary('fieldCollection__fieldCollection_placeFeature')
StratigraphyVocabularyFactory = ObjectVocabulary('fieldCollection__habitatStratigraphy_stratigraphy')
UnitVocabularyFactory = ObjectVocabulary('physicalCharacteristics__dimensions_unit')
EventsVocabularyFactory = ObjectVocabulary('fieldCollection__fieldCollection_event')
PlaceCodeVocabularyFactory = ObjectVocabulary('fieldCollection__fieldCollection_placeCode')
PlaceCodeTypeVocabularyFactory = ObjectVocabulary('fieldCollection__fieldCollection_placeCodeType')
RelatedAssociationsVocabularyFactory = ObjectVocabulary('numbersRelationships__relationshipsWithOtherObjects_relatedObjects_association')
CollectionVocabularyFactory = ObjectVocabulary('identification__identification_collections')
AssociationVocabularyFactory = ObjectVocabulary('associations__associatedSubjects_association')
PeriodVocabularyFactory = ObjectVocabulary('productionDating__production_periods')
AspectVocabularyFactory = ObjectVocabulary('physicalCharacteristics__keyword_aspect')
KeywordVocabularyFactory = ObjectVocabulary('physicalCharacteristics__keyword_keyword')

#
# ATVM vocabularies
#
ObjectStatusVocabularyFactory = ATVMVocabulary('ObjectStatus')
NameTypeVocabularyFactory = ATVMVocabulary('NameType')
SubjectTypeVocabularyFactory = ATVMVocabulary('SubjectType')
DimensionsUnitVocabularyFactory = ATVMVocabulary('Unit')
TaxonomyRankVocabularyFactory = ATVMVocabulary('TaxonomyRank')
MakerControllerVocabularyFactory = ATVMVocabulary('PersonFolder')

#
# Static vocabula
#
priority_vocabulary = SimpleVocabulary(list(_createPriorityVocabulary()))
insurance_type_vocabulary = SimpleVocabulary(list(_createInsuranceTypeVocabulary()))
objectstatus_vocabulary = SimpleVocabulary(list(_createObjectStatusVocabulary()))
nametype_vocabulary = SimpleVocabulary(list(_createNameTypeVocabulary()))
subjecttype_vocabulary = SimpleVocabulary(list(_createSubjectTypeVocabulary()))
taxonomyrank_vocabulary = SimpleVocabulary(list(_createTaxonomyRankVocabulary()))

