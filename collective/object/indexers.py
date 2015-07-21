
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
    if hasattr(object, 'productionDating_productionDating'):
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
    if hasattr(object, 'productionDating_productionDating'):
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


@indexer(IObject)
def physicalCharacteristics_technique(object, **kw):
    if hasattr(object, 'physicalCharacteristics_technique'):
        techniques = []
        items = object.physicalCharacteristics_technique
        if items != None:
            for item in items:
                if item['technique'] != None:
                    for term in item['technique']:
                        if term:
                            techniques.append(term)
        return techniques
    else:
        return []

@indexer(IObject)
def physicalCharacteristics_material(object, **kw):
    if hasattr(object, 'physicalCharacteristics_material'):
        materials = []
        items = object.physicalCharacteristics_material
        if items != None:
            for item in items:
                if item['material'] != None:
                    for term in item['material']:
                        if term:
                            materials.append(term)
        return materials
    else:
        return []

@indexer(IObject)
def physicalCharacteristics_dimension(object, **kw):
    if hasattr(object, 'physicalCharacteristics_dimension'):
        dimensions = []
        items = object.physicalCharacteristics_dimension
        if items != None:
            for item in items:
                if item['dimension'] != None:
                    for term in item['dimension']:
                        if term:
                            dimensions.append(term)
        return dimensions
    else:
        return []

@indexer(IObject)
def iconography_generalSearchCriteria_generalThemes(object, **kw):
    if hasattr(object, 'iconography_generalSearchCriteria_generalThemes'):
        terms = []
        items = object.iconography_generalSearchCriteria_generalThemes
        if items != None:
            for item in items:
                if item['term'] != None:
                    for term in item['term']:
                        if term:
                            terms.append(term)
        return terms
    else:
        return []


@indexer(IObject)
def iconography_generalSearchCriteria_specificThemes(object, **kw):
    if hasattr(object, 'iconography_generalSearchCriteria_specificThemes'):
        terms = []
        items = object.iconography_generalSearchCriteria_specificThemes
        if items != None:
            for item in items:
                if item['term'] != None:
                    for term in item['term']:
                        if term:
                            terms.append(term)
        return terms
    else:
        return []


@indexer(IObject)
def iconography_contentSubjects(object, **kw):
    if hasattr(object, 'iconography_contentSubjects'):
        terms = []
        items = object.iconography_contentSubjects
        if items != None:
            for item in items:
                if item['subject'] != None:
                    for term in item['subject']:
                        if term:
                            terms.append(term)
        return terms
    else:
        return []

