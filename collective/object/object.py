#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Zope dependencies
#
from zope import schema
from zope.interface import invariant, Invalid, Interface, implements
from zope.interface import alsoProvides
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.fieldproperty import FieldProperty
from zope.component import getMultiAdapter

#
# Plone dependencies
#
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.supermodel import model
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

#
# z3c.forms dependencies
#
from z3c.form import group, field
from z3c.form.form import extends
from z3c.form.browser.textlines import TextLinesFieldWidget
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from z3c.relationfield.interfaces import IRelationList

try:
    from z3c.form.browser.textlines import TextLinesFieldWidget
except ImportError:
    from plone.z3cform.textlines.textlines import TextLinesFieldWidget

from collective.z3cform.datagridfield.interfaces import IDataGridField

#
# Plone app widget dependencies
#
from plone.app.widgets.dx import AjaxSelectFieldWidget, AjaxSelectWidget, SelectWidget, DatetimeFieldWidget, IAjaxSelectWidget
from plone.formwidget.autocomplete import AutocompleteFieldWidget


#
# DataGridFields dependencies
#
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from collective.z3cform.datagridfield.blockdatagridfield import BlockDataGridFieldFactory


# # # # # # # # # # # # # # # 
# Dexterity imports         # 
# # # # # # # # # # # # # # # 
from five import grok
from collective import dexteritytextindexer
from plone.dexterity.browser.view import DefaultView
from plone.dexterity.content import Container
from plone.dexterity.browser import add, edit


# # # # # # # # # # # # # # # # 
# !Object specific imports!   #
# # # # # # # # # # # # # # # #
from collective.object import MessageFactory as _
from .utils.vocabularies import *
from .utils.interfaces import *
from .utils.views import *
from .utils.source import ObjPathSourceBinder
from .utils.variables import *
from .utils.widgets import AjaxSingleSelectFieldWidget

from plone.formwidget.contenttree import ObjPathSourceBinder as sb

# # # # # # # # # #
# # # # # # # # # #
# Object schema   #
# # # # # # # # # #
# # # # # # # # # #



class IObject(form.Schema):

    priref = schema.TextLine(
        title=_(u'priref'), 
        required=False
    )

    # Vocabularies
    identification_objectName_objectname = ListField(title=_(u'Object name'),
        value_type=DictRow(title=_(u'Object name'), schema=IObjectname),
        required=False)
    form.widget(identification_objectName_objectname=DataGridFieldFactory)
    dexteritytextindexer.searchable('identification_objectName_objectname')

    identification_objectName_category = schema.List(
        title=_(u'Object Category'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    form.widget('identification_objectName_category', AjaxSelectFieldWidget,  vocabulary="collective.object.objectCategory")

    identification_identification_collections = schema.List(
        title=_(u'Collection'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    form.widget('identification_identification_collections', AjaxSelectFieldWidget,  vocabulary="collective.object.collection")

    # Production
    productionDating_productionDating = ListField(title=_(u'Production & Dating'),
        value_type=DictRow(title=_(u'Production & Dating'), schema=IProductiondating),
        required=False)
    form.widget(productionDating_productionDating=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('productionDating_productionDating')

    productionDating_production_schoolstyle = ListField(title=_(u'School / style'),
        value_type=DictRow(title=_(u'School / style'), schema=ISchoolStyle),
        required=False)
    form.widget(productionDating_production_schoolstyle=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('productionDating_production_schoolStyle')

    productionDating_production_schoolStyles = schema.List(
        title=_(u'School / style'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    form.widget('productionDating_production_schoolStyles', AjaxSelectFieldWidget,  vocabulary="collective.object.productionSchoolStyle")

    productionDating_production_periods = schema.List(
        title=_(u'Period'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    form.widget('productionDating_production_periods', AjaxSelectFieldWidget,  vocabulary="collective.object.periods")

    # Physical characteristics
    physicalCharacteristics_technique = ListField(title=_(u'Techniques'),
        value_type=DictRow(title=_(u'Techniques'), schema=ITechniques),
        required=False)
    form.widget(physicalCharacteristics_technique=DataGridFieldFactory)

    physicalCharacteristics_material = ListField(title=_(u'Materials'),
        value_type=DictRow(title=_(u'Materials'), schema=IMaterials),
        required=False)
    form.widget(physicalCharacteristics_material=DataGridFieldFactory)

    physicalCharacteristics_dimension = ListField(title=_(u'Dimensions'),
        value_type=DictRow(title=_(u'Dimensions'), schema=IDimensions),
        required=False)
    form.widget(physicalCharacteristics_dimension=DataGridFieldFactory)

    # Iconography
    # General search criteria
    iconography_generalSearchCriteria_generalThemes = ListField(title=_(u'General theme'),
        value_type=DictRow(title=_(u'General theme'), schema=IIconographyGeneralThemes),
        required=False)
    form.widget(iconography_generalSearchCriteria_generalThemes=DataGridFieldFactory)
    dexteritytextindexer.searchable('iconography_generalSearchCriteria_generalTheme')

    iconography_generalSearchCriteria_specificThemes = ListField(title=_(u'Specific theme'),
        value_type=DictRow(title=_(u'Specific theme'), schema=IIconographySpecificThemes),
        required=False)
    form.widget(iconography_generalSearchCriteria_specificThemes=DataGridFieldFactory)
    dexteritytextindexer.searchable('iconography_generalSearchCriteria_specificThemes')

    # Content subject
    iconography_contentSubjects = ListField(title=_(u'Content subject'),
        value_type=DictRow(title=_(u'Content subject'), schema=IIconographyContentSubjects),
        required=False)
    form.widget(iconography_contentSubjects=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('iconography_contentSubjects')

    # Inscriptions and markings
    inscriptionsMarkings_inscriptionsAndMarkings = ListField(title=_(u'Inscriptions and markings'),
        value_type=DictRow(title=_(u'Inscriptions and markings'), schema=IInscriptions),
        required=False)
    form.widget(inscriptionsMarkings_inscriptionsAndMarkings=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('inscriptionsMarkings_inscriptionsAndMarkings')

    # Associations
    associations_associatedSubjects = ListField(title=_(u'Associated subject'),
        value_type=DictRow(title=_(u'Associated subject'), schema=IAssociatedSubjects),
        required=False)
    form.widget(associations_associatedSubjects=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('associations_associatedSubjects')

    associations_associatedPeriods = ListField(title=_(u'Associated period'),
        value_type=DictRow(title=_(u'Associated period'), schema=IAssociatedPeriods),
        required=False)
    form.widget(associations_associatedPeriods=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('associations_associatedPeriods')

    # Value & Insurance
    valueInsurance_valuations = ListField(title=_(u'Valuation'),
        value_type=DictRow(title=_(u'Valuation'), schema=IValuations),
        required=False)
    form.widget(valueInsurance_valuations=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('valueInsurance_valuations')

    # Condition & Conservation 
    conditionConservation_conditions = ListField(title=_(u'Condition'),
        value_type=DictRow(title=_(u'Condition'), schema=IConditions),
        required=False)
    form.widget(conditionConservation_conditions=DataGridFieldFactory)
    dexteritytextindexer.searchable('conditionConservation_conditions')

    conditionConservation_preservationForm = ListField(title=_(u'Preservation form'),
        value_type=DictRow(title=_(u'Preservation form'), schema=IEnvConditions),
        required=False)
    form.widget(conditionConservation_preservationForm=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('conditionConservation_preservationForm')


    # Aquisition
    acquisition_methods = schema.List(
        title=_(u'Method'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    form.widget('acquisition_methods', AjaxSelectFieldWidget,  vocabulary="collective.object.aquisitionmethod")

    acquisition_places = schema.List(
        title=_(u'label_acquisition_place', default=u"Place"),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    form.widget('acquisition_places', AjaxSelectFieldWidget,  vocabulary="collective.object.aquisitionplace")

    acquisition_costs_offer_price_currency = schema.List(
        title=_(u'Curr.'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    form.widget('acquisition_costs_offer_price_currency', AjaxSelectFieldWidget,  vocabulary="collective.object.currency")

    acquisition_costs_purchase_price_currency = schema.List(
        title=_(u'Curr.'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    form.widget('acquisition_costs_purchase_price_currency', AjaxSelectFieldWidget,  vocabulary="collective.object.currency")

    # Funding *
    acquisition_fundings = ListField(title=_(u'Funding'),
        value_type=DictRow(title=_(u'Funding'), schema=IFundings),
        required=False)
    form.widget(acquisition_fundings=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('acquisition_fundings')

    # Disposal
    disposal_finance_currency = schema.List(
        title=_(u'Curr.'),
        required=False,
        value_type=schema.TextLine()
    )
    form.widget('disposal_finance_currency', AjaxSelectFieldWidget,  vocabulary="collective.object.currency")

    # Ownership history
    ownershipHistory_history_exchangeMethod = schema.List(
        title=_(u'Exchange method'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    form.widget('ownershipHistory_history_exchangeMethod', AjaxSelectFieldWidget,  vocabulary="collective.object.exchangemethod")

    ownershipHistory_history_place = schema.List(
        title=_(u'label_plaats', default=u'Place'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    form.widget('ownershipHistory_history_place', AjaxSelectFieldWidget,  vocabulary="collective.object.historyplace")


    # Location
    location_normalLocation_normalLocation = schema.List(
        title=_(u'Normal location'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    form.widget('location_normalLocation_normalLocation', AjaxSingleSelectFieldWidget,  vocabulary="collective.object.location")

    # Current location
    location_currentLocation = ListField(title=_(u'Current location'),
        value_type=DictRow(title=_(u'Current location'), schema=ICurrentLocations),
        required=False)
    form.widget(location_currentLocation=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('location_currentLocation')

    # Field collection
    fieldCollection_fieldCollection_collectors = ListField(title=_(u'Collector'),
        value_type=DictRow(title=_(u'Collector'), schema=ICollectionCollectors),
        required=False)
    form.widget(fieldCollection_fieldCollection_collectors=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('fieldCollection_fieldCollection_collectors')

    fieldCollection_fieldCollection_events = schema.List(
        title=_(u'Event'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    form.widget('fieldCollection_fieldCollection_events', AjaxSelectFieldWidget,  vocabulary="collective.object.events")


    fieldCollection_fieldCollection_methods = schema.List(
        title=_(u'Method'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    form.widget('fieldCollection_fieldCollection_methods', AjaxSelectFieldWidget,  vocabulary="collective.object.fieldCollection_method")

    fieldCollection_fieldCollection_places = schema.List(
        title=_(u'Place'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    form.widget('fieldCollection_fieldCollection_places', AjaxSelectFieldWidget,  vocabulary="collective.object.fieldCollection_place")

    fieldCollection_fieldCollection_placeFeatures = schema.List(
        title=_(u'Place feature'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    form.widget('fieldCollection_fieldCollection_placeFeatures', AjaxSelectFieldWidget,  vocabulary="collective.object.fieldCollection_placeFeature")

    fieldCollection_fieldCollection_placeCodes = ListField(title=_(u'Place code'),
        value_type=DictRow(title=_(u'Place code'), schema=IPlaceCodes),
        required=False)
    form.widget(fieldCollection_fieldCollection_placeCodes=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('fieldCollection_fieldCollection_placeCodes')

    fieldCollection_habitatStratigraphy_stratigrafie = ListField(title=_(u'Stratigraphy'),
        value_type=DictRow(title=_(u'Stratigraphy'), schema=IStratigrafie),
        required=False)
    form.widget(fieldCollection_habitatStratigraphy_stratigrafie=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('fieldCollection_habitatStratigraphy_stratigrafie')


    # Numbers / relations
    numbersRelationships_relationshipsWithOtherObjects_relatedObjects = ListField(title=_(u'Related object'),
        value_type=DictRow(title=_(u'Related object'), schema=IRelatedObjects),
        required=False)
    form.widget(numbersRelationships_relationshipsWithOtherObjects_relatedObjects=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('numbersRelationships_relationshipsWithOtherObjects_relatedObjects')


    text = RichText(
        title=_(u"Body"),
        required=False
    )

    # # # # # # # # # # # # # # 
    # Identification fieldset #
    # # # # # # # # # # # # # # 
    
    model.fieldset('identification', label=_(u'Identification'), 
        fields=['identification_identification_institutionName', 'identification_identification_institutionNames', 'identification_identification_institutionCode', 'identification_identification_administrativeName', 'identification_identification_collection', 'identification_identification_objectNumber',
                'identification_identification_recType', 'identification_identification_part', 'identification_identification_totNumber', 'identification_identification_copyNumber', 
                'identification_identification_edition', 'identification_identification_distinguishFeatures', 'identification_taxonomy_determiners',
                'identification_objectName_objectCategory', 'identification_objectName_objectName', 'identification_objectName_otherName', 'identification_titleDescription_notes',
                'identification_titleDescription_translatedTitle', 'identification_titleDescription_language', 'identification_titleDescription_describer', 'identification_titleDescription_date',
                'identification_titleDescription_titleDate', 'identification_taxonomy', 'identification_taxonomy_determiner', 'identification_taxonomy_objectStatus', 'identification_taxonomy_objectstatus', 'identification_taxonomy_notes']
    )

    # Identification #
    identification_identification_institutionName = schema.TextLine(
        title=_(u'Institution name'), 
        required=False,
        description=_(u"Institution name<br><br>The name of the institution responsible for managing the object.<br><br>Enter the common name of your institution, possibly shortened and with a place name. This field is especially relevant if object descriptions are used by third parties.<br><br> Examples:<br>National Museums of Scotland<br>NMS<br>REME<br>Met")
    )
    dexteritytextindexer.searchable('identification_identification_institutionName')

    identification_identification_institutionNames = RelationList(
        title=_(u'Institution name'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution', navigation_tree_query={'path':{'query':PERSON_INSTITUTION_FOLDER}})
        ),
        required=False
    )

    identification_identification_institutionCode = schema.TextLine(
        title=_(u'Institution code'), 
        required=False
    )
    dexteritytextindexer.searchable('identification_identification_institutionCode')

    identification_identification_administrativeName = schema.TextLine(
        title=_(u'Administrative name'), 
        required=False,
        default=u"",
        missing_value=u"",
        description=_(u"Administration name<br><br>The name of the department responsible for the object itself and for the documentation about the object.<br><br>Examples:<br>Textiles<br>Geology<br>Glass and ceramics")
    )
    dexteritytextindexer.searchable('identification_identification_administrativeName')

    identification_identification_collection = ListField(title=_(u'Collection'),
        value_type=DictRow(title=_(u'Collection'), schema=ICollection),
        required=False,
        description=_(u"Collection<br><br>If this object is part of a specific collection within the overall museum collection, use this field to enter its name.<br><br>Examples:<br>manuscripts<br>Muller"))
    form.widget(identification_identification_collection=DataGridFieldFactory)

    identification_identification_objectNumber = schema.TextLine(
        title=_(u'Object number'),
        required=False
    )
    dexteritytextindexer.searchable('identification_identification_objectNumber')

    identification_identification_recType = schema.TextLine(
        title=_(u'Rec. type'),
        required=False
    )
    dexteritytextindexer.searchable('identification_identification_recType')

    identification_identification_part = schema.TextLine(
        title=_(u'Part'),
        required=False
    )
    dexteritytextindexer.searchable('identification_identification_part')

    identification_identification_totNumber = schema.TextLine(
        title=_(u'Tot. Number'),
        required=False
    )
    dexteritytextindexer.searchable('identification_identification_totNumber')

    identification_identification_copyNumber = schema.TextLine(
        title=_(u'Copy number'),
        required=False
    )
    dexteritytextindexer.searchable('identification_identification_copyNumber')

    identification_identification_edition = schema.TextLine(
        title=_(u'Edition'),
        required=False
    )
    dexteritytextindexer.searchable('identification_identification_edition')

    identification_identification_distinguishFeatures = schema.TextLine(
        title=_(u'Distinguish features'),
        required=False
    )
    dexteritytextindexer.searchable('identification_identification_distinguishFeatures')

    # Object name #
    identification_objectName_objectCategory = ListField(title=_(u'Object Category'),
        value_type=DictRow(title=_(u'Object Category'), schema=IObjectCategory),
        required=False)
    form.widget(identification_objectName_objectCategory=DataGridFieldFactory)
    dexteritytextindexer.searchable('identification_objectName_objectCategory')

    
    identification_objectName_objectName = ListField(title=_(u'Object name'),
        value_type=DictRow(title=_(u'Object name'), schema=IObjectName),
        required=False)
    form.widget(identification_objectName_objectName=DataGridFieldFactory)
    dexteritytextindexer.searchable('identification_objectName_objectName')

    identification_objectName_otherName = ListField(title=_(u'Other name'),
        value_type=DictRow(title=_(u'Other name'), schema=IOtherName),
        required=False)
    form.widget(identification_objectName_otherName=DataGridFieldFactory)
    dexteritytextindexer.searchable('identification_objectName_otherName')

    # Title and description
    identification_titleDescription_notes = schema.TextLine(
        title=_(u'Notes'),
        required=False
    )
    dexteritytextindexer.searchable('identification_titleDescription_notes')

    identification_titleDescription_translatedTitle = schema.TextLine(
        title=_(u'Translated title'),
        required=False
    )
    dexteritytextindexer.searchable('identification_titleDescription_translatedTitle')

    identification_titleDescription_language = schema.TextLine(
        title=_(u'Language'),
        required=False
    )
    dexteritytextindexer.searchable('identification_titleDescription_language')

    identification_titleDescription_describer = schema.TextLine(
        title=_(u'Describer'),
        required=False
    )
    dexteritytextindexer.searchable('identification_titleDescription_describer')

    identification_titleDescription_date = schema.TextLine(
        title=_(u'Date'),
        required=False
    )
    dexteritytextindexer.searchable('identification_titleDescription_date')

    identification_titleDescription_titleDate = schema.TextLine(
        title=_(u'Date'),
        required=False
    )
    dexteritytextindexer.searchable('identification_titleDescription_titleDate')
    #form.widget(identification_titleDescription_titleDate=DatetimeFieldWidget)

    # Taxonomy
    identification_taxonomy = ListField(title=_(u'Taxonomy'),
        value_type=DictRow(title=_(u'Taxonomy'), schema=ITaxonomy),
        required=False)
    form.widget(identification_taxonomy=DataGridFieldFactory)
    dexteritytextindexer.searchable('identification_taxonomy')

    identification_taxonomy_determiner = ListField(title=_(u'Determiner'),
        value_type=DictRow(title=_(u'Determiner'), schema=IDeterminer),
        required=False)
    form.widget(identification_taxonomy_determiner=DataGridFieldFactory)
    dexteritytextindexer.searchable('identification_taxonomy_determiner')

    identification_taxonomy_determiners = ListField(title=_(u'Determiner'),
        value_type=DictRow(title=_(u'Determiner'), schema=IDeterminers),
        required=False)
    form.widget(identification_taxonomy_determiners=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('identification_taxonomy_determiners')

    identification_taxonomy_objectStatus = schema.TextLine(
        title=_(u'Object status'),
        required=False
    )
    dexteritytextindexer.searchable('identification_taxonomy_objectStatus')

    identification_taxonomy_objectstatus = schema.Choice(
        title=_(u'Object status'),
        required=True,
        vocabulary="collective.object.objectstatus",
        default="No value"
    )
    dexteritytextindexer.searchable('identification_taxonomy_objectstatus')

    identification_taxonomy_notes = ListField(title=_(u'Notes'),
        value_type=DictRow(title=_(u'Notes'), schema=INotes),
        required=False)
    form.widget(identification_taxonomy_notes=DataGridFieldFactory)

    # # # # # # # # # # # # # # # # #
    # Production & Dating           #
    # # # # # # # # # # # # # # # # #

    model.fieldset('production_dating', label=_(u'Production & Dating'), 
        fields=['productionDating_production', 'productionDating_production_productionReason', 'productionDating_production_schoolStyle',
                'productionDating_dating_period', 'productionDating_dating_notes']
    )

    productionDating_production = ListField(title=_(u'Production & Dating'),
        value_type=DictRow(title=_(u'Production & Dating'), schema=IProduction),
        required=False)
    form.widget(productionDating_production=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('productionDating_production')

    productionDating_production_productionReason = schema.Text(
        title=_(u'Production reason'),
        required=False
    )
    dexteritytextindexer.searchable('productionDating_production_productionReason')

    productionDating_production_schoolStyle = ListField(title=_(u'School / style'),
        value_type=DictRow(title=_(u'School / style'), schema=ISchool),
        required=False)
    form.widget(productionDating_production_schoolStyle=DataGridFieldFactory)
    dexteritytextindexer.searchable('productionDating_production_schoolStyle')

    # Dating #
    productionDating_dating_period = ListField(title=_(u'Period'),
        value_type=DictRow(title=_(u'Period'), schema=IPeriod),
        required=False)
    form.widget(productionDating_dating_period=DataGridFieldFactory)
    dexteritytextindexer.searchable('productionDating_dating_period')



    productionDating_dating_notes = ListField(title=_(u'Notes'),
        value_type=DictRow(title=_(u'Notes'), schema=INotes),
        required=False)
    form.widget(productionDating_dating_notes=DataGridFieldFactory)
    dexteritytextindexer.searchable('productionDating_dating_notes')


    # # # # # # # # # # # # # # # # #
    # Physical Characteristics      #
    # # # # # # # # # # # # # # # # #

    model.fieldset('physical_characteristics', label=_(u'Physical Characteristics'), 
        fields=['physicalCharacteristics_physicalDescription_description', 'physicalCharacteristics_keywords',
                'physicalCharacteristics_techniques', 'physicalCharacteristics_materials', 'physicalCharacteristics_dimensions',
                'physicalCharacteristics_frame']
    )

    # Physical Description
    physicalCharacteristics_physicalDescription_description = schema.Text(
        title=_(u'Description'),
        required=False
    )
    dexteritytextindexer.searchable('physicalCharacteristics_physicalDescription_description')

    # Keywords #
    physicalCharacteristics_keywords = ListField(title=_(u'Keywords'),
        value_type=DictRow(title=_(u'Keywords'), schema=IKeyword),
        required=False)
    form.widget(physicalCharacteristics_keywords=DataGridFieldFactory)

    # Techniques #
    physicalCharacteristics_techniques = ListField(title=_(u'Techniques'),
        value_type=DictRow(title=_(u'Techniques'), schema=ITechnique),
        required=False)
    form.widget(physicalCharacteristics_techniques=DataGridFieldFactory)

    # Materials #
    physicalCharacteristics_materials = ListField(title=_(u'Materials'),
        value_type=DictRow(title=_(u'Materials'), schema=IMaterial),
        required=False)
    form.widget(physicalCharacteristics_materials=DataGridFieldFactory)

    # Dimensions #
    physicalCharacteristics_dimensions = ListField(title=_(u'Dimensions'),
        value_type=DictRow(title=_(u'Dimensions'), schema=IDimension),
        required=False)
    form.widget(physicalCharacteristics_dimensions=DataGridFieldFactory)

    # Frame #
    physicalCharacteristics_frame = ListField(title=_(u'Frame'),
        value_type=DictRow(title=_(u'Frame'), schema=IFrame),
        required=False)
    form.widget(physicalCharacteristics_frame=DataGridFieldFactory)

    # # # # # # # # # #
    # Iconography     #
    # # # # # # # # # #

    model.fieldset('iconography', label=_(u'Iconography'), 
        fields=['iconography_generalSearchCriteria_generalTheme', 'iconography_generalSearchCriteria_specificTheme',
                'iconography_generalSearchCriteria_classificationTheme', 'iconography_contentDescription',
                'iconography_contentPersonInstitution', 'iconography_contentSubject', 'iconography_contentPeriodDate',
                'iconography_iconographySource_sourceGeneral', 'iconography_iconographySource_sourceSpecific',
                'iconography_iconographySource_sourceObjectNumber']
    )

    # General search criteria
    iconography_generalSearchCriteria_generalTheme = ListField(title=_(u'General theme'),
        value_type=DictRow(title=_(u'General theme'), schema=IIconographyGeneralTheme),
        required=False)
    form.widget(iconography_generalSearchCriteria_generalTheme=DataGridFieldFactory)
    dexteritytextindexer.searchable('iconography_generalSearchCriteria_generalTheme')

    iconography_generalSearchCriteria_specificTheme = ListField(title=_(u'Specific theme'),
        value_type=DictRow(title=_(u'Specific theme'), schema=IIconographySpecificTheme),
        required=False)
    form.widget(iconography_generalSearchCriteria_specificTheme=DataGridFieldFactory)
    dexteritytextindexer.searchable('iconography_generalSearchCriteria_specificTheme')

    iconography_generalSearchCriteria_classificationTheme = ListField(title=_(u'Classification theme'),
        value_type=DictRow(title=_(u'Classification theme'), schema=IIconographyClassificationTheme),
        required=False)
    form.widget(iconography_generalSearchCriteria_classificationTheme=DataGridFieldFactory)
    dexteritytextindexer.searchable('iconography_generalSearchCriteria_classificationTheme')

    # Content description
    iconography_contentDescription = ListField(title=_(u'Content description'),
        value_type=DictRow(title=_(u'Content description'), schema=IIconographyContentDescription),
        required=False)
    form.widget(iconography_contentDescription=DataGridFieldFactory)
    dexteritytextindexer.searchable('iconography_contentDescription')

    # Content person/institution
    iconography_contentPersonInstitution = ListField(title=_(u'Content person/institution'),
        value_type=DictRow(title=_(u'Content person/institution'), schema=IIconographyContentPersonInstitution),
        required=False)
    form.widget(iconography_contentPersonInstitution=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('iconography_contentPersonInstitution')

    # Content subject
    iconography_contentSubject = ListField(title=_(u'Content subject'),
        value_type=DictRow(title=_(u'Content subject'), schema=IIconographyContentSubject),
        required=False)
    form.widget(iconography_contentSubject=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('iconography_contentSubject')

    # Content period/date
    iconography_contentPeriodDate = ListField(title=_(u'Content period/date'),
        value_type=DictRow(title=_(u'Content period/date'), schema=IIconographyContentPeriodDate),
        required=False)
    form.widget(iconography_contentPeriodDate=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('iconography_contentPeriodDate')

    # Iconography source
    iconography_iconographySource_sourceGeneral = schema.TextLine(
        title=_(u'Source general'),
        required=False
    )
    dexteritytextindexer.searchable('iconography_iconographySource_sourceGeneral')

    iconography_iconographySource_sourceSpecific = schema.TextLine(
        title=_(u'Source specific'),
        required=False
    )
    dexteritytextindexer.searchable('iconography_iconographySource_sourceSpecific')

    iconography_iconographySource_sourceObjectNumber = schema.TextLine(
        title=_(u'Source object number'),
        required=False
    )
    dexteritytextindexer.searchable('iconography_iconographySource_sourceObjectNumber')

    # # # # # # # # # # # # # # #
    # Inscriptions & Markings   #
    # # # # # # # # # # # # # # #

    model.fieldset('inscriptions_markings', label=_(u'Inscriptions and markings'), 
        fields=['inscriptionsMarkings_inscriptionsMarkings']
    )

    inscriptionsMarkings_inscriptionsMarkings = ListField(title=_(u'Inscriptions and markings'),
        value_type=DictRow(title=_(u'Inscriptions and markings'), schema=IInscription),
        required=False)
    form.widget(inscriptionsMarkings_inscriptionsMarkings=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('inscriptionsMarkings_inscriptionsMarkings')


    # # # # # # # # #
    # Associations  #      
    # # # # # # # # # 
    model.fieldset('associations', label=_(u'Associations'), 
        fields=['associations_associatedPersonInstitution', 'associations_associatedSubject',
                'associations_associatedPeriod']
    )

    associations_associatedPersonInstitution = ListField(title=_(u'Associated person/institution'),
        value_type=DictRow(title=_(u'Associated person/institution'), schema=IAssociatedPersonInstitution),
        required=False)
    form.widget(associations_associatedPersonInstitution=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('associations_associatedPersonInstitution')

    associations_associatedSubject = ListField(title=_(u'Associated subject'),
        value_type=DictRow(title=_(u'Associated subject'), schema=IAssociatedSubject),
        required=False)
    form.widget(associations_associatedSubject=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('associations_associatedSubject')

    associations_associatedPeriod = ListField(title=_(u'Associated period'),
        value_type=DictRow(title=_(u'Associated period'), schema=IAssociatedPeriod),
        required=False)
    form.widget(associations_associatedPeriod=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('associations_associatedPeriod')


    # # # # # # # # # # # # # 
    # Numbers/relationships #
    # # # # # # # # # # # # # 
    model.fieldset('numbers_relationships', label=_(u'Numbers/relationships'), 
        fields=['numbersRelationships_numbers', 'numbersRelationships_relationshipsWithOtherObjects_partOf',
                'numbersRelationships_relationshipsWithOtherObjects_notes', 'numbersRelationships_relationshipsWithOtherObjects_parts',
                'numbersRelationships_relationshipsWithOtherObjects_relatedObject',
                'numbersRelationships_digitalReferences', 'documentationFreeArchive_archives']
    )

    # Numbers
    numbersRelationships_numbers = ListField(title=_(u'Numbers'),
        value_type=DictRow(title=_(u'Numbers'), schema=INumbers),
        required=False)
    form.widget(numbersRelationships_numbers=DataGridFieldFactory)
    dexteritytextindexer.searchable('numbersRelationships_numbers')

    # Relationships with other objects
    numbersRelationships_relationshipsWithOtherObjects_partOf = RelationList(
        title=_(u'Part of'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='Object', navigation_tree_query={'path':{'query':OBJECT_FOLDER}})
        ),
        required=False
    )
    
    numbersRelationships_relationshipsWithOtherObjects_notes = schema.TextLine(
        title=_(u'Notes'),
        required=False
    )
    dexteritytextindexer.searchable('numbersRelationships_relationshipsWithOtherObjects_notes')

    numbersRelationships_relationshipsWithOtherObjects_parts = ListField(title=_(u'Parts'),
        value_type=DictRow(title=_(u'Parts'), schema=IParts),
        required=False)
    form.widget(numbersRelationships_relationshipsWithOtherObjects_parts=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('numbersRelationships_relationshipsWithOtherObjects_parts')

    numbersRelationships_relationshipsWithOtherObjects_relatedObject = ListField(title=_(u'Related object'),
        value_type=DictRow(title=_(u'Related object'), schema=IRelatedObject),
        required=False)
    form.widget(numbersRelationships_relationshipsWithOtherObjects_relatedObject=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('numbersRelationships_relationshipsWithOtherObjects_relatedObject')

    # Digital references
    numbersRelationships_digitalReferences = ListField(title=_(u'Digital references'),
        value_type=DictRow(title=_(u'Digital references'), schema=IDigitalReferences),
        required=False)
    form.widget(numbersRelationships_digitalReferences=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('numbersRelationships_digitalReferences')

    # # # # # # # # # #
    # Documentation   #
    # # # # # # # # # #
    model.fieldset('documentation', label=_(u'Documentation'), 
        fields=['documentation_documentation']
    )

    documentation_documentation = ListField(title=_(u'Documentation'),
        value_type=DictRow(title=_(u'Documentation'), schema=IDocumentationDocumentation),
        required=False)
    form.widget(documentation_documentation=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('documentation_documentation')

    # # # # # # # # # # # # # # # # # # #
    # Documentation (free) / archive    #
    # # # # # # # # # # # # # # # # # # #

    model.fieldset('documentation_free_archive', label=_(u'Documentation (free) / archive'), 
        fields=['documentationFreeArchive_documentationFreeText', 'documentationFreeArchive_archive', 'documentationFreeArchive_archives']
    )

    documentationFreeArchive_documentationFreeText = ListField(title=_(u'Documentation (free text)'),
        value_type=DictRow(title=_(u'Documentation (free text)'), schema=IDocumentationFreeText),
        required=False)
    form.widget(documentationFreeArchive_documentationFreeText=DataGridFieldFactory)
    dexteritytextindexer.searchable('documentationFreeArchive_documentationFreeText')

    documentationFreeArchive_archive = ListField(title=_(u'Archive'),
        value_type=DictRow(title=_(u'Archive'), schema=IArchive),
        required=False)
    form.widget(documentationFreeArchive_archive=DataGridFieldFactory)
    dexteritytextindexer.searchable('documentationFreeArchive_archive')

    documentationFreeArchive_archives = RelationList(
        title=_(u'Archive number'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='Archive', navigation_tree_query={'path':{'query':ARCHIVE_FOLDER}})
        ),
        required=False
    )

    # # # # # # # # # # # # # # #
    # Condition & Conservation  #
    # # # # # # # # # # # # # # #

    model.fieldset('condition_conservation', label=_(u'Condition & Conservation'), 
        fields=['conditionConservation_priority', 'conditionConservation_next_condition_check', 'conditionConservation_date',
                'conditionConservation_completeness', 'conditionConservation_condition', 'conditionConservation_enviromental_condition', 'conditionConservation_conservation_request', 
                'conditionConservation_recommendations_display', 'conditionConservation_conservationTreatment',
                'conditionConservation_recommendations_environment', 'conditionConservation_recommendations_handling',
                'conditionConservation_recommendations_packing', 'conditionConservation_recommendations_security',
                'conditionConservation_recommendations_specialRequirements', 'conditionConservation_conservationTreatments',
                'conditionConservation_recommendations_storage', ]
    )


    # Conservation treatment

    # Choice field
    conditionConservation_priority = schema.Choice(
        vocabulary=priority_vocabulary,
        title=_(u'Priority'),
        required=False
    )
    dexteritytextindexer.searchable('conditionConservation_priority')

    conditionConservation_next_condition_check = schema.TextLine(
        title=_(u'Next condition check'),
        required=False
    )
    dexteritytextindexer.searchable('conditionConservation_next_condition_check')

    conditionConservation_date = schema.TextLine(
        title=_(u'Date'),
        required=False
    )
    dexteritytextindexer.searchable('conditionConservation_date')

    # Condition*
    conditionConservation_condition = ListField(title=_(u'Condition'),
        value_type=DictRow(title=_(u'Condition'), schema=ICondition),
        required=False)
    form.widget(conditionConservation_condition=DataGridFieldFactory)
    dexteritytextindexer.searchable('conditionConservation_condition')

    # Completeness*
    conditionConservation_completeness = ListField(title=_(u'Completeness'),
        value_type=DictRow(title=_(u'Completeness'), schema=ICompleteness),
        required=False)
    form.widget(conditionConservation_completeness=DataGridFieldFactory)
    dexteritytextindexer.searchable('conditionConservation_completeness')

    # Enviromental condition*
    conditionConservation_enviromental_condition = ListField(title=_(u'Enviromental condition'),
        value_type=DictRow(title=_(u'Enviromental condition'), schema=IEnvCondition),
        required=False)
    form.widget(conditionConservation_enviromental_condition=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('conditionConservation_enviromental_condition')

    # Conservation request*
    conditionConservation_conservation_request = ListField(title=_(u'Conservation request'),
        value_type=DictRow(title=_(u'Conservation request'), schema=IConsRequest),
        required=False)
    form.widget(conditionConservation_conservation_request=DataGridFieldFactory)
    dexteritytextindexer.searchable('conditionConservation_conservation_request')

    #Conservation treatment
    conditionConservation_conservationTreatment = ListField(title=_(u'Conservation treatment'),
        value_type=DictRow(title=_(u'Conservation treatment'), schema=IConsTreatment),
        required=False)
    form.widget(conditionConservation_conservationTreatment=DataGridFieldFactory)
    dexteritytextindexer.searchable('conditionConservation_conservationTreatment')

    conditionConservation_conservationTreatments = ListField(title=_(u'Conservation treatment'),
        value_type=DictRow(title=_(u'Conservation treatment'), schema=IConsTreatments),
        required=False)
    form.widget(conditionConservation_conservationTreatments=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('conditionConservation_conservationTreatments')


    # Recommendations
    conditionConservation_recommendations_display = schema.TextLine(
        title=_(u'Display'),
        required=False
    )
    dexteritytextindexer.searchable('conditionConservation_recommendations_display')
    
    conditionConservation_recommendations_environment = schema.TextLine(
        title=_(u'Environment'),
        required=False
    )
    dexteritytextindexer.searchable('conditionConservation_recommendations_environment')

    conditionConservation_recommendations_handling = schema.TextLine(
        title=_(u'Handling'),
        required=False
    )
    dexteritytextindexer.searchable('conditionConservation_recommendations_handling')

    conditionConservation_recommendations_packing = schema.TextLine(
        title=_(u'Packing'),
        required=False
    )
    dexteritytextindexer.searchable('conditionConservation_recommendations_packing')

    conditionConservation_recommendations_security = schema.TextLine(
        title=_(u'Security'),
        required=False
    )
    dexteritytextindexer.searchable('conditionConservation_recommendations_security')

    conditionConservation_recommendations_storage = schema.TextLine(
        title=_(u'Storage'),
        required=False
    )
    dexteritytextindexer.searchable('conditionConservation_recommendations_storage')

    conditionConservation_recommendations_specialRequirements = schema.TextLine(
        title=_(u'Special requirements'),
        required=False
    )
    dexteritytextindexer.searchable('conditionConservation_recommendations_specialRequirements')

    # # # # # # # # # # # # # # # # # 
    # Recommendations/requirements  #
    # # # # # # # # # # # # # # # # # 
    model.fieldset('recommendations_requirements', label=_(u'Recommendations/requirements'), 
        fields=['recommendationsRequirements_creditLine_creditLine', 'recommendationsRequirements_legalLicenceRequirements_requirements',
                'recommendationsRequirements_legalLicenceRequirements_requirementsHeld']
    )

    # Credit line
    recommendationsRequirements_creditLine_creditLine = schema.TextLine(
        title=_(u'Credit line'),
        required=False
    )
    dexteritytextindexer.searchable('recommendationsRequirements_creditLine_creditLine')

    # Legal / license requirements
    recommendationsRequirements_legalLicenceRequirements_requirements = schema.TextLine(
        title=_(u'Requirements'),
        required=False
    )
    dexteritytextindexer.searchable('recommendationsRequirements_legalLicenceRequirements_requirements')

    recommendationsRequirements_legalLicenceRequirements_requirementsHeld = ListField(title=_(u'Requirements held'),
        value_type=DictRow(title=_(u'Requirements held'), schema=IRequirements),
        required=False)
    form.widget(recommendationsRequirements_legalLicenceRequirements_requirementsHeld=DataGridFieldFactory)
    dexteritytextindexer.searchable('recommendationsRequirements_legalLicenceRequirements_requirementsHeld')


    # # # # # # # # # #
    # Reproductions   #
    # # # # # # # # # #
    model.fieldset('reproductions', label=_(u'Reproductions'), 
        fields=['reproductions_reproduction']
    )

    # Reproduction
    reproductions_reproduction = ListField(title=_(u'Reproduction'),
        value_type=DictRow(title=_(u'Reproduction'), schema=IReproduction),
        required=False)
    form.widget(reproductions_reproduction=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('reproductions_reproduction')


    # # # # # # # # # # #
    # Value & Insurance #
    # # # # # # # # # # #

    model.fieldset('value_insurance', label=_(u'Value & Insurance'), 
        fields=['valueInsurance_valuation', 'valueInsurance_insurance']
    )

    valueInsurance_valuation = ListField(title=_(u'Valuation'),
        value_type=DictRow(title=_(u'Valuation'), schema=IValuation),
        required=False)
    form.widget(valueInsurance_valuation=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('valueInsurance_valuation')

    valueInsurance_insurance = ListField(title=_(u'Insurance'),
        value_type=DictRow(title=_(u'Insurance'), schema=IInsurance),
        required=False)
    form.widget(valueInsurance_insurance=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('valueInsurance_insurance')

    # # # # # # # # # #
    # Acquisition     #
    # # # # # # # # # #

    model.fieldset('acquisition', label=_(u'Acquisition'), 
        fields=['acquisition_accession_date', 'acquisition_number', 'acquisition_date', 'acquisition_precision',
                'acquisition_method', 'acquisition_rec_no', 'acquisition_lot_no',
                'acquisition_from', 'acquisition_auction', 'acquisition_place', 'acquisition_reason',
                'acquisition_conditions', 'acquisition_authorization_authorizer', 'acquisition_authorization_date',
                'acquisition_costs_offer_price', 'acquisition_costs_offer_price_curr', 'acquisition_costs_purchase_price',
                'acquisition_costs_purchase_price_curr', 'acquisition_costs_notes', 'acquisition_funding', 'acquisition_documentation',
                'acquisition_copyright', 'acquisition_notes', 'acquisition_acquisition_from']
    )

    # Accession
    acquisition_accession_date = schema.TextLine(
        title=_(u'Accession date'),
        required=False
    )
    dexteritytextindexer.searchable('acquisition_accession_date')

    # Acquisition
    acquisition_number = schema.TextLine(
        title=_(u'Acquisition number'),
        required=False
    )
    dexteritytextindexer.searchable('acquisition_number')

    acquisition_date = schema.TextLine(
        title=_(u'Date'),
        required=False
    )
    dexteritytextindexer.searchable('acquisition_date')

    acquisition_precision = schema.TextLine(
        title=_(u'Precision'),
        required=False
    )
    dexteritytextindexer.searchable('acquisition_precision')

    acquisition_method = schema.TextLine(
        title=_(u'Method'),
        required=False
    )
    dexteritytextindexer.searchable('acquisition_method')

    acquisition_rec_no = schema.TextLine(
        title=_(u'Rec.no.'),
        required=False
    )
    dexteritytextindexer.searchable('acquisition_rec_no')

    acquisition_lot_no = schema.TextLine(
        title=_(u'Lot no.'),
        required=False
    )
    dexteritytextindexer.searchable('acquisition_lot_no')


    acquisition_from = schema.TextLine(
        title=_(u'label_from', default=u'From'),
        required=False
    )
    dexteritytextindexer.searchable('acquisition_from')

    acquisition_acquisition_from = RelationList(
        title=_(u'label_from', default=u'From'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution', navigation_tree_query={'path':{'query':PERSON_INSTITUTION_FOLDER}})
        ),
        required=False
    )
    
    acquisition_auction = schema.TextLine(
        title=_(u'Auction'),
        required=False
    )
    dexteritytextindexer.searchable('acquisition_auction')

    acquisition_place = schema.TextLine(
        title=_(u'Place'),
        required=False
    )
    dexteritytextindexer.searchable('acquisition_place')

    acquisition_reason = schema.TextLine(
        title=_(u'Reason'),
        required=False
    )
    dexteritytextindexer.searchable('acquisition_reason')

    acquisition_conditions = schema.TextLine(
        title=_(u'Conditions'),
        required=False
    )
    dexteritytextindexer.searchable('acquisition_conditions')

    # Authorization
    acquisition_authorization_authorizer = schema.TextLine(
        title=_(u'Authorizer'),
        required=False
    )
    dexteritytextindexer.searchable('acquisition_authorization_authorizer')

    acquisition_authorization_date = schema.TextLine(
        title=_(u'Date'),
        required=False
    )
    dexteritytextindexer.searchable('acquisition_authorization_date')

    # Costs
    acquisition_costs_offer_price = schema.TextLine(
        title=_(u'Offer price'),
        required=False
    )
    dexteritytextindexer.searchable('acquisition_costs_offer_price')

    acquisition_costs_offer_price_curr = schema.TextLine(
        title=_(u'Curr.'),
        required=False
    )
    dexteritytextindexer.searchable('acquisition_costs_offer_price_curr')

    acquisition_costs_purchase_price = schema.TextLine(
        title=_(u'Purchase price'),
        required=False
    )
    dexteritytextindexer.searchable('acquisition_costs_purchase_price')

    acquisition_costs_purchase_price_curr = schema.TextLine(
        title=_(u'Curr.'),
        required=False
    )
    dexteritytextindexer.searchable('acquisition_costs_purchase_price_curr')

    acquisition_costs_notes = schema.TextLine(
        title=_(u'Notes'),
        required=False
    )
    dexteritytextindexer.searchable('acquisition_costs_notes')

    # Funding *
    acquisition_funding = ListField(title=_(u'Funding'),
        value_type=DictRow(title=_(u'Funding'), schema=IFunding),
        required=False)
    form.widget(acquisition_funding=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('acquisition_funding')

    # Documentation *
    acquisition_documentation = ListField(title=_(u'Documentation'),
        value_type=DictRow(title=_(u'Documentation'), schema=IDocumentation),
        required=False)
    form.widget(acquisition_documentation=DataGridFieldFactory)
    dexteritytextindexer.searchable('acquisition_documentation')

    # Copyright
    acquisition_copyright = schema.TextLine(
        title=_(u'Copyright'),
        required=False
    )
    dexteritytextindexer.searchable('acquisition_copyright')

    # Notes
    acquisition_notes = schema.TextLine(
        title=_(u'Notes'),
        required=False
    )
    dexteritytextindexer.searchable('acquisition_notes')

    # # # # # # # 
    # Disposal  #
    # # # # # # #

    model.fieldset('disposal', label=_(u'Disposal'), 
        fields=['disposal_deaccession', 'disposal_new_object_number', 'disposal_number',
                'disposal_date', 'disposal_method', 'disposal_proposed_recipient', 'disposal_disposal_proposedRecipient',
                'disposal_disposal_recipient', 'disposal_recipient', 'disposal_reason', 'disposal_provisos', 'disposal_finance_disposal_price',
                'disposal_documentation', 'disposal_notes'
        ]
    )

    # Deaccession
    disposal_deaccession = schema.TextLine(
        title=_(u'Deaccession date'),
        required=False
    )
    dexteritytextindexer.searchable('disposal_deaccession')

    disposal_new_object_number = schema.TextLine(
        title=_(u'New object number'),
        required=False
    )
    dexteritytextindexer.searchable('disposal_new_object_number')

    # Disposal
    disposal_number = schema.TextLine(
        title=_(u'Disposal number'),
        required=False
    )
    dexteritytextindexer.searchable('disposal_number')

    disposal_date = schema.TextLine(
        title=_(u'Date'),
        required=False
    )
    dexteritytextindexer.searchable('disposal_date')

    disposal_method = schema.TextLine(
        title=_(u'Method'),
        required=False
    )
    dexteritytextindexer.searchable('disposal_method')

    disposal_proposed_recipient = schema.TextLine(
        title=_(u'Proposed recipient'),
        required=False
    )
    dexteritytextindexer.searchable('disposal_proposed_recipient')

    disposal_disposal_recipient = RelationList(
        title=_(u'Recipient'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution', navigation_tree_query={'path':{'query':PERSON_INSTITUTION_FOLDER}})
        ),
        required=False
    )

    disposal_disposal_proposedRecipient = RelationList(
        title=_(u'Proposed recipient'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution', navigation_tree_query={'path':{'query':PERSON_INSTITUTION_FOLDER}})
        ),
        required=False
    )

    disposal_recipient = schema.TextLine(
        title=_(u'Recipient'),
        required=False
    )
    dexteritytextindexer.searchable('disposal_recipient')

    disposal_reason = schema.TextLine(
        title=_(u'Reason'),
        required=False
    )
    dexteritytextindexer.searchable('disposal_reason')

    disposal_provisos = schema.TextLine(
        title=_(u'Provisos'),
        required=False
    )
    dexteritytextindexer.searchable('disposal_provisos')

    # Finance
    disposal_finance_disposal_price = schema.TextLine(
        title=_(u'Disposal price'),
        required=False
    )
    dexteritytextindexer.searchable('disposal_finance_disposal_price')

    # Documentation
    disposal_documentation = ListField(title=_(u'Documentation'),
        value_type=DictRow(title=_(u'Documentation'), schema=IDocumentation),
        required=False)
    form.widget(disposal_documentation=DataGridFieldFactory)
    dexteritytextindexer.searchable('disposal_documentation')

    # Notes 
    disposal_notes = schema.Text(
        title=_(u'Notes'),
        required=False
    )
    dexteritytextindexer.searchable('disposal_notes')

    # # # # # # # # # # # # #
    # Ownership history     #
    # # # # # # # # # # # # #

    model.fieldset('ownership_history', label=_(u'Ownership history'), 
        fields=['ownershipHistory_current_owner', 'ownershipHistory_ownership_currentOwner', 
                'ownershipHistory_owner', 'ownershipHistory_history_owner', 'ownershipHistory_from',
                'ownershipHistory_until', 'ownershipHistory_exchange_method', 'ownershipHistory_acquired_from',
                'ownershipHistory_history_acquiredFrom',
                'ownershipHistory_auction', 'ownershipHistory_rec_no', 'ownershipHistory_lot_no', 'ownershipHistory_place',
                'ownershipHistory_price', 'ownershipHistory_category', 'ownershipHistory_access', 'ownershipHistory_notes']
    )

    # Ownership
    ownershipHistory_current_owner = schema.TextLine(
        title=_(u'Current Owner'),
        required=False
    )
    dexteritytextindexer.searchable('ownershipHistory_current_owner')

    ownershipHistory_ownership_currentOwner = RelationList(
        title=_(u'Current Owner'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution', navigation_tree_query={'path':{'query':PERSON_INSTITUTION_FOLDER}})
        ),
        required=False
    )

    # History
    ownershipHistory_owner = schema.TextLine(
        title=_(u'Owner'),
        required=False
    )
    dexteritytextindexer.searchable('ownershipHistory_owner')

    ownershipHistory_history_owner = RelationList(
        title=_(u'Owner'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution', navigation_tree_query={'path':{'query':PERSON_INSTITUTION_FOLDER}})
        ),
        required=False
    )

    ownershipHistory_from = schema.TextLine(
        title=_(u'From'),
        required=False
    )
    dexteritytextindexer.searchable('ownershipHistory_from')

    ownershipHistory_until = schema.TextLine(
        title=_(u'Until'),
        required=False
    )
    dexteritytextindexer.searchable('ownershipHistory_until')

    ownershipHistory_exchange_method = schema.TextLine(
        title=_(u'Exchange method'),
        required=False
    )
    dexteritytextindexer.searchable('ownershipHistory_exchange_method')

    ownershipHistory_acquired_from = schema.TextLine(
        title=_(u'Acquired from'),
        required=False
    )
    dexteritytextindexer.searchable('ownershipHistory_acquired_from')

    ownershipHistory_history_acquiredFrom = RelationList(
        title=_(u'Acquired from'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution', navigation_tree_query={'path':{'query':PERSON_INSTITUTION_FOLDER}})
        ),
        required=False
    )

    ownershipHistory_auction = schema.TextLine(
        title=_(u'Auction'),
        required=False
    )
    dexteritytextindexer.searchable('ownershipHistory_auction')

    ownershipHistory_rec_no = schema.TextLine(
        title=_(u'Rec.no.'),
        required=False
    )
    dexteritytextindexer.searchable('ownershipHistory_rec_no')

    ownershipHistory_lot_no = schema.TextLine(
        title=_(u'Lot no.'),
        required=False
    )
    dexteritytextindexer.searchable('ownershipHistory_lot_no')

    ownershipHistory_place = schema.TextLine(
        title=_(u'label_plaats', default=u'Place'),
        required=False
    )
    dexteritytextindexer.searchable('ownershipHistory_place')

    ownershipHistory_price = schema.TextLine(
        title=_(u'Price'),
        required=False
    )
    dexteritytextindexer.searchable('ownershipHistory_price')

    ownershipHistory_category = schema.TextLine(
        title=_(u'Ownership category'),
        required=False
    )
    dexteritytextindexer.searchable('ownershipHistory_category')

    ownershipHistory_access = schema.TextLine(
        title=_(u'Access'),
        required=False
    )
    dexteritytextindexer.searchable('ownershipHistory_access')

    ownershipHistory_notes = schema.TextLine(
        title=_(u'Notes'),
        required=False
    )
    dexteritytextindexer.searchable('ownershipHistory_notes')

    # # # # # # # # 
    # Location    #
    # # # # # # # #

    model.fieldset('location', label=_(u'Location'), 
        fields=['location_normal_location', 'location_current_location', 'location_checks']
    )

    # Normal location
    location_normal_location = schema.TextLine(
        title=_(u'Normal location'),
        required=False
    )
    dexteritytextindexer.searchable('location_normal_location')

    # Current location
    location_current_location = ListField(title=_(u'Current location'),
        value_type=DictRow(title=_(u'Current location'), schema=ICurrentLocation),
        required=False)
    form.widget(location_current_location=DataGridFieldFactory)
    dexteritytextindexer.searchable('location_current_location')

    # Location checks
    location_checks = ListField(title=_(u'Location checks'),
        value_type=DictRow(title=_(u'Location checks'), schema=ILocationChecks),
        required=False)
    form.widget(location_checks=DataGridFieldFactory)
    dexteritytextindexer.searchable('location_checks')

    # # # # # # # # # # # 
    # Field Collection  #
    # # # # # # # # # # #

    model.fieldset('field_collection', label=_(u'Field Collection'), 
        fields=['fieldCollection_fieldCollection_fieldCollNumber', 'fieldCollection_fieldCollection_collector',
                'fieldCollection_fieldCollection_event', 'fieldCollection_fieldCollection_dateEarly',
                'fieldCollection_fieldCollection_dateEarlyPrecision', 'fieldCollection_fieldCollection_dateLate',
                'fieldCollection_fieldCollection_dateLatePrecision', 'fieldCollection_fieldCollection_method',
                'fieldCollection_fieldCollection_place', 'fieldCollection_fieldCollection_placeCode',
                'fieldCollection_fieldCollection_placeFeature', 'fieldCollection_coordinatesFieldCollectionPlace',
                'fieldCollection_habitatStratigraphy_habitat', 'fieldCollection_habitatStratigraphy_stratigraphy',
                'fieldCollection_notes']
    )

    fieldCollection_fieldCollection_fieldCollNumber = ListField(title=_(u'Field coll. number'),
        value_type=DictRow(title=_(u'Field coll. number'), schema=IFieldCollNumber),
        required=False)
    form.widget(fieldCollection_fieldCollection_fieldCollNumber=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('fieldCollection_fieldCollection_fieldCollNumber')

    fieldCollection_fieldCollection_collector = ListField(title=_(u'Collector'),
        value_type=DictRow(title=_(u'Collector'), schema=ICollector),
        required=False)
    form.widget(fieldCollection_fieldCollection_collector=DataGridFieldFactory)
    dexteritytextindexer.searchable('fieldCollection_fieldCollection_collector')

    fieldCollection_fieldCollection_event = ListField(title=_(u'Event'),
        value_type=DictRow(title=_(u'Event'), schema=IEvent),
        required=False)
    form.widget(fieldCollection_fieldCollection_event=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('fieldCollection_fieldCollection_event')

    fieldCollection_fieldCollection_dateEarly = schema.TextLine(
        title=_(u'Date (early)'),
        required=False
    )
    dexteritytextindexer.searchable('fieldCollection_fieldCollection_dateEarly')

    fieldCollection_fieldCollection_dateEarlyPrecision = schema.TextLine(
        title=_(u'Precision'),
        required=False
    )
    dexteritytextindexer.searchable('fieldCollection_fieldCollection_dateEarlyPrecision')

    fieldCollection_fieldCollection_dateLate = schema.TextLine(
        title=_(u'Date (late)'),
        required=False
    )
    dexteritytextindexer.searchable('fieldCollection_fieldCollection_dateLate')

    fieldCollection_fieldCollection_dateLatePrecision = schema.TextLine(
        title=_(u'Precision'),
        required=False
    )
    dexteritytextindexer.searchable('fieldCollection_fieldCollection_dateLatePrecision')

    fieldCollection_fieldCollection_method = ListField(title=_(u'Method'),
        value_type=DictRow(title=_(u'Method'), schema=IMethod),
        required=False)
    form.widget(fieldCollection_fieldCollection_method=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('fieldCollection_fieldCollection_method')

    fieldCollection_fieldCollection_place = ListField(title=_(u'Place'),
        value_type=DictRow(title=_(u'Place'), schema=IPlace),
        required=False)
    form.widget(fieldCollection_fieldCollection_place=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('fieldCollection_fieldCollection_place')

    fieldCollection_fieldCollection_placeCode = ListField(title=_(u'Place code'),
        value_type=DictRow(title=_(u'Place code'), schema=IPlaceCode),
        required=False)
    form.widget(fieldCollection_fieldCollection_placeCode=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('fieldCollection_fieldCollection_placeCode')

    fieldCollection_fieldCollection_placeFeature = ListField(title=_(u'Place feature'),
        value_type=DictRow(title=_(u'Place feature'), schema=IPlaceFeature),
        required=False)
    form.widget(fieldCollection_fieldCollection_placeFeature=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('fieldCollection_fieldCollection_placeFeature')

    # Co-ordinates field collection place
    fieldCollection_coordinatesFieldCollectionPlace = ListField(title=_(u'Co-ordinates field collection place'),
        value_type=DictRow(title=_(u'Co-ordinates field collection place'), schema=IFieldCollectionPlace),
        required=False)
    form.widget(fieldCollection_coordinatesFieldCollectionPlace=DataGridFieldFactory)
    dexteritytextindexer.searchable('fieldCollection_coordinatesFieldCollectionPlace')


    # Habitat and stratigraphy
    fieldCollection_habitatStratigraphy_habitat = ListField(title=_(u'Habitat'),
        value_type=DictRow(title=_(u'Habitat'), schema=IHabitat),
        required=False)
    form.widget(fieldCollection_habitatStratigraphy_habitat=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('fieldCollection_habitatStratigraphy_habitat')

    fieldCollection_habitatStratigraphy_stratigraphy = ListField(title=_(u'Stratigraphy'),
        value_type=DictRow(title=_(u'Stratigraphy'), schema=IStratigraphy),
        required=False)
    form.widget(fieldCollection_habitatStratigraphy_stratigraphy=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('fieldCollection_habitatStratigraphy_stratigraphy')

    # Notes
    fieldCollection_notes = ListField(title=_(u'Notes'),
        value_type=DictRow(title=_(u'Notes'), schema=INotes),
        required=False)
    form.widget(fieldCollection_notes=DataGridFieldFactory)
    dexteritytextindexer.searchable('fieldCollection_notes')

    # # # # # # # # #
    # Exhibitions   #
    # # # # # # # # #

    model.fieldset('exhibitions', label=_(u'Exhibitions'), 
        fields=['exhibitions_exhibition', 'exhibitions_relatedExhibitions']
    )

    exhibitions_exhibition = ListField(title=_(u'Exhibition'),
        value_type=DictRow(title=_(u'Exhibition'), schema=IExhibition),
        required=False)
    form.widget(exhibitions_exhibition=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('exhibitions_exhibition')


    exhibitions_relatedExhibitions = RelationList(
        title=_(u'Exhibition'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='Exhibition', navigation_tree_query={'path':{'query':EXHIBITION_FOLDER}})
        ),
        required=False
    )

    # # # # # # # #
    # Loans       #
    # # # # # # # #

    model.fieldset('loans', label=_(u'Loans'), 
        fields=['loans_incomingLoans', 'loans_outgoingLoans',
                'loans_incomingLoan', 'loans_outgoingLoan']
    )

    loans_incomingLoans = ListField(title=_(u'Incoming loans'),
        value_type=DictRow(title=_(u'Incoming loans'), schema=IIncomingLoan),
        required=False)
    form.widget(loans_incomingLoans=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('loans_incomingLoans')

    loans_outgoingLoans = ListField(title=_(u'Outgoing loans'),
        value_type=DictRow(title=_(u'Outgoing loans'), schema=IOutgoingLoan),
        required=False)
    form.widget(loans_outgoingLoans=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('loans_outgoingLoans')

    loans_incomingLoan = RelationList(
        title=_(u'Incoming loans'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='IncomingLoan', navigation_tree_query={'path':{'query':INCOMINGLOAN_FOLDER}})
        ),
        required=False
    )

    loans_outgoingLoan = RelationList(
        title=_(u'Outgoing loans'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='OutgoingLoan', navigation_tree_query={'path':{'query':OUTGOINGLOAN_FOLDER}})
        ),
        required=False
    )

    # # # # # # #
    # Labels    #
    # # # # # # #

    model.fieldset('labels', label=_(u'Labels'), 
        fields=['labels']
    )

    labels = ListField(title=_(u'Labels'),
        value_type=DictRow(title=_(u'Labels'), schema=ILabel),
        required=False)
    form.widget(labels=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('labels')

    # # # # # #
    # Notes   #
    # # # # # #
    model.fieldset('notes', label=_(u"label_opmerkingen", default=u'Notes'), 
        fields=['notes', 'notes_free_fields']
    )

    notes = ListField(title=_(u"label_opmerkingen", default=u'Notes'),
        value_type=DictRow(title=_(u"label_opmerkingen", default=u'Notes'), schema=INotes),
        required=False)
    form.widget(notes=DataGridFieldFactory)
    dexteritytextindexer.searchable('notes')

    # Free fields
    notes_free_fields = ListField(title=_(u'Free Fields'),
        value_type=DictRow(title=_(u'Free Fields'), schema=IFreeFields),
        required=False)
    form.widget(notes_free_fields=DataGridFieldFactory)
    dexteritytextindexer.searchable('notes_free_fields')
    


# # # # # # # # # # # # #
# Object declaration    #
# # # # # # # # # # # # #

class Object(Container):
    grok.implements(IObject)
    pass

# # # # # # # # # # # # # #
# Object add/edit views   # 
# # # # # # # # # # # # # #

class AddForm(add.DefaultAddForm):
    template = ViewPageTemplateFile('object_templates/add.pt')
    def update(self):
        super(AddForm, self).update()
        for group in self.groups:
            for widget in group.widgets.values():
                if IDataGridField.providedBy(widget):
                    widget.auto_append = True
                    widget.allow_reorder = True
                alsoProvides(widget, IFormWidget)

        for widget in self.widgets.values():
            if IDataGridField.providedBy(widget) or IAjaxSelectWidget.providedBy(widget):
                widget.auto_append = True
                widget.allow_reorder = True
                alsoProvides(widget, IFormWidget)

class AddView(add.DefaultAddView):
    form = AddForm
    
class EditForm(edit.DefaultEditForm):
    template = ViewPageTemplateFile('object_templates/edit.pt')

    def update(self):
        super(EditForm, self).update()
        for group in self.groups:
            for widget in group.widgets.values():
                if IDataGridField.providedBy(widget):
                    widget.auto_append = False
                    widget.allow_reorder = True
                alsoProvides(widget, IFormWidget)

        for widget in self.widgets.values():
            if IDataGridField.providedBy(widget) or IAjaxSelectWidget.providedBy(widget):
                widget.auto_append = False
                widget.allow_reorder = True
                alsoProvides(widget, IFormWidget)

    def get_page_title(self):
        context = self.context
        heading = self.label
        if hasattr(context, 'identification_identification_objectNumber'):
            if context.identification_identification_objectNumber:
                heading = str(context.identification_identification_objectNumber)

        return heading

    def get_lead_media(self):
        obj = self.context

        uid = obj.UID()
        catalog = self.context.portal_catalog

        url = ""
        brains = catalog.searchResults({"UID":uid})
        if len(brains) > 0:
            brain = brains[0]
            if brain.hasMedia:
                lead_uid = brain.leadMedia
                lead_brains = catalog.searchResults({"UID":lead_uid})
                if lead_brains:
                    image = lead_brains[0]
                    url = image.getURL()+"/@@images/image/large"

        return url

    
    

