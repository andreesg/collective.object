#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Zope dependencies
#
from zope import schema
from zope.interface import invariant, Invalid, Interface, implements
from zope.component import adapts
from zope.interface import alsoProvides
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.fieldproperty import FieldProperty
from zope.component import getMultiAdapter
from z3c.form import validator
from zope.interface import Invalid
from z3c.form.interfaces import DISPLAY_MODE, HIDDEN_MODE, IDataConverter, NO_VALUE
from z3c.form.converter import BaseDataConverter
import datetime
from plone.app.uuid.utils import uuidToCatalogBrain, uuidToObject

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
from z3c.form import group, field, button
from z3c.form.form import extends
from z3c.form.browser.textlines import TextLinesFieldWidget
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from z3c.relationfield.interfaces import IRelationList, IRelationValue

try:
    from z3c.form.browser.textlines import TextLinesFieldWidget
except ImportError:
    from plone.z3cform.textlines.textlines import TextLinesFieldWidget

from collective.z3cform.datagridfield.interfaces import IDataGridField

#
# Plone app widget dependencies
#
from plone.app.widgets.dx import AjaxSelectFieldWidget, AjaxSelectWidget, SelectWidget, DatetimeFieldWidget, IAjaxSelectWidget, RelatedItemsFieldWidget
from plone.formwidget.autocomplete import AutocompleteFieldWidget


#
# DataGridFields dependencies
#
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow, IDataGridField
from collective.z3cform.datagridfield.blockdatagridfield import BlockDataGridFieldFactory


# # # # # # # # # # # # # # # 
# Dexterity imports         # 
# # # # # # # # # # # # # # # 
from five import grok
from collective import dexteritytextindexer
from plone.dexterity.browser.view import DefaultView
from plone.dexterity.content import Container
from plone.dexterity.browser import add, edit
from z3c.form.interfaces import IWidget

# # # # # # # # # # # # # # # # 
# !Object specific imports!   #
# # # # # # # # # # # # # # # #
from collective.object import MessageFactory as _
from .utils.vocabularies import *
from .utils.interfaces import *
from .utils.views import *
from .utils.source import ObjPathSourceBinder
from .utils.variables import *
from .utils.widgets import AjaxSingleSelectFieldWidget, SimpleRelatedItemsFieldWidget, ExtendedRelatedItemsFieldWidget

from plone.formwidget.contenttree import ObjPathSourceBinder as sb
from collective.dexteritytextindexer.converters import DefaultDexterityTextIndexFieldConverter
from collective.dexteritytextindexer.interfaces import IDexterityTextIndexFieldConverter
from plone.dexterity.interfaces import IDexterityContent
from Products.CMFCore.utils import getToolByName

# # # # # # # # # #
# # # # # # # # # #
# Object schema   #
# # # # # # # # # #
# # # # # # # # # #

class ListFieldConverter(DefaultDexterityTextIndexFieldConverter):
    implements(IDexterityTextIndexFieldConverter)
    adapts(IDexterityContent, IListRelatedField, IWidget)

    def convert(self):
        html = self.widget.render().strip()

        transforms = getToolByName(self.context, 'portal_transforms')
        if isinstance(html, unicode):
            html = html.encode('utf-8')
        stream = transforms.convertTo('text/plain', html, mimetype='text/html')

        datastripped = stream.getData().strip()
        
        for line in self.widget.value:
            if 'makers' in line:
                for maker in line['makers']:
                    if IRelationValue.providedBy(maker):
                        maker_obj = maker.to_object
                        title = getattr(maker_obj, 'title', "")
                        datastripped = "%s %s" %(datastripped, title)
                    elif getattr(maker, 'portal_type', "") == "PersonOrInstitution":
                        title = getattr(maker, 'title', "")
                        datastripped = "%s %s" %(datastripped, title)
                    else:
                        continue

        return datastripped

class IObject(form.Schema):

    priref = schema.TextLine(
        title=_(u'priref'), 
        required=False
    )

    # Vocabularies

    identification_identification_collections = schema.List(
        title=_(u'Collection'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    form.widget('identification_identification_collections', AjaxSelectFieldWidget,  vocabulary="collective.object.collection")

    identification_objectName_category = schema.List(
        title=_(u'Object category'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    form.widget('identification_objectName_category', AjaxSelectFieldWidget,  vocabulary="collective.object.objectCategory")

    identification_objectName_objectname = ListField(title=_(u'Object name'),
        value_type=DictRow(title=_(u'Object name'), schema=IObjectname),
        required=False)
    form.widget(identification_objectName_objectname=DataGridFieldFactory)

    # Production
    productionDating_productionDating = ListRelatedField(title=_(u'Production & Dating'),
        value_type=DictRow(title=_(u'Production & Dating'), schema=IProductiondating),
        required=False)
    form.widget(productionDating_productionDating=BlockDataGridFieldFactory)

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

    physicalCharacteristics_keyword = ListField(title=_(u'Keywords'),
        value_type=DictRow(title=_(u'Keywords'), schema=IKeywords),
        required=False)
    form.widget(physicalCharacteristics_keyword=DataGridFieldFactory)

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

    iconography_generalSearchCriteria_generalthemes = schema.List(
        title=_(u'General theme'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    form.widget('iconography_generalSearchCriteria_generalthemes', AjaxSelectFieldWidget,  vocabulary="collective.object.generalthemes")

    iconography_generalSearchCriteria_specificthemes = schema.List(
        title=_(u'Specific theme'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    form.widget('iconography_generalSearchCriteria_specificthemes', AjaxSelectFieldWidget,  vocabulary="collective.object.specificthemes")

    # Content subject
    iconography_contentSubjects = ListField(title=_(u'Content subject'),
        value_type=DictRow(title=_(u'Content subject'), schema=IIconographyContentSubjects),
        required=False)
    form.widget(iconography_contentSubjects=BlockDataGridFieldFactory)

    # Content period/date
    iconography_contentPeriodDates = ListField(title=_(u'Content period/date'),
        value_type=DictRow(title=_(u'Content period/date'), schema=IIconographyContentPeriodDates),
        required=False)
    form.widget(iconography_contentPeriodDates=BlockDataGridFieldFactory)

    # Inscriptions and markings
    inscriptionsMarkings_inscriptionsAndMarkings = ListField(title=_(u'Inscriptions and markings'),
        value_type=DictRow(title=_(u'Inscriptions and markings'), schema=IInscriptions),
        required=False)
    form.widget(inscriptionsMarkings_inscriptionsAndMarkings=BlockDataGridFieldFactory)

    # Associations
    associations_associatedSubjects = ListField(title=_(u'Associated subject'),
        value_type=DictRow(title=_(u'Associated subject'), schema=IAssociatedSubjects),
        required=False)
    form.widget(associations_associatedSubjects=BlockDataGridFieldFactory)

    associations_associatedPeriods = ListField(title=_(u'Associated period'),
        value_type=DictRow(title=_(u'Associated period'), schema=IAssociatedPeriods),
        required=False)
    form.widget(associations_associatedPeriods=BlockDataGridFieldFactory)

    associations_associatedPersonInstitutions = ListField(title=_(u'Associated person/institution'),
        value_type=DictRow(title=_(u'Associated person/institution'), schema=IAssociatedPersonInstitutions),
        required=False)
    form.widget(associations_associatedPersonInstitutions=BlockDataGridFieldFactory)

    # Value & Insurance
    valueInsurance_valuations = ListField(title=_(u'Valuation'),
        value_type=DictRow(title=_(u'Valuation'), schema=IValuations),
        required=False)
    form.widget(valueInsurance_valuations=BlockDataGridFieldFactory)

    # Condition & Conservation 
    conditionConservation_conditions = ListField(title=_(u'Condition'),
        value_type=DictRow(title=_(u'Condition'), schema=IConditions),
        required=False)
    form.widget(conditionConservation_conditions=DataGridFieldFactory)

    conditionConservation_preservationForm = ListField(title=_(u'Preservation form'),
        value_type=DictRow(title=_(u'Preservation form'), schema=IEnvConditions),
        required=False)
    form.widget(conditionConservation_preservationForm=BlockDataGridFieldFactory)


    # Aquisition
    acquisition_methods = schema.List(
        title=_(u'Method'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    form.widget('acquisition_methods', AjaxSingleSelectFieldWidget,  vocabulary="collective.object.aquisitionmethod")

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
    form.widget('acquisition_costs_offer_price_currency', AjaxSingleSelectFieldWidget,  vocabulary="collective.object.currency")

    acquisition_costs_purchase_price_currency = schema.List(
        title=_(u'Curr.'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    form.widget('acquisition_costs_purchase_price_currency', AjaxSingleSelectFieldWidget,  vocabulary="collective.object.currency")

    # Funding *
    acquisition_fundings = ListField(title=_(u'Funding'),
        value_type=DictRow(title=_(u'Funding'), schema=IFundings),
        required=False)
    form.widget(acquisition_fundings=BlockDataGridFieldFactory)

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
    form.widget('ownershipHistory_history_exchangeMethod', AjaxSingleSelectFieldWidget,  vocabulary="collective.object.exchangemethod")

    ownershipHistory_history_place = schema.List(
        title=_(u'label_plaats', default=u'Place'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    form.widget('ownershipHistory_history_place', AjaxSingleSelectFieldWidget,  vocabulary="collective.object.historyplace")

    ownershipHistory_historyOwner = ListField(title=_(u'Owner'),
        value_type=DictRow(title=_(u'Owner'), schema=IHistoryOwner),
        required=False)
    form.widget(ownershipHistory_historyOwner=BlockDataGridFieldFactory)

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

    # Field collection
    fieldCollection_fieldCollection_collectors = ListField(title=_(u'Collector'),
        value_type=DictRow(title=_(u'Collector'), schema=ICollectionCollectors),
        required=False)
    form.widget(fieldCollection_fieldCollection_collectors=BlockDataGridFieldFactory)

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

    fieldCollection_habitatStratigraphy_stratigrafie = ListField(title=_(u'Stratigraphy'),
        value_type=DictRow(title=_(u'Stratigraphy'), schema=IStratigrafie),
        required=False)
    form.widget(fieldCollection_habitatStratigraphy_stratigrafie=BlockDataGridFieldFactory)


    # Numbers / relations
    numbersRelationships_relationshipsWithOtherObjects_relatedObjects = ListField(title=_(u'Related object'),
        value_type=DictRow(title=_(u'Related object'), schema=IRelatedObjects),
        required=False)
    form.widget(numbersRelationships_relationshipsWithOtherObjects_relatedObjects=BlockDataGridFieldFactory)


    text = RichText(
        title=_(u"Body"),
        required=False
    )

    # # # # # # # # # # # # # # 
    # Identification fieldset #
    # # # # # # # # # # # # # # 
    model.fieldset('identification', label=_(u'Identification'), 
        fields=[
                'identification_identification_institutionNames', 
                'identification_identification_institutionPlace', 'identification_identification_administrativeName', 
                'identification_identification_objectNumber',
                'identification_identification_part', 'identification_identification_totNumber', 'identification_identification_copyNumber', 
                'identification_identification_edition', 'identification_identification_distinguishFeatures',
                'identification_objectName_otherName', 
                'identification_titleDescription_title',
                'identification_titleDescription_translatedTitle',
                'identification_titleDescription_description',
                'identification_titleDescription_language',
                'identification_titleDescription_describer',
                'identification_titleDescription_titleDate',
                'identification_taxonomy',
                'identification_taxonomy_determiners',
                'identification_taxonomy_objectstatus', 'identification_taxonomy_notes']
    )

    identification_identification_institutionNames = RelationList(
        title=_(u'Institution name'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution')
        ),
        required=False
    )

    form.widget('identification_identification_institutionNames', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relatedInstitution')

    identification_identification_institutionPlace = schema.TextLine(
        title=_(u'Institution place'), 
        required=False
    )

    identification_identification_administrativeName = schema.TextLine(
        title=_(u'Administrative name'), 
        required=False,
        default=u"",
        missing_value=u"",
        description=_(u"Administration name<br><br>The name of the department responsible for the object itself and for the documentation about the object.<br><br>Examples:<br>Textiles<br>Geology<br>Glass and ceramics")
    )

    identification_identification_objectNumber = schema.TextLine(
        title=_(u'Object number'),
        required=False
    )
    dexteritytextindexer.searchable('identification_identification_objectNumber')
   
    identification_identification_part = schema.TextLine(
        title=_(u'Part'),
        required=False
    )

    identification_identification_totNumber = schema.TextLine(
        title=_(u'Tot. Number'),
        required=False
    )

    identification_identification_copyNumber = schema.TextLine(
        title=_(u'Copy number'),
        required=False
    )

    identification_identification_edition = schema.TextLine(
        title=_(u'Edition'),
        required=False
    )

    identification_identification_distinguishFeatures = schema.TextLine(
        title=_(u'Distinguish features'),
        required=False
    )

    identification_titleDescription_title = ListField(title=_(u'Title'),
        value_type=DictRow(title=_(u'Title'), schema=ITitle),
        required=False)
    form.widget(identification_titleDescription_title=BlockDataGridFieldFactory)
    
    identification_titleDescription_description = schema.Text(
        title=_(u'Description'),
        required=False
    )

    identification_titleDescription_translatedTitle = ListField(title=_(u'Translated title'),
        value_type=DictRow(title=_(u'Translated title'), schema=ITranslatedTitle),
        required=False)
    form.widget(identification_titleDescription_translatedTitle=BlockDataGridFieldFactory)

    identification_titleDescription_language = schema.TextLine(
        title=_(u'Language'),
        required=False
    )

    identification_titleDescription_describer = schema.TextLine(
        title=_(u'Describer'),
        required=False
    )

    identification_titleDescription_titleDate = schema.TextLine(
        title=_(u'Date'),
        required=False
    )

    # Taxonomy
    identification_taxonomy = ListField(title=_(u'Taxonomy'),
        value_type=DictRow(title=_(u'Taxonomy'), schema=ITaxonomy),
        required=False)
    form.widget(identification_taxonomy=BlockDataGridFieldFactory)

    identification_taxonomy_determiners = ListField(title=_(u'Determiner'),
        value_type=DictRow(title=_(u'Determiner'), schema=IDeterminers),
        required=False)
    form.widget(identification_taxonomy_determiners=BlockDataGridFieldFactory)

    identification_objectName_otherName = ListField(title=_(u'Other name'),
        value_type=DictRow(title=_(u'Other name'), schema=IOtherName),
        required=False)
    form.widget(identification_objectName_otherName=DataGridFieldFactory)

    identification_taxonomy_objectstatus = schema.Choice(
        title=_(u'Object status'),
        required=True,
        vocabulary="collective.object.objectstatus",
        default="No value",
        missing_value=" "
    )

    identification_taxonomy_notes = ListField(title=_(u'Notes'),
        value_type=DictRow(title=_(u'Notes'), schema=INotes),
        required=False)
    form.widget(identification_taxonomy_notes=BlockDataGridFieldFactory)

    # # # # # # # # # # # # # # # # #
    # Production & Dating           #
    # # # # # # # # # # # # # # # # #

    model.fieldset('production_dating', label=_(u'Production & Dating'), 
        fields=[
                'productionDating_production_productionReason', 
                'productionDating_dating_period', 'productionDating_dating_notes']
    )

    productionDating_production_productionReason = schema.Text(
        title=_(u'Production reason'),
        required=False
    )

    # Dating #
    productionDating_dating_period = ListField(title=_(u'Dating'),
        value_type=DictRow(title=_(u'Dating'), schema=IPeriod),
        required=False)
    form.widget(productionDating_dating_period=DataGridFieldFactory)

    productionDating_dating_notes = ListField(title=_(u'Notes'),
        value_type=DictRow(title=_(u'Notes'), schema=INotes),
        required=False)
    form.widget(productionDating_dating_notes=DataGridFieldFactory)


    # # # # # # # # # # # # # # # # #
    # Physical Characteristics      #
    # # # # # # # # # # # # # # # # #

    model.fieldset('physical_characteristics', label=_(u'Physical Characteristics'), 
        fields=['physicalCharacteristics_physicalDescription_description', 
                'physicalCharacteristics_frame']
    )

    # Physical Description
    physicalCharacteristics_physicalDescription_description = schema.Text(
        title=_(u'Description'),
        required=False
    )

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
                'iconography_contentPersonInstitution',
                'iconography_iconographySource_sourceGeneral', 'iconography_iconographySource_sourceSpecific',
                'iconography_iconographySource_sourceObjectNumber']
    )

    # General search criteria
    iconography_generalSearchCriteria_generalTheme = ListField(title=_(u'General theme'),
        value_type=DictRow(title=_(u'General theme'), schema=IIconographyGeneralTheme),
        required=False)
    form.widget(iconography_generalSearchCriteria_generalTheme=DataGridFieldFactory)

    iconography_generalSearchCriteria_specificTheme = ListField(title=_(u'Specific theme'),
        value_type=DictRow(title=_(u'Specific theme'), schema=IIconographySpecificTheme),
        required=False)
    form.widget(iconography_generalSearchCriteria_specificTheme=DataGridFieldFactory)

    iconography_generalSearchCriteria_classificationTheme = ListField(title=_(u'Classification theme'),
        value_type=DictRow(title=_(u'Classification theme'), schema=IIconographyClassificationTheme),
        required=False)
    form.widget(iconography_generalSearchCriteria_classificationTheme=DataGridFieldFactory)

    # Content description
    iconography_contentDescription = ListField(title=_(u'Content description'),
        value_type=DictRow(title=_(u'Content description'), schema=IIconographyContentDescription),
        required=False)
    form.widget(iconography_contentDescription=DataGridFieldFactory)

    # Content person/institution
    iconography_contentPersonInstitution = ListField(title=_(u'Content person/institution'),
        value_type=DictRow(title=_(u'Content person/institution'), schema=IIconographyContentPersonInstitution),
        required=False)
    form.widget(iconography_contentPersonInstitution=BlockDataGridFieldFactory)

    # Iconography source
    iconography_iconographySource_sourceGeneral = schema.TextLine(
        title=_(u'Source general'),
        required=False
    )

    iconography_iconographySource_sourceSpecific = schema.TextLine(
        title=_(u'Source specific'),
        required=False
    )

    iconography_iconographySource_sourceObjectNumber = schema.TextLine(
        title=_(u'Source object number'),
        required=False
    )

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


    # # # # # # # # #
    # Associations  #      
    # # # # # # # # # 
    model.fieldset('associations', label=_(u'Associations'), 
        fields=['associations_associatedPersonInstitution']
    )

    associations_associatedPersonInstitution = ListField(title=_(u'Associated person/institution'),
        value_type=DictRow(title=_(u'Associated person/institution'), schema=IAssociatedPersonInstitution),
        required=False)
    form.widget(associations_associatedPersonInstitution=BlockDataGridFieldFactory)


    # # # # # # # # # # # # # 
    # Numbers/relationships #
    # # # # # # # # # # # # # 
    model.fieldset('numbers_relationships', label=_(u'Numbers/relationships'), 
        fields=['numbersRelationships_numbers', 'numbersRelationships_relationshipsWithOtherObjects_partOf',
                'numbersRelationships_relationshipsWithOtherObjects_notes', 'numbersRelationships_relationshipsWithOtherObjects_parts',
                'numbersRelationships_relationshipsWithOtherObjects_relatedObject',
                'numbersRelationships_digitalReferences']
    )

    # Numbers
    numbersRelationships_numbers = ListField(title=_(u'Numbers'),
        value_type=DictRow(title=_(u'Numbers'), schema=INumbers),
        required=False)
    form.widget(numbersRelationships_numbers=DataGridFieldFactory)

    # Relationships with other objects
    numbersRelationships_relationshipsWithOtherObjects_partOf = RelationList(
        title=_(u'Part of'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='Object')
        ),
        required=False
    )
    form.widget('numbersRelationships_relationshipsWithOtherObjects_partOf', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')
    
    numbersRelationships_relationshipsWithOtherObjects_notes = schema.TextLine(
        title=_(u'Notes'),
        required=False
    )

    numbersRelationships_relationshipsWithOtherObjects_parts = ListField(title=_(u'Parts'),
        value_type=DictRow(title=_(u'Parts'), schema=IParts),
        required=False)
    form.widget(numbersRelationships_relationshipsWithOtherObjects_parts=BlockDataGridFieldFactory)

    numbersRelationships_relationshipsWithOtherObjects_relatedObject = ListField(title=_(u'Related object'),
        value_type=DictRow(title=_(u'Related object'), schema=IRelatedObject),
        required=False)
    form.widget(numbersRelationships_relationshipsWithOtherObjects_relatedObject=BlockDataGridFieldFactory)

    # Digital references
    numbersRelationships_digitalReferences = ListField(title=_(u'Digital references'),
        value_type=DictRow(title=_(u'Digital references'), schema=IDigitalReferences),
        required=False)
    form.widget(numbersRelationships_digitalReferences=DataGridFieldFactory)

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

    # # # # # # # # # # # # # # # # # # #
    # Documentation (free) / archive    #
    # # # # # # # # # # # # # # # # # # #

    model.fieldset('documentation_free_archive', label=_(u'Documentation (free) / archive'), 
        fields=['documentationFreeArchive_documentationFreeText', 'documentationFreeArchive_archive', 'documentationFreeArchive_archiveNumber']
    )

    documentationFreeArchive_documentationFreeText = ListField(title=_(u'Documentation (free text)'),
        value_type=DictRow(title=_(u'Documentation (free text)'), schema=IDocumentationFreeText),
        required=False)
    form.widget(documentationFreeArchive_documentationFreeText=BlockDataGridFieldFactory)

    documentationFreeArchive_archive = ListField(title=_(u'Archive'),
        value_type=DictRow(title=_(u'Archive'), schema=IArchive),
        required=False)
    form.widget(documentationFreeArchive_archive=DataGridFieldFactory)

    documentationFreeArchive_archiveNumber = ListField(title=_(u'Archive number'),
        value_type=DictRow(title=_(u'Archive number'), schema=IArchive),
        required=False)
    form.widget(documentationFreeArchive_archiveNumber=BlockDataGridFieldFactory)

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


    # # # # # # # # # # # # # # #
    # Condition & Conservation  #
    # # # # # # # # # # # # # # #

    model.fieldset('condition_conservation', label=_(u'Condition & Conservation'), 
        fields=['conditionConservation_priority', 'conditionConservation_next_condition_check', 'conditionConservation_date',
                'conditionConservation_completeness', 'conditionConservation_condition', 'conditionConservation_enviromental_condition', 'conditionConservation_conservation_request',
                'conditionConservation_conservationTreatments']
    )


    # Conservation treatment

    # Choice field
    conditionConservation_priority = schema.Choice(
        vocabulary=priority_vocabulary,
        title=_(u'Priority'),
        required=False,
        missing_value=" "
    )

    conditionConservation_next_condition_check = schema.TextLine(
        title=_(u'Next condition check'),
        required=False
    )

    conditionConservation_date = schema.TextLine(
        title=_(u'Date'),
        required=False
    )

    # Condition*
    conditionConservation_condition = ListField(title=_(u'Condition'),
        value_type=DictRow(title=_(u'Condition'), schema=ICondition),
        required=False)
    form.widget(conditionConservation_condition=DataGridFieldFactory)

    # Completeness*
    conditionConservation_completeness = ListField(title=_(u'Completeness'),
        value_type=DictRow(title=_(u'Completeness'), schema=ICompleteness),
        required=False)
    form.widget(conditionConservation_completeness=DataGridFieldFactory)

    # Enviromental condition*
    conditionConservation_enviromental_condition = ListField(title=_(u'Enviromental condition'),
        value_type=DictRow(title=_(u'Enviromental condition'), schema=IEnvCondition),
        required=False)
    form.widget(conditionConservation_enviromental_condition=BlockDataGridFieldFactory)

    # Conservation request*
    conditionConservation_conservation_request = ListField(title=_(u'Conservation request'),
        value_type=DictRow(title=_(u'Conservation request'), schema=IConsRequest),
        required=False)
    form.widget(conditionConservation_conservation_request=DataGridFieldFactory)

    #Conservation treatment
    conditionConservation_conservationTreatment = ListField(title=_(u'Conservation treatment'),
        value_type=DictRow(title=_(u'Conservation treatment'), schema=IConsTreatment),
        required=False)
    form.widget(conditionConservation_conservationTreatment=DataGridFieldFactory)

    conditionConservation_conservationTreatments = ListField(title=_(u'Conservation treatment'),
        value_type=DictRow(title=_(u'Conservation treatment'), schema=IConsTreatments),
        required=False)
    form.widget(conditionConservation_conservationTreatments=BlockDataGridFieldFactory)


    # Recommendations
    conditionConservation_recommendations_display = schema.TextLine(
        title=_(u'Display'),
        required=False
    )
    
    conditionConservation_recommendations_environment = schema.TextLine(
        title=_(u'Environment'),
        required=False
    )

    conditionConservation_recommendations_handling = schema.TextLine(
        title=_(u'Handling'),
        required=False
    )

    conditionConservation_recommendations_packing = schema.TextLine(
        title=_(u'Packing'),
        required=False
    )

    conditionConservation_recommendations_security = schema.TextLine(
        title=_(u'Security'),
        required=False
    )

    conditionConservation_recommendations_storage = schema.TextLine(
        title=_(u'Storage'),
        required=False
    )

    conditionConservation_recommendations_specialRequirements = schema.TextLine(
        title=_(u'Special requirements'),
        required=False
    )

    # # # # # # # # # # # # # # # # # 
    # Recommendations/requirements  #
    # # # # # # # # # # # # # # # # # 
    model.fieldset('recommendations_requirements', label=_(u'Recommendations/requirements'), 
        fields=['recommendationsRequirements_creditLine_creditLine', 'recommendationsRequirements_legalLicenceRequirements_requirements',
                'recommendationsRequirements_legalLicenceRequirements_requirementsHeld',
                'conditionConservation_recommendations_display', 'conditionConservation_conservationTreatment',
                'conditionConservation_recommendations_environment', 'conditionConservation_recommendations_handling',
                'conditionConservation_recommendations_packing', 'conditionConservation_recommendations_security',
                'conditionConservation_recommendations_specialRequirements',
                'conditionConservation_recommendations_storage']
    )

    # Credit line
    recommendationsRequirements_creditLine_creditLine = schema.TextLine(
        title=_(u'Credit line'),
        required=False
    )

    # Legal / license requirements
    recommendationsRequirements_legalLicenceRequirements_requirements = schema.TextLine(
        title=_(u'Requirements'),
        required=False
    )

    recommendationsRequirements_legalLicenceRequirements_requirementsHeld = ListField(title=_(u'Requirements held'),
        value_type=DictRow(title=_(u'Requirements held'), schema=IRequirements),
        required=False)
    form.widget(recommendationsRequirements_legalLicenceRequirements_requirementsHeld=DataGridFieldFactory)


    # # # # # # # # # # #
    # Value & Insurance #
    # # # # # # # # # # #

    model.fieldset('value_insurance', label=_(u'Value & Insurance'), 
        fields=['valueInsurance_insurance']
    )

    valueInsurance_insurance = ListField(title=_(u'Insurance'),
        value_type=DictRow(title=_(u'Insurance'), schema=IInsurance),
        required=False)
    form.widget(valueInsurance_insurance=BlockDataGridFieldFactory)

    # # # # # # # # # #
    # Acquisition     #
    # # # # # # # # # #

    model.fieldset('acquisition', label=_(u'Acquisition'), 
        fields=['acquisition_accession_date', 'acquisition_number', 'acquisition_date', 'acquisition_precision',
                'acquisition_method', 'acquisition_rec_no', 'acquisition_lot_no', 'acquisition_acquisition_acquisitionfrom',
                'acquisition_auction', 'acquisition_place', 'acquisition_reason',
                'acquisition_conditions', 'acquisition_authorization_authorizer', 'acquisition_authorization_date',
                'acquisition_costs_offer_price', 'acquisition_costs_offer_price_curr', 'acquisition_costs_purchase_price',
                'acquisition_costs_purchase_price_curr', 'acquisition_costs_notes', 'acquisition_funding', 'acquisition_documentation',
                'acquisition_copyright', 'acquisition_notes']
    )

    # Accession
    acquisition_accession_date = schema.TextLine(
        title=_(u'Accession date'),
        required=False
    )

    # Acquisition
    acquisition_number = schema.TextLine(
        title=_(u'Acquisition number'),
        required=False
    )

    acquisition_date = schema.TextLine(
        title=_(u'Date'),
        required=False
    )

    acquisition_precision = schema.TextLine(
        title=_(u'Precision'),
        required=False
    )

    acquisition_method = schema.TextLine(
        title=_(u'Method'),
        required=False
    )

    acquisition_rec_no = schema.TextLine(
        title=_(u'Rec.no.'),
        required=False
    )

    acquisition_lot_no = schema.TextLine(
        title=_(u'Lot no.'),
        required=False
    )

    acquisition_acquisition_acquisitionfrom = RelationList(
        title=_(u'label_from', default=u'From'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution')
        ),
        required=False
    )

    form.widget('acquisition_acquisition_acquisitionfrom', ExtendedRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')
    
    acquisition_auction = schema.TextLine(
        title=_(u'Auction'),
        required=False
    )

    acquisition_place = schema.TextLine(
        title=_(u'Place'),
        required=False
    )

    acquisition_reason = schema.TextLine(
        title=_(u'Reason'),
        required=False
    )

    acquisition_conditions = schema.TextLine(
        title=_(u'Conditions'),
        required=False
    )

    # Authorization
    acquisition_authorization_authorizer = schema.TextLine(
        title=_(u'Authorizer'),
        required=False
    )

    acquisition_authorization_date = schema.TextLine(
        title=_(u'Date'),
        required=False
    )

    # Costs
    acquisition_costs_offer_price = schema.TextLine(
        title=_(u'Offer price'),
        required=False
    )

    acquisition_costs_offer_price_curr = schema.TextLine(
        title=_(u'Curr.'),
        required=False
    )

    acquisition_costs_purchase_price = schema.TextLine(
        title=_(u'Purchase price'),
        required=False
    )

    acquisition_costs_purchase_price_curr = schema.TextLine(
        title=_(u'Curr.'),
        required=False
    )

    acquisition_costs_notes = schema.Text(
        title=_(u'Notes'),
        required=False
    )

    # Funding *
    acquisition_funding = ListField(title=_(u'Funding'),
        value_type=DictRow(title=_(u'Funding'), schema=IFunding),
        required=False)
    form.widget(acquisition_funding=BlockDataGridFieldFactory)

    # Documentation *
    acquisition_documentation = ListField(title=_(u'Documentation'),
        value_type=DictRow(title=_(u'Documentation'), schema=IDocumentation),
        required=False)
    form.widget(acquisition_documentation=DataGridFieldFactory)

    # Copyright
    acquisition_copyright = schema.TextLine(
        title=_(u'Copyright'),
        required=False
    )

    # Notes
    acquisition_notes = schema.TextLine(
        title=_(u'Notes'),
        required=False
    )

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

    disposal_new_object_number = schema.TextLine(
        title=_(u'New object number'),
        required=False
    )

    # Disposal
    disposal_number = schema.TextLine(
        title=_(u'Disposal number'),
        required=False
    )

    disposal_date = schema.TextLine(
        title=_(u'Date'),
        required=False
    )

    disposal_method = schema.TextLine(
        title=_(u'Method'),
        required=False
    )

    disposal_proposed_recipient = schema.TextLine(
        title=_(u'Proposed recipient'),
        required=False
    )

    disposal_disposal_recipient = RelationList(
        title=_(u'Recipient'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution')
        ),
        required=False
    )
    form.widget('disposal_disposal_recipient', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    disposal_disposal_proposedRecipient = RelationList(
        title=_(u'Proposed recipient'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution')
        ),
        required=False
    )
    form.widget('disposal_disposal_proposedRecipient', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')


    disposal_recipient = schema.TextLine(
        title=_(u'Recipient'),
        required=False
    )

    disposal_reason = schema.TextLine(
        title=_(u'Reason'),
        required=False
    )

    disposal_provisos = schema.TextLine(
        title=_(u'Provisos'),
        required=False
    )

    # Finance
    disposal_finance_disposal_price = schema.TextLine(
        title=_(u'Disposal price'),
        required=False
    )

    # Documentation
    disposal_documentation = ListField(title=_(u'Documentation'),
        value_type=DictRow(title=_(u'Documentation'), schema=IDocumentation),
        required=False)
    form.widget(disposal_documentation=DataGridFieldFactory)

    # Notes 
    disposal_notes = schema.Text(
        title=_(u'Notes'),
        required=False
    )

    # # # # # # # # # # # # #
    # Ownership history     #
    # # # # # # # # # # # # #

    model.fieldset('ownership_history', label=_(u'Ownership history'), 
        fields=['ownershipHistory_current_owner', 'ownershipHistory_ownership_currentOwner', 
                'ownershipHistory_owner', 'ownershipHistory_history_owner', 'ownershipHistory_from',
                'ownershipHistory_until', 'ownershipHistory_exchange_method', 'ownershipHistory_acquired_from',
                'ownershipHistory_history_acquiredFrom', 'ownershipHistory_auctions',
                'ownershipHistory_auction', 'ownershipHistory_rec_no', 'ownershipHistory_lot_no', 'ownershipHistory_place',
                'ownershipHistory_price', 'ownershipHistory_category', 'ownershipHistory_access', 'ownershipHistory_notes']
    )

    # Ownership
    ownershipHistory_current_owner = schema.TextLine(
        title=_(u'Current Owner'),
        required=False
    )

    ownershipHistory_ownership_currentOwner = RelationList(
        title=_(u'Current Owner'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution')
        ),
        required=False
    )
    form.widget('ownershipHistory_ownership_currentOwner', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    # History
    ownershipHistory_owner = schema.TextLine(
        title=_(u'Owner'),
        required=False
    )

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

    ownershipHistory_until = schema.TextLine(
        title=_(u'Until'),
        required=False
    )

    ownershipHistory_exchange_method = schema.TextLine(
        title=_(u'Exchange method'),
        required=False
    )

    ownershipHistory_acquired_from = schema.TextLine(
        title=_(u'Acquired from'),
        required=False
    )

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

    ownershipHistory_auctions = ListField(title=_(u'Auction'),
        value_type=DictRow(title=_(u'Auction'), schema=IAuction),
        required=False)
    form.widget(ownershipHistory_auctions=BlockDataGridFieldFactory)

    ownershipHistory_rec_no = schema.TextLine(
        title=_(u'Rec.no.'),
        required=False
    )

    ownershipHistory_lot_no = schema.TextLine(
        title=_(u'Lot no.'),
        required=False
    )

    ownershipHistory_place = schema.TextLine(
        title=_(u'label_plaats', default=u'Place'),
        required=False
    )

    ownershipHistory_price = schema.TextLine(
        title=_(u'Price'),
        required=False
    )

    ownershipHistory_category = schema.TextLine(
        title=_(u'Ownership category'),
        required=False
    )

    ownershipHistory_access = schema.TextLine(
        title=_(u'Access'),
        required=False
    )

    ownershipHistory_notes = schema.TextLine(
        title=_(u'Notes'),
        required=False
    )

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

    # Current location
    location_current_location = ListField(title=_(u'Current location'),
        value_type=DictRow(title=_(u'Current location'), schema=ICurrentLocation),
        required=False)
    form.widget(location_current_location=BlockDataGridFieldFactory)

    # Location checks
    location_checks = ListField(title=_(u'Location checks'),
        value_type=DictRow(title=_(u'Location checks'), schema=ILocationChecks),
        required=False)
    form.widget(location_checks=BlockDataGridFieldFactory)

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
                'fieldCollection_habitatStratigraphy_stratigraphy',
                'fieldCollection_notes', 'fieldCollection_habitatStratigraphy_habitats']
    )

    fieldCollection_fieldCollection_fieldCollNumber = ListField(title=_(u'Field coll. number'),
        value_type=DictRow(title=_(u'Field coll. number'), schema=IFieldCollNumber),
        required=False)
    form.widget(fieldCollection_fieldCollection_fieldCollNumber=BlockDataGridFieldFactory)

    fieldCollection_fieldCollection_collector = ListField(title=_(u'Collector'),
        value_type=DictRow(title=_(u'Collector'), schema=ICollector),
        required=False)
    form.widget(fieldCollection_fieldCollection_collector=DataGridFieldFactory)

    fieldCollection_fieldCollection_event = ListField(title=_(u'Event'),
        value_type=DictRow(title=_(u'Event'), schema=IEvent),
        required=False)
    form.widget(fieldCollection_fieldCollection_event=BlockDataGridFieldFactory)

    fieldCollection_fieldCollection_dateEarly = schema.TextLine(
        title=_(u'Date (early)'),
        required=False
    )

    fieldCollection_fieldCollection_dateEarlyPrecision = schema.TextLine(
        title=_(u'Precision'),
        required=False
    )

    fieldCollection_fieldCollection_dateLate = schema.TextLine(
        title=_(u'Date (late)'),
        required=False
    )

    fieldCollection_fieldCollection_dateLatePrecision = schema.TextLine(
        title=_(u'Precision'),
        required=False
    )

    fieldCollection_fieldCollection_method = ListField(title=_(u'Method'),
        value_type=DictRow(title=_(u'Method'), schema=IMethod),
        required=False)
    form.widget(fieldCollection_fieldCollection_method=BlockDataGridFieldFactory)

    fieldCollection_fieldCollection_place = ListField(title=_(u'Place'),
        value_type=DictRow(title=_(u'Place'), schema=IPlace),
        required=False)
    form.widget(fieldCollection_fieldCollection_place=BlockDataGridFieldFactory)

    fieldCollection_fieldCollection_placeCode = ListField(title=_(u'Place code'),
        value_type=DictRow(title=_(u'Place code'), schema=IPlaceCode),
        required=False)
    form.widget(fieldCollection_fieldCollection_placeCode=BlockDataGridFieldFactory)

    fieldCollection_fieldCollection_placeFeature = ListField(title=_(u'Place feature'),
        value_type=DictRow(title=_(u'Place feature'), schema=IPlaceFeature),
        required=False)
    form.widget(fieldCollection_fieldCollection_placeFeature=BlockDataGridFieldFactory)

    # Co-ordinates field collection place
    fieldCollection_coordinatesFieldCollectionPlace = ListField(title=_(u'Co-ordinates field collection place'),
        value_type=DictRow(title=_(u'Co-ordinates field collection place'), schema=IFieldCollectionPlace),
        required=False)
    form.widget(fieldCollection_coordinatesFieldCollectionPlace=DataGridFieldFactory)


    # Habitat and stratigraphy

    fieldCollection_habitatStratigraphy_habitats = schema.List(
        title=_(u'Habitat'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )
    form.widget('fieldCollection_habitatStratigraphy_habitats', AjaxSelectFieldWidget,  vocabulary="collective.object.habitat")

    fieldCollection_habitatStratigraphy_stratigraphy = ListField(title=_(u'Stratigraphy'),
        value_type=DictRow(title=_(u'Stratigraphy'), schema=IStratigraphy),
        required=False)
    form.widget(fieldCollection_habitatStratigraphy_stratigraphy=BlockDataGridFieldFactory)

    # Notes
    fieldCollection_notes = ListField(title=_(u'Notes'),
        value_type=DictRow(title=_(u'Notes'), schema=INotes),
        required=False)
    form.widget(fieldCollection_notes=DataGridFieldFactory)

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
        fields=['loans_incomingLoans', 'loans_outgoingLoans']
    )

    loans_incomingLoans = ListField(title=_(u'Incoming loans'),
        value_type=DictRow(title=_(u'Incoming loans'), schema=IIncomingLoan),
        required=False)
    form.widget(loans_incomingLoans=BlockDataGridFieldFactory)

    loans_outgoingLoans = ListField(title=_(u'Outgoing loans'),
        value_type=DictRow(title=_(u'Outgoing loans'), schema=IOutgoingLoan),
        required=False)
    form.widget(loans_outgoingLoans=BlockDataGridFieldFactory)

    #
    # Transport tab
    #
    model.fieldset('transport', label=_(u'Transport'), 
        fields=["transport_despatch", "transport_despatchNumber", "transport_entry_number"]
    )

    transport_despatch = ListField(title=_(u'Despatch'),
        value_type=DictRow(title=_(u'Despatch'), schema=IDespatch),
        required=False)
    form.widget(transport_despatch=DataGridFieldFactory)

    transport_despatchNumber = ListField(title=_(u'Despatch number'),
        value_type=DictRow(title=_(u'Despatch number'), schema=IDespatchNumber),
        required=False)
    form.widget(transport_despatchNumber=BlockDataGridFieldFactory)

    transport_entry_number = ListField(title=_(u'Entry number'),
        value_type=DictRow(title=_(u'Entry number'), schema=IEntryNumber),
        required=False)
    form.widget(transport_entry_number=BlockDataGridFieldFactory)

    # # # # # # #
    # Labels    #
    # # # # # # #

    model.fieldset('labels', label=_(u'Labels'), 
        fields=['labels']
    )

    labels = ListField(title=_(u'Labels'),
        value_type=DictRow(title=_(u'Labels'), schema=ILabel),
        required=False)
    form.widget(labels=DataGridFieldFactory)

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

    # Free fields
    notes_free_fields = ListField(title=_(u'Free Fields'),
        value_type=DictRow(title=_(u'Free Fields'), schema=IFreeFields),
        required=False)
    form.widget(notes_free_fields=DataGridFieldFactory)

    #
    # management details
    #

    model.fieldset('management_details', label=_(u'Beheergegevens'), 
        fields=["managementDetails_edit", "managementDetails_input"]
    )

    managementDetails_edit = ListField(title=_(u'Wijziging'),
        value_type=DictRow(title=_(u'Wijziging'), schema=IManagementDetails),
        required=False)
    form.widget(managementDetails_edit=DataGridFieldFactory)

    managementDetails_input = ListField(title=_(u'Invoer'),
        value_type=DictRow(title=_(u'Invoer'), schema=IInvoer),
        required=False)
    form.widget(managementDetails_input=DataGridFieldFactory)


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
                    widget.auto_append = False
                    widget.allow_reorder = True
                alsoProvides(widget, IFormWidget)

        for widget in self.widgets.values():
            if IDataGridField.providedBy(widget) or IAjaxSelectWidget.providedBy(widget):
                widget.auto_append = False
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

    def print_time(self):
        print datetime.datetime.today().isoformat()
        return True

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
        brain = uuidToCatalogBrain(uid)

        if brain:
            lead_uid = brain.leadMedia
            lead_brain = uuidToCatalogBrain(lead_uid)
            if lead_brain:
                url = lead_brain.getURL()+"/@@images/image/large"

        return url

    """@button.buttonAndHandler(u'Save', name='save')
    def handleSave(self, action):
        print "handle save"

        data, errors = self.extractData()
        print data['productionDating_productionDating']

        if errors:
            self.status = self.formErrorsMessage
            return

        context = self.getContent()
        print context
        for k, v in data.items():
            setattr(context, k, v)"""


class ObjectNumberValidator(validator.SimpleFieldValidator):
    def validate(self, value):
        super(ObjectNumberValidator, self).validate(value)

        if value:
            # Fetch context
            context = self.context
            context_uid = context.UID()
            catalog = self.context.portal_catalog
            
            # Check if identification number already exists
            search_value = value.lower()
            brains = catalog(identification_identification_objectNumber=search_value)
            if brains:
                for brain in brains:
                    if brain.UID == context_uid:
                        return None

                raise Invalid(_(u"Object number already exists."))
        else:
            return None

validator.WidgetValidatorDiscriminators(ObjectNumberValidator, field=IObject['identification_identification_objectNumber'])
grok.global_adapter(ObjectNumberValidator)



    
    

