
from plone.indexer.decorator import indexer
from .object import IObject

@indexer(IObject)
def identification_objectName_category(object, **kw):
    if hasattr(object, 'identification_objectName_category'):
        return object.identification_objectName_category
    else:
        return []

@indexer(IObject)
def identification_objectName_objectname(object, **kw):
    if hasattr(object, 'identification_objectName_objectname'):
        object_names = []
        items = object.identification_objectName_objectname
        if items != None:
            for item in items:
                name = item['name']
                if name:
                    object_names.append(name)
        return object_names
    else:
        return []