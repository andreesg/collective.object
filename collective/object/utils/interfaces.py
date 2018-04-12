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
from plone.autoform import directives
from plone.app.z3cform.widget import AjaxSelectFieldWidget

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

class IMotif(form.Schema):
    motif = schema.TextLine(title=_(u'More of the same motive'), required=False)

class ILocation(form.Schema):
    name = schema.TextLine(title=_(u'Location'), required=False)

class IExhibition(form.Schema):
    title = schema.TextLine(title=_(u'Title'), required=False)
    venue = schema.TextLine(title=_(u'Venue'), required=False)
    place = schema.TextLine(title=_(u'Place'), required=False)
    date_start = schema.TextLine(title=_(u'Date start'), required=False)
    date_end = schema.TextLine(title=_(u'Date end'), required=False)
    nummer_cm = schema.TextLine(title=_(u'Nummer CM'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)

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
    equivalent_name = schema.TextLine(title=_(u'Equivalent name'), required=False)
    priref = schema.TextLine(title=_(u'priref'), required=False, default=u'', missing_value=u'')
    

class IDocumentation_reference(Interface):
    title = schema.TextLine(title=_(u'Title'), required=False)
    lead_word = schema.TextLine(title=_(u'Lead word'), required=False)
    author = schema.List(title=_(u'Author'), required=False, default=[], missing_value=[], value_type=schema.TextLine())
    statement_of_responsibility = schema.TextLine(title=_(u'Statement of responsability'), required=False)
    place_of_publication = schema.TextLine(title=_(u'Place of publication'), required=False)
    year_of_publication = schema.TextLine(title=_(u'Year of publication'), required=False)
    page_references = schema.TextLine(title=_(u'Page reference'), required=False, missing_value=u'', default=u'')

    directives.widget(
        'author',
        AjaxSelectFieldWidget,
        vocabulary='collective.object.author'
    )

class IDocumentation(Interface):
    title = schema.TextLine(title=_(u'Title'), required=False)
    lead_word = schema.TextLine(title=_(u'Lead word'), required=False)
    author = schema.List(title=_(u'Author'), required=False, default=[], missing_value=[], value_type=schema.TextLine())
    statement_of_responsibility = schema.TextLine(title=_(u'Statement of responsability'), required=False)
    place_of_publication = schema.TextLine(title=_(u'Place of publication'), required=False)
    year_of_publication = schema.TextLine(title=_(u'Year of publication'), required=False)
    page_references = schema.TextLine(title=_(u'Page reference'), required=False, missing_value=u'', default=u'')

    directives.widget(
        'author',
        AjaxSelectFieldWidget,
        vocabulary='collective.object.author'
    )


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
    
