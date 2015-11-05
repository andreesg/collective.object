#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface
from collective.object import MessageFactory as _
from zope.component import adapts

## 
## Utils
##
from ..utils.vocabularies import _createPriorityVocabulary, _createInsuranceTypeVocabulary, \
                                _createNameTypeVocabulary, _createSubjectTypeVocabulary, _createTaxonomyRankVocabulary,RelatedItemsVocabulary, RelatedItemsVocabularyFactory

from ..utils.source import ObjPathSourceBinder
from ..utils.variables import *
from ..utils.widgets import AjaxSingleSelectFieldWidget, SimpleRelatedItemsFieldWidget, TaxonomicRelatedItemsFieldWidget

from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from plone.directives import form
from plone.app.widgets.dx import AjaxSelectFieldWidget, DatetimeFieldWidget
from plone.formwidget.autocomplete import AutocompleteFieldWidget

from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList, Relation

import datetime
from five import grok

priority_vocabulary = SimpleVocabulary(list(_createPriorityVocabulary()))
insurance_type_vocabulary = SimpleVocabulary(list(_createInsuranceTypeVocabulary()))
nametype_vocabulary = SimpleVocabulary(list(_createNameTypeVocabulary()))
subjecttype_vocabulary = SimpleVocabulary(list(_createSubjectTypeVocabulary()))
taxonomyrank_vocabulary = SimpleVocabulary(list(_createTaxonomyRankVocabulary()))


class IListField(Interface):
    pass

class ListField(schema.List):
    grok.implements(IListField)
    """We need to have a unique class for the field list so that we
    can apply a custom adapter."""
    pass

# # # # # # # # # # # # #
# Widget interface      #
# # # # # # # # # # # # #

class IFormWidget(Interface):
    pass


# # # # # # # # # # # # # #
# DataGrid interfaces     # 
# # # # # # # # # # # # # #


##
## Vocabularies
##

## Identification
class IObjectname(form.Schema):
    form.widget('name', AjaxSingleSelectFieldWidget, vocabulary="collective.object.objectname")
    name = schema.List(
        title=_(u'Object name'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )

    type = schema.TextLine(title=_(u'Type'), required=False)
    
    form.widget('types', AjaxSingleSelectFieldWidget, vocabulary="collective.object.objectname_type")
    types = schema.List(
        title=_(u'Type'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[],
        default=[]
    )

    notes = schema.Text(title=_(u'Notes'), required=False, default=u"", missing_value=u"")

class ITitle(Interface):
    title = schema.TextLine(title=_(u'Title'), required=False)
    type = schema.TextLine(title=_(u'Type'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

class ITranslatedTitle(Interface):
    title = schema.TextLine(title=_(u'Translated title'), required=False)


class IFrom(Interface):
    aquisitionFrom = RelationList(
        title=_(u'label_from', default=u'From'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution')
        ),
        required=False
    )

    form.widget('aquisitionFrom', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

## Production & Dating
class IProductiondating(form.Schema):
    #makerController = schema.Choice(title=_(u' '), 
    #    required=True, 
    #    vocabulary="collective.object.makerController", 
    #    default=u"A", 
    #    missing_value=u"A"
    #)

    makers = RelationList(
        title=_(u'Maker'),
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution')
        ),
        required=False
    )
    form.widget('makers', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    qualifier = schema.TextLine(title=_(u'label_kwal'), required=False)
    
    form.widget('role', AjaxSingleSelectFieldWidget, vocabulary="collective.object.productionRole")
    role = schema.List(
        title=_(u'Role'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[],
        max_length=1
    )

    form.widget('place', AjaxSingleSelectFieldWidget, vocabulary="collective.object.productionPlace")
    place = schema.List(
        title=_(u'label_plaats'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[],
        max_length=1
    )

    dateBirth = schema.TextLine(title=_(u'Date birth'), required=False)
    dateDeath = schema.TextLine(title=_(u'Date death'), required=False)

    production_notes = schema.Text(title=_(u'Production notes'), required=False, default=u" ", missing_value=u" ")

class ISchoolStyle(Interface):
    form.widget('term', AjaxSelectFieldWidget, vocabulary="collective.object.productionSchoolStyle")
    term = schema.List(
        title=_(u'School / style'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )

## Physical Characteristics
class ITechniques(Interface):
    part = schema.TextLine(title=_(u'Part'), required=False)
    form.widget('technique', AjaxSingleSelectFieldWidget, vocabulary="collective.object.techniques")
    technique = schema.List(
        title=_(u'Technique'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    notes = schema.Text(title=_(u'Notes'), required=False)

class IMaterials(Interface):
    part = schema.TextLine(title=_(u'Part'), required=False)

    form.widget('material', AjaxSingleSelectFieldWidget, vocabulary="collective.object.materials")
    material = schema.List(
        title=_(u'Material'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )

    notes = schema.Text(title=_(u'Notes'), required=False)

class IAuction(Interface):
    auction = RelationList(
        title=_(u'Auction'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='Auction')
        ),
        required=False
    )

class IDimensions(Interface):
    part = schema.TextLine(title=_(u'Part'), required=False)
    
    form.widget('dimension', AjaxSingleSelectFieldWidget, vocabulary="collective.object.dimensions")
    dimension = schema.List(
        title=_(u'Dimension'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )

    value = schema.TextLine(title=_(u'Value'), required=False)

    #form.widget('unit', AjaxSelectFieldWidget, vocabulary="collective.object.units")
    units = schema.Choice(
        title=_(u'Unit'),
        required=True,
        vocabulary="collective.object.units",
        default="No value",
        missing_value=" "
    )

    precision = schema.TextLine(title=_(u'Precision'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

class IKeywords(Interface):
    part = schema.TextLine(title=_(u'Part'), required=False)
    
    form.widget('aspect', AjaxSingleSelectFieldWidget, vocabulary="collective.object.aspects")
    aspect = schema.List(
        title=_(u'Aspect'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )

    form.widget('keyword', AjaxSingleSelectFieldWidget, vocabulary="collective.object.keywords")
    keyword = schema.List(
        title=_(u'Keyword'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    notes = schema.Text(title=_(u'Notes'), required=False)

# Iconography
class IIconographyGeneralThemes(Interface):
    form.widget('term', AjaxSingleSelectFieldWidget, vocabulary="collective.object.generalthemes")
    term = schema.List(
        title=_(u'General theme'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )

class IIconographySpecificThemes(Interface):
    form.widget('term', AjaxSingleSelectFieldWidget, vocabulary="collective.object.specificthemes")
    term = schema.List(
        title=_(u'Specific theme'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )

class IIconographyContentSubjects(Interface):
    position = schema.TextLine(title=_(u'Position'), required=False)    
    subjectType = schema.Choice(title=_(u'Subject type'), required=True, vocabulary="collective.object.subjecttype", default="No value", missing_value=" ")
    
    form.widget('subject', AjaxSingleSelectFieldWidget, vocabulary="collective.object.contentsubjects")
    subject = schema.List(
        title=_(u'Subject'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )

    taxonomicRank = schema.Choice(title=_(u'Taxonomic rank'), required=True, vocabulary="collective.object.taxonomyrank", default="No value", missing_value=" ")
    
    form.widget('properName', AjaxSingleSelectFieldWidget, vocabulary="collective.object.contentsubjects")
    
    scientificName = RelationList(
        title=_(u'Scientific name'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type="Taxonomie")
        ),
        required=False
    )
    form.widget('scientificName', TaxonomicRelatedItemsFieldWidget, vocabulary='collective.object.relatedTaxonomicRank')

    properName = schema.List(
        title=_(u'Proper name'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    
    notes = schema.Text(title=_(u'Notes'), required=False)

# Inscriptions and Markings
## Inscriptions and Markings
class IInscriptions(Interface):
    form.widget('type', AjaxSingleSelectFieldWidget, vocabulary="collective.object.inscriptionsType")
    type = schema.List(
        title=_(u'Type'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    
    position = schema.TextLine(title=_(u'Position'),required=False)
    method = schema.TextLine(title=_(u'Method'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)
    #creator = schema.TextLine(title=_(u'Creator'), required=False)
    
    creators = RelationList(
        title=_(u'Creator'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution')
        ),
        required=False
    )
    form.widget('creators', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    form.widget('role', AjaxSingleSelectFieldWidget, vocabulary="collective.object.inscriptionsRole")
    role = schema.List(
        title=_(u'Role'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )

    content = schema.TextLine(title=_(u'Content'), required=False)
    description = schema.TextLine(title=_(u'Description'), required=False)
    interpretation = schema.TextLine(title=_(u'Interpretation'), required=False)
    language = schema.TextLine(title=_(u'Language'), required=False)
    
    #New field
    translation = schema.TextLine(title=_(u'Translation'), required=False, missing_value="")
    
    form.widget('script', AjaxSingleSelectFieldWidget, vocabulary="collective.object.inscriptionsScript")
    script = schema.List(
        title=_(u'Script'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )

    transliteration = schema.TextLine(title=_(u'Transliteration'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

# Associations
class IAssociatedSubjects(Interface):
    # Caroline feedback: Remove properName, startData, endDate

    form.widget('associations', AjaxSingleSelectFieldWidget, vocabulary="collective.object.associatedSubjects_association")
    associations = schema.List(
        title=_(u'Association'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )

    subjectType = schema.Choice(title=_(u'Subject type'), required=True, vocabulary="collective.object.subjecttype", default="No value", missing_value=" ")
        
    form.widget('subject', AjaxSingleSelectFieldWidget, vocabulary="collective.object.associatedsubjects")
    subject = schema.List(
        title=_(u'Subject'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )

    taxonomicRank = schema.Choice(title=_(u'Taxonomic rank'), required=True, vocabulary="collective.object.taxonomyrank", default="No value", missing_value=" ")
    scientificName = RelationList(
        title=_(u'Scientific name'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type="Taxonomie")
        ),
        required=False
    )
    form.widget('scientificName', TaxonomicRelatedItemsFieldWidget, vocabulary='collective.object.relatedTaxonomicRank')

    # These fields are going to be removed in the future
    form.widget('properName', AjaxSingleSelectFieldWidget, vocabulary="collective.object.associatedsubjects")
    properName = schema.List(
        title=_(u'Proper name'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )

    startDate = schema.TextLine(title=_(u'Start date'), required=False)
    endDate = schema.TextLine(title=_(u'End date'), required=False)
    identifier = schema.TextLine(title=_(u'Identifier'), required=False)

    notes = schema.Text(title=_(u'Notes'), required=False)

class IAssociatedPeriods(Interface):
    form.widget('associations', AjaxSingleSelectFieldWidget, vocabulary="collective.object.associatedSubjects_association")
    associations = schema.List(
        title=_(u'Association'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    
    form.widget('period', AjaxSingleSelectFieldWidget, vocabulary="collective.object.associatedperiods")
    period = schema.List(
        title=_(u'Period'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )

    startDate = schema.TextLine(title=_(u'Start date'), required=False)
    endDate = schema.TextLine(title=_(u'End date'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

# Value & Insurance
class IValuations(Interface):
    value = schema.TextLine(title=_(u'Value'), required=False)

    form.widget('curr', AjaxSingleSelectFieldWidget, vocabulary="collective.object.currency")
    curr = schema.List(
        title=_(u'Curr.'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )

    valuer = schema.TextLine(title=_(u'Valuer'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)
    #reference = schema.TextLine(title=_(u'Reference'), required=False)

class IConditions(Interface):
    part = schema.TextLine(title=_(u'Part'), required=False)

    form.widget('condition', AjaxSingleSelectFieldWidget, vocabulary="collective.object.condition")
    condition = schema.List(
        title=_(u'Condition'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    
    notes = schema.Text(title=_(u'Notes'), required=False)
    checked_by = schema.TextLine(title=_(u'Checked by'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)


class IEnvConditions(Interface):    
    form.widget('preservation_form', AjaxSingleSelectFieldWidget, vocabulary="collective.object.preservationform")
    preservation_form = schema.List(
        title=_(u'Preservation form'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    notes = schema.Text(title=_(u'Notes'), required=False)


# Aquisition
class IFundings(Interface):
    amount = schema.TextLine(title=_(u'Amount'), required=False)
    
    form.widget('curr', AjaxSingleSelectFieldWidget, vocabulary="collective.object.currency")
    curr = schema.List(
        title=_(u'Curr.'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    
    source = schema.TextLine(title=_(u'Source'), required=False)
    provisos = schema.TextLine(title=_(u'label_provisos', default=u"Provisos"), required=False)


# Location
class ICurrentLocations(Interface):
    start_date = schema.TextLine(title=_(u'Start date'), required=False)
    end_date = schema.TextLine(title=_(u'End date'), required=False)
    location_type = schema.TextLine(title=_(u'Location type'), required=False)
    
    form.widget('location', AjaxSingleSelectFieldWidget, vocabulary="collective.object.currentlocation")
    location = schema.List(
        title=_(u'Location'), 
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )

    fitness = schema.TextLine(title=_(u'Fitness'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

class ICollectionCollectors(Interface):
    #name = schema.TextLine(title=_(u'Collector'), required=False)
    name = RelationList(
        title=_(u'Collector'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type="PersonOrInstitution")
        ),
        required=False
    )
    form.widget('name', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    form.widget('role', AjaxSingleSelectFieldWidget, vocabulary="collective.object.fieldCollection_collector_role")
    role = schema.List(
        title=_(u'Role'), 
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )

class IHistoryOwner(Interface):
    owner = RelationList(
        title=_(u'Owner'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution')
        ),
        required=False
    )
    form.widget('owner', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    startDate = schema.TextLine(title=_(u'From'), required=False)
    endDate = schema.TextLine(title=_(u'Until'), required=False)

    form.widget('method', AjaxSingleSelectFieldWidget, vocabulary="collective.object.fieldCollection_collector_role")
    method = schema.List(
        title=_(u'Exchange method'), 
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )

    acquiredFrom = RelationList(
        title=_(u'Acquired from'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution')
        ),
        required=False
    )
    form.widget('acquiredFrom', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    lotnr =  schema.TextLine(title=_(u'Lot no.'), required=False)
    auction = schema.TextLine(title=_(u'Auction'), required=False)

    form.widget('place', AjaxSingleSelectFieldWidget, vocabulary="collective.object.fieldCollection_collector_role")
    place = schema.List(
        title=_(u'label_plaats', default=u'Place'), 
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )

    price = schema.TextLine(title=_(u'Price'), required=False)
    category = schema.TextLine(title=_(u'Ownership category'), required=False)
    access = schema.TextLine(title=_(u'Access'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)






class ICollectors(Interface):
    #name = schema.TextLine(title=_(u'Collector'), required=False)
    
    name = RelationList(
        title=_(u'Determiner'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type="PersonOrInstitution")
        ),
        required=False
    )

    form.widget('role', AjaxSelectFieldWidget, vocabulary="collective.object.fieldCollection_collector_role")
    role = schema.List(
        title=_(u'Role'), 
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )

class IStratigrafie(Interface):

    form.widget('unit', AjaxSingleSelectFieldWidget, vocabulary="collective.object.fieldCollection_stratigraphy")
    unit = schema.List(
        title=_(u'Stratigraphy'), 
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    type = schema.TextLine(title=_(u'Strat. type'), required=False)


class IPlaceCodes(Interface):
    form.widget('code', AjaxSingleSelectFieldWidget, vocabulary="collective.object.placecode")
    code = schema.List(
        title=_(u'Place code'), 
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )

    form.widget('codeType', AjaxSingleSelectFieldWidget, vocabulary="collective.object.placecodetype")
    codeType = schema.List(
        title=_(u'Code type'), 
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )

##
## Numbers / relations
##
class IRelatedObjects(Interface):
    relatedObject = RelationList(
        title=_(u'Related object'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='Object')
        ),
        required=False
    )
    form.widget('relatedObject', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    
    #relatedObject = schema.TextLine(title=_(u'Related object'), required=False)
    form.widget('associations', AjaxSelectFieldWidget, vocabulary="collective.object.relatedassociations")
    associations = schema.List(
        title=_(u'Association'), 
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )

    notes = schema.Text(title=_(u'Notes'), required=False)




##
## Fields
##

# Identification
class ICollection(Interface):
    term = schema.TextLine(title=_(u'Collection'), required=False)

class IObjectName(form.Schema):
    name = schema.TextLine(title=_(u'Object name'), required=False)
    type = schema.TextLine(title=_(u'Type'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

class IObjectCategory(Interface):
    term = schema.TextLine(title=_(u'Object Category'), required=False)

class IOtherName(Interface):
    name = schema.TextLine(title=_(u'Other name'), required=False)
    type = schema.TextLine(title=_(u'Type'), required=False)

class ITaxonomyRank(Interface):
    text = schema.TextLine(title=_(u'Taxonomy rank'), required=False)

class ITaxonomy(Interface):
    rank = schema.Choice(
        title=_(u'Taxonomy rank'), 
        required=True,
        vocabulary="collective.object.taxonomyrank",
        default="No value",
        missing_value=" "
    )

    scientific_name = RelationList(
        title=_(u'Scientific name'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type="Taxonomie")
        ),
        required=False
    )
    form.widget('scientific_name', TaxonomicRelatedItemsFieldWidget, vocabulary='collective.object.relatedTaxonomicRank')

    #common_name = schema.TextLine(title=_(u'Common name'), required=False)

class IDeterminer(form.Schema):
    name = schema.TextLine(title=_(u'Determiner'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)
    #form.widget(determinerDate=DatetimeFieldWidget)
    #determinerDate = schema.Datetime(title=_(u'Date'), required=False)


class IDeterminers(form.Schema):
    name = RelationList(
        title=_(u'Determiner'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type="PersonOrInstitution")
        ),
        required=False
    )
    form.widget('name', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    date = schema.TextLine(title=_(u'Date'), required=False)
    #form.widget(determinerDate=DatetimeFieldWidget)
    #determinerDate = schema.Datetime(title=_(u'Date'), required=False)


# Physical Characteristics
class IKeyword(Interface):
    part = schema.TextLine(title=_(u'Part'), required=False)
    aspect = schema.TextLine(title=_(u'Aspect'), required=False)
    keyword = schema.TextLine(title=_(u'Keyword'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

class ITechnique(Interface):
    part = schema.TextLine(title=_(u'Part'), required=False)
    technique = schema.TextLine(title=_(u'Technique'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

class IMaterial(Interface):
    part = schema.TextLine(title=_(u'Part'), required=False)
    material = schema.TextLine(title=_(u'Material'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

class IDimension(Interface):
    part = schema.TextLine(title=_(u'Part'), required=False)
    dimension = schema.TextLine(title=_(u'Dimension'), required=False)
    value = schema.TextLine(title=_(u'Value'), required=False)
    unit = schema.TextLine(title=_(u'Unit'), required=False)
    precision = schema.TextLine(title=_(u'Precision'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

class IPeriod(Interface):
    date_early = schema.TextLine(title=_(u'label_datering_van', default=u'Date (early)'), required=False, default=u" ", missing_value=u" ")
    date_early_precision = schema.TextLine(title=_(u'Precision'), required=False, default=u" ", missing_value=u" ")
    date_late = schema.TextLine(title=_(u'label_date_tot', default=u'Date (late)'), required=False, default=u" ", missing_value=u" ")
    date_late_precision = schema.TextLine(title=_(u'Precision'), required=False, default=u" ", missing_value=u" ")
    period = schema.TextLine(title=_(u'Period'), required=False)

## Production & Dating
class IProduction(Interface):
    maker = schema.TextLine(title=_(u'Maker'), required=False)
    qualifier = schema.TextLine(title=_(u'Qualifier'), required=False)
    role = schema.TextLine(title=_(u'Role'), required=False)
    place = schema.TextLine(title=_(u'Place'), required=False)
    production_notes = schema.Text(title=_(u'Production notes'), required=False)

class ISchool(Interface):
    term = schema.TextLine(title=_(u'School / style'), required=False)

class IFrame(Interface):
    frame = schema.TextLine(title=_(u'Frame'), required=False)
    detail = schema.Text(title=_(u'Detail'), required=False)

## Recommendations/requirements
class IRequirements(Interface):
    requirementsHeld = schema.TextLine(title=_(u'Requirements held'), required=False)
    number = schema.TextLine(title=_(u'Number'), required=False)
    currentFrom = schema.TextLine(title=_(u'Current From'), required=False)
    until = schema.TextLine(title=_(u'Until'), required=False)
    renewalDate = schema.TextLine(title=_(u'Renewal date'), required=False)

## Condition & Conservation Interfaces
class ICompleteness(Interface):
    completeness = schema.TextLine(title=_(u'Completeness'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)
    checked_by = schema.TextLine(title=_(u'Checked by'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)

class ICondition(Interface):
    part = schema.TextLine(title=_(u'Part'), required=False)
    condition = schema.TextLine(title=_(u'Condition'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)
    checked_by = schema.TextLine(title=_(u'Checked by'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)

class IEnvCondition(Interface):
    preservation_form = schema.TextLine(title=_(u'Preservation form'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)
    #date = schema.TextLine(title=_(u'Date'), required=False)

class IConsRequest(Interface):
    treatment = schema.TextLine(title=_(u'Treatment'), required=False)
    requester = schema.TextLine(title=_(u'Requester'), required=False)
    reason = schema.TextLine(title=_(u'Reason'), required=False)
    status = schema.TextLine(title=_(u'Status'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)

class IConsTreatment(Interface):
    treatmentNumber = schema.TextLine(title=_(u'Treatment number'), required=False)
    treatmentMethod = schema.TextLine(title=_(u'Treatment method'), required=False)
    startDate = schema.TextLine(title=_(u'Start date'), required=False)
    endDate = schema.TextLine(title=_(u'End date'), required=False)

class IConsTreatments(Interface):
    treatmentNumber = RelationList(
        title=_(u'Treatment number'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder()
        ),
        required=False
    )
    form.widget('treatmentNumber', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    treatmentMethod = schema.TextLine(title=_(u'Treatment method'), required=False)
    startDate = schema.TextLine(title=_(u'Start date'), required=False)
    endDate = schema.TextLine(title=_(u'End date'), required=False)

## Inscriptions and Markings
class IInscription(Interface):
    type = schema.TextLine(title=_(u'Type'), required=False)
    position = schema.TextLine(title=_(u'Position'),required=False)
    method = schema.TextLine(title=_(u'Method'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)
    creator = schema.TextLine(title=_(u'Creator'), required=False)
    role = schema.TextLine(title=_(u'Role'), required=False)
    content = schema.TextLine(title=_(u'Content'), required=False)
    description = schema.TextLine(title=_(u'Description'), required=False)
    interpretation = schema.TextLine(title=_(u'Interpretation'), required=False)
    language = schema.TextLine(title=_(u'Language'), required=False)
    
    #New field
    translation = schema.TextLine(title=_(u'Translation'), required=False, missing_value="")
    
    script = schema.TextLine(title=_(u'Script'), required=False)
    transliteration = schema.TextLine(title=_(u'Transliteration'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

## Numbers/relationships
class INumbers(Interface):
    type = schema.TextLine(title=_(u'Type'), required=False)
    number = schema.TextLine(title=_(u'Number'), required=False)
    institution = schema.TextLine(title=_(u'Institution'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)

class IParts(Interface):
    parts = RelationList(
        title=_(u'Parts'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='Object')
        ),
        required=False
    )
    form.widget('parts', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    notes = schema.Text(title=_(u'Notes'), required=False)

class IRelatedObject(Interface):
    relatedObject = RelationList(
        title=_(u'Related object'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='Object', navigation_tree_query={'path':{'query':OBJECT_FOLDER}})
        ),
        required=False
    )
    
    #relatedObject = schema.TextLine(title=_(u'Related object'), required=False)
    association = schema.TextLine(title=_(u'Association'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

    

class IDigitalReferences(Interface):
    type = schema.TextLine(title=_(u'Type'), required=False)
    reference = schema.TextLine(title=_(u'Reference'), required=False)
     
## Documentation
class IDocumentationDocumentation(Interface):
    article = schema.TextLine(title=_(u'Article'), required=False)
    #title = schema.TextLine(title=_(u'Title'), required=False)

    titles = RelationList(
        title=_(u'Title'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder()
        ),
        required=False
    )
    form.widget('titles', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    #author = schema.TextLine(title=_(u'Author'), required=False)
    pageMark = schema.TextLine(title=_(u'Page mark'), required=False)
    #shelfMark = schema.TextLine(title=_(u'Shelf mark'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

## Documentation (free) / archive
class IDocumentationFreeText(Interface):
    title = schema.Text(title=_(u'Title'), required=False)

class IArchive(Interface):
    archiveNumber = schema.TextLine(title=_(u'Archive number'), required=False)
    #content = schema.TextLine(title=_(u'Content'), required=False)

class IArchives(Interface):
    archiveNumber = RelationList(
        title=_(u'Archive number'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='Archive', navigation_tree_query={'path':{'query':ARCHIVE_FOLDER}})
        ),
        required=False
    )

## Transport
class IDespatch(Interface):
    date = schema.TextLine(title=_(u'Date'), required=False)
    arrival_date = schema.TextLine(title=_(u'Arrival date'), required=False)
    destination = schema.TextLine(title=_(u'Destination'), required=False)

class IDespatchNumber(Interface):
    """transport_number = RelationList(
        title=_(u'Despatch number'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='ObjectDespatch')
        ),
        required=False
    )"""
    transport_number = schema.TextLine(title=_(u'Despatch number'), required=False)
    despatch_date = schema.TextLine(title=_(u'Despatch date'), required=False)
    delivery_date = schema.TextLine(title=_(u'Delivery date'), required=False)
    destination = schema.TextLine(title=_(u'Destination'), required=False)
    
class IEntryNumber(Interface):
    transport_number = RelationList(
        title=_(u'Transport number'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='ObjectEntry')
        ),
        required=False
    )
    form.widget('transport_number', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    depositor = schema.TextLine(title=_(u'Depositor'), required=False)
    entry_reason = schema.TextLine(title=_(u'Entry reason'), required=False)
    entry_date = schema.TextLine(title=_(u'Entry date'), required=False)
    return_date = schema.TextLine(title=_(u'Return date'), required=False)
    depositor = schema.TextLine(title=_(u'Depositor'), required=False)
    owner = schema.TextLine(title=_(u'Owner'), required=False)

## Reproductions
class IReproduction(Interface):
    reference = schema.TextLine(title=_(u'Reference'), required=False)
    type = schema.TextLine(title=_(u'Type'), required=False)
    format = schema.TextLine(title=_(u'Format'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)
    identifierURL = schema.TextLine(title=_(u'Identifier (URL)'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)
    creator = schema.TextLine(title=_(u'Creator'), required=False)

## Associations
class IAssociatedPersonInstitution(Interface):
    associations = schema.TextLine(title=_(u'Association'), required=False)

    nameType = schema.Choice(title=_(u'Name type'), required=True, vocabulary="collective.object.nametype", default="No value", missing_value=" ")
    
    names = RelationList(
        title=_(u'Name'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution', navigation_tree_query={'path':{'query':PERSON_INSTITUTION_FOLDER}})
        ),
        required=False
    )
    
    startDate = schema.TextLine(title=_(u'Start date'), required=False)
    endDate = schema.TextLine(title=_(u'End date'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

## Associations
class IAssociatedPersonInstitutions(Interface):
    form.widget('associations', AjaxSingleSelectFieldWidget, vocabulary="collective.object.associatedSubjects_association")
    associations = schema.List(
        title=_(u'Association'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )

    nameType = schema.Choice(title=_(u'Name type'), required=True, vocabulary="collective.object.nametype", default="No value", missing_value=" ")
    
    names = RelationList(
        title=_(u'Name'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution')
        ),
        required=False
    )
    form.widget('names', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')
    
    startDate = schema.TextLine(title=_(u'Start date'), required=False)
    endDate = schema.TextLine(title=_(u'End date'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

class IAssociatedPeriod(Interface):
    association = schema.TextLine(title=_(u'Association'), required=False)
    period = schema.TextLine(title=_(u'Period'), required=False)
    startDate = schema.TextLine(title=_(u'Start date'), required=False)
    endDate = schema.TextLine(title=_(u'End date'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

# Value & Insurance
class IValuation(Interface):
    value = schema.TextLine(title=_(u'Value'), required=False)
    curr = schema.TextLine(title=_(u'Curr.'), required=False)
    valuer = schema.TextLine(title=_(u'Valuer'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)
    #reference = schema.TextLine(title=_(u'Reference'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

class IInsurance(Interface):
    #type = schema.Choice(
    #    vocabulary=insurance_type_vocabulary,
    #    title=_(u'Type'),
    #    required=False
    #)
    value = schema.TextLine(title=_(u'Value'), required=False)
    curr = schema.TextLine(title=_(u'Curr.'), required=False)
    valuer = schema.TextLine(title=_(u'Valuer'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)
    policy_number = schema.TextLine(title=_(u'Policy number'), required=False)
    insurance_company = schema.TextLine(title=_(u'Insurance company'), required=False)
    #confirmation_date = schema.TextLine(title=_(u'Confirmation date'), required=False)
    renewal_date = schema.TextLine(title=_(u'Renewal date'), required=False)
    reference = schema.TextLine(title=_(u'Reference'), required=False)
    conditions = schema.TextLine(title=_(u'Conditions'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

# Aquisition
class IFunding(Interface):
    amount = schema.TextLine(title=_(u'Amount'), required=False)
    curr = schema.TextLine(title=_(u'Curr.'), required=False)
    source = schema.TextLine(title=_(u'Source'), required=False)
    provisos = schema.TextLine(title=_(u'Provisos'), required=False)

class IInvoer(Interface):
    name = schema.TextLine(title=_(u'Name'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)
    time = schema.TextLine(title=_(u'management_time', default=u"Time"), required=False)
    source = schema.TextLine(title=_(u'Dataset'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

class IManagementDetails(Interface):
    editName = schema.TextLine(title=_(u'Name'), required=False)
    editDate = schema.TextLine(title=_(u'Date'), required=False)
    editTime = schema.TextLine(title=_(u'management_time', default=u"Time"), required=False)
    editSource = schema.TextLine(title=_(u'Dataset'), required=False)
    editNotes = schema.Text(title=_(u'Notes'), required=False)

class IDocumentation(Interface):
    description = schema.TextLine(title=_(u'label_description', default=u'Description'), required=False)
    reference = schema.TextLine(title=_(u'Reference'), required=False)

# Location
class ICurrentLocation(Interface):
    start_date = schema.TextLine(title=_(u'Start date'), required=False)
    end_date = schema.TextLine(title=_(u'End date'), required=False)
    location_type = schema.TextLine(title=_(u'Location type'), required=False)
    location = schema.TextLine(title=_(u'Location'), required=False)
    fitness = schema.TextLine(title=_(u'Fitness'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

class ILocationChecks(Interface):
    date = schema.TextLine(title=_(u'Date'), required=False)
    checked_by = schema.TextLine(title=_(u'Checked by'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

# Notes
class INotes(Interface):
    notes = schema.Text(title=_(u'Notes'), required=False)

class IFreeFields(Interface):
    date = schema.TextLine(title=_(u'Date'), required=False)
    type = schema.TextLine(title=_(u'Type'), required=False)
    #confidential = schema.TextLine(title=_(u'Confidential'), required=False)

    notesConfidential = schema.Bool(title=_(u'Confidential'), required=False, default=False)
    content = schema.TextLine(title=_(u'Content'), required=False)

# Labels
class ILabel(Interface):
    date = schema.TextLine(title=_(u'Date'), required=False)
    text = schema.Text(title=_(u'Text'), required=False)
    type = schema.TextLine(title=_(u"label_soort_doel", default=u'Type'), required=False, missing_value=" ")

# Iconography
class IIconographyGeneralTheme(Interface):
    term = schema.TextLine(title=_(u'General theme'), required=False)

class IIconographySpecificTheme(Interface):
    term = schema.TextLine(title=_(u'Specific theme'), required=False)

class IIconographyClassificationTheme(Interface):
    term = schema.TextLine(title=_(u'Classification theme'), required=False)
    code = schema.TextLine(title=_(u'Code'), required=False)

class IIconographyContentDescription(Interface):
    part = schema.TextLine(title=_(u'Part'), required=False)
    description = schema.TextLine(title=_(u'Description'), required=False)

class IIconographyContentPersonInstitution(Interface):
    position = schema.TextLine(title=_(u'Position'), required=False)
    #nameType = schema.TextLine(title=_(u'Name type'), required=False)
    nameType = schema.Choice(title=_(u'Name type'), required=True, vocabulary="collective.object.nametype", default="No value", missing_value=" ")

    #name = schema.TextLine(title=_(u'Name'), required=False)
    names = RelationList(
        title=_(u'Name'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution')
        ),
        required=False
    )
    form.widget('names', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')


    notes = schema.Text(title=_(u'Notes'), required=False)

class IIconographyContentPeriodDates(Interface):
    position = schema.TextLine(title=_(u'Position'), required=False)
    
    form.widget('period', AjaxSingleSelectFieldWidget, vocabulary="collective.object.associatedperiods")
    period = schema.List(
        title=_(u'Period'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )

    startDate = schema.TextLine(title=_(u'Start date'), required=False)
    endDate = schema.TextLine(title=_(u'End date'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

class IIconographyContentPeriodDate(Interface):
    position = schema.TextLine(title=_(u'Position'), required=False)
    period = schema.TextLine(title=_(u'Period'), required=False)
    startDate = schema.TextLine(title=_(u'Start date'), required=False)
    endDate = schema.TextLine(title=_(u'End date'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

# Field Collection
class IFieldCollNumber(Interface):
    number = schema.TextLine(title=_(u'Field coll. number'), required=False)

class ICollector(Interface):
    name = schema.TextLine(title=_(u'Collector'), required=False)
    role = schema.TextLine(title=_(u'Role'), required=False)

class IEvent(Interface):
    term = schema.TextLine(title=_(u'Event'), required=False)

class IMethod(Interface):
    term = schema.TextLine(title=_(u'Method'), required=False)

class IPlace(Interface):
    term = schema.TextLine(title=_(u'Place'), required=False)

class IPlaceCode(Interface):
    code = schema.TextLine(title=_(u'Place code'), required=False)
    codeType = schema.TextLine(title=_(u'Code type'), required=False)

class IPlaceFeature(Interface):
    term = schema.TextLine(title=_(u'Place feature'), required=False)

class IFieldCollectionPlace(Interface):
    gridType = schema.TextLine(title=_(u'Grid type'), required=False)
    xCoordinate = schema.TextLine(title=_(u'X co-ordinate'), required=False)
    xAddition = schema.TextLine(title=_(u'Addition'), required=False)
    yCoordinate = schema.TextLine(title=_(u'Y co-ordinate'), required=False)
    yAddition = schema.TextLine(title=_(u'Addition'), required=False)
    precision = schema.TextLine(title=_(u'Precision'), required=False)

class IHabitat(Interface):
    term = schema.TextLine(title=_(u'Habitat'), required=False)

class IStratigraphy(Interface):
    unit = schema.TextLine(title=_(u'Stratigraphy'), required=False)
    type = schema.TextLine(title=_(u'Strat. type'), required=False)

## Exhibitions
class IExhibition(Interface):
    exhibitionName = RelationList(
        title=_(u'Exhibition name'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='Exhibition')
        ),
        required=False
    )
    form.widget('exhibitionName', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    name = schema.TextLine(title=_(u'Exhibition name'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)
    to = schema.TextLine(title=_(u'to'), required=False)
    organiser = schema.TextLine(title=_(u'Organiser'), required=False)
    venue = schema.TextLine(title=_(u'Venue'), required=False)
    place = schema.TextLine(title=_(u'Place'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)
    catObject = schema.TextLine(title=_(u'Cat. no. object'), required=False)


## Loans
class IIncomingLoan(Interface):
    loannumber = RelationList(
        title=_(u'Loan number'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='IncomingLoan')
        ),
        required=False
    )
    form.widget('loannumber', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    loanNumber = schema.TextLine(title=_(u'Loan number'), required=False)
    status = schema.TextLine(title=_(u'Status'), required=False)
    lender = schema.TextLine(title=_(u'Lender'), required=False)
    contact = schema.TextLine(title=_(u'Contact'), required=False)
    requestReason = schema.TextLine(title=_(u'Request reason'), required=False)
    requestPeriod = schema.TextLine(title=_(u'Request period'), required=False)
    requestPeriodTo = schema.TextLine(title=_(u'to'), required=False)
    contractPeriod = schema.TextLine(title=_(u'Contract period'), required=False)
    contractPeriodTo = schema.TextLine(title=_(u'to'), required=False)

class IArchiveNumber(Interface):
    number = RelationList(
        title=_(u'Archive number'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='Archive')
        ),
        required=False
    )
    form.widget('number', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')


class IOutgoingLoan(Interface):
    loannumber = RelationList(
        title=_(u'Loan number'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='OutgoingLoan')
        ),
        required=False
    )
    form.widget('loannumber', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    status = schema.TextLine(title=_(u'Status'), required=False)
    requester = schema.TextLine(title=_(u'Requester'), required=False)
    contact = schema.TextLine(title=_(u'Contact'), required=False)
    requestReason = schema.TextLine(title=_(u'Request reason'), required=False)
    requestPeriod = schema.TextLine(title=_(u'Request period'), required=False)
    requestPeriodTo = schema.TextLine(title=_(u'to'), required=False)
    contractPeriod = schema.TextLine(title=_(u'Contract period'), required=False)
    contractPeriodTo = schema.TextLine(title=_(u'to'), required=False)



