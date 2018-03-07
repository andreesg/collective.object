#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface
from collective.object import MessageFactory as _
from zope.component import adapts

from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from plone.directives import form
from plone.app.z3cform.widget import AjaxSelectFieldWidget, DatetimeFieldWidget

from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList, Relation

import datetime
from five import grok

class IThemeSpecific(Interface):
    """ Marker interface that defines a Zope 3 Interface.
    """

class IListField(Interface):
    pass

 
class IListRelatedField(Interface):
    pass   

class ListField(schema.List):
    grok.implements(IListField)
    """We need to have a unique class for the field list so that we
    can apply a custom adapter."""
    pass

class ListRelatedField(schema.List):
    grok.implements(IListRelatedField)
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

class IObjectName(form.Schema):
    name = schema.TextLine(title=_(u'Object name'), required=False)

class IProduction(Interface):
    date_start = schema.TextLine(title=_(u'Date start'), required=False)
    date_start_precision = schema.TextLine(title=_(u'Date start precision'), required=False)
    date_end = schema.TextLine(title=_(u'Date end'), required=False)
    date_end_precision = schema.TextLine(title=_(u'Date end precision'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

class ICreator(Interface):
    name = schema.TextLine(title=_(u'Name'), required=False)
    role = schema.TextLine(title=_(u'Role'), required=False)
    qualifier = schema.TextLine(title=_(u'Qualifier'), required=False)
    birth_place = schema.TextLine(title=_(u'Birth place'), required=False)
    death_place = schema.TextLine(title=_(u'Death place'), required=False)
    
    birth_date_start = schema.TextLine(title=_(u'Birth date start'), required=False)
    birth_date_end = schema.TextLine(title=_(u'Birth date end'), required=False)
    birth_date_precision = schema.TextLine(title=_(u'Birth date precision'), required=False)

    death_date_start = schema.TextLine(title=_(u'Death date start'), required=False)
    death_date_end = schema.TextLine(title=_(u'Death date end'), required=False)
    death_date_precision = schema.TextLine(title=_(u'Death date precision '), required=False)

    url = schema.TextLine(title=_(u'URL'), required=False)


class IProductionNotes(Interface):
    notes = schema.TextLine(title=_(u'Notes'), required=False)

class ITechnique(Interface):
    technique = schema.TextLine(title=_(u'Technique'), required=False)

class IMaterial(Interface):
    material = schema.TextLine(title=_(u'Material'), required=False)

class IDimension(Interface):
    value = schema.TextLine(title=_(u'Value'), required=False)
    unit = schema.TextLine(title=_(u'Unit'), required=False)
    part = schema.TextLine(title=_(u'Part'), required=False)
    type = schema.TextLine(title=_(u'Type'), required=False)
    precision = schema.TextLine(title=_(u'Precision'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

class IInscription(Interface):
    type = schema.TextLine(title=_(u'Type'), required=False)
    position = schema.TextLine(title=_(u'Position'), required=False)
    method = schema.TextLine(title=_(u'Method'), required=False)
    content = schema.TextLine(title=_(u'Content'), required=False)
    description = schema.TextLine(title=_(u'Description'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

class IAcquisition(form.Schema):
    method = schema.TextLine(title=_(u'Method'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)
    date_precision = schema.TextLine(title=_(u'Precision'), required=False)

# Associations
class IAssociatedSubject(Interface):
    subject = schema.TextLine(title=_(u'Subject'), required=False)
    association = schema.TextLine(title=_(u'Association'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

class IAssociatedPeriod(Interface):
    period = schema.TextLine(title=_(u'Period'), required=False)

## Associations
class IAssociatedPerson(Interface):
    person = schema.TextLine(title=_(u'Person'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

class ICollection(Interface):
    term = schema.TextLine(title=_(u'Collection'), required=False)

class INotes(Interface):
    note = schema.TextLine(title=_(u'Notes'), required=False)
    
