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
from .variables import PERSON_INSTITUTION_FOLDER

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

        args['name'] = self.name
        args['value'] = self.value

        args.setdefault('pattern_options', {})

        field_name = self.field and self.field.__name__ or None

        context = self.context
        # We need special handling for AddForms
        if IAddForm.providedBy(getattr(self, 'form')):
            context = self.form

        vocabulary_name = self.vocabulary
        field = None

        args['pattern_options']['maximumSelectionSize'] = 1
        field = self.field.value_type
        
        #if IChoice.providedBy(self.field):
        #    args['pattern_options']['maximumSelectionSize'] = 1
        #    field = self.field
        #elif ICollection.providedBy(self.field):
        #    field = self.field.value_type


        if not vocabulary_name and field is not None:
            vocabulary_name = field.vocabularyName

        args['pattern_options'] = dict_merge(
            get_ajaxselect_options(context, args['value'], self.separator,
                                   vocabulary_name, self.vocabulary_view,
                                   field_name),
            args['pattern_options'])

        if field and getattr(field, 'vocabulary', None):
            form_url = self.request.getURL()
            source_url = "%s/++widget++%s/@@getSource" % (form_url, self.name)
            args['pattern_options']['vocabularyUrl'] = source_url

        # ISequence represents an orderable collection
        if ISequence.providedBy(self.field) or self.orderable:
            args['pattern_options']['orderable'] = True

        return args

class SimpleRelatedItemsWidget(RelatedItemsWidget):
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
        args = super(SimpleRelatedItemsWidget, self)._base_args()

        """args['name'] = self.name
        args['value'] = self.value
        args.setdefault('pattern_options', {})

        field = None
        field = self.field
        args['pattern_options']['maximumSelectionSize'] = 1

        vocabulary_name = self.vocabulary
        if not vocabulary_name:
            if field is not None and field.vocabularyName:
                vocabulary_name = field.vocabularyName
            else:
                vocabulary_name = 'plone.app.vocabularies.Catalog'

        field_name = self.field and self.field.__name__ or None
        args['pattern_options'] = dict_merge(
            get_relateditems_options(self.context, args['value'],
                                     self.separator, vocabulary_name,
                                     self.vocabulary_view, field_name,
                                     ),
            args['pattern_options'])

        args['pattern_options']['selectableTypes'] = ['PersonOrInstitution']
        
        #args['pattern_options']['basePath'] = '/nl/personen-en-instellingen/personen-en-instellingen'
        #args['pattern_options']['baseCriteria'] = [{
        #    'i': 'path',
        #    'o': 'plone.app.querystring.operation.string.path',
        #    'v': '/nl/personen-en-instellingen/personen-en-instellingen'
        #}]

        args['pattern_options']['baseCriteria'] = [{
            'i': 'portal_type',
            'o': 'plone.app.querystring.operation.selection.is',
            'v': 'PersonOrInstitution'
        }]

        if not self.vocabulary:  # widget vocab takes precedence over field
            if field and getattr(field, 'vocabulary', None):
                form_url = self.request.getURL()
                source_url = "%s/++widget++%s/@@getSource" % (
                    form_url, self.name)
                args['pattern_options']['vocabularyUrl'] = source_url
        """

        args['pattern_options']['maximumSelectionSize'] = 1
        args['pattern_options']['selectableTypes'] = ['PersonOrInstitution']
        args['pattern_options']['baseCriteria'] = [{
            'i': 'portal_type',
            'o': 'plone.app.querystring.operation.selection.is',
            'v': 'PersonOrInstitution'
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

