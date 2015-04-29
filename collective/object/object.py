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

# # # # # # # # # #
# # # # # # # # # #
# Object schema   #
# # # # # # # # # #
# # # # # # # # # #

class IObject(form.Schema):
    text = RichText(
        title=_(u"Body"),
        required=False
    )

    # # # # # # # # # # # # # # 
    # Identification fieldset #
    # # # # # # # # # # # # # # 
    
    model.fieldset('identification', label=_(u'Identification'), 
        fields=['identification_institution_name', 'identification_administrative_name', 'identification_collection', 'identification_object_number',
                'identification_rec_type', 'identification_part', 'identification_tot_number', 'identification_copy_number', 'identification_edition', 'identification_distinguish_features', 
                'identification_object_category', 'identification_object_name', 'identification_other_name', 'identification_title_notes',
                'identification_translated_title', 'identification_title_language', 'identification_describer', 'identification_describer_date',
                'identification_taxonomy', 'identification_taxonomy_determiner', 'identification_taxonomy_object_status', 'identification_taxonomy_notes']
    )

    # Identification #
    identification_institution_name = schema.TextLine(
        title=_(u'Institution name'), 
        required=False,
        description=_(u"Institution name<br><br>The name of the institution responsible for managing the object.<br><br>Enter the common name of your institution, possibly shortened and with a place name. This field is especially relevant if object descriptions are used by third parties.<br><br> Examples:<br>National Museums of Scotland<br>NMS<br>REME<br>Met")
    )
    dexteritytextindexer.searchable('identification_institution_name')

    identification_administrative_name = schema.TextLine(
        title=_(u'Administrative name'), 
        required=False,
        description=_(u"Administration name<br><br>The name of the department responsible for the object itself and for the documentation about the object.<br><br>Examples:<br>Textiles<br>Geology<br>Glass and ceramics")
    )
    dexteritytextindexer.searchable('identification_administrative_name')

    identification_collection = ListField(title=_(u'Collection'),
        value_type=DictRow(title=_(u'Collection'), schema=ICollection),
        required=False,
        description=_(u"Collection<br><br>If this object is part of a specific collection within the overall museum collection, use this field to enter its name.<br><br>Examples:<br>manuscripts<br>Muller"))
    form.widget(identification_collection=DataGridFieldFactory)

    identification_object_number = schema.TextLine(
        title=_(u'Object number'),
        required=False
    )
    dexteritytextindexer.searchable('identification_object_number')

    identification_rec_type = schema.TextLine(
        title=_(u'Rec. type'),
        required=False
    )
    dexteritytextindexer.searchable('identification_rec_type')

    identification_part = schema.TextLine(
        title=_(u'Part'),
        required=False
    )
    dexteritytextindexer.searchable('identification_part')

    identification_tot_number = schema.TextLine(
        title=_(u'Tot. Number'),
        required=False
    )
    dexteritytextindexer.searchable('identification_tot_number')

    identification_copy_number = schema.TextLine(
        title=_(u'Copy number'),
        required=False
    )
    dexteritytextindexer.searchable('identification_copy_number')

    identification_edition = schema.TextLine(
        title=_(u'Edition'),
        required=False
    )
    dexteritytextindexer.searchable('identification_edition')

    identification_distinguish_features = schema.TextLine(
        title=_(u'Distinguish features'),
        required=False
    )
    dexteritytextindexer.searchable('identification_distinguish_features')

    # Object name #
    identification_object_category = ListField(title=_(u'Object Category'),
        value_type=DictRow(title=_(u'Object Category'), schema=IObjectCategory),
        required=False)
    form.widget(identification_object_category=DataGridFieldFactory)
    dexteritytextindexer.searchable('identification_object_category')

    identification_object_name = ListField(title=_(u'Object name'),
        value_type=DictRow(title=_(u'Object name'), schema=IObjectName),
        required=False)
    form.widget(identification_object_name=DataGridFieldFactory)
    dexteritytextindexer.searchable('identification_object_name')

    identification_other_name = ListField(title=_(u'Other name'),
        value_type=DictRow(title=_(u'Other name'), schema=IOtherName),
        required=False)
    form.widget(identification_other_name=DataGridFieldFactory)
    dexteritytextindexer.searchable('identification_other_name')

    # Title and description
    identification_title_notes = schema.TextLine(
        title=_(u'Notes'),
        required=False
    )
    dexteritytextindexer.searchable('identification_title_notes')

    identification_translated_title = schema.TextLine(
        title=_(u'Translated title'),
        required=False
    )
    dexteritytextindexer.searchable('identification_translated_title')

    identification_title_language = schema.TextLine(
        title=_(u'Language'),
        required=False
    )
    dexteritytextindexer.searchable('identification_title_language')

    identification_describer = schema.TextLine(
        title=_(u'Describer'),
        required=False
    )
    dexteritytextindexer.searchable('identification_describer')

    identification_describer_date = schema.TextLine(
        title=_(u'Date'),
        required=False
    )
    dexteritytextindexer.searchable('identification_describer_date')

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

    identification_taxonomy_object_status = schema.TextLine(
        title=_(u'Object status'),
        required=False
    )
    dexteritytextindexer.searchable('identification_taxonomy_object_status')

    identification_taxonomy_notes = ListField(title=_(u'Notes'),
        value_type=DictRow(title=_(u'Notes'), schema=INotes),
        required=False)
    form.widget(identification_taxonomy_notes=DataGridFieldFactory)





    # # # # # # # # # # # # # # # # #
    # Physical Characteristics      #
    # # # # # # # # # # # # # # # # #

    model.fieldset('physical_characteristics', label=_(u'Physical Characteristics'), 
        fields=['physicalCharacteristics_description', 'physicalCharacteristics_keywords',
                'physicalCharacteristics_techniques', 'physicalCharacteristics_materials', 'physicalCharacteristics_dimensions', 'physicalCharacteristics_dimensions_free_text',
                'physicalCharacteristics_frame', 'physicalCharacteristics_frame_detail']
    )

    # Physical Description
    physicalCharacteristics_description = schema.TextLine(
        title=_(u'Description'),
        required=False
    )
    dexteritytextindexer.searchable('physicalCharacteristics_description')

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

    physicalCharacteristics_dimensions_free_text = schema.TextLine(
        title=_(u'Dimensions (free text)'),
        required=False
    )

    # Frame #
    physicalCharacteristics_frame = schema.TextLine(
        title=_(u'Frame'),
        required=False
    )
    dexteritytextindexer.searchable('physicalCharacteristics_frame')

    physicalCharacteristics_frame_detail = schema.TextLine(
        title=_(u'Detail'),
        required=False
    )
    dexteritytextindexer.searchable('physicalCharacteristics_frame_detail')


    # # # # # # # # # # # # # # # # #
    # Production | Dating           #
    # # # # # # # # # # # # # # # # #

    model.fieldset('production_dating', label=_(u'Production | Dating'), 
        fields=['productionDating_creator', 'productionDating_qualifier',
                'productionDating_role', 'productionDating_place', 'productionDating_school', 'productionDating_notes',
                'productionDating_reason', 'productionDating_period', 'productionDating_dating_notes']
    )

    productionDating_creator = schema.TextLine(
        title=_(u'Creator'),
        required=False
    )
    dexteritytextindexer.searchable('productionDating_creator')

    productionDating_qualifier = schema.TextLine(
        title=_(u'Qualifier'),
        required=False
    )
    dexteritytextindexer.searchable('productionDating_qualifier')

    productionDating_role = schema.TextLine(
        title=_(u'Role'),
        required=False
    )
    dexteritytextindexer.searchable('productionDating_role')

    productionDating_place = schema.TextLine(
        title=_(u'Place'),
        required=False
    )
    dexteritytextindexer.searchable('productionDating_place')

    productionDating_school = schema.TextLine(
        title=_(u'School / style'),
        required=False
    )
    dexteritytextindexer.searchable('productionDating_school')

    productionDating_notes = schema.TextLine(
        title=_(u'Production notes'),
        required=False
    )
    dexteritytextindexer.searchable('productionDating_notes')

    productionDating_reason = schema.TextLine(
        title=_(u'Production reason'),
        required=False
    )
    dexteritytextindexer.searchable('productionDating_reason')

    # Dating #
    productionDating_period = ListField(title=_(u'Period'),
        value_type=DictRow(title=_(u'Period'), schema=IPeriod),
        required=False)
    form.widget(productionDating_period=DataGridFieldFactory)
    dexteritytextindexer.searchable('productionDating_period')

    productionDating_dating_notes = schema.TextLine(
        title=_(u'Notes'),
        required=False
    )
    dexteritytextindexer.searchable('productionDating_dating_notes')


    # # # # # # # # # # # # # # #
    # Condition & Conservation  #
    # # # # # # # # # # # # # # #

    model.fieldset('condition_conservation', label=_(u'Condition & Conservation'), 
        fields=['conditionConservation_priority', 'conditionConservation_next_condition_check', 'conditionConservation_date',
                'conditionConservation_completeness', 'conditionConservation_condition', 'conditionConservation_enviromental_condition', 'conditionConservation_conservation_request']
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

    # Completeness*
    conditionConservation_completeness = ListField(title=_(u'Completeness'),
        value_type=DictRow(title=_(u'Completeness'), schema=ICompleteness),
        required=False)
    form.widget(conditionConservation_completeness=DataGridFieldFactory)
    dexteritytextindexer.searchable('conditionConservation_completeness')

    # Condition*
    conditionConservation_condition = ListField(title=_(u'Condition'),
        value_type=DictRow(title=_(u'Condition'), schema=ICondition),
        required=False)
    form.widget(conditionConservation_condition=DataGridFieldFactory)
    dexteritytextindexer.searchable('conditionConservation_condition')

    # Enviromental condition*
    conditionConservation_enviromental_condition = ListField(title=_(u'Enviromental condition'),
        value_type=DictRow(title=_(u'Enviromental condition'), schema=IEnvCondition),
        required=False)
    form.widget(conditionConservation_enviromental_condition=DataGridFieldFactory)
    dexteritytextindexer.searchable('conditionConservation_enviromental_condition')

    # Conservation request*
    conditionConservation_conservation_request = ListField(title=_(u'Conservation request'),
        value_type=DictRow(title=_(u'Conservation request'), schema=IConsRequest),
        required=False)
    form.widget(conditionConservation_conservation_request=DataGridFieldFactory)
    dexteritytextindexer.searchable('conditionConservation_conservation_request')


    # # # # # # # # # # # # # # #
    # Inscriptions & Markings   #
    # # # # # # # # # # # # # # #

    model.fieldset('inscriptions_markings', label=_(u'Inscriptions and markings'), 
        fields=['inscriptionsMarkings_inscriptions']
    )

    inscriptionsMarkings_inscriptions = ListField(title=_(u'Inscriptions and markings'),
        value_type=DictRow(title=_(u'Inscriptions and markings'), schema=IInscription),
        required=False)
    form.widget(inscriptionsMarkings_inscriptions=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('inscriptionsMarkings_inscriptions')

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
                'acquisition_copyright', 'acquisition_notes']
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
        title=_(u'From'),
        required=False
    )
    dexteritytextindexer.searchable('acquisition_from')

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
                'disposal_date', 'disposal_method', 'disposal_proposed_recipient', 'disposal_recipient',
                'disposal_reason', 'disposal_provisos', 'disposal_finance_disposal_price', 'disposal_finance_currency',
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

    disposal_finance_currency = schema.TextLine(
        title=_(u'Curr.'),
        required=False
    )
    dexteritytextindexer.searchable('disposal_finance_currency')

    # Documentation
    disposal_documentation = ListField(title=_(u'Documentation'),
        value_type=DictRow(title=_(u'Documentation'), schema=IDocumentation),
        required=False)
    form.widget(disposal_documentation=DataGridFieldFactory)
    dexteritytextindexer.searchable('disposal_documentation')

    # Notes 
    disposal_notes = schema.TextLine(
        title=_(u'Notes'),
        required=False
    )
    dexteritytextindexer.searchable('disposal_notes')

    # # # # # # # # # # # # #
    # Ownership history     #
    # # # # # # # # # # # # #

    model.fieldset('ownership_history', label=_(u'Ownership history'), 
        fields=['ownershipHistory_current_owner', 'ownershipHistory_owner', 'ownershipHistory_from',
                'ownershipHistory_until', 'ownershipHistory_exchange_method', 'ownershipHistory_acquired_from',
                'ownershipHistory_auction', 'ownershipHistory_rec_no', 'ownershipHistory_lot_no', 'ownershipHistory_place',
                'ownershipHistory_price', 'ownershipHistory_category', 'ownershipHistory_access', 'ownershipHistory_notes']
    )

    # Ownership
    ownershipHistory_current_owner = schema.TextLine(
        title=_(u'Current Owner'),
        required=False
    )
    dexteritytextindexer.searchable('ownershipHistory_current_owner')

    # History
    ownershipHistory_owner = schema.TextLine(
        title=_(u'Owner'),
        required=False
    )
    dexteritytextindexer.searchable('ownershipHistory_owner')

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
        title=_(u'Place'),
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

    # Current location
    location_current_location = ListField(title=_(u'Current location'),
        value_type=DictRow(title=_(u'Current location'), schema=ICurrentLocation),
        required=False)
    form.widget(location_current_location=DataGridFieldFactory)

    # Location checks
    location_checks = ListField(title=_(u'Location checks'),
        value_type=DictRow(title=_(u'Location checks'), schema=ILocationChecks),
        required=False)
    form.widget(location_checks=DataGridFieldFactory)

    # # # # # #
    # Notes   #
    # # # # # #
    model.fieldset('notes', label=_(u'Notes'), 
        fields=['notes', 'notes_free_fields']
    )

    notes = ListField(title=_(u'Notes'),
        value_type=DictRow(title=_(u'Notes'), schema=INotes),
        required=False)
    form.widget(notes=DataGridFieldFactory)

    # Free fields
    notes_free_fields = ListField(title=_(u'Free Fields'),
        value_type=DictRow(title=_(u'Free Fields'), schema=IFreeFields),
        required=False)
    form.widget(notes_free_fields=DataGridFieldFactory)

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
                alsoProvides(widget, IFormWidget)

class AddView(add.DefaultAddView):
    form = AddForm
    

class EditForm(edit.DefaultEditForm):
    template = ViewPageTemplateFile('object_templates/edit.pt')
    
    def update(self):
        super(EditForm, self).update()
        for group in self.groups:
            for widget in group.widgets.values():
                alsoProvides(widget, IFormWidget)

