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
        "No value":" "
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
        "subject": _(u"subject"),
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

        items = []

        for i in index._index:
            if type(i) != list and (query is None or safe_encode(query).lower() in safe_encode(i).lower()):
                items.append(SimpleTerm(i, b2a_qp(safe_encode(i)), safe_unicode(i)))

        items.sort(key=lambda x: x.token.lower())

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

            if 'name_type' in query:
                if query['name_type'] != "" and query['name_type'] != " " and query["name_type"] != "No value":
                    parsed['nameInformation_name_nameType_type'] = query['name_type']

            if 'SearchableText' in parsed:
                parsed['Title'] = parsed.pop('SearchableText')
                
        try:
            catalog = getToolByName(context, 'portal_catalog')
        except AttributeError:
            catalog = getToolByName(getSite(), 'portal_catalog')
        brains = catalog(**parsed)

        return CatalogVocabulary.fromItems(brains, context)


class InstitutioRelatedItemsVocabulary(object):
    
    implements(IVocabularyFactory)

    def __init__(self, index=""):
        self.index = index

    def __call__(self, context, query=None):
        parsed = {}
        if query:
            if self.index:
                index_choice = self.index
            else:
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

            if 'SearchableText' in parsed:
                parsed['Title'] = parsed.pop('SearchableText')
                
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
                if query['taxonomic_rank'] != "" and query['taxonomic_rank'] != " " and query['taxonomic_rank'] != "No value":
                    parsed['taxonomicTermDetails_term_rank'] = query['taxonomic_rank']

            if 'SearchableText' in parsed:
                parsed['Title'] = parsed.pop('SearchableText')
                
        try:
            catalog = getToolByName(context, 'portal_catalog')
        except AttributeError:
            catalog = getToolByName(getSite(), 'portal_catalog')
        
        brains = catalog(**parsed)

        return CatalogVocabulary.fromItems(brains, context)


RelatedItemsVocabularyFactory = RelatedItemsVocabulary('sortable_title')
TaxonomicRelatedItemsVocabularyFactory = TaxonomicRelatedItemsVocabulary()
InstitutioRelatedItemsVocabularyFactory = InstitutioRelatedItemsVocabulary('institution')
MakerRelatedItemsVocabularyFactory = InstitutioRelatedItemsVocabulary('maker')
CollectorRelatedItemsVocabularyFactory = InstitutioRelatedItemsVocabulary('field collector')


# Updated vocabularies


### FIXED
CommonNameVocabularyFactory = ObjectVocabulary('identification_taxonomy_commonName')
ScientificNameVocabularyFactory = ObjectVocabulary('identification_taxonomy_scientificName')

AssociationVocabularyFactory = ObjectVocabulary('associations_associatedSubjects_association')
AssociatedSubjectVocabularyFactory = ObjectVocabulary('associations_associatedSubjects_subject')
AssociatedPeriodVocabularyFactory = ObjectVocabulary('associations_associatedSubjects_period')
ConditionVocabularyFactory = ObjectVocabulary('conditionConservation_conditions_condition')
PreservationFormVocabularyFactory = ObjectVocabulary('conditionConservation_preservationForms')
CollectorRoleVocabularyFactory = ObjectVocabulary('fieldCollection_fieldCollection_collector_role')
CollectorNameVocabularyFactory = ObjectVocabulary('fieldCollection_fieldCollection_collector_name')
FieldCollectionMethodVocabularyFactory = ObjectVocabulary('fieldCollection_fieldCollection_method')
FieldCollectionPlaceVocabularyFactory = ObjectVocabulary('fieldCollection_fieldCollection_place')
PlaceFeatureVocabularyFactory = ObjectVocabulary('fieldCollection_fieldCollection_placeFeature')
StratigraphyVocabularyFactory = ObjectVocabulary('fieldCollection_habitatAndStratigraphy_stratigraphy')
UnitVocabularyFactory = ObjectVocabulary('physicalCharacteristics_dimensions_unit')
EventsVocabularyFactory = ObjectVocabulary('fieldCollection_fieldCollection_event')
PlaceCodeVocabularyFactory = ObjectVocabulary('fieldCollection_fieldCollection_placeCode')
PlaceCodeTypeVocabularyFactory = ObjectVocabulary('fieldCollection_fieldCollection_placeCodeType')
GeneralThemesVocabularyFactory = ObjectVocabulary('iconography_generalSearchCriteria_generalThemes')
SpecificThemesVocabularyFactory = ObjectVocabulary('iconography_generalSearchCriteria_specificThemes')
ContentSubjectsVocabularyFactory = ObjectVocabulary('iconography_contentsubjects')
ObjectNameTypeVocabularyFactory = ObjectVocabulary('identification_objectName_objectname_type')
CollectionVocabularyFactory = ObjectVocabulary('identification_identification_collection')
InscriptionsTypeVocabularyFactory = ObjectVocabulary('inscriptionsMarkings_inscriptionsAndMarkings_type')
InscriptionsRoleVocabularyFactory = ObjectVocabulary('inscriptionsMarkings_inscriptionsAndMarkings_role')
InscriptionsScriptVocabularyFactory = ObjectVocabulary('inscriptionsMarkings_inscriptionsAndMarkings_script')
LocationVocabularyFactory = ObjectVocabulary('location_normalLocation_normallocation')
CurrentLocationVocabularyFactory = ObjectVocabulary('location_currentlocation')
ExchangeMethodVocabularyFactory = ObjectVocabulary('ownershipHistory_history_exchangeMethods')
HistoryPlaceVocabularyFactory = ObjectVocabulary("ownershipHistory_history_places")
TechniqueVocabularyFactory = ObjectVocabulary('physicalCharacteristics_techniques')
MaterialVocabularyFactory = ObjectVocabulary('physicalCharacteristics_materials')
DimensionVocabularyFactory = ObjectVocabulary('physicalCharacteristics_dimensions')
AspectVocabularyFactory = ObjectVocabulary('physicalCharacteristics_keyword_aspect')
KeywordVocabularyFactory = ObjectVocabulary('physicalCharacteristics_keyword_keyword')
RoleVocabularyFactory = ObjectVocabulary('productionDating_production_productionRole')
PlaceVocabularyFactory = ObjectVocabulary('productionDating_production_productionPlace')
SchoolStyleVocabularyFactory = ObjectVocabulary('productionDating_production_schoolStyle')
PeriodVocabularyFactory = ObjectVocabulary('productionDating_production_period')
AquisitionMethodVocabularyFactory = ObjectVocabulary('acquisition_method')
AquisitionPlaceVocabularyFactory = ObjectVocabulary('acquisition_place')
CategoryVocabularyFactory = ObjectVocabulary('identification_objectName_category')
ObjectNameVocabularyFactory = ObjectVocabulary('identification_objectName_objectname')
CurrencyVocabularyFactory = ObjectVocabulary('valueInsurance_valuations_currency')
HabitatVocabularyFactory = ObjectVocabulary('fieldCollection_habitatStratigraphy_habitats')
RelatedAssociationsVocabularyFactory = ObjectVocabulary('numbersRelationships_relationshipsWithOtherObjects_relatedObjects_association')


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

