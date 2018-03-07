from plone.indexer.decorator import indexer
from .object import IObject
import datetime
from z3c.relationfield.interfaces import IRelationList, IRelationValue


@indexer(IObject)
def object_number(object, **kw):
    try:
        if hasattr(object, 'object_number'):
            value = object.object_number
            if value:
                return value.lower()
            else:
                return ""
        else:
            return ""
    except:
        return ""

@indexer(IObject)
def identification_objectNumber(object, **kw):
    try:
        if hasattr(object, 'object_number'):
            value = object.object_number
            if value:
                return value.lower()
            else:
                return ""
        else:
            return ""
    except:
        return ""

@indexer(IObject)
def object_priref(object, **kw):
    try:
        if hasattr(object, 'priref'):
            value = object.priref
            if value:
                return value.lower()
            else:
                return ""
        else:
            return ""
    except:
        return ""







