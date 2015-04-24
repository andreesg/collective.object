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
from collective.z3cform.datagridfield import DataGridFieldFactory
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
        fields=['institution_name', 'administrative_name', 'collection', 'object_number',
                'rec_type', 'part', 'tot_number', 'copy_number', 'edition', 'distinguish_features', 
                'object_category', 'object_name', 'other_name']
    )

    # Identification #
    institution_name = schema.TextLine(
        title=_(u'Institution name'), 
        required=False,
        description=_(u"Institution name<br><br>The name of the institution responsible for managing the object.<br><br>Enter the common name of your institution, possibly shortened and with a place name. This field is especially relevant if object descriptions are used by third parties.<br><br> Examples:<br>National Museums of Scotland<br>NMS<br>REME<br>Met")
    )
    dexteritytextindexer.searchable('institution_name')

    administrative_name = schema.TextLine(
        title=_(u'Administrative name'), 
        required=False,
        description=_(u"Administration name<br><br>The name of the department responsible for the object itself and for the documentation about the object.<br><br>Examples:<br>Textiles<br>Geology<br>Glass and ceramics")
    )
    dexteritytextindexer.searchable('administrative_name')

    collection = schema.TextLine(
        title=_(u'Collection'), 
        required=False,
        description=_(u"Collection<br><br>If this object is part of a specific collection within the overall museum collection, use this field to enter its name.<br><br>Examples:<br>manuscripts<br>Muller")
    )
    dexteritytextindexer.searchable('collection')

    object_number = schema.TextLine(
        title=_(u'Object number'),
        required=False
    )
    dexteritytextindexer.searchable('object_number')

    rec_type = schema.TextLine(
        title=_(u'Rec. type'),
        required=False
    )
    dexteritytextindexer.searchable('rec_type')

    part = schema.TextLine(
        title=_(u'Part'),
        required=False
    )
    dexteritytextindexer.searchable('part')

    tot_number = schema.TextLine(
        title=_(u'Tot. Number'),
        required=False
    )
    dexteritytextindexer.searchable('tot_number')

    copy_number = schema.TextLine(
        title=_(u'Copy number'),
        required=False
    )
    dexteritytextindexer.searchable('copy_number')

    edition = schema.TextLine(
        title=_(u'Edition'),
        required=False
    )
    dexteritytextindexer.searchable('edition')

    distinguish_features = schema.TextLine(
        title=_(u'Distinguish features'),
        required=False
    )
    dexteritytextindexer.searchable('distinguish_features')

    # Object name #
    object_category = schema.TextLine(
        title=_(u'Object Category'),
        required=False
    )
    dexteritytextindexer.searchable('object_category')

    object_name = schema.TextLine(
        title=_(u'Object name'),
        required=False
    )
    dexteritytextindexer.searchable('object_name')

    other_name = schema.TextLine(
        title=_(u'Other name'),
        required=False
    )
    dexteritytextindexer.searchable('other_name')


    # # # # # # # # # # # # # # # # #
    # Physical Characteristics      #
    # # # # # # # # # # # # # # # # #

    model.fieldset('physical_characteristics', label=_(u'Physical Characteristics'), 
        fields=['physical_description', 'keywords',
                'techniques', 'materials', 'dimensions', 'dimensions_free_text',
                'frame', 'frame_detail']
    )

    # Physical Description
    physical_description = schema.TextLine(
        title=_(u'Description'),
        required=False
    )
    dexteritytextindexer.searchable('physical_description')

    # Keywords #
    keywords = ListField(title=_(u'Keywords'),
        value_type=schema.Object(title=_(u'Keywords'), schema=IKeyword),
        required=False)
    form.widget(keywords=DataGridFieldFactory)

    # Techniques #
    techniques = ListField(title=_(u'Techniques'),
        value_type=schema.Object(title=_(u'Techniques'), schema=ITechnique),
        required=False)
    form.widget(techniques=DataGridFieldFactory)

    # Materials #
    materials = ListField(title=_(u'Materials'),
        value_type=schema.Object(title=_(u'Materials'), schema=IMaterial),
        required=False)
    form.widget(materials=DataGridFieldFactory)

    # Dimensions #
    dimensions = ListField(title=_(u'Dimensions'),
        value_type=schema.Object(title=_(u'Dimensions'), schema=IDimension),
        required=False)
    form.widget(dimensions=DataGridFieldFactory)

    dimensions_free_text = schema.TextLine(
        title=_(u'Dimensions (free text)'),
        required=False
    )

    # Frame #
    frame = schema.TextLine(
        title=_(u'Frame'),
        required=False
    )
    dexteritytextindexer.searchable('frame')

    frame_detail = schema.TextLine(
        title=_(u'Detail'),
        required=False
    )
    dexteritytextindexer.searchable('frame_detail')


    # # # # # # # # # # # # # # # # #
    # Production | Dating           #
    # # # # # # # # # # # # # # # # #

    model.fieldset('production_dating', label=_(u'Production | Dating'), 
        fields=['production_creator', 'production_qualifier',
                'production_role', 'production_place', 'production_school', 'production_notes',
                'production_reason', 'production_period', 'production_dating_notes']
    )

    production_creator = schema.TextLine(
        title=_(u'Creator'),
        required=False
    )
    dexteritytextindexer.searchable('production_creator')

    production_qualifier = schema.TextLine(
        title=_(u'Qualifier'),
        required=False
    )
    dexteritytextindexer.searchable('production_qualifier')

    production_role = schema.TextLine(
        title=_(u'Role'),
        required=False
    )
    dexteritytextindexer.searchable('production_role')

    production_place = schema.TextLine(
        title=_(u'Place'),
        required=False
    )
    dexteritytextindexer.searchable('production_place')

    production_school = schema.TextLine(
        title=_(u'School / style'),
        required=False
    )
    dexteritytextindexer.searchable('production_school')

    production_notes = schema.TextLine(
        title=_(u'Production notes'),
        required=False
    )
    dexteritytextindexer.searchable('production_notes')

    production_reason = schema.TextLine(
        title=_(u'Production reason'),
        required=False
    )
    dexteritytextindexer.searchable('production_reason')

    # Dating #
    production_period = ListField(title=_(u'Period'),
        value_type=schema.Object(title=_(u'Period'), schema=IPeriod),
        required=False)
    form.widget(production_period=DataGridFieldFactory)
    dexteritytextindexer.searchable('production_period')

    production_dating_notes = schema.TextLine(
        title=_(u'Notes'),
        required=False
    )
    dexteritytextindexer.searchable('production_dating_notes')


    # # # # # # # # # # # # # # #
    # Condition & Conservation  #
    # # # # # # # # # # # # # # #

    model.fieldset('condition_conservation', label=_(u'Condition & Conservation'), 
        fields=['conservation_priority', 'conservation_next_condition_check', 'conservation_date',
                'completeness', 'condition', 'enviromental_condition', 'conservation_request']
    )

    # Conservation treatment

    # Choice field
    conservation_priority = schema.Choice(
        vocabulary=priority_vocabulary,
        title=_(u'Priority'),
        required=False
    )
    dexteritytextindexer.searchable('conservation_priority')

    conservation_next_condition_check = schema.TextLine(
        title=_(u'Next condition check'),
        required=False
    )
    dexteritytextindexer.searchable('conservation_next_condition_check')

    conservation_date = schema.TextLine(
        title=_(u'Date'),
        required=False
    )
    dexteritytextindexer.searchable('conservation_date')

    # Completeness*
    completeness = ListField(title=_(u'Completeness'),
        value_type=schema.Object(title=_(u'Completeness'), schema=ICompleteness),
        required=False)
    form.widget(completeness=DataGridFieldFactory)
    dexteritytextindexer.searchable('completeness')

    # Condition*
    condition = ListField(title=_(u'Condition'),
        value_type=schema.Object(title=_(u'Condition'), schema=ICondition),
        required=False)
    form.widget(condition=DataGridFieldFactory)
    dexteritytextindexer.searchable('condition')

    # Enviromental condition*
    enviromental_condition = ListField(title=_(u'Enviromental condition'),
        value_type=schema.Object(title=_(u'Enviromental condition'), schema=IEnvCondition),
        required=False)
    form.widget(enviromental_condition=DataGridFieldFactory)
    dexteritytextindexer.searchable('enviromental_condition')

    # Conservation request*
    conservation_request = ListField(title=_(u'Conservation request'),
        value_type=schema.Object(title=_(u'Conservation request'), schema=IConsRequest),
        required=False)
    form.widget(conservation_request=DataGridFieldFactory)
    dexteritytextindexer.searchable('conservation_request')


    # # # # # # # # # # # # # # #
    # Inscriptions & Markings   #
    # # # # # # # # # # # # # # #

    model.fieldset('inscriptions_markings', label=_(u'Inscriptions and markings'), 
        fields=['inscriptions']
    )

    inscriptions = ListField(title=_(u'Inscriptions and markings'),
        value_type=schema.Object(title=_(u'Inscriptions and markings'), schema=IInscription),
        required=False)
    form.widget(inscriptions=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('inscriptions')

    # # # # # # # # # # #
    # Value & Insurance #
    # # # # # # # # # # #

    model.fieldset('value_insurance', label=_(u'Value & Insurance'), 
        fields=['valuation', 'insurance']
    )

    valuation = ListField(title=_(u'Valuation'),
        value_type=schema.Object(title=_(u'Valuation'), schema=IValuation),
        required=False)
    form.widget(valuation=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('valuation')

    insurance = ListField(title=_(u'Insurance'),
        value_type=schema.Object(title=_(u'Insurance'), schema=IInsurance),
        required=False)
    form.widget(insurance=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('insurance')

    # # # # # # # # # #
    # Acquisition     #
    # # # # # # # # # #

    model.fieldset('acquisition', label=_(u'Acquisition'), 
        fields=['accession_date', 'acquisition_number', 'acquisition_date', 'acquisition_precision',
                'acquisition_method', 'acquisition_rec_no', 'acquisition_lot_no',
                'acquisition_from', 'acquisition_auction', 'acquisition_place', 'acquisition_reason',
                'acquisition_conditions', 'authorization_authorizer', 'authorization_date',
                'costs_offer_price', 'costs_offer_price_curr', 'costs_purchase_price',
                'costs_purchase_price_curr', 'costs_notes', 'funding', 'documentation',
                'acquisition_copyright', 'acquisition_notes']
    )

    # Accession
    accession_date = schema.TextLine(
        title=_(u'Accession date'),
        required=False
    )
    dexteritytextindexer.searchable('accession_date')

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
    authorization_authorizer = schema.TextLine(
        title=_(u'Authorizer'),
        required=False
    )
    dexteritytextindexer.searchable('authorization_authorizer')

    authorization_date = schema.TextLine(
        title=_(u'Date'),
        required=False
    )
    dexteritytextindexer.searchable('authorization_date')

    # Costs
    costs_offer_price = schema.TextLine(
        title=_(u'Offer price'),
        required=False
    )
    dexteritytextindexer.searchable('costs_offer_price')

    costs_offer_price_curr = schema.TextLine(
        title=_(u'Curr.'),
        required=False
    )
    dexteritytextindexer.searchable('costs_offer_price_curr')

    costs_purchase_price = schema.TextLine(
        title=_(u'Purchase price'),
        required=False
    )
    dexteritytextindexer.searchable('costs_purchase_price')

    costs_purchase_price_curr = schema.TextLine(
        title=_(u'Curr.'),
        required=False
    )
    dexteritytextindexer.searchable('costs_purchase_price_curr')

    costs_notes = schema.TextLine(
        title=_(u'Notes'),
        required=False
    )
    dexteritytextindexer.searchable('costs_notes')

    # Funding *
    funding = ListField(title=_(u'Funding'),
        value_type=schema.Object(title=_(u'Funding'), schema=IFunding),
        required=False)
    form.widget(funding=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('funding')

    # Documentation *
    documentation = ListField(title=_(u'Documentation'),
        value_type=schema.Object(title=_(u'Documentation'), schema=IDocumentation),
        required=False)
    form.widget(documentation=DataGridFieldFactory)
    dexteritytextindexer.searchable('documentation')

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
                'disposal_reason', 'disposal_provisos', 'finance_disposal_price', 'finance_curr',
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
    finance_disposal_price = schema.TextLine(
        title=_(u'Disposal price'),
        required=False
    )
    dexteritytextindexer.searchable('finance_disposal_price')

    finance_curr = schema.TextLine(
        title=_(u'Curr.'),
        required=False
    )
    dexteritytextindexer.searchable('finance_curr')

    # Documentation
    disposal_documentation = ListField(title=_(u'Documentation'),
        value_type=schema.Object(title=_(u'Documentation'), schema=IDocumentation),
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
        fields=['ownership_current_owner', 'ownership_history_owner', 'ownership_history_from',
                'ownership_history_until', 'ownership_exchange_method', 'ownership_acquired_from',
                'ownership_auction', 'ownership_rec_no', 'ownership_lot_no', 'ownership_place',
                'ownership_price', 'ownership_category', 'ownership_access', 'ownership_notes']
    )

    # Ownership
    ownership_current_owner = schema.TextLine(
        title=_(u'Current Owner'),
        required=False
    )
    dexteritytextindexer.searchable('ownership_current_owner')

    # History
    ownership_history_owner = schema.TextLine(
        title=_(u'Owner'),
        required=False
    )
    dexteritytextindexer.searchable('ownership_history_owner')

    ownership_history_from = schema.TextLine(
        title=_(u'From'),
        required=False
    )
    dexteritytextindexer.searchable('ownership_history_from')

    ownership_history_until = schema.TextLine(
        title=_(u'Until'),
        required=False
    )
    dexteritytextindexer.searchable('ownership_history_until')

    ownership_exchange_method = schema.TextLine(
        title=_(u'Exchange method'),
        required=False
    )
    dexteritytextindexer.searchable('ownership_exchange_method')

    ownership_acquired_from = schema.TextLine(
        title=_(u'Acquired from'),
        required=False
    )
    dexteritytextindexer.searchable('ownership_acquired_from')

    ownership_auction = schema.TextLine(
        title=_(u'Auction'),
        required=False
    )
    dexteritytextindexer.searchable('ownership_auction')

    ownership_rec_no = schema.TextLine(
        title=_(u'Rec.no.'),
        required=False
    )
    dexteritytextindexer.searchable('ownership_rec_no')

    ownership_lot_no = schema.TextLine(
        title=_(u'Lot no.'),
        required=False
    )
    dexteritytextindexer.searchable('ownership_lot_no')

    ownership_place = schema.TextLine(
        title=_(u'Place'),
        required=False
    )
    dexteritytextindexer.searchable('ownership_place')

    ownership_price = schema.TextLine(
        title=_(u'Price'),
        required=False
    )
    dexteritytextindexer.searchable('ownership_price')

    ownership_category = schema.TextLine(
        title=_(u'Ownership category'),
        required=False
    )
    dexteritytextindexer.searchable('ownership_category')

    ownership_access = schema.TextLine(
        title=_(u'Access'),
        required=False
    )
    dexteritytextindexer.searchable('ownership_access')

    ownership_notes = schema.TextLine(
        title=_(u'Notes'),
        required=False
    )
    dexteritytextindexer.searchable('ownership_notes')

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
        value_type=schema.Object(title=_(u'Current location'), schema=ICurrentLocation),
        required=False)
    form.widget(location_current_location=DataGridFieldFactory)

    # Location checks
    location_checks = ListField(title=_(u'Location checks'),
        value_type=schema.Object(title=_(u'Location checks'), schema=ILocationChecks),
        required=False)
    form.widget(location_checks=DataGridFieldFactory)

    # # # # # #
    # Notes   #
    # # # # # #
    model.fieldset('notes', label=_(u'Notes'), 
        fields=['notes', 'notes_free_fields']
    )

    notes = ListField(title=_(u'Notes'),
        value_type=schema.Object(title=_(u'Notes'), schema=INotes),
        required=False)
    form.widget(notes=DataGridFieldFactory)

    # Free fields
    notes_free_fields = ListField(title=_(u'Free Fields'),
        value_type=schema.Object(title=_(u'Free Fields'), schema=IFreeFields),
        required=False)
    form.widget(notes_free_fields=DataGridFieldFactory)

    # # # # # # #
    # Labels    #
    # # # # # # #

    model.fieldset('labels', label=_(u'Labels'), 
        fields=['labels']
    )

    labels = ListField(title=_(u'Labels'),
        value_type=schema.Object(title=_(u'Labels'), schema=ILabel),
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

