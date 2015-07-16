
from plone.indexer.decorator import indexer
from .object import IObject

@indexer(IObject)
def identification_objectName_category(object, **kw):
    if hasattr(object, 'identification_objectName_category'):
        return object.identification_objectName_category
    else:
        return []
