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
from plone.app.z3cform.widget import AjaxSelectFieldWidget, AjaxSelectWidget, SelectWidget, DatetimeFieldWidget, IAjaxSelectWidget, RelatedItemsFieldWidget


#
# DataGridFields dependencies
#
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow, IDataGridField
from collective.z3cform.datagridfield.blockdatagridfield import BlockDataGridFieldFactory


# # # # # # # # # # # # # # # 
# Dexterity imports         # 
# # # # # # # # # # # # # # # 
from five import grok
from plone.dexterity.content import Container
from collective import dexteritytextindexer

# # # # # # # # # # # # # # # # 
# !Object specific imports!   #
# # # # # # # # # # # # # # # #
from collective.object import MessageFactory as _
from .utils.interfaces import *


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
    

    # # # # # # # # # # # # # # # # #
    # Production & Dating           #
    # # # # # # # # # # # # # # # # #
    model.fieldset('production_dating', label=_(u'Production & Dating'), 
        fields=['creator', 'production']
    )

    creator = ListField(title=_(u'Creator'),
        value_type=DictRow(title=_(u'Creator'), schema=ICreator),
        required=False)
    form.widget(creator=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('creator')

    production = ListField(title=_(u'Dating'),
        value_type=DictRow(title=_(u'Dating'), schema=IProduction),
        required=False)
    form.widget(production=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('production')


    # # # # # # # # # # # # # # 
    # Identification fieldset #
    # # # # # # # # # # # # # # 
    model.fieldset('identification', label=_(u'Identification'), 
        fields=['technique', 'material', 'collection','object_number','object_name']
    )

    technique = ListField(title=_(u'Techniques'),
        value_type=DictRow(title=_(u'Techniques'), schema=ITechnique),
        required=False)
    form.widget(technique=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('technique')

    material = ListField(title=_(u'Materials'),
        value_type=DictRow(title=_(u'Materials'), schema=IMaterial),
        required=False)
    form.widget(material=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('material')
    
    object_number = schema.TextLine(
        title=_(u'Object number'),
        required=False
    )
    dexteritytextindexer.searchable('object_number')

    object_name = ListField(title=_(u'Object name'),
        value_type=DictRow(title=_(u'Object name'), schema=IObjectName),
        required=False)
    form.widget(object_name=BlockDataGridFieldFactory)


    collection = ListField(title=_(u'Collection'),
        value_type=DictRow(title=_(u'Collection'), schema=ICollection),
        required=False)
    form.widget(collection=BlockDataGridFieldFactory)

    in_museum = schema.TextLine(
        title=_(u'In museum'),
        required=False
    )
    dexteritytextindexer.searchable('in_museum')
    

    record_published = schema.TextLine(
        title=_(u'Published'),
        required=False
    )
    dexteritytextindexer.searchable('in_museum')

    # # # # # # # #
    # Acquisition #
    # # # # # # # #

    model.fieldset('acquisition', label=_(u'Acquisitions'), 
        fields=['acquisition']
    )

    acquisition = ListField(title=_(u'Acquisition'),
        value_type=DictRow(title=_(u'Acquisition'), schema=IAcquisition),
        required=False)
    form.widget(acquisition=BlockDataGridFieldFactory)


    # # # # # # # # # # # # # # # # #
    # Physical Characteristics      #
    # # # # # # # # # # # # # # # # #
    model.fieldset('physical_characteristics', label=_(u'Physical Characteristics'), 
        fields=['dimension']
    )

    dimension = ListField(title=_(u'Dimensions'),
        value_type=DictRow(title=_(u'Dimensions'), schema=IDimension),
        required=False)
    form.widget(dimension=BlockDataGridFieldFactory)

    # # # # # # # # # # # # # # #
    # Inscriptions & Markings   #
    # # # # # # # # # # # # # # #
    model.fieldset('inscriptionsMarkings_inscriptionsAndMarkings', label=_(u'Inscriptions and markings'), 
        fields=['inscription', 'physical_description']
    )

    inscription = ListField(title=_(u'Inscriptions and markings'),
        value_type=DictRow(title=_(u'Inscriptions and markings'), schema=IInscription),
        required=False)
    form.widget(inscription=BlockDataGridFieldFactory)
    
    # Physical Description
    physical_description = schema.Text(
        title=_(u'Physical description'),
        required=False
    )

    
    # # # # # # # # #
    # Associations  #      
    # # # # # # # # # 
    model.fieldset('associations', label=_(u'Associations'), 
        fields=["associated_subject", "associated_period", "associated_person"]
    )

    associated_subject = ListField(title=_(u'Associated subject'),
        value_type=DictRow(title=_(u'Associated subject'), schema=IAssociatedSubject),
        required=False)
    form.widget(associated_subject=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('associated_subject')

    associated_period = ListField(title=_(u'Associated period'),
        value_type=DictRow(title=_(u'Associated period'), schema=IAssociatedPeriod),
        required=False)
    form.widget(associated_period=BlockDataGridFieldFactory)

    associated_person = ListField(title=_(u'Associated person/institution'),
        value_type=DictRow(title=_(u'Associated person/institution'), schema=IAssociatedPerson),
        required=False)
    form.widget(associated_person=BlockDataGridFieldFactory)


    # # # # # # # # #
    # Notes         #      
    # # # # # # # # # 
    model.fieldset('notes', label=_(u'notes'), 
        fields=["content_motif", "notes"]
    )

    content_motif = ListField(title=_(u'More of the same motive'),
        value_type=DictRow(title=_(u'More of the same motive'), schema=IMotif),
        required=False)
    form.widget(content_motif=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('content_motif')


    notes = ListField(title=_(u'Notes'),
        value_type=DictRow(title=_(u'Notes'), schema=INotes),
        required=False)
    form.widget(notes=BlockDataGridFieldFactory)

    # # # # # # # # # # #
    # Location          #       
    # # # # # # # # # # #
    model.fieldset('location', label=_(u'location'), 
        fields=["current_location"]
    )

    current_location = ListField(title=_(u'Location'),
        value_type=DictRow(title=_(u'Location'), schema=ILocation),
        required=False)
    form.widget(current_location=BlockDataGridFieldFactory)
    

    # # # # # # # # # #
    # Related objects #
    # # # # # # # # # #

    model.fieldset('related_objects', label=_(u'Related Objects'), 
        fields=['related_objects']
    )

    related_objects = RelationList(
        title=_(u'Related Object'),
        required=False
    )
    

    # # # # # # # # # # # # #
    # Documentation         #      
    # # # # # # # # # # # # #
    model.fieldset('documentation', label=_(u'Documentation'), 
        fields=["documentation"]
    )

    documentation = ListField(title=_(u'Documentation'),
        value_type=DictRow(title=_(u'Documentation'), schema=IDocumentation_reference),
        required=False)
    form.widget(documentation=BlockDataGridFieldFactory)

    # # # # # # # # #
    # Exhibitions   #
    # # # # # # # # #
    model.fieldset('exhibitions', label=_(u'Exhibitions'), 
        fields=['exhibition', 'exhibitions']
    )

    exhibitions = ListField(title=_(u'Exhibitions'),
        value_type=DictRow(title=_(u'Exhibitions'), schema=IExhibition),
        required=False)
    form.widget(exhibitions=BlockDataGridFieldFactory)

    exhibition = RelationList(
        title=_(u'Exhibition name'),
        required=False
    )


# # # # # # # # # # # # #
# Object declaration    #
# # # # # # # # # # # # #

class Object(Container):
    grok.implements(IObject)
    pass

