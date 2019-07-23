#!/usr/bin/python
# -*- coding: utf-8 -*-

from plone.indexer.decorator import indexer
from .object import IObject
import datetime
from z3c.relationfield.interfaces import IRelationList, IRelationValue
from Products.CMFPlone.utils import safe_unicode
from plone.dexterity.interfaces import IDexterityContainer
from plonetheme.centraalmuseum.browser.views import is_event_past

def find_century(year):
    if year < 0:
        return "Voor Christus"
    elif year <= 100:
        return "1e Eeuw"
    elif year % 100 == 0:
        return "%se Eeuw" %(str(year/100))
    else:
        return "%se Eeuw" %(str((year/100)+1))

def safe_value(value):
    try:
        term = None
        if isinstance(value, unicode):
            # no need to use portal encoding for transitional encoding from
            # unicode to ascii. utf-8 should be fine.
            term = value.encode('utf-8')
            return term
        else:
            return value
    except:
        return None

@indexer(IDexterityContainer)
def website_collection_exhibition_index(object, **kw):
    try:
        portal_type = getattr(object, 'portal_type', None)
        terms = []
        if portal_type in ["Event"]:
            if is_event_past(object) and '/agenda' not in object.absolute_url() and 'man-next-door' not in object.absolute_url():
                terms.append(safe_value("Alleen in het tentoonstellingsarchief"))
            else:
                terms.append(safe_value("Alleen in de website"))
        elif portal_type in ["Object"]:
            terms.append(safe_value("Alleen in de collectie"))
        else:
            terms.append(safe_value("Alleen in de website"))
        return terms
    except:
        return []

@indexer(IObject)
def object_on_display(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'in_museum'):
                value = object.in_museum
                if value and value not in ['', None, ' ']:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    except:
        return False

@indexer(IObject)
def sortable_object_number(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'object_number'):
                value = object.object_number
                if value:
                    return value.lower()
                else:
                    return ""
            else:
                return ""
        else:
            return ""
    except:
        return ""

@indexer(IObject)
def identification_objectNumber(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'object_number'):
                value = object.object_number
                if value:
                    return value.lower()
                else:
                    return ""
            else:
                return ""
        else:
            return ""
    except:
        return ""

@indexer(IObject)
def object_priref(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'priref'):
                value = object.priref
                if value:
                    return value.lower()
                else:
                    return ""
            else:
                return ""
        else:
            return ""
    except:
        return ""

@indexer(IObject)
def documentation_author(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'documentation'):
                authors = []
                items = object.documentation
                if items != None:
                    for item in items:
                        if item['author'] != None:
                            for name in item['author']:
                                value = safe_value(name)
                                if value:
                                    authors.append(value)
                return authors
            else:
                return []
        else:
            return []
    except:
        return []

@indexer(IObject)
def content_motif(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'content_motif'):
                motifs = []
                items = object.content_motif
                if items != None:
                    for item in items:
                        if item['motif'] != None:
                            value = safe_value(item['motif'])
                            if value:
                                motifs.append(value)
                return motifs
            else:
                return []
        else:
            return []
    except:
        return []

@indexer(IObject)
def content_motifs(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'content_motif'):
                terms = []
                items = object.content_motif
                if items != None:
                    for item in items:
                        if item['motif'] != None:
                            terms.append(item['motif'])
                            
                final_terms = " ".join(terms)
                return final_terms
            else:
                return ""
        else:
            return ""
    except:
        return ""


@indexer(IObject)
def association_subject(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'associated_subject'):
                terms = []
                items = object.associated_subject
                if items != None:
                    for item in items:
                        if item['subject'] != None:
                            value = safe_value(item['subject'])
                            if value:
                                terms.append(value)
                return terms
            else:
                return []
        else:
            return []
    except:
        return []

@indexer(IObject)
def creator_name(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'creator'):
                terms = []
                items = object.creator
                if items != None:
                    for item in items:
                        if item['name'] != None:
                            terms.append(item['name'])
                        if item['equivalent_name'] != None:
                            terms.append(item['equivalent_name'])

                final_terms = " ".join(terms)
                return final_terms
            else:
                return ""
        else:
            return ""
    except:
        return ""

@indexer(IObject)
def sortable_creator_name(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'creator'):
                terms = []
                items = object.creator
                if items != None:
                    for item in items:
                        if item['name'] != None:
                            value = safe_value(item['name'])
                            if value:
                                terms.append(value)
                        if item['equivalent_name'] != None:
                            value = safe_value(item['equivalent_name'])
                            if value:
                                terms.append(value)
                return terms
            else:
                return []
        else:
            return []
    except:
        return []


@indexer(IObject)
def creator_name_index(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'creator'):
                terms = []
                items = object.creator
                if items != None:
                    for item in items:
                        if item['name'] != None:
                            value = safe_value(item['name'])
                            if value:
                                terms.append(value)
                return terms
            else:
                return []
        else:
            return []
    except:
        return []

@indexer(IObject)
def label_text(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'text'):
                terms = []
                items = object.text
                all_text = items.raw
                return all_text
            else:
                return ""
        else:
            return ""
    except:
        return ""

@indexer(IObject)
def objectname(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'object_name'):
                terms = []
                items = object.object_name
                if items != None:
                    for item in items:
                        if item['name'] != None:
                            value = safe_value(item['name'])
                            if value:
                                terms.append(value)
                return terms
            else:
                return None
        else:
            return None
    except:
        return None

@indexer(IObject)
def object_person_priref(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'creator'):
                terms = []
                items = object.creator
                if items != None:
                    for item in items:
                        if item['priref'] != None:
                            terms.append(item['priref'])
                return terms
            else:
                return []
        else:
            return []
    except:
        return []

@indexer(IObject)
def technique(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'technique'):
                terms = []
                items = object.technique
                if items != None:
                    for item in items:
                        if item['technique'] != None:
                            value = safe_value(item['technique'])
                            if value:
                                terms.append(value)
                return terms
            else:
                return []
        else:
            return []
    except:
        return []

@indexer(IObject)
def material_index(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'material'):
                terms = []
                items = object.material
                if items != None:
                    for item in items:
                        if item['material'] != None:
                            value = safe_value(item['material'])
                            if value:
                                terms.append(value)
                return terms
            else:
                return []
        else:
            return []
    except:
        return []


@indexer(IObject)
def technique_index(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'technique'):
                terms = []
                items = object.technique
                if items != None:
                    for item in items:
                        if item['technique'] != None:
                            if "," in item['technique']:
                                values = [v.strip() for v in item['technique'].split(',')]
                            elif ";" in item['technique']:
                                values = [v.strip() for v in item['technique'].split(';')]
                            else:
                                values = [item['technique']]

                            for v in values:
                                value = safe_value(v)
                                if value:
                                    terms.append(value)
                return terms
            else:
                return []
        else:
            return []
    except:
        return []


@indexer(IObject)
def object_technique(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'technique'):
                terms = []
                items = object.technique
                if items != None:
                    for item in items:
                        if item['technique'] != None:
                            terms.append(item['technique'])
                
                final_terms = " ".join(terms)
                return final_terms
            else:
                return ""
        else:
            return ""
    except:
        return ""


@indexer(IObject)
def acquisition_date(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'acquisition'):
                terms = []
                items = object.acquisition
                if items != None:
                    for item in items:
                        if item['date'] != None:
                            terms.append(item['date'])

                final_terms = " ".join(terms)
                return final_terms
            else:
                return ""
        else:
            return ""
    except:
        return ""

@indexer(IObject)
def inscriptions_markings(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'inscription'):
                terms = []
                items = object.inscription
                if items != None:
                    for item in items:
                        if item['type'] != None:
                            terms.append(item['type'])
                        if item['position'] != None:
                            terms.append(item['position'])
                        if item['method'] != None:
                            terms.append(item['method'])
                        if item['date'] != None:
                            terms.append(item['date'])
                        if item['description'] != None:
                            terms.append(item['description'])
                        if item['notes'] != None:
                            terms.append(item['notes'])
                final_terms = " ".join(terms)
                return final_terms
            else:
                return ""
        else:
            return ""
    except:
        return ""


@indexer(IObject)
def acquisition_method(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'acquisition'):
                terms = []
                items = object.acquisition
                if items != None:
                    for item in items:
                        if item['method'] != None:
                            value = safe_value(item['method'])
                            if value:
                                terms.append(value)

                return terms
            else:
                return []
        else:
            return []
    except:
        return []

@indexer(IObject)
def object_acquisition_method(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'acquisition'):
                terms = []
                items = object.acquisition
                if items != None:
                    for item in items:
                        if item['method'] != None:
                            terms.append(item['method'])

                final_terms = " ".join(terms)
                return final_terms
            else:
                return ""
        else:
            return ""
    except:
        return ""


@indexer(IObject)
def association_person(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'associated_person'):
                terms = []
                items = object.associated_person
                if items != None:
                    for item in items:
                        if item['person'] != None:
                            terms.append(item['person'])
                        if item['notes'] != None:
                            terms.append(item['notes'])

                final_terms = " ".join(terms)
                return final_terms
            else:
                return ""
        else:
            return ""
    except:
        return ""

@indexer(IObject)
def object_association_subject(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'associated_subject'):
                terms = []
                items = object.associated_subject
                if items != None:
                    for item in items:
                        if item['subject'] != None:
                            terms.append(item['subject'])

                        if item['association'] != None:
                            terms.append(item['association'])

                        if item['date'] != None:
                            terms.append(item['date'])

                        if item['notes'] != None:
                            terms.append(item['notes'])

                final_terms = " ".join(terms)
                return final_terms

            else:
                return ""
        else:
            return ""
    except:
        return ""


@indexer(IObject)
def association_period(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'associated_period'):
                terms = []
                items = object.associated_period
                if items != None:
                    for item in items:
                        if item['period'] != None:
                            value = safe_value(item['period'])
                            if value:
                                terms.append(value)
                return terms
            else:
                return []
        else:
            return []
    except:
        return []


@indexer(IObject)
def object_association_period(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'associated_period'):
                terms = []
                items = object.associated_period
                if items != None:
                    for item in items:
                        if item['period'] != None:
                            terms.append(item['period'])
                
                final_terms = " ".join(terms)
                return final_terms
            else:
                return ""
        else:
            return ""
    except:
        return ""


@indexer(IObject)
def documentation_title(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'documentation'):
                terms = []
                items = object.documentation
                if items != None:
                    for item in items:
                        if item['title'] != None:
                            terms.append(item['title'])

                final_terms = " ".join(terms)
                return final_terms
            else:
                return ""
        else:
            return ""
    except:
        return ""

@indexer(IObject)
def exhibition_title(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'exhibitions'):
                terms = []
                items = object.exhibitions
                if items != None:
                    for item in items:
                        if item['title'] != None:
                            terms.append(item['title'])

                final_terms = " ".join(terms)
                return final_terms
            else:
                return ""
        else:
            return ""
    except:
        return ""

@indexer(IObject)
def creator_role(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'creator'):
                terms = []
                items = object.creator
                if items != None:
                    for item in items:
                        if item['role'] != None:
                            value = safe_value(item['role'])
                            if value:
                                terms.append(value)

                return terms
            else:
                return []
        else:
            return []
    except:
        return []


@indexer(IObject)
def creator_qualifier(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'creator'):
                terms = []
                items = object.creator
                if items != None:
                    for item in items:
                        if item['qualifier'] != None:
                            value = safe_value(item['qualifier'])
                            if value:
                                terms.append(value)
                return terms
            else:
                return []
        else:
            return []
    except:
        return []

@indexer(IObject)
def creator_place(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'creator'):
                terms = []
                items = object.creator
                if items != None:
                    for item in items:
                        if item['birth_place'] != None:
                            value = safe_value(item['birth_place'])
                            if value:
                                terms.append(value)
                        if item['death_place'] != None:
                            value = safe_value(item['death_place'])
                            if value:
                                terms.append(value)
                return terms
            else:
                return []
        else:
            return []
    except:
        return []

@indexer(IObject)
def place_index(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            terms = []
            if hasattr(object, 'production_place'):
                items = object.production_place
                if items:
                    for item in items:
                        if item['place']:
                            value = safe_value(item['place'])
                            if value:
                                terms.append(value)

            if hasattr(object, 'associated_subjects'):
                items = object.associated_subjects
                if items:
                    for item in items:

                        if item['subject'] and item['subject_type']:
                            if item['subject_type'] in ['geografie']:
                                subject_split = item['subject'].split(",")
                                final_subject = subject_split[0].strip()
                                value = safe_value(final_subject)
                                if value:
                                    terms.append(value)
            return terms
        else:
            return []
    except:
        return []

@indexer(IObject)
def inscription_content(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'inscription'):
                terms = []
                items = object.inscription
                if items != None:
                    for item in items:
                        if item['content'] != None:
                            terms.append(item['content'])

                final_terms = " ".join(terms)
                return final_terms
            else:
                return ""
        else:
            return ""
    except:
        return ""

@indexer(IObject)
def object_collection(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'collection'):
                terms = []
                items = object.collection
                if items != None:
                    for item in items:
                        if item['term'] != None:
                            terms.append(item['term'])

                final_terms = " ".join(terms)
                return final_terms
            else:
                return ""
        else:
            return ""
    except:
        return ""

@indexer(IObject)
def collection(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'collection'):
                terms = []
                items = object.collection
                if items != None:
                    for item in items:
                        if item['term'] != None:
                            value = safe_value(item['term'])
                            if value:
                                terms.append(value)
                return terms
            else:
                return []
        else:
            return []
    except:
        return []

@indexer(IObject)
def collection_index(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'collection'):
                terms = []
                items = object.collection
                if items != None:
                    for item in items:
                        if item['term'] != None:
                            value = safe_value(item['term'])
                            if value:
                                terms.append(value)
                return terms
            else:
                return []
        else:
            return []
    except:
        return []
        

@indexer(IObject)
def inscription_type(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'inscription'):
                terms = []
                items = object.inscription
                if items != None:
                    for item in items:
                        if item['type'] != None:
                            terms.append(item['type'])

                final_terms = " ".join(terms)
                return final_terms
            else:
                return ""
        else:
            return ""
    except:
        return ""

@indexer(IObject)
def inscription_description(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'inscription'):
                terms = []
                items = object.inscription
                if items != None:
                    for item in items:
                        if item['description'] != None:
                            terms.append(item['description'])

                final_terms = " ".join(terms)
                return final_terms
            else:
                return ""
        else:
            return ""
    except:
        return ""

@indexer(IObject)
def object_notes(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'notes'):
                terms = []
                items = object.notes
                if items != None:
                    for item in items:
                        if item['note'] != None:
                            terms.append(item['note'])

                final_terms = " ".join(terms)
                return final_terms
            else:
                return ""
        else:
            return ""
    except:
        return ""


@indexer(IObject)
def physical_description(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'physical_description'):
                terms = []
                items = object.physical_description
                return items
            else:
                return ""
        else:
            return ""
    except:
        return ""

@indexer(IObject)
def production_date_start(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'production'):
                terms = []
                items = object.production
                if items != None:
                    for item in items:
                        if item['date_start'] != None:
                            terms.append(item['date_start'])

                final_terms = " ".join(terms)
                return final_terms
            else:
                return ""
        else:
            return ""
    except:
        return ""

@indexer(IObject)
def period_index(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'production'):
                terms = []
                items = object.production
                if items != None:
                    for item in items:
                        date_start = ""
                        if item['date_start_precision'] != None:
                            date_start = "%s" %(item['date_start_precision'])

                        if item['date_start'] != None:
                            date_start = "%s %s" %(date_start, item['date_start'])
                            if date_start:
                                value = safe_value(date_start.strip())
                                if value:
                                    terms.append(value)
                return terms
            else:
                return []
        else:
            return []
    except:
        return []


@indexer(IObject)
def object_period_index(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'production'):
                terms = []
                items = object.production
                if items != None:
                    for item in items:
                        date_start = ""
                        if item['date_start'] != None:
                            date_start = int(item['date_start'])

                            if date_start:
                                century = find_century(date_start)
                                terms.append(safe_value(century))
                            else:
                                terms.append(safe_value("Onbekend"))
                return terms
            else:
                return []
        else:
            return []
    except:
        return []


@indexer(IObject)
def sortable_production_date(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'production'):
                terms = []
                items = object.production
                if items != None:
                    for item in items:
                        if item['date_start'] != None:
                            value = safe_value(item['date_start'])
                            if value:
                                terms.append(value)

                return terms
            else:
                return []
        else:
            return []
    except:
        return []

@indexer(IObject)
def production_date_end(object, **kw):
    try:
        if getattr(object, 'portal_type', None) == "Object":
            if hasattr(object, 'production'):
                terms = []
                items = object.production
                if items != None:
                    for item in items:
                        if item['date_end'] != None:
                            terms.append(item['date_end'])

                final_terms = " ".join(terms)
                return final_terms
            else:
                return ""
        else:
            return ""
    except:
        return ""





