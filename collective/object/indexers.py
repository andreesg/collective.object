
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
                if item['name'] != None:
                    for name in item['name']:
                        if name:
                            object_names.append(name)
        return object_names
    else:
        return []

@indexer(IObject)
def productionDating_production_productionRole(object, **kw):
    if hasattr(object, 'productionDating_production_productionRole'):
        roles = []
        items = object.productionDating_productionDating
        if items != None:
            for item in items:
                for role in item['role']:
                    if role:
                        roles.append(role)
        return roles
    else:
        return []

@indexer(IObject)
def productionDating_production_productionPlace(object, **kw):
    if hasattr(object, 'productionDating_production_productionPlace'):
        places = []
        items = object.productionDating_productionDating
        if items != None:
            for item in items:
                if item['place'] != None:
                    for place in item['place']:
                        if place:
                            places.append(place)
        return places
    else:
        return []

@indexer(IObject)
def productionDating_production_schoolStyle(object, **kw):
    if hasattr(object, 'productionDating_production_schoolstyle'):
        styles = []
        items = object.productionDating_production_schoolstyle
        if items != None:
            for item in items:
                if item['term'] != None:
                    for term in item['term']:
                        if term:
                            styles.append(term)
        return styles
    else:
        return []