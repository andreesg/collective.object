#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Customise widgets
#

from plone.app.widgets.dx import AjaxSelectFieldWidget, AjaxSelectWidget, IRelatedItemsWidget, RelatedItemsWidget
from z3c.form.interfaces import IFieldWidget
from zope.interface import implementer
from z3c.form.interfaces import IAddForm
from zope.schema.interfaces import ISequence
from plone.app.widgets.utils import get_ajaxselect_options
from z3c.form.widget import FieldWidget
from plone.app.widgets.base import dict_merge
from plone.app.widgets.utils import get_relateditems_options
from .variables import PERSON_INSTITUTION_FOLDER, DEFAULT_LANGUAGE, \
                        ROOT_FOLDER, OBJECT_FOLDER, BIBLIOTHEEK_FOLDER, ARCHIVE_FOLDER, \
                        TREATMENT_FOLDER, EXHIBITION_FOLDER, INCOMINGLOAN_FOLDER, OBJECTENTRY_FOLDER, \
                        OUTGOINGLOAN_FOLDER, LOANS_FOLDER, TAXONOMY_FOLDER

CONTENTTYPE_CHOICES = {
    "makers": PERSON_INSTITUTION_FOLDER,
    "name": PERSON_INSTITUTION_FOLDER,
    "identification_identification_institutionNames": PERSON_INSTITUTION_FOLDER,
    "names": PERSON_INSTITUTION_FOLDER,
    "creators": PERSON_INSTITUTION_FOLDER,
    "creator": PERSON_INSTITUTION_FOLDER,
    "numbersRelationships_relationshipsWithOtherObjects_partOf": OBJECT_FOLDER,
    "parts": OBJECT_FOLDER,
    "relatedObject": OBJECT_FOLDER,
    "titles": BIBLIOTHEEK_FOLDER,
    "title": BIBLIOTHEEK_FOLDER,
    "number": ARCHIVE_FOLDER,
    "treatmentNumber": TREATMENT_FOLDER,
    "aquisitionFrom": PERSON_INSTITUTION_FOLDER,
    "disposal_disposal_proposedRecipient": PERSON_INSTITUTION_FOLDER,
    "disposal_disposal_recipient": PERSON_INSTITUTION_FOLDER,
    "ownershipHistory_ownership_currentOwner": PERSON_INSTITUTION_FOLDER,
    "owner": PERSON_INSTITUTION_FOLDER,
    "acquiredFrom": PERSON_INSTITUTION_FOLDER,
    "exhibitionName": EXHIBITION_FOLDER,
    "loannumber": INCOMINGLOAN_FOLDER,
    "loannumber_out": OUTGOINGLOAN_FOLDER,
    "loanNumber": LOANS_FOLDER, # Needs fix
    "transport_number": OBJECTENTRY_FOLDER,
    "authors": PERSON_INSTITUTION_FOLDER,
    "illustrators": PERSON_INSTITUTION_FOLDER,
    "partOf": BIBLIOTHEEK_FOLDER,
    "consistsOf": BIBLIOTHEEK_FOLDER,
    "objectNo": OBJECT_FOLDER,
    "copyNumber": BIBLIOTHEEK_FOLDER,
    "publisher": PERSON_INSTITUTION_FOLDER,
    "printer": PERSON_INSTITUTION_FOLDER,
    "corpAuthor": PERSON_INSTITUTION_FOLDER,
    "use": PERSON_INSTITUTION_FOLDER,
    "usedFor": PERSON_INSTITUTION_FOLDER,
    "venue": PERSON_INSTITUTION_FOLDER,
    "objectNumber": OBJECT_FOLDER,
    "broadcastingCompany": PERSON_INSTITUTION_FOLDER,
    "productionCompany": PERSON_INSTITUTION_FOLDER,
    "loanRequest_general_requester": PERSON_INSTITUTION_FOLDER,
    "loanRequest_general_contact": PERSON_INSTITUTION_FOLDER,
    "loanRequest_internalCoordination_coordinator": PERSON_INSTITUTION_FOLDER,
    "loanRequest_requestDetails_exhibition": EXHIBITION_FOLDER,
    "authoriserInternal": PERSON_INSTITUTION_FOLDER,
    "review_authoriser": PERSON_INSTITUTION_FOLDER,
    "entryNumber": OBJECTENTRY_FOLDER,
    "loanRequest_general_lender": PERSON_INSTITUTION_FOLDER,
    "general_entry_currentOwner": PERSON_INSTITUTION_FOLDER,
    "general_entry_depositor": PERSON_INSTITUTION_FOLDER,
    "general_entry_depositorContact": PERSON_INSTITUTION_FOLDER,
    "general_entry_destinationContact": PERSON_INSTITUTION_FOLDER,
    "general_entry_destination": PERSON_INSTITUTION_FOLDER,
    "shipper": PERSON_INSTITUTION_FOLDER,
    "templateForObjectData_currentOwner": PERSON_INSTITUTION_FOLDER,
    "contributor": PERSON_INSTITUTION_FOLDER,
    "taxonomicTermDetails_status_validAcceptedName": TAXONOMY_FOLDER,
    "synonym": TAXONOMY_FOLDER,
    "childName": TAXONOMY_FOLDER,
    "taxonomicTermDetails_hierarchy_parentName": TAXONOMY_FOLDER
}

# form.widget('makers', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

class AjaxSingleSelectWidget(AjaxSelectWidget):
    separator = '_'

    def _base_args(self):
        """Method which will calculate _base class arguments.
        Returns (as python dictionary):
            - `pattern`: pattern name
            - `pattern_options`: pattern options
            - `name`: field name
            - `value`: field value
        :returns: Arguments which will be passed to _base
        :rtype: dict
        """

        args = super(AjaxSingleSelectWidget, self)._base_args()
        args['pattern_options']['maximumSelectionSize'] = 1

        return args

class SimpleRelatedItemsWidget(RelatedItemsWidget):
    """RelatedItems widget for z3c.form."""

    def get_current_fieldname(self):
        fieldname = self.field.__name__
        try:
            if fieldname in ['loannumber']: # Loans exception 
                if self.field.value_type.source.selectable_filter.criteria['portal_type'][0] == 'OutgoingLoan':
                    fieldname = "loannumber_out"
        except:
            return fieldname
        return fieldname

    def _base_args(self):
        """Method which will calculate _base class arguments.
        Returns (as python dictionary):
            - `pattern`: pattern name
            - `pattern_options`: pattern options
            - `name`: field name
            - `value`: field value
        :returns: Arguments which will be passed to _base
        :rtype: dict
        """
        args = super(SimpleRelatedItemsWidget, self)._base_args()
        
        # Get current fieldname
        fieldname = self.get_current_fieldname()

        # Get request language
        context = self.request.PARENTS[0]
        language = DEFAULT_LANGUAGE
        if context:
            language = context.language

        # Get content type folder
        contenttype_folder = CONTENTTYPE_CHOICES.get(fieldname, ROOT_FOLDER)
        portal_type = contenttype_folder['portal_type']
        basePath = contenttype_folder[language]

        # Set extra settings
        args['pattern_options']['maximumSelectionSize'] = 1
        
        if basePath:
            args['pattern_options']['basePath'] = basePath
       
        if portal_type:
            args['pattern_options']['selectableTypes'] = [portal_type]
            args['pattern_options']['baseCriteria'] = [{
                'i': 'portal_type',
                'o': 'plone.app.querystring.operation.selection.is',
                'v': portal_type
            }]

        if fieldname in ['titles', 'partOf', 'consistsOf', "copyNumber", "title", "loanNumber"]:
            criteria = contenttype_folder['criteria']
            args['pattern_options']['baseCriteria'] = criteria

        return args

class TaxonomicRelatedItemsWidget(RelatedItemsWidget):
    """RelatedItems widget for z3c.form."""

    def _base_args(self):
        """Method which will calculate _base class arguments.
        Returns (as python dictionary):
            - `pattern`: pattern name
            - `pattern_options`: pattern options
            - `name`: field name
            - `value`: field value
        :returns: Arguments which will be passed to _base
        :rtype: dict
        """
        args = super(TaxonomicRelatedItemsWidget, self)._base_args()
        
        # Get request language
        context = self.request.PARENTS[0]
        language = DEFAULT_LANGUAGE
        if context:
            language = context.language

        # Get content type folder
        contenttype_folder = TAXONOMY_FOLDER
        portal_type = contenttype_folder['portal_type']
        basePath = contenttype_folder[language]
        
        # Set extra settings
        args['pattern_options']['maximumSelectionSize'] = 1
        
        if basePath:
            args['pattern_options']['basePath'] = basePath
       
        if portal_type:
            args['pattern_options']['selectableTypes'] = [portal_type]
            args['pattern_options']['baseCriteria'] = [{
                'i': 'portal_type',
                'o': 'plone.app.querystring.operation.selection.is',
                'v': portal_type
            }]

        return args

@implementer(IFieldWidget)
def AjaxSingleSelectFieldWidget(field, request, extra=None):
    if extra is not None:
        request = extra
    return FieldWidget(field, AjaxSingleSelectWidget(request))

@implementer(IFieldWidget)
def SimpleRelatedItemsFieldWidget(field, request, extra=None):
    if extra is not None:
        request = extra
    return FieldWidget(field, SimpleRelatedItemsWidget(request))

@implementer(IFieldWidget)
def TaxonomicRelatedItemsFieldWidget(field, request, extra=None):
    if extra is not None:
        request = extra
    return FieldWidget(field, TaxonomicRelatedItemsWidget(request))

