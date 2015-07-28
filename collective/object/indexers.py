
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
def physicalCharacteristics_dimensions_unit(object, **kw):
    return []
    if hasattr(object, 'physicalCharacteristics_dimension'):
        terms = []
        items = object.physicalCharacteristics_dimension
        if items != None:
            for item in items:
                if item['unit'] != None:
                    for term in item['unit']:
                        if term:
                            terms.append(term)
        return terms
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

@indexer(IObject)
def inscriptionsMarkings_inscriptionsAndMarkings_role(object, **kw):
    if hasattr(object, 'inscriptionsMarkings_inscriptionsAndMarkings'):
        terms = []
        items = object.inscriptionsMarkings_inscriptionsAndMarkings
        if items != None:
            for item in items:
                if item['role'] != None:
                    for term in item['role']:
                        if term:
                            terms.append(term)
        return terms
    else:
        return []

@indexer(IObject)
def inscriptionsMarkings_inscriptionsAndMarkings_type(object, **kw):
    if hasattr(object, 'inscriptionsMarkings_inscriptionsAndMarkings'):
        terms = []
        items = object.inscriptionsMarkings_inscriptionsAndMarkings
        if items != None:
            for item in items:
                if item['type'] != None:
                    for term in item['type']:
                        if term:
                            terms.append(term)
        return terms
    else:
        return []

@indexer(IObject)
def inscriptionsMarkings_inscriptionsAndMarkings_script(object, **kw):
    if hasattr(object, 'inscriptionsMarkings_inscriptionsAndMarkings'):
        terms = []
        items = object.inscriptionsMarkings_inscriptionsAndMarkings
        if items != None:
            for item in items:
                if item['script'] != None:
                    for term in item['script']:
                        if term:
                            terms.append(term)
        return terms
    else:
        return []

@indexer(IObject)
def associations_associatedSubjects_subject(object, **kw):
    if hasattr(object, 'associations_associatedSubjects'):
        terms = []
        items = object.associations_associatedSubjects
        if items != None:
            for item in items:
                if item['subject'] != None:
                    for term in item['subject']:
                        if term:
                            terms.append(term)
        return terms
    else:
        return []

@indexer(IObject)
def associations__associatedSubjects_association(object, **kw):
    if hasattr(object, 'associations_associatedSubjects'):
        terms = []
        items = object.associations_associatedSubjects
        if items != None:
            for item in items:
                if item['associations'] != None:
                    for term in item['associations']:
                        if term:
                            terms.append(term)
        return terms
    else:
        return []

@indexer(IObject)
def associations_associatedSubjects_period(object, **kw):
    if hasattr(object, 'associations_associatedPeriods'):
        terms = []
        items = object.associations_associatedPeriods
        if items != None:
            for item in items:
                if item['period'] != None:
                    for term in item['period']:
                        if term:
                            terms.append(term)
        return terms
    else:
        return []

@indexer(IObject)
def valueInsurance_valuations_currency(object, **kw):
    if hasattr(object, 'valueInsurance_valuations'):
        terms = []
        items = object.valueInsurance_valuations
        if items != None:
            for item in items:
                if item['curr'] != None:
                    for term in item['curr']:
                        if term:
                            terms.append(term)
        return terms
    else:
        return []

@indexer(IObject)
def conditionConservation_conditions_condition(object, **kw):
    if hasattr(object, 'conditionConservation_conditions'):
        terms = []
        items = object.conditionConservation_conditions
        if items != None:
            for item in items:
                if item['condition'] != None:
                    for term in item['condition']:
                        if term:
                            terms.append(term)
        return terms
    else:
        return []

@indexer(IObject)
def conditionConservation_preservationForm(object, **kw):
    if hasattr(object, 'conditionConservation_preservationForm'):
        terms = []
        items = object.conditionConservation_preservationForm
        if items != None:
            for item in items:
                if item['preservation_form'] != None:
                    for term in item['preservation_form']:
                        if term:
                            terms.append(term)
        return terms
    else:
        return []

@indexer(IObject)
def acquisition_methods(object, **kw):
    if hasattr(object, 'acquisition_methods'):
        return object.acquisition_methods
    else:
        return []


@indexer(IObject)
def acquisition_places(object, **kw):
    if hasattr(object, 'acquisition_places'):
        return object.acquisition_places
    else:
        return []

@indexer(IObject)
def ownershipHistory_history_exchangeMethod(object, **kw):
    if hasattr(object, 'ownershipHistory_history_exchangeMethod'):
        return object.ownershipHistory_history_exchangeMethod
    else:
        return []

@indexer(IObject)
def identification_identification_objectNumber(object, **kw):
    if hasattr(object, 'identification_identification_objectNumber'):
        return object.identification_identification_objectNumber
    else:
        return ""

@indexer(IObject)
def ownershipHistory_history_place(object, **kw):
    if hasattr(object, 'ownershipHistory_history_place'):
        return object.ownershipHistory_history_place
    else:
        return []

@indexer(IObject)
def location_normalLocation_normalLocation(object, **kw):
    if hasattr(object, 'location_normalLocation_normalLocation'):
        return object.location_normalLocation_normalLocation
    else:
        return []


@indexer(IObject)
def location_currentLocation(object, **kw):
    if hasattr(object, 'location_currentLocation'):
        terms = []
        items = object.location_currentLocation
        if items != None:
            for item in items:
                if item['location'] != None:
                    for term in item['location']:
                        if term:
                            terms.append(term)
        return terms
    else:
        return []


@indexer(IObject)
def fieldCollection_fieldCollection_collector_role(object, **kw):
    if hasattr(object, 'fieldCollection_fieldCollection_collectors'):
        terms = []
        items = object.fieldCollection_fieldCollection_collectors
        if items != None:
            for item in items:
                if item['role'] != None:
                    for term in item['role']:
                        if term:
                            terms.append(term)
        return terms
    else:
        return []

@indexer(IObject)
def fieldCollection_fieldCollection_method(object, **kw):
    if hasattr(object, 'fieldCollection_fieldCollection_methods'):
        return object.fieldCollection_fieldCollection_methods
    else:
        return []

@indexer(IObject)
def fieldCollection_fieldCollection_place(object, **kw):
    if hasattr(object, 'fieldCollection_fieldCollection_places'):
        return object.fieldCollection_fieldCollection_places
    else:
        return []

@indexer(IObject)
def fieldCollection_fieldCollection_event(object, **kw):
    if hasattr(object, 'fieldCollection_fieldCollection_events'):
        return object.fieldCollection_fieldCollection_events
    else:
        return []

@indexer(IObject)
def fieldCollection_fieldCollection_placeFeature(object, **kw):
    if hasattr(object, 'fieldCollection_fieldCollection_placeFeatures'):
        return object.fieldCollection_fieldCollection_placeFeatures
    else:
        return []

@indexer(IObject)
def fieldCollection_habitatStratigraphy_stratigraphy(object, **kw):
    if hasattr(object, 'fieldCollection_habitatStratigraphy_stratigrafie'):
        terms = []
        items = object.fieldCollection_habitatStratigraphy_stratigrafie
        if items != None:
            for item in items:
                if item['unit'] != None:
                    for term in item['unit']:
                        if term:
                            terms.append(term)
        return terms
    else:
        return []

@indexer(IObject)
def fieldCollection__fieldCollection_placeCodeType(object, **kw):
    if hasattr(object, 'fieldCollection_fieldCollection_placeCodes'):
        terms = []
        items = object.fieldCollection_fieldCollection_placeCodes
        if items != None:
            for item in items:
                if item['codeType'] != None:
                    for term in item['codeType']:
                        if term:
                            terms.append(term)
        return terms
    else:
        return []

@indexer(IObject)
def fieldCollection__fieldCollection_placeCode(object, **kw):
    if hasattr(object, 'fieldCollection_fieldCollection_placeCodes'):
        terms = []
        items = object.fieldCollection_fieldCollection_placeCodes
        if items != None:
            for item in items:
                if item['code'] != None:
                    for term in item['code']:
                        if term:
                            terms.append(term)
        return terms
    else:
        return []

@indexer(IObject)
def identification__identification_collections(object, **kw):
    if hasattr(object, 'identification_identification_collections'):
        return object.identification_identification_collections
    else:
        return []





