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
        args['pattern_options']['maximumSelectionSize'] = 1
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

