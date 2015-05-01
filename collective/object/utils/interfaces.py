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

# Identification
class ICollection(Interface):
    term = schema.TextLine(title=_(u'Collection'), required=False)

class IObjectName(Interface):
    name = schema.TextLine(title=_(u'Object name'), required=False)
    type = schema.TextLine(title=_(u'Type'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)

class IObjectCategory(Interface):
    term = schema.TextLine(title=_(u'Object Category'), required=False)

class IOtherName(Interface):
    name = schema.TextLine(title=_(u'Other name'), required=False)
    type = schema.TextLine(title=_(u'Type'), required=False)

class ITaxonomyRank(Interface):
    text = schema.TextLine(title=_(u'Taxonomy rank'), required=False)

class ITaxonomy(Interface):
    rank = schema.TextLine(title=_(u'Taxonomy rank'), required=False)
    scientific_name = schema.TextLine(title=_(u'Scient. name'), required=False)
    common_name = schema.TextLine(title=_(u'Common name'), required=False)

class IDeterminer(Interface):
    name = schema.TextLine(title=_(u'Determiner'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)


# Physical Characteristics
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

## Production & Dating
class IProduction(Interface):
    maker = schema.TextLine(title=_(u'Maker'), required=False)
    qualifier = schema.TextLine(title=_(u'Qualifier'), required=False)
    role = schema.TextLine(title=_(u'Role'), required=False)
    place = schema.TextLine(title=_(u'Place'), required=False)
    production_notes = schema.TextLine(title=_(u'Production notes'), required=False)

class ISchool(Interface):
    term = schema.TextLine(title=_(u'School / style'), required=False)

class IFrame(Interface):
    frame = schema.TextLine(title=_(u'Frame'), required=False)
    detail = schema.TextLine(title=_(u'Detail'), required=False)

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
    role = schema.TextLine(title=_(u'Role'), required=False)
    content = schema.TextLine(title=_(u'Content'), required=False)
    description = schema.TextLine(title=_(u'Description'), required=False)
    interpretation = schema.TextLine(title=_(u'Interpretation'), required=False)
    language = schema.TextLine(title=_(u'Language'), required=False)
    script = schema.TextLine(title=_(u'Script'), required=False)
    transliteration = schema.TextLine(title=_(u'Transliteration'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)

## Numbers/relationships
class INumbers(Interface):
    type = schema.TextLine(title=_(u'Type'), required=False)
    number = schema.TextLine(title=_(u'Number'), required=False)
    institution = schema.TextLine(title=_(u'Institution'), required=False)
    date = schema.TextLine(title=_(u'Date'), required=False)

class IParts(Interface):
    parts = schema.TextLine(title=_(u'Parts'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)

class IRelatedObject(Interface):
    relatedObject = schema.TextLine(title=_(u'Related object'), required=False)
    association = schema.TextLine(title=_(u'Association'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)

class IDigitalReferences(Interface):
    type = schema.TextLine(title=_(u'Type'), required=False)
    reference = schema.TextLine(title=_(u'Reference'), required=False)
     
## Documentation

class IDocumentationDocumentation(Interface):
    article = schema.TextLine(title=_(u'Article'), required=False)
    title = schema.TextLine(title=_(u'Title'), required=False)
    author = schema.TextLine(title=_(u'Author'), required=False)
    pageMark = schema.TextLine(title=_(u'Page mark'), required=False)
    shelfMark = schema.TextLine(title=_(u'Shelf mark'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)


## Associations
class IAssociatedPersonInstitution(Interface):
    association = schema.TextLine(title=_(u'Association'), required=False)
    nameType = schema.TextLine(title=_(u'Name Type'), required=False)
    name = schema.TextLine(title=_(u'Name'), required=False)
    startDate = schema.TextLine(title=_(u'Start date'), required=False)
    endDate = schema.TextLine(title=_(u'End date'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)
    
class IAssociatedSubject(Interface):
    association = schema.TextLine(title=_(u'Association'), required=False)
    subjectType = schema.TextLine(title=_(u'Subject type'), required=False)
    subject = schema.TextLine(title=_(u'Subject'), required=False)
    taxonomicRank = schema.TextLine(title=_(u'Taxonomic rank'), required=False)
    scientificName = schema.TextLine(title=_(u'Scientific name'), required=False)
    properName = schema.TextLine(title=_(u'Proper name'), required=False)
    startDate = schema.TextLine(title=_(u'Start date'), required=False)
    endDate = schema.TextLine(title=_(u'End date'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)

class IAssociatedPeriod(Interface):
    association = schema.TextLine(title=_(u'Association'), required=False)
    period = schema.TextLine(title=_(u'Period'), required=False)
    startDate = schema.TextLine(title=_(u'Start date'), required=False)
    endDate = schema.TextLine(title=_(u'End date'), required=False)
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
    text = schema.TextLine(title=_(u'Text'), required=False)


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
    nameType = schema.TextLine(title=_(u'Name type'), required=False)
    name = schema.TextLine(title=_(u'Name'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)

class IIconographyContentSubject(Interface):
    position = schema.TextLine(title=_(u'Position'), required=False)
    subjectType = schema.TextLine(title=_(u'Subject type'), required=False)
    subject = schema.TextLine(title=_(u'Subject'), required=False)
    taxonomicRank = schema.TextLine(title=_(u'Taxonomic rank'), required=False)
    scientificName = schema.TextLine(title=_(u'Scientific name'), required=False)
    properName = schema.TextLine(title=_(u'Proper name'), required=False)
    identifier = schema.TextLine(title=_(u'Identifier'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)

class IIconographyContentPeriodDate(Interface):
    position = schema.TextLine(title=_(u'Position'), required=False)
    period = schema.TextLine(title=_(u'Period'), required=False)
    startDate = schema.TextLine(title=_(u'Start date'), required=False)
    endDate = schema.TextLine(title=_(u'End date'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)

