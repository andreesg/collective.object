#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface
from collective.object import MessageFactory as _
from ..utils.vocabularies import _createPriorityVocabulary, _createInsuranceTypeVocabulary
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

priority_vocabulary = SimpleVocabulary(list(_createPriorityVocabulary()))
insurance_type_vocabulary = SimpleVocabulary(list(_createInsuranceTypeVocabulary()))

class ListField(schema.List):
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

class IKeyword(Interface):
    part = schema.TextLine(title=_(u'Part'), required=False)
    aspect = schema.TextLine(title=_(u'Aspect'), required=False)
    keyword = schema.TextLine(title=_(u'Keyword'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)

class ITechnique(Interface):
    part = schema.TextLine(title=_(u'Part'), required=False)
    technique = schema.TextLine(title=_(u'Technique'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)

class IMaterial(Interface):
    part = schema.TextLine(title=_(u'Part'), required=False)
    material = schema.TextLine(title=_(u'Material'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)

class IDimension(Interface):
    part = schema.TextLine(title=_(u'Part'), required=False)
    dimension = schema.TextLine(title=_(u'Dimension'), required=False)
    value = schema.TextLine(title=_(u'Value'), required=False)
    unit = schema.TextLine(title=_(u'Unit'), required=False)
    precision = schema.TextLine(title=_(u'Precision'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)

class IPeriod(Interface):
    period = schema.TextLine(title=_(u'Period'), required=False)
    date_early = schema.TextLine(title=_(u'Date (early)'), required=False)
    date_early_precision = schema.TextLine(title=_(u'Precision'), required=False)
    date_late = schema.TextLine(title=_(u'Date (late)'), required=False)
    date_late_precision = schema.TextLine(title=_(u'Precision'), required=False)

## Condition & Conservation Interfaces
class ICompleteness(Interface):
    completeness = schema.TextLine(title=_(u'Completeness'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)
    checked_by = schema.TextLine(title=_(u'Checked by'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)

class ICondition(Interface):
    part = schema.TextLine(title=_(u'Part'), required=False)
    condition = schema.TextLine(title=_(u'Condition'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)
    checked_by = schema.TextLine(title=_(u'Checked by'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)

class IEnvCondition(Interface):
    preservation_form = schema.TextLine(title=_(u'Preservation form'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)

class IConsRequest(Interface):
    treatment = schema.TextLine(title=_(u'Treatment'), required=False)
    requester = schema.TextLine(title=_(u'Requester'), required=False)
    reason = schema.TextLine(title=_(u'Reason'), required=False)
    status = schema.TextLine(title=_(u'Status'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)

## Inscriptions and Markings

class IInscription(Interface):
    type = schema.TextLine(title=_(u'Type'), required=False)
    position = schema.TextLine(title=_(u'Position'),required=False)
    method = schema.TextLine(title=_(u'Method'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)
    creator = schema.TextLine(title=_(u'Creator'), required=False)
    creator_role = schema.TextLine(title=_(u'Role'), required=False)
    content = schema.TextLine(title=_(u'Content'), required=False)
    description = schema.TextLine(title=_(u'Description'), required=False)
    interpretation = schema.TextLine(title=_(u'Interpretation'), required=False)
    language = schema.TextLine(title=_(u'Language'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)

# Value & Insurance
class IValuation(Interface):
    value = schema.TextLine(title=_(u'Value'), required=False)
    curr = schema.TextLine(title=_(u'Curr.'), required=False)
    valuer = schema.TextLine(title=_(u'Valuer'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)
    reference = schema.TextLine(title=_(u'Reference'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)

class IInsurance(Interface):
    type = schema.Choice(
        vocabulary=insurance_type_vocabulary,
        title=_(u'Type'),
        required=False
    )
    value = schema.TextLine(title=_(u'Value'), required=False)
    curr = schema.TextLine(title=_(u'Curr.'), required=False)
    valuer = schema.TextLine(title=_(u'Valuer'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)
    policy_number = schema.TextLine(title=_(u'Policy number'), required=False)
    insurance_company = schema.TextLine(title=_(u'Insurance company'), required=False)
    confirmation_date = schema.TextLine(title=_(u'Confirmation date'), required=False)
    renewal_date = schema.TextLine(title=_(u'Renewal date'), required=False)
    reference = schema.TextLine(title=_(u'Reference'), required=False)
    conditions = schema.TextLine(title=_(u'Conditions'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)

# Aquisition
class IFunding(Interface):
    amount = schema.TextLine(title=_(u'Amount'), required=False)
    curr = schema.TextLine(title=_(u'Curr.'), required=False)
    source = schema.TextLine(title=_(u'Source'), required=False)
    provisos = schema.TextLine(title=_(u'Provisos'), required=False)

class IDocumentation(Interface):
    description = schema.TextLine(title=_(u'Description'), required=False)
    reference = schema.TextLine(title=_(u'Reference'), required=False)

# Location
class ICurrentLocation(Interface):
    start_date = schema.TextLine(title=_(u'Start date'), required=False)
    end_date = schema.TextLine(title=_(u'End date'), required=False)
    location_type = schema.TextLine(title=_(u'Location type'), required=False)
    location = schema.TextLine(title=_(u'Location'), required=False)
    fitness = schema.TextLine(title=_(u'Fitness'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)

class ILocationChecks(Interface):
    date = schema.TextLine(title=_(u'Date'), required=False)
    checked_by = schema.TextLine(title=_(u'Checked by'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)

# Notes
class INotes(Interface):
	notes = schema.Text(title=_(u'Notes'), required=False)

class IFreeFields(Interface):
	date = schema.TextLine(title=_(u'Date'), required=False)
	type = schema.TextLine(title=_(u'Type'), required=False)
	confidential = schema.TextLine(title=_(u'Confidential'), required=False)
	content = schema.TextLine(title=_(u'Content'), required=False)

# Labels
class ILabel(Interface):
    date = schema.TextLine(title=_(u'Date'), required=False)
    text = schema.Text(title=_(u'Text'), required=False)
