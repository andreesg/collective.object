
from plone.indexer.decorator import indexer
from .object import IObject

# TODO: code needs to be moved to the correct product
from collective.personOrInstitution.personOrInstitution import IPersonOrInstitution
#from collective.archive.archive import IArchive
from collective.treatment.treatment import ITreatment
from collective.outgoingLoan.outgoingLoan import IOutgoingLoan
from collective.incomingLoan.incomingLoan import IIncomingLoan
from collective.objectentry.objectentry import IObjectEntry


from z3c.relationfield.interfaces import IRelationList, IRelationValue


@indexer(IObject)
def identification_objectName_category(object, **kw):
    try:
        if hasattr(object, 'identification_objectName_category'):
            return object.identification_objectName_category
        else:
            return []
    except:
        return []

@indexer(IObject)
def identification_objectName_objectname(object, **kw):
    try:
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
    except:
        return []

@indexer(IObject)
def identification_objectName_objectname_type(object, **kw):
    try:
        if hasattr(object, 'identification_objectName_objectname'):
            object_names = []
            items = object.identification_objectName_objectname
            if items != None:
                for item in items:
                    if item['types'] != None:
                        for name in item['types']:
                            if name:
                                object_names.append(name)
            return object_names
        else:
            return []
    except:
        return []

@indexer(IObject)
def productionDating_production_productionRole(object, **kw):
    try:
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
    except:
        return []

@indexer(IObject)
def productionDating_production_productionPlace(object, **kw):
    try:
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
    except:
        return []

@indexer(IObject)
def productionDating_production_schoolStyle(object, **kw):
    try:
        if hasattr(object, 'productionDating_production_schoolStyles'):
            return object.productionDating_production_schoolStyles
        else:
            return []
    except:
        return []

@indexer(IObject)
def fieldCollection_habitatStratigraphy_habitats(object, **kw):
    try:
        if hasattr(object, 'fieldCollection_habitatStratigraphy_habitats'):
            return object.fieldCollection_habitatStratigraphy_habitats
        else:
            return []
    except:
        return []

@indexer(IObject)
def productionDating__production_periods(object, **kw):
    try:
        if hasattr(object, 'productionDating_production_periods'):
            return object.productionDating_production_periods
        else:
            return []
    except:
        return []

@indexer(IObject)
def physicalCharacteristics_technique(object, **kw):
    try:
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
    except:
        return []

@indexer(IObject)
def physicalCharacteristics_material(object, **kw):
    try:
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
    except:
        return []

@indexer(IObject)
def physicalCharacteristics_dimension(object, **kw):
    try:
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
    except:
        return []


@indexer(IObject)
def physicalCharacteristics_dimensions_unit(object, **kw):
    try:
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
    except:
        return []

@indexer(IObject)
def iconography_generalSearchCriteria_generalThemes(object, **kw):
    try:
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
    except:
        return []


@indexer(IObject)
def iconography_generalSearchCriteria_specificThemes(object, **kw):
    try:
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
    except:
        return []


@indexer(IObject)
def iconography_contentSubjects(object, **kw):
    try:
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

    except:
        return []

@indexer(IObject)
def inscriptionsMarkings_inscriptionsAndMarkings_role(object, **kw):
    try:
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
    except:
        return []

@indexer(IObject)
def inscriptionsMarkings_inscriptionsAndMarkings_type(object, **kw):
    try:
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
    except:
        return []

@indexer(IObject)
def inscriptionsMarkings_inscriptionsAndMarkings_script(object, **kw):
    try:
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
    except:
        return []

@indexer(IObject)
def associations_associatedSubjects_subject(object, **kw):
    try:
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
    except:
        return []

@indexer(IObject)
def associations__associatedSubjects_association(object, **kw):
    try:
        if hasattr(object, 'associations_associatedSubjects'):
            terms = []
            try:
                items = object.associations_associatedSubjects
                if items != None:
                    for item in items:
                        if item['associations'] != None:
                            for term in item['associations']:
                                if term:
                                    terms.append(term)
            except:
                return []
            return terms
        else:
            return []
    except:
        return []

@indexer(IObject)
def associations_associatedSubjects_period(object, **kw):
    try:
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
    except:
        return []

@indexer(IObject)
def valueInsurance_valuations_currency(object, **kw):
    try:
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
    except:
        return []

@indexer(IObject)
def conditionConservation_conditions_condition(object, **kw):
    try:
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
    except:
        return []

@indexer(IObject)
def conditionConservation_preservationForm(object, **kw):
    try:
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
    except:
        return []

@indexer(IObject)
def acquisition_methods(object, **kw):
    try:
        if hasattr(object, 'acquisition_methods'):
            return object.acquisition_methods
        else:
            return []
    except:
        return []


@indexer(IObject)
def acquisition_places(object, **kw):
    try:
        if hasattr(object, 'acquisition_places'):
            return object.acquisition_places
        else:
            return []
    except:
        return []

@indexer(IObject)
def ownershipHistory_history_exchangeMethod(object, **kw):
    try:
        if hasattr(object, 'ownershipHistory_history_exchangeMethod'):
            return object.ownershipHistory_history_exchangeMethod
        else:
            return []
    except:
        return []

@indexer(IObject)
def identification_identification_objectNumber(object, **kw):
    try:
        if hasattr(object, 'identification_identification_objectNumber'):
            value = object.identification_identification_objectNumber
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
        if hasattr(object, 'identification_identification_objectNumber'):
            value = object.identification_identification_objectNumber
            if value:
                return value.lower()
            else:
                return ""
        else:
            return ""
    except:
        return ""

@indexer(IObject)
def ownershipHistory_history_place(object, **kw):
    try:
        if hasattr(object, 'ownershipHistory_history_place'):
            return object.ownershipHistory_history_place
        else:
            return []
    except:
        return []

@indexer(IObject)
def location_normalLocation_normalLocation(object, **kw):
    try:
        if hasattr(object, 'location_normalLocation_normalLocation'):
            return object.location_normalLocation_normalLocation
        else:
            return []
    except:
        return []


@indexer(IObject)
def location_currentLocation(object, **kw):
    try:
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
    except:
        return []


@indexer(IObject)
def fieldCollection_fieldCollection_collector_role(object, **kw):
    try:
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
    except:
        return []

@indexer(IObject)
def fieldCollection_fieldCollection_method(object, **kw):
    try:
        if hasattr(object, 'fieldCollection_fieldCollection_methods'):
            return object.fieldCollection_fieldCollection_methods
        else:
            return []
    except:
        return []

@indexer(IObject)
def fieldCollection_fieldCollection_place(object, **kw):
    try:
        if hasattr(object, 'fieldCollection_fieldCollection_places'):
            return object.fieldCollection_fieldCollection_places
        else:
            return []
    except:
        return []

@indexer(IObject)
def fieldCollection_fieldCollection_event(object, **kw):
    try:
        if hasattr(object, 'fieldCollection_fieldCollection_events'):
            return object.fieldCollection_fieldCollection_events
        else:
            return []
    except:
        return []

@indexer(IObject)
def fieldCollection_fieldCollection_placeFeature(object, **kw):
    try:
        if hasattr(object, 'fieldCollection_fieldCollection_placeFeatures'):
            return object.fieldCollection_fieldCollection_placeFeatures
        else:
            return []
    except:
        return []

@indexer(IObject)
def fieldCollection_habitatStratigraphy_stratigraphy(object, **kw):
    try:
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
    except:
        return []

@indexer(IObject)
def fieldCollection__fieldCollection_placeCodeType(object, **kw):
    try:
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
    except:
        return []


@indexer(IObject)
def numbersRelationships__relationshipsWithOtherObjects_relatedObjects_association(object, **kw):
    try:
        if hasattr(object, 'numbersRelationships_relationshipsWithOtherObjects_relatedObjects'):
            try:
                terms = []
                items = object.numbersRelationships_relationshipsWithOtherObjects_relatedObjects
                if items != None:
                    for item in items:
                        if item['associations'] != None:
                            for term in item['associations']:
                                if term:
                                    terms.append(term)
                return terms
            except:
                return []
        else:
            return []
    except:
        return []

@indexer(IObject)
def fieldCollection__fieldCollection_placeCode(object, **kw):
    try:
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
    except:
        return []

@indexer(IObject)
def physicalCharacteristics__keyword_aspect(object, **kw):
    try:
        if hasattr(object, 'physicalCharacteristics_keyword'):
            terms = []
            items = object.physicalCharacteristics_keyword
            if items != None:
                for item in items:
                    if item['aspect'] != None:
                        for term in item['aspect']:
                            if term:
                                terms.append(term)
            return terms
        else:
            return []
    except:
        return []

@indexer(IObject)
def physicalCharacteristics__keyword_keyword(object, **kw):
    try:
        if hasattr(object, 'physicalCharacteristics_keyword'):
            terms = []
            items = object.physicalCharacteristics_keyword
            if items != None:
                for item in items:
                    if item['keyword'] != None:
                        for term in item['keyword']:
                            if term:
                                terms.append(term)
            return terms
        else:
            return []
    except:
        return []


@indexer(IObject)
def identification__identification_collections(object, **kw):
    try:
        if hasattr(object, 'identification_identification_collections'):
            return object.identification_identification_collections
        else:
            return []
    except:
        return []

@indexer(IPersonOrInstitution)
def person_priref(object, **kw):
    try:
        if hasattr(object, 'priref'):
            return object.priref
        else:
            return ""
    except:
        return ""

"""
@indexer(IArchive)
def archive_priref(object, **kw):
    try:
        if hasattr(object, 'priref'):
            return object.priref
        else:
            return ""
    except:
        return ""
"""
@indexer(ITreatment)
def treatment_priref(object, **kw):
    try:
        if hasattr(object, 'priref'):
            return object.priref
        else:
            return ""
    except:
        return ""


@indexer(IOutgoingLoan)
def outgoingloan_priref(object, **kw):
    try:
        if hasattr(object, 'priref'):
            return object.priref
        else:
            return ""
    except:
        return ""


@indexer(IIncomingLoan)
def incomingloan_priref(object, **kw):
    try:
        if hasattr(object, 'priref'):
            return object.priref
        else:
            return ""
    except:
        return ""

@indexer(IObjectEntry)
def objectentry_priref(object, **kw):
    try:
        if hasattr(object, 'priref'):
            return object.priref
        else:
            return ""
    except:
        return ""

@indexer(IObject)
def identification_taxonomy_commonName(object, **kw):
    try:
        if hasattr(object, 'identification_taxonomy'):
            terms = []

            taxonomies = object.identification_taxonomy

            if taxonomies:
                for line in taxonomies:
                    tax = line['scientific_name']
                    if tax:
                        tax_rel = tax[0]
                        if IRelationValue.providedBy(tax_rel):
                            tax_obj = tax_rel.to_object
                        elif getattr(tax_rel, 'portal_type', "") == "Taxonomie":
                            tax_obj = tax_rel
                        else:
                            continue

                        tax_title = getattr(tax_obj, 'title', '')
                        if tax_title:
                            terms.append(tax_title)
                            
                        common_name = getattr(tax_obj, 'taxonomicTermDetails_commonName', None)
                        if common_name:
                            for name in common_name:
                                new_name = name['commonName']
                                if new_name:
                                    terms.append(new_name)

            final_terms = " ".join(terms)
            return final_terms
        else:
            return []
    except:
        return []

@indexer(IObject)
def productionDating_productionDating_maker(object, **kw):
    try:
        if hasattr(object, 'productionDating_productionDating'):
            terms = []
            production = object.productionDating_productionDating
            for line in production:
                if 'makers' in line:
                    makers = line['makers']
                    for maker in makers:
                        if IRelationValue.providedBy(maker):
                            maker_obj = maker.to_object
                            title = getattr(maker_obj, 'title', "")
                            titles = title.split()
                            terms.extend(titles)
                        elif getattr(maker, 'portal_type', "") == "PersonOrInstitution":
                            title = getattr(maker, 'title', "")
                            titles = title.split()
                            terms.extend(titles)
                        else:
                            continue
                            
            final_terms = " ".join(terms)
            return final_terms
        else:
            return ""
    except:
        return ""






