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

@indexer(IObject)
def documentation_author(object, **kw):
    try:
        if hasattr(object, 'documentation'):
            authors = []
            items = object.documentation
            if items != None:
                for item in items:
                    if item['author'] != None:
                        for name in item['author']:
                            if name:
                                authors.append(name)
            return authors
        else:
            return []
    except:
        return []

@indexer(IObject)
def content_motif(object, **kw):
    try:
        if hasattr(object, 'content_motif'):
            motifs = []
            items = object.content_motif
            if items != None:
                for item in items:
                    if item['motif'] != None:
                        motifs.append(item['motif'])
            return motifs
        else:
            return []
    except:
        return []


@indexer(IObject)
def association_subject(object, **kw):
    try:
        if hasattr(object, 'associated_subject'):
            terms = []
            items = object.associated_subject
            if items != None:
                for item in items:
                    if item['subject'] != None:
                        terms.append(item['subject'])
            return terms
        else:
            return []
    except:
        return []

@indexer(IObject)
def association_period(object, **kw):
    try:
        if hasattr(object, 'associated_period'):
            terms = []
            items = object.associated_period
            if items != None:
                for item in items:
                    if item['period'] != None:
                        terms.append(item['period'])
            return terms
        else:
            return []
    except:
        return []

@indexer(IObject)
def creator_name(object, **kw):
    try:
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
    except:
        return ""

@indexer(IObject)
def label_text(object, **kw):
    try:
        if hasattr(object, 'text'):
            terms = []
            items = object.text
            all_text = items.raw
            return all_text
        else:
            return ""
    except:
        return ""

@indexer(IObject)
def object_name(object, **kw):
    try:
        if hasattr(object, 'object_name'):
            terms = []
            items = object.object_name
            if items != None:
                for item in items:
                    if item['name'] != None:
                        terms.append(item['name'])
            return terms
        else:
            return []
    except:
        return []

@indexer(IObject)
def object_person_priref(object, **kw):
    try:
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
    except:
        return []

@indexer(IObject)
def technique(object, **kw):
    try:
        if hasattr(object, 'technique'):
            terms = []
            items = object.technique
            if items != None:
                for item in items:
                    if item['technique'] != None:
                        terms.append(item['technique'])
            return terms
        else:
            return []
    except:
        return []


@indexer(IObject)
def acquisition_date(object, **kw):
    try:
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
    except:
        return ""

@indexer(IObject)
def acquisition_method(object, **kw):
    try:
        if hasattr(object, 'acquisition'):
            terms = []
            items = object.acquisition
            if items != None:
                for item in items:
                    if item['method'] != None:
                        terms.append(item['method'])

            return terms
        else:
            return []
    except:
        return []


@indexer(IObject)
def association_person(object, **kw):
    try:
        if hasattr(object, 'associated_person'):
            terms = []
            items = object.associated_person
            if items != None:
                for item in items:
                    if item['person'] != None:
                        terms.append(item['person'])

            final_terms = " ".join(terms)
            return final_terms
        else:
            return ""
    except:
        return ""


@indexer(IObject)
def documentation_title(object, **kw):
    try:
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
    except:
        return ""

@indexer(IObject)
def exhibition_title(object, **kw):
    try:
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
    except:
        return ""

@indexer(IObject)
def creator_role(object, **kw):
    try:
        if hasattr(object, 'creator'):
            terms = []
            items = object.creator
            if items != None:
                for item in items:
                    if item['role'] != None:
                        terms.append(item['role'])

            return terms
        else:
            return []
    except:
        return []


@indexer(IObject)
def inscription_content(object, **kw):
    try:
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
    except:
        return ""

@indexer(IObject)
def inscription_type(object, **kw):
    try:
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
    except:
        return ""

@indexer(IObject)
def inscription_description(object, **kw):
    try:
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
    except:
        return ""

@indexer(IObject)
def object_notes(object, **kw):
    try:
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
    except:
        return ""


@indexer(IObject)
def physical_description(object, **kw):
    try:
        if hasattr(object, 'physical_description'):
            terms = []
            items = object.physical_description
            return items
        else:
            return ""
    except:
        return ""

@indexer(IObject)
def production_date_start(object, **kw):
    try:
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
    except:
        return ""

@indexer(IObject)
def production_date_end(object, **kw):
    try:
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
    except:
        return ""





