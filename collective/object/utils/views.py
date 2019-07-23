#!/usr/bin/python
# -*- coding: utf-8 -*-

#from collective.leadmedia.adapters import ICanContainMedia
from zope.component import getMultiAdapter, getUtility
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFCore.utils import getToolByName
import csv

from plone.dexterity.browser.view import DefaultView
from AccessControl import getSecurityManager
from Products.CMFCore.permissions import ModifyPortalContent
from zope.schema.interfaces import IChoice, ITextLine, IList, IText, IBool
from collective.z3cform.datagridfield.interfaces import IDataGridField
from plone.app.textfield.interfaces import IRichText
from collective.object.utils.interfaces import IListField
from z3c.relationfield.interfaces import IRelationList
from zope.schema import getFields, getFieldsInOrder
from plone.app.z3cform.widget import AjaxSelectFieldWidget, AjaxSelectWidget, SelectWidget, DatetimeFieldWidget, IAjaxSelectWidget, RelatedItemsFieldWidget
from zope.interface import alsoProvides
from .interfaces import IFormWidget
from plone.dexterity.browser import add, edit
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.uuid.utils import uuidToCatalogBrain, uuidToObject
from Products.Five import BrowserView
import json
from collective.object import MessageFactory as _
from z3c.relationfield.interfaces import IRelationList, IRelationValue
from lxml import etree
from zope.schema import getFieldsInOrder
#from collective.slickcarousel.viewlets import SlickCarouselUtils
from collective.object.object import IObject
from operator import itemgetter
from Products.PythonScripts.standard import url_quote
from datetime import datetime, timedelta
import datetime as dateTimeProd
import urllib2, urllib
import requests

NOT_ALLOWED = [None, '', ' ', 'None']
NOT_ALLOWED_FIELDS = ['priref', 'collection', 'in_museum', 'record_published', 'current_location', 'rights', 'freeofcopyright', 'material', 'associated_subjects', 'production_place']

# # # # # # # # # # # # #
# View specific methods #
# # # # # # # # # # # # #
import logging

def reindex_search_filters(start=0, end=-1, lang='nl', indexes=["sortable_creator_name", "creator_role", "creator_qualifier", "creator_place", "Title", "label_text", "content_motifs", "objectname", "collection_index", "object_technique", "inscriptions_markings", "object_acquisition_method", "acquisition_date", "exhibition_title", "documentation_title", "object_association_subject", "association_person", "object_association_period", "object_name_index","technique_index", "creator_name_index", "place_index", "object_period_index"]):

    import plone.api
    import datetime
    import transaction

    catalog = plone.api.portal.get().portal_catalog
    brains = catalog(portal_type="Object", Language=lang)

    curr = start
    total = len(brains)

    if end == -1:
        end = total

    for brain in list(brains)[start:end]:
        try:
            curr += 1
            print "Reindexing %s / %s" %(curr, end)

            obj = brain.getObject()
            obj.reindexObject(idxs=indexes)
            transaction.get().commit()
        except:
            pass
            
    transaction.get().commit()
    return True


def strip_sensitive_data(event, hint):
    
    if event['logger'] != 'root':
        return {}
    else:
        event['logger'] = 'sync'

    return event

def test_sentry():
    import logging
    import sentry_sdk
    from sentry_sdk.integrations.logging import LoggingIntegration
    from sentry_sdk import configure_scope, push_scope

    # All of this is already happening by default!
    sentry_logging = LoggingIntegration(
        level=logging.INFO,       # Capture info and above as breadcrumbs
        event_level=logging.INFO  # Send errors as events
    )
    sentry_sdk.init(
        environment="collection",
        dsn="https://13316496b58e413687b16d98e99c984a@sentry.io/1460071",
        integrations=[sentry_logging],
        before_send=strip_sensitive_data
    )

    """with configure_scope() as scope:
        scope.set_tag("sync", "info")
        logging.info("Updated record 10000001",
            extra={
                "url": "https://centraalmuseum-stage.intk.com/nl/collectie/bruna/bruna2006-de-puppies-van-snuffie-dick-bruna",
                "updated_fields": ["title", "creator", "production_date", "material", "object_number", "technique", "acquisition", "dimension", "inscriptions_markings", "exhibitions"],
                "priref": "10000001"
            })

        logging.info("Updated image \inventarisnrs\YBruna2006.jpg",
            extra={
                "url": "https://centraalmuseum-stage.intk.com/nl/collectie/bruna/bruna2006-de-puppies-van-snuffie-dick-bruna/slideshow/ybruna2006-jpg",
                "image_reference": "\inventarisnrs\YBruna2006.jpg"
            })

    with push_scope() as scope:
        scope.set_tag("sync", "info")
        logging.info("Updated record 10000025", 
            extra={
                "url": "https://centraalmuseum-stage.intk.com/nl/collectie/bruna/bruna6851-leve-god-en-engeltjes-rein-laat-mij-een-lief-kindje-zijn-maak-dat-gauw-mijn-hemdje-wordt-veel-te-krap-en-veel-te-kort-dick-bruna",
                "updated_fields": ["title", "creator", "material", "technique", "object_number", "object_name", "acquisition", "dimension"],
                "priref": "10000025"
            })

        logging.info("Updated image \inventarisnrs\YBruna6851.jpg",
            extra={
                "url": "https://centraalmuseum-stage.intk.com/nl/collectie/bruna/bruna6851-leve-god-en-engeltjes-rein-laat-mij-een-lief-kindje-zijn-maak-dat-gauw-mijn-hemdje-wordt-veel-te-krap-en-veel-te-kort-dick-bruna/slideshow/ybruna6851-jpg",
                "image_reference": "\inventarisnrs\YBruna6851.jpg"
            })
    
    with push_scope() as scope:
        scope.set_tag("sync", "info")
        logging.info("Updated record 10000039", 
            extra={
                "url": "https://centraalmuseum-stage.intk.com/nl/collectie/bruna/bruna0005-meneer-knie-omslag-p-29-dick-bruna",
                "updated_fields": ["title", "creator", "production_date", "material", "techique", "object_name", "acquisition", "dimension"],
                "priref": "10000039",
            })

        logging.info("Updated image \inventarisnrs\YBruna0005.jpg",
            extra={
                "url": "https://centraalmuseum-stage.intk.com/nl/collectie/bruna/bruna0005-meneer-knie-omslag-p-29-dick-bruna/slideshow/ybruna0005-jpg",
                "image_reference": "\inventarisnrs\YBruna0005.jpg"
            })"""


    
    with push_scope() as scope:
        scope.set_tag("sync", "error")
        logging.error("Failed to update record 28446", extra={
            'priref': '28446',
            'url': 'https://centraalmuseum-stage.intk.com/nl/collectie/29611-do-add-2-prototype-jurgen-bey',
            'error_message': 'ValueError: Disallowed subobject type: Object'
            })

        logging.error("Failed to update image 24426_001-007_02.tif", extra={
            'image_reference': "OBJECTEN\INVENTARISNUMMERS\gecropt\24426_001-007_02.tif",
            'error_message': 'ValueError: Disallowed subobject type: Image'
            })

        logging.error("Failed to download image 34940_02.tif from the API", extra={
            'image_reference': 'OBJECTEN\INVENTARISNUMMERS\gecropt\34940_02.tif',
            'url': 'http://cmu-web.adlibhosting.com/wwwopacximages/wwwopac.ashx?command=getcontent&server=full&value=OBJECTEN\INVENTARISNUMMERS\gecropt\34940_02.tif&imageformat=jpg',
            'error_message': 'Adlib.Imaging.Exceptions.ImagePathNotFoundException'
            })

        logging.error("Field cannot be recognised: copy.number", extra={
            'field_name': 'copy.number',
            })



    with push_scope() as scope:
        scope.set_tag("sync", "")
        scope.set_extra("url", "")

    return True


def setup_logger(name, log_file, level=logging.INFO, formatter=logging.Formatter('%(asctime)s %(levelname)s %(message)s')):
    """Function setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

def move_exhibitions():
    import plone.api
    import datetime
    import transaction

    old_folder = plone.api.content.get(path="/nl/tentoonstellingen/tentoonstellingsarchief")
    curr = 0
    total = len(old_folder)
    dest = plone.api.content.get(path="/nl/tentoonstellingen")    

    for _id in list(old_folder):
        obj = old_folder[_id]
        if getattr(obj, 'portal_type', None) == "Event":
            plone.api.content.move(source=obj, target=dest)

        curr += 1
        print "Moving %s / %s" %(curr, total)
        if curr % 10:
            transaction.get().commit()
    
    transaction.get().commit()
    return True


def reindex_website_collection_exhibition_index(indexes=['website_collection_exhibition_index'], limit=1000):

    import plone.api
    import datetime
    import transaction

    catalog = plone.api.portal.get().portal_catalog
    brains_collection = catalog(portal_type="Object", Language="nl")
    brains_website = catalog(portal_type=["Document", "News Item"], Language="nl")
    brains_archive = catalog(portal_type="Event", Language="nl")

    all_brains = [brains_collection, brains_website, brains_archive]
    curr = 0

    for brain_type in all_brains:
        if limit == -1:
            to_reindex = list(brain_type)
        else:
            to_reindex = list(brain_type)[:limit]

        for brain in to_reindex:
            try:
                curr += 1
                print "Reindexing %s" %(curr)

                obj = brain.getObject()
                obj.reindexObject(idxs=indexes)

                if limit == -1:
                    if curr % 500 == 0:
                        transaction.get().commit()
                else:
                    transaction.get().commit()
            except:
                pass

    return True





def update_exhibition_field_by_priref(priref="18753", catalog="", commit=True):
    import transaction
    import plone.api
    import urllib2, urllib
    import requests
    from lxml import etree

    url = "http://cmu-web.adlibhosting.com/wwwopacximagesnew/wwwopac.ashx?database=collect&search=priref=%s" %(priref)

    if not catalog:
        catalog = plone.api.portal.get().portal_catalog
    brains = catalog(portal_type="Object", object_priref=priref, Language="nl")

    if brains:
        brain = brains[0]
        obj = brain.getObject()

        database_url = url
        quoted_query = database_url
        api_request = quoted_query
        req = urllib2.Request(api_request)
        req.add_header('User-Agent', 'Mozilla/5.0')
        response = urllib2.urlopen(req)
        xmldoc = etree.parse(response)

        root = xmldoc.getroot()
        recordList = root.find("recordList")
        records = recordList.getchildren()

        record = records[0]

        new_exhibitions = []

        exhibitions = record.findall('Exhibition')

        if exhibitions:
            print "[%s] Total exhibitions to be added %s" %(priref, len(exhibitions))
            for exhibition in exhibitions:
                title = ""
                venue = ""
                place = ""
                date_start = ""
                date_end = ""
                nummer_cm = ""
                notes = ""
                priref = ""

                try:
                    priref = exhibition.find('exhibition.lref').text
                except:
                    pass

                try:
                    title = exhibition.find('exhibition').find('title').text
                except:
                    pass

                try:
                    venue = exhibition.find('exhibition').find('venue').find('venue').find('value').text
                except:
                    pass

                try:
                    place = exhibition.find('exhibition').find('venue').find('venue.place').find('value').text
                except:
                    pass

                try:
                    date_start = exhibition.find('exhibition').find('venue').find('venue.date.start').text
                except:
                    pass

                try: 
                    date_end = exhibition.find('exhibition').find('venue').find('venue.date.end').text
                except:
                    pass

                try:
                    nummer_cm = exhibition.find('exhibition').find('nummer_cm').text
                except:
                    pass

                try:
                    notes = ""
                except:
                    pass

                new_exhibition = {"priref": priref, "title":title, "venue":venue, "place":place, "date_start":date_start, "date_end":date_end, "nummer_cm":nummer_cm, "notes":notes}
                new_exhibitions.append(new_exhibition)

            obj.exhibitions = new_exhibitions
            obj.reindexObject(idxs=["object_name_index","technique_index","material_index","period_index","creator_name_index","place_index", "object_period_index", "collection_index"])
        
            print "[%s] Updated exhibitions on the object %s" %(priref, obj.absolute_url())
            if commit:
                transaction.get().commit()
        else:
            print "[%s] Cannot find exhibitions in the priref" %(priref)
            return False
    else:
        print "[%s] Cannot find priref in the website" %(priref)
        return False

    return True


def update_production_filter_by_priref(priref="18753", catalog="", database="collect"):
    import transaction
    import plone.api
    import urllib2, urllib
    import requests
    from lxml import etree

    url = "http://cmu-web.adlibhosting.com/wwwopacximages/wwwopac.ashx?database=%s&search=priref=%s" %(database, priref)

    if not catalog:
        catalog = plone.api.portal.get().portal_catalog

    database_url = url
    quoted_query = database_url
    api_request = quoted_query
    req = urllib2.Request(api_request)
    req.add_header('User-Agent', 'Mozilla/5.0')
    response = urllib2.urlopen(req)
    xmldoc = etree.parse(response)

    root = xmldoc.getroot()
    recordList = root.find("recordList")
    records = recordList.getchildren()

    record = records[0]

    places = record.findall('Production')
    associations = record.findall('Associated_subject')
    brains = None

    if len(places) > 0 or len(associations) > 0:
        brains = catalog(portal_type="Object", object_priref=priref, Language="nl")
    else:
        print "[%s] Cannot find places or associations in the priref" %(priref)
        return False

    if brains:
        brain = brains[0]
        obj = brain.getObject()

        new_places = []
        new_associations = []

        for place in places:
            if place.find('production.place') != None:
                if place.find('production.place').find('value') != None:
                    if place.find('production.place').find('value').text:
                        new_places.append({'place': place.find('production.place').find('value').text})

        for subject in associations:
            if subject.find('association.subject.type') != None:
                for lang in subject.find('association.subject.type').findall('value'):
                    if lang.get('lang') == "1" and lang.text in ['geografie']:
                        if subject.find('association.subject') != None:
                            if subject.find('association.subject').find('value') != None:
                                new_associations.append({"subject_type": lang.text, "subject": subject.find('association.subject').find('value').text})
                                break

        obj.production_place = new_places
        obj.associated_subjects = new_associations
        obj.reindexObject(idxs=["object_name_index","technique_index","material_index","period_index","creator_name_index","place_index", "object_period_index"])
        
        print "[%s] Updated place filter on the object %s" %(priref, obj.absolute_url())
        transaction.get().commit()
    else:
        print "[%s] Cannot find priref in the website" %(priref)
        return False

    return True


def update_production_field(start=0, end=100, limit=100, database="collect"):
    import transaction
    import plone.api
    import urllib2, urllib
    import requests
    from lxml import etree

    url = "http://cmu-web.adlibhosting.com/wwwopacximages/wwwopac.ashx?database=%s&search=all&fields=priref&limit=%s" %(database, limit)

    database_url = url
    quoted_query = database_url
    api_request = quoted_query
    req = urllib2.Request(api_request)
    req.add_header('User-Agent', 'Mozilla/5.0')
    response = urllib2.urlopen(req)
    xmldoc = etree.parse(response)

    root = xmldoc.getroot()
    recordList = root.find("recordList")
    records = recordList.getchildren()

    total = len(list(records))
    curr = start

    catalog = plone.api.portal.get().portal_catalog

    if end == -1:
        end = total

    for record in list(records)[start:end]:
        curr += 1
        print "Updating production filter %s / %s" %(curr, total)

        if record.find('priref') != None:
            priref = record.find('priref').text
            try:
                update_production_filter_by_priref(priref, catalog, database)
                print "[%s] Fixed %s / %s" %(priref, curr, total)
            except:
                print "[%s] Failed to update the production filter" %(priref)
                pass
        else:
            pass

    return True

def update_exhibition_field(start=0, end=100, limit=100):
    import transaction
    import plone.api
    import urllib2, urllib
    import requests
    from lxml import etree

    url = "http://cmu-web.adlibhosting.com/wwwopacximagesnew/wwwopac.ashx?database=collect&search=exhibition=*&limit=%s" %(limit)

    database_url = url
    quoted_query = database_url
    api_request = quoted_query
    req = urllib2.Request(api_request)
    req.add_header('User-Agent', 'Mozilla/5.0')
    response = urllib2.urlopen(req)
    xmldoc = etree.parse(response)

    root = xmldoc.getroot()
    recordList = root.find("recordList")
    records = recordList.getchildren()

    total = len(list(records))
    curr = 0

    catalog = plone.api.portal.get().portal_catalog

    if end == -1:
        end = len(total)

    for record in list(records)[start:end]:
        curr += 1
        print "Fixing exhibitions %s / %s" %(curr, total)

        if record.find('priref') != None:
            priref = record.find('priref').text
            try:
                update_exhibition_field_by_priref(priref, catalog)
                print "[%s] Fixed %s / %s" %(priref, curr, total)
            except:
                print "[%s] Failed to update the exhibition field" %(priref)
                pass
        else:
            pass

    return True


def fix_fine_art_tags():
    import transaction
    import plone.api
    catalog = plone.api.portal.get().portal_catalog

    all_prenten = catalog(portal_type="Object", Language="nl", Subject="prenten en tekeningen")

    with_modern_art = [brain for brain in all_prenten if 'beeldende kunst 1850 - heden' in brain.Subject]
    without_modern_art = [brain for brain in all_prenten if 'beeldende kunst 1850 - heden' not in brain.Subject]

    print "Total modern art: %s" %(len(with_modern_art))
    print "Total fine art: %s" %(len(without_modern_art))

    """for brain in with_modern_art:
        tags = list(brain.Subject)
        tags.append("prenten en tekeningen 1850 - heden")
        obj = brain.getObject()
        obj.setSubject(tags)
        obj.reindexObject(idxs="Subject")

        transaction.get().commit()"""

    curr = 0
    total = len(without_modern_art)

    for brain in list(without_modern_art):
        curr += 1
        print "Fixing %s / %s" %(curr, total)
        tags = list(brain.Subject)
        tags.append("prenten en tekeningen tot 1850")
        obj = brain.getObject()
        obj.setSubject(tags)
        obj.reindexObject(idxs=["Subject"])
        transaction.get().commit()

    return True


def calculate_missing_objects(database="collect", limit=100):

    import transaction
    import plone.api
    from plone.app.textfield.value import RichTextValue
    import urllib2, urllib
    import requests
    from lxml import etree

    database_url = "http://cmu-web.adlibhosting.com/wwwopacximages/wwwopac.ashx?database=%s&search=all&fields=priref&limit=%s" %(database, limit)
    quoted_query = database_url
    api_request = quoted_query
    req = urllib2.Request(api_request)
    req.add_header('User-Agent', 'Mozilla/5.0')
    response = urllib2.urlopen(req)
    xmldoc = etree.parse(response)

    root = xmldoc.getroot()
    recordList = root.find("recordList")
    records = recordList.getchildren()

    catalog = plone.api.portal.get().portal_catalog

    missing = []
    curr = 0
    total = len(list(records))

    for record in list(records):
        curr += 1
        print "Checking %s / %s" %(curr, total)
        if record.find('priref') != None:
            priref = record.find('priref').text
            brains = catalog(portal_type="Object", Language="nl", object_priref=priref)
            if not brains:
                missing.append(priref)
            else:
                pass
        else:
            pass
    print missing

    return True


def calculate_total_objects():

    import plone.api
    import datetime
    import transaction

    catalog = plone.api.portal.get().portal_catalog
    brains_collect = catalog(portal_type="Object", Language="nl", path={"query": "/CM/nl/collectie", "depth": 1})
    brains_bruna = catalog(portal_type="Object", Language="nl", path={"query": "/CM/nl/collectie/bruna", "depth": 1})
    brains_rsa = catalog(portal_type="Object", Language="nl", path={"query": "/CM/nl/collectie/rsa", "depth": 1})

    print "Collect: %s" %(len(brains_collect))
    print "Bruna: %s" %(len(brains_bruna))
    print "RSA: %s" %(len(brains_rsa))

    return True

def reindex_objects_index(objects=['2868'], index='creatorname'):
    import plone.api
    import datetime
    import transaction

    catalog = plone.api.portal.get().portal_catalog
    
    theoloog = ['2868', '4290', '4545', '4700', '5030', '5393', '7085', '7090', '7118', '8636', '8694', '14538', '14539', '30102', '30203', '30285', '30343']
    gestorven = ['25', '813', '1092', '1735', '2470', '2680', '4865', '5338', '5453', '6343', '14853', '19342', '39938', '39939']

    for priref in gestorven:
        brains = catalog(portal_type="Object", object_priref=priref)
        if brains: 
            brain = brains[0]
            try:
                obj = brain.getObject()
                obj.reindexObject(idxs=[index])
                transaction.get().commit()
                print "Reindexed %s" %(priref)
            except:
                pass

    return True

def reindex_object_index(indexes=['creatorname'], limit=1000):

    import plone.api
    import datetime
    import transaction

    catalog = plone.api.portal.get().portal_catalog
    brains = catalog(portal_type="Object", Language="nl")

    curr = 0
    for brain in list(brains)[:limit]:
        try:
            curr += 1
            print "Reindexing %s" %(curr)

            obj = brain.getObject()
            obj.reindexObject(idxs=indexes)
            if curr % 500 == 0:
                transaction.get().commit()
        except:
            pass

    return True


def update_persons_url(limit=100, language="nl"):
    import transaction
    import plone.api
    from plone.app.textfield.value import RichTextValue
    import urllib2, urllib
    import requests
    from lxml import etree

    persons_url = "http://cmu-web.adlibhosting.com/wwwopacximages/wwwopac.ashx?database=people&search=all&fields=url&limit=%s" %(limit)
    quoted_query = persons_url
    api_request = quoted_query
    req = urllib2.Request(api_request)
    req.add_header('User-Agent', 'Mozilla/5.0')
    response = urllib2.urlopen(req)
    xmldoc = etree.parse(response)

    root = xmldoc.getroot()
    recordList = root.find("recordList")
    records = recordList.getchildren()

    catalog = plone.api.portal.get().portal_catalog
    
    curr = 0
    total = len(list(records))
    for record in list(records):
        curr += 1
        print "Updating %s / %s" %(curr, total)

        if record.find('priref') != None:

            priref = record.find('priref').text
            url = ""

            for iaddr in record.findall('Internet_address'):
                if iaddr.find('url') != None:
                    temp_url = iaddr.find('url').text
                    if 'rkd.nl' in temp_url:
                        url = temp_url
                        break

            if url:
                persons = catalog(portal_type="Person", Language=language, person_priref=priref)
                if persons:
                    person = persons[0].getObject()
                    if language == "nl":
                        url_text = "<p>Bekijk hier alle werken van %s in de collectie van Centraal Museum. Voor kunsthistorische documentatie over %s, ga naar <a href='%s' target='_blank'>%s</a></p>" %(getattr(person, 'title', '').strip(), getattr(person, 'title', '').strip(), url, url)
                    else:
                        url_text = "<p>View all art works by %s in the Centraal Museum collection. For art historical documentation on %s, go to <a href='%s' target='_blank'>%s</a> (in Dutch).</p>" %(getattr(person, 'title', '').strip(), getattr(person, 'title', '').strip(), url, url)

                    url_value = RichTextValue(url_text, 'text/html', 'text/html')
                    setattr(person, 'text', url_value)
                    transaction.get().commit()
                    print "Updated %s / %s - %s" %(curr, total, person.absolute_url())
        else:
            print "Failed to update %s / %s - No priref available" %(curr, total)


def validate_dates(database="collect", limit=0):

    dates_start_list = "http://cmu.adlibhosting.com/wwwopacximages/wwwopac.ashx?database=%s&command=facets&search=nummer_cm=*&facet=date.start&limit=%s" %(database, limit)
    dates_end_list = "http://cmu.adlibhosting.com/wwwopacximages/wwwopac.ashx?database=%s&command=facets&search=nummer_cm=*&facet=date.end&limit=%s" %(database, limit)


    all_dates_file = open("/var/www/centraalmuseum-collection/exports/all_exhibit_dates.csv", "w")
    all_dates_csv = csv.writer(all_dates_file, quoting=csv.QUOTE_ALL)

    invalid_dates_file = open("/var/www/centraalmuseum-collection/exports/invalid_exhibit_dates.csv", "w")
    invalid_dates_csv = csv.writer(invalid_dates_file, quoting=csv.QUOTE_ALL)

    formats = ["1930-11-13", "1983-12"]

    date_formats = ["%Y", "%Y-%M-%d"]

    quoted_query = dates_start_list
    api_request = quoted_query
    req = urllib2.Request(api_request)
    req.add_header('User-Agent', 'Mozilla/5.0')
    response = urllib2.urlopen(req)
    xmldoc = etree.parse(response)

    root = xmldoc.getroot()
    recordList = root.find("recordList")
    date_start_records = recordList.getchildren()

    quoted_query = dates_end_list
    api_request = quoted_query
    req = urllib2.Request(api_request)
    req.add_header('User-Agent', 'Mozilla/5.0')
    response = urllib2.urlopen(req)
    xmldoc = etree.parse(response)

    root = xmldoc.getroot()
    recordList = root.find("recordList")
    date_end_records = recordList.getchildren()

    records = date_start_records + date_end_records

    valid_formats = []
    invalid_formats = []
    only_year = 0

    total_dates = len(list(records))

    for record in list(records):
        if record.find('term') != None:
            term = record.find('term').text

            date_split = term.split('-')
            if len(date_split) == 1:
                try:
                    datetime_date = dateTimeProd.date(year=int(date_split[0]),month=1,day=1)
                    valid_formats.append(term)
                    only_year += 1
                    all_dates_csv.writerow([term, "valid"])
                except:
                    only_year += 1
                    invalid_formats.append(term)
                    all_dates_csv.writerow([term, "invalid"])
                    invalid_dates_csv.writerow([term, "invalid"])
                    pass
            elif len(date_split) == 3:
                try:
                    datetime_date = dateTimeProd.date(year=int(date_split[0]),month=int(date_split[1]),day=int(date_split[2]))
                    valid_formats.append(term)
                    all_dates_csv.writerow([term, "valid"])
                except:
                    invalid_formats.append(term)
                    all_dates_csv.writerow([term, "invalid"])
                    invalid_dates_csv.writerow([term, "invalid"])
                    pass
            else:
                invalid_formats.append(term)
                all_dates_csv.writerow([term, "invalid"])
                invalid_dates_csv.writerow([term, "invalid"])

    print "Total valid formats: %s" %(len(valid_formats))
    print "Total invalid formats: %s" %(len(invalid_formats))
    print "Total dates with only year: %s" %(only_year)
    print "Total dates: %s" %(len(valid_formats)+len(invalid_formats))
    print "Total dates api: %s" %(total_dates)

    print "Percentage of valid dates: %s" %(float(float(len(valid_formats))/float(len(valid_formats)+len(invalid_formats))) * 100)
    print "Percentage of dates with only year: %s" %(float(float(only_year)/float(total_dates)))
    return True



def get_index_unique_values(index):
    import plone.api

    portal = plone.api.portal.get()
    catalog = portal.portal_catalog
    values = get_unique_values_for(catalog, index)
    print values

    return ""

def change_pub_order():
    import transaction
    import plone.api
    from DateTime import DateTime
    from random import randint

    modern = plone.api.content.get(path="/nl/ontdek/collectie/moderne-en-hedendaagse-kunst/aggregator")

    collections = [
        {"name": "Moderne en hedendaagse kunst", "url": "/nl/ontdek/collectie/moderne-en-hedendaagse-kunst/aggregator"},
        {"name": "Stadsgeschiedenis", "url": "/nl/ontdek/collectie/stadsgeschiedenis/stadsgeschiedenis"},
        {"name": "Mode", "url": "/nl/ontdek/collectie/mode/mode"},
        {"name": "Dick Bruna", "url": "/CM/nl/collectie/bruna"},
        {"name": "Rietveld Schröderarchief", "url": "/nl/ontdek/collectie/rietveld-schroderarchief/rietveld-schroder-archive"},
        {"name": "Beeldende kunst tot 1850", "url": "/nl/ontdek/collectie/beeldende-kunst-tot-1850"},
        {"name": "Toegepaste kunst", "url": "/nl/ontdek/collectie/toegepaste-kunst"},
    ]
    
    catalog = plone.api.portal.get().portal_catalog
    items_with_image_and_on_display = catalog(portal_type="Object", Language="nl", hasMedia=True, object_on_display=True, path={"query": "/CM/nl/collectie/bruna", "depth": 1})
    total = len(items_with_image_and_on_display)
    curr = 0
    for brain in list(items_with_image_and_on_display):
        curr += 1
        print "IMAGE ON DISPLAY: %s / %s" %(curr, total)
        obj = brain.getObject()
        old_effective = obj.effective()
        
        day = old_effective.day()
        month = old_effective.month()
        year = old_effective.year()
        if year != 2018:
            year = 2016
            new_effective = "%s/%s/%s %s:%s:%s.%s" %(year, month, randint(1, 27), randint(1,23), randint(1, 58), randint(1,58), randint(100, 900000))
            new_datetime = DateTime(new_effective)
            obj.setEffectiveDate(new_datetime)
            obj.reindexObject()
            transaction.get().commit()
    

    items_with_image_and_not_on_display = catalog(portal_type="Object", Language="nl", hasMedia=True, object_on_display=False, path={"query": "/CM/nl/collectie/bruna", "depth": 1})
    total = len(items_with_image_and_not_on_display)
    curr = 0
    for brain in list(items_with_image_and_not_on_display)[:200]:
        curr += 1
        print "IMAGE NOT ON DISPLAY: %s / %s" %(curr, total)
        obj = brain.getObject()
        old_effective = obj.effective()
        
        day = old_effective.day()
        month = old_effective.month()
        year = old_effective.year()
        if year != 2018:
            year = 2017
            new_effective = "%s/%s/%s %s:%s:%s.%s" %(year, month, randint(1, 27), randint(1,23), randint(1, 58), randint(1,58), randint(100, 900000))
            new_datetime = DateTime(new_effective)
            obj.setEffectiveDate(new_datetime)
            obj.reindexObject()
            transaction.get().commit()
    """
    all_the_rest = catalog(portal_type="Object", Language="nl", hasMedia=False, path={"query": "/CM/nl/collectie/bruna", "depth": 1})

    total = len(all_the_rest)
    curr = 0
    for brain in list(all_the_rest):
        curr += 1
        print "ALL THE REST: %s / %s" %(curr, total)
        obj = brain.getObject()
        old_effective = obj.effective()
        
        day = old_effective.day()
        month = old_effective.month()
        year = old_effective.year()
        if year != 2018:
            new_effective = "%s/%s/%s %s:%s:%s.%s" %(year, randint(1, 7), randint(1, 27), randint(1,23), randint(1, 58), randint(1,58), randint(100, 900000))
            new_datetime = DateTime(new_effective)
            obj.setEffectiveDate(new_datetime)
            obj.reindexObject()
            transaction.get().commit()"""

    return True


def reindex_object_on_display():

    import plone.api
    import datetime
    import transaction

    catalog = plone.api.portal.get().portal_catalog
    brains = catalog(Subject="beeldende kunst 1850 - heden", portal_type="Object", Language="nl", path={"query": "/CM/nl/collectie", "depth": 1})

    curr = 0
    for brain in brains[:500]:
        curr += 1
        print "Reindexing %s" %(curr)

        obj = brain.getObject()
        obj.reindexObject()

    transaction.get().commit()

    return True

def move_persons():
    import plone.api
    import datetime
    import transaction

    persons = plone.api.content.get(path="/nl/personen-en-instellingen/personen-en-instellingen")
    curr = 0
    total = len(persons)
    dest = plone.api.content.get(path="/nl/personen-en-instellingen")    

    for _id in list(persons):
        obj = persons[_id]
        if getattr(obj, 'portal_type', None) == "Person":
            plone.api.content.move(source=obj, target=dest)

        curr += 1
        print "Moving %s / %s" %(curr, total)
        if curr % 500:
            transaction.get().commit()
    
    transaction.get().commit()
    return True

def reindexAllObjects():
    import plone.api
    import datetime
    import transaction

    brains = plone.api.portal.get().portal_catalog(portal_type="Object", Language="nl")
    curr = 0
    total = len(brains)
    for brain in list(brains)[1000:2000]:
        try:
            obj = brain.getObject()
            obj.reindexObject()
            curr += 1
            print "Reindexing %s / %s" %(curr, total)

            if curr % 500 == 0:
                transaction.get().commit()
        except:
            raise
    try:
        transaction.get().commit()
    except:
        raise

    return True


class ObjectView(DefaultView):
    """ View class """

    template = ViewPageTemplateFile('../object_templates/view.pt')


    # # # # # #
    # Utils   #
    # # # # # #
    def get_schema(self, item):
        return getFieldsInOrder(IObject)

    def final_text(self, value):
        return self.context.translate(_(value))

    def checkUserPermission(self):
        sm = getSecurityManager()
        if sm.checkPermission(ModifyPortalContent, self.context):
            return True
        return False

    def get_url_by_uid(self, uid):
        brains = uuidToCatalogBrain(uid)
        if brains:
            return brains.getURL()
        return ""

    def get_details(self):
        item = self.context
        item_uid = item.UID()
        
        details = {}
        details["title"] = item.Title()
        details["description"] = item.Description()
        details["image"] = ""

        return details



    # # # # # # # # # #
    # Object fields   # 
    # # # # # # # # # #
    def object_templates(self, template=None, value=""):
        TEMPLATES = {
            "label":"<div class='col-lg-4 col-md-4 col-sm-4 col-xs-12 object-label'><p>%s</p></div>",
            "value":"<div class='col-lg-8 col-md-8 col-sm-8 col-xs-12 object-value'><p>%s</p></div>"
        }
        if not template:
            return TEMPLATES
        else:
            if not value:
                return TEMPLATES.get(template, '')
            else:
                template = TEMPLATES.get(template, '')
                return template % (value)

    def get_custom_fields(self):
        CUSTOM_FIELDS = {
            "creator": self.generate_creator_value,
            "dimension": self.generate_dimension_value,
            "inscription": self.generate_inscription_value,
            "associated_subject": self.generate_associated_subject_value,
            "production": self.generate_production_value,
            "acquisition": self.generate_acquisition_value,
            "documentation": self.generate_documentation_value,
            "exhibitions": self.generate_exhibitions_value,
            "handle_url": self.generate_handle_url_value
        }
        return CUSTOM_FIELDS

    def get_datagrid_subfield(self, field):

        DATAGRID_SUBFIELDS = {
            "technique": "technique",
            "material": "material",
            "collection": "term",
            "object_name": "name",
            "associated_period": "period",
            "associated_person": "person",
            "notes": "note",
            "content_motif":"motif",
        }

        SEPARATORS = {
            "notes":"<br>",
            "associated_person": "<br>",
        }

        SEARCHABLE = {
            "content_motif":"c15", 
            "associated_period": "c27",
            "object_name":"c32",
            "technique":"c16",
            "associated_person": "c26"
        }

        is_searchable = False

        separator = ", "
        if field in SEPARATORS:
            separator = SEPARATORS[field]

        if field in SEARCHABLE:
            is_searchable = SEARCHABLE[field]

        if field in DATAGRID_SUBFIELDS:
            return DATAGRID_SUBFIELDS[field], separator, is_searchable
        else:
            return None, separator, is_searchable

    def generate_regular_datagrid(self, field, item, subfield, separator=', ', is_searchable=False):
        value = getattr(item, field, None)

        values = []

        if subfield:
            if value:
                for subitem in value:
                    if subfield in subitem:
                        subfield_value = subitem.get(subfield, '')
                        if subfield_value:
                            if separator == "<br>":
                                if not is_searchable:
                                    values.append("<span>%s</span>" %(subfield_value))
                                else:
                                    subfield_value = "<a href='/%s/zoeken#b_start=0&%s=%s'>%s</a>" %(getattr(self.context, 'language', 'nl'), is_searchable, url_quote(subfield_value),subfield_value)
                                    values.append("<span>%s</span>" %(subfield_value))
                            else:
                                if not is_searchable:
                                    values.append("%s" %(subfield_value))
                                else:
                                    if is_searchable == "content_motif":
                                        subfield_value = "<a href='/%s/zoeken#b_start=0&c15=%s*'>%s</a>" %(getattr(self.context, 'language', 'nl'), url_quote(subfield_value), subfield_value)
                                    else:
                                        subfield_value = "<a href='/%s/zoeken#b_start=0&%s=%s'>%s</a>" %(getattr(self.context, 'language', 'nl'), is_searchable, url_quote(subfield_value), subfield_value)
                                    values.append("%s" %(subfield_value))
                        else:
                            pass
                    else:
                        pass
            else:
                return None

            final_value = separator.join(values)
            return final_value
        else:
            return None


    def generate_creator_value(self, field, item):
        value = getattr(item, field, None)
        creators = []
        context_catalog = getToolByName(self.context, 'portal_catalog')

        if value:

            # Check if DataGridField
            for creator in value:
                new_creator = ""
                name = creator.get('name', '')
                qualifier = creator.get('qualifier', '')
                role = creator.get('role', '')
                
                birth_place = creator.get('birth_place', '')
                death_place = creator.get('death_place', '')
                
                birth_date_start = creator.get('birth_date_start', '')
                birth_date_end = creator.get('birth_date_end', '')
                birth_date_precision = creator.get('birth_date_precision', '')

                death_date_start = creator.get('death_date_start', '')
                death_date_end = creator.get('death_date_end', '')
                death_date_precision = creator.get('death_date_precision', '')

                creator_priref = creator.get('priref', '')

                url = creator.get('url', '')

                # Create name
                if name:
                    name_split = name.split(",")
                    if len(name_split) > 1:
                        firstname = name_split[1]
                        lastname = name_split[0]
                        name = "%s %s" %(firstname, lastname)

                    index_search = "creator_name"
                    search_term = name
                    person_obj_url = ""

                    if creator_priref:
                        persons = context_catalog(portal_type="Person", person_priref=creator_priref, Language=getattr(self.context,'language', 'nl'))
                        if persons:
                            person_obj = persons[0]
                            if person_obj:
                                person_obj_url = person_obj.getURL()

                    if not person_obj_url:
                        new_creator = "<a href='/%s/@@search?%s=%s'>%s</a>" %(getattr(self.context, 'language','nl'), index_search, url_quote(search_term), name)
                    else:
                        new_creator = "<a href='%s'>%s</a>" %(person_obj_url, name)

                if qualifier:
                    new_creator = "%s %s" %(qualifier, new_creator)

                if role:
                    new_creator = "%s (<a href='/%s/@@search?creator_role=%s'>%s</a>)" %(new_creator, getattr(self.context, 'language', 'nl'), url_quote(role), role)

                start_date = ""
                end_date = ""
                creator_date_range = ""

                if birth_date_start:
                    dates = birth_date_start.split("-")
                    if dates:
                        start_date = dates[0]
                        if start_date and birth_place:
                            start_date = "%s %s" %(birth_place, start_date)
                        elif birth_place and not start_date:
                            start_date = "%s" %(birth_place)
                        else:
                            start_date = start_date

                if birth_date_end and not start_date:
                    dates = birth_date_end.split("-")
                    if dates:
                        start_date = dates[0]
                        if start_date and birth_place:
                            start_date = "%s %s" %(start_date, birth_place)
                        elif birth_place and not start_date:
                            start_date = "%s" %(birth_place)
                        else:
                            start_date = start_date

                if death_date_start:
                    death_dates = death_date_start.split("-")
                    if death_dates:
                        end_date = death_dates[0]
                        if end_date and death_place:
                            end_date = "%s %s" %(end_date, death_place)
                        elif death_place and not end_date:
                            end_date = "%s" %(death_place)
                        else:
                            end_date = end_date

                if death_date_end and not end_date:
                    death_dates = death_date_end.split("-")
                    if death_dates:
                        end_date = death_dates[0]
                        if end_date and death_place:
                            end_date = "%s %s" %(end_date, death_place)
                        elif death_place and not end_date:
                            end_date = "%s" %(death_place)
                        else:
                            end_date = end_date

                if start_date:
                    creator_date_range = "%s" %(start_date)

                if start_date and end_date:
                    creator_date_range = "%s - %s" %(start_date, end_date)

                if not start_date and end_date:
                    creator_date_range = "%s" %(end_date)

                if creator_date_range:
                    creator_date_range = "(%s)" %(creator_date_range)
                    new_creator = "%s %s" %(new_creator, creator_date_range)

                """if birth_place:
                    new_creator = "%s<br>%s: %s" %(new_creator, self.context.translate(_("Birth place")), birth_place)
                if death_place:
                    new_creator = "%s<br>%s: %s" %(new_creator, self.context.translate(_("Death place")), death_place)"""

                #if url:
                #    new_creator = "%s<br><a href='%s' target='_blank'>%s</a>" %(new_creator, url, self.context.translate(_("Read more")))
                
                if new_creator:
                    new_creator = new_creator.strip()
                    creators.append(new_creator)

        final_value = "<br>".join(creators)
        return final_value


    def fix_author_name(self, value):

        author = value
        if value:
            try:
                author_split = value.split(',')
                if len(author_split) > 1:
                    firstname = author_split[1]
                    lastname = author_split[0]
                    firstname = firstname.strip()
                    lastname = lastname.strip()
                    author = "%s %s" %(firstname, lastname)
                    return author
            except:
                return value

        return author

    def generate_exhibitions_value(self, field, item):
        value = getattr(item, field, None)
        exhibitions = []
        context_catalog = getToolByName(self.context, 'portal_catalog')

        if value:
            # Check if DataGridField
            for doc in value:
                new_ex = ""

                title = doc.get('title', '')
                venue = doc.get('venue', '')
                place = doc.get('place', '')
                date_start = doc.get('date_start', '')
                date_end = doc.get('date_end', '')
                priref = doc.get('priref', '')
                
                if title:
                    new_ex = "%s" %(title)

                    if "activiteit" not in title:
                        if venue:
                            new_ex = "%s, %s" %(new_ex, venue)

                        if place:
                            new_ex = "%s, %s" %(new_ex, place)

                        if date_start:
                            date_start_split = date_start.split("-")
                            if date_start_split:
                                new_ex = "%s, %s" %(new_ex, date_start_split[0])
                            else:
                                new_ex = "%s, %s" %(new_ex, date_start)
                        elif date_end:
                            date_end_split = date_end.split("-")
                            if date_end_split:
                                new_ex = "%s, %s" %(new_ex, date_end_split[0])
                            else:
                                new_ex = "%s, %s" %(new_ex, date_start)
                        else:
                            new_ex = new_ex

                        if new_ex:
                            try:
                                if priref:
                                    exhibitions_objs = context_catalog(portal_type="Event", exhibition_priref=priref, Language='nl')
                                    if exhibitions_objs:
                                        exhibition_obj = exhibitions_objs[0]
                                        if exhibition_obj:
                                            exhibition_obj_url = exhibition_obj.getURL()
                                            if exhibition_obj_url:
                                                new_ex = "<a href='%s'>%s</a>" %(exhibition_obj_url, new_ex)
                                    else:
                                        pass
                            except:
                                pass

                            exhibitions.append("<li><span>"+new_ex+"</span></li>")

        if len(exhibitions) > 3:

            text_en = ["Show more +", "Show less -"]
            text_nl = ["Toon alles +", "Toon minder -"]

            text_expand = text_nl
            if getattr(self.context, 'language', 'nl') == 'en':
                text_expand = text_en

            exhibition_show = exhibitions[:3]
            exhibition_hide = exhibitions[3:]
            trigger = "<p><a href='javascript:void();' class='doc-more-info' data-toggle='collapse' data-target='#exhibition-list' aria-expanded='false'><span class='notariaexpanded'>%s</span><span class='ariaexpanded'>%s</span></a></p>" %(text_expand[0], text_expand[1])
            exhibition_show_html = "<ul>"+"".join(exhibition_show)+"</ul>"
            exhibition_hide_html = "<ul>"+"".join(exhibition_hide)+"</ul>"
            exhibition_hide_div = "<div id='exhibition-list'class='collapse' aria-expanded='false'><p>%s</p></div>" %(exhibition_hide_html)

            final_value = exhibition_show_html + trigger + exhibition_hide_div
            return final_value

        if exhibitions:
            final_value = "<ul>"+"".join(exhibitions)+"</ul>"
        else:
            final_value = ""
        return final_value

    def generate_documentation_value(self, field, item):
        value = getattr(item, field, None)
        documentations = []

        if value:
            try:
                value_sorted = sorted(list(value), key=lambda a: a.get('title', '').lower() if a.get('title', '') else a.get('title', ''))
            except:
                value_sorted = value

            # Check if DataGridField
            for doc in value_sorted:

                new_doc = ""

                title = doc.get('title', '')
                lead_word = doc.get('lead_word', '')
                author = doc.get('author', '')
                statement_of_responsibility = doc.get('statement_of_responsibility', '')
                place_of_publication = doc.get('place_of_publication', '')
                year_of_publication = doc.get('year_of_publication', '')
                page_reference = doc.get('page_references', '')

                authors = []

                for name in author:
                    final_name = self.fix_author_name(name)
                    if final_name:
                        authors.append(final_name)

                authors_final = ", ".join(authors)

                dates = ""

                if place_of_publication and year_of_publication:
                    dates = "%s, %s" %(place_of_publication, year_of_publication)
                elif not place_of_publication and year_of_publication:
                    dates = "%s" %(year_of_publication)
                elif not year_of_publication and place_of_publication:
                    dates = "%s" %(place_of_publication)
                else:
                    dates = dates

                if lead_word and title:
                    new_doc = "%s %s" %(lead_word, title)
                elif not lead_word and title:
                    new_doc = "%s" %(title)
                elif lead_word and not title:
                    new_doc = "%s" %(lead_word)
                else:
                    new_doc = new_doc

                if authors_final and not statement_of_responsibility:
                    new_doc = "%s, %s" %(new_doc, authors_final)
                elif statement_of_responsibility and not authors_final:
                    new_doc = "%s, %s" %(new_doc, statement_of_responsibility)
                elif statement_of_responsibility and authors_final:
                    new_doc = "%s, %s" %(new_doc, statement_of_responsibility)
                else:
                    new_doc = new_doc

                if dates:
                    new_doc = "%s (%s)" %(new_doc, dates)

                if page_reference:
                    new_doc = "%s (%s)" %(new_doc, page_reference)

                if new_doc:
                    documentations.append("<li><span>"+new_doc+"</span></li>")


        if len(documentations) > 3:

            text_en = ["Show more +", "Show less -"]
            text_nl = ["Toon alles +", "Toon minder -"]

            text_expand = text_nl
            if getattr(self.context, 'language', 'nl') == 'en':
                text_expand = text_en

            documentation_show = documentations[:3]
            documentation_hide = documentations[3:]
            trigger = "<p><a href='javascript:void();' class='doc-more-info' data-toggle='collapse' data-target='#doc-list' aria-expanded='false'><span class='notariaexpanded'>%s</span><span class='ariaexpanded'>%s</span></a></p>" %(text_expand[0], text_expand[1])
            documentation_show_html = "<ul>"+"".join(documentation_show)+"</ul>"
            documentation_hide_html = "<ul>"+"".join(documentation_hide)+"</ul>"
            documentation_hide_div = "<div id='doc-list'class='collapse' aria-expanded='false'><p>%s</p></div>" %(documentation_hide_html)

            final_value = documentation_show_html + trigger + documentation_hide_div
            return final_value

        if documentations:
            final_value = "<ul>"+"".join(documentations)+"</ul>"
        else:
            final_value = ""
        return final_value

    def generate_dimension_value(self, field, item):
        dimensionvalue = getattr(item, field, None)
        dimensions = []

        if dimensionvalue:

            for dimension in dimensionvalue:
                value = dimension.get('value', '')
                unit = dimension.get('unit', '')
                part = dimension.get('part', '')
                _type = dimension.get('type', '')
                precision = dimension.get('precision', '')
                notes = dimension.get('notes', '')

                new_dimension = ""

                if _type:
                    new_dimension = "%s" %(_type)

                if part:
                    new_dimension = "%s (%s)" %(new_dimension, part)

                if value:
                    new_dimension = "%s %s" %(new_dimension, value)

                if unit:
                    new_dimension = "%s %s" %(new_dimension, unit)

                if notes:
                    new_dimension = "%s (%s)" %(new_dimension, notes)

                if new_dimension:
                    new_dimension = new_dimension.strip()
                    dimensions.append(new_dimension)

        final_value = "<br>".join(dimensions)
        return final_value

    def generate_inscription_value(self, field, item):
        inscriptionvalue = getattr(item, field, None)
        inscriptions = []

        if inscriptionvalue:
            for inscription in inscriptionvalue:
                _type = inscription.get('type', '')
                position = inscription.get('position', '')
                method = inscription.get('method', '')
                content = inscription.get('content', '')
                description = inscription.get('description', '')
                notes = inscription.get('notes', '')

                new_inscription = ""

                if _type:
                    new_inscription = "%s" %(_type)

                if position:
                    new_inscription = "%s %s" %(new_inscription, position)

                if method:
                    new_inscription = "%s (%s)" %(new_inscription, method)

                new_inscription_right_part = ""
                if content:
                    new_inscription_right_part = "%s" %(content)

                if description:
                    new_inscription_right_part = "%s %s" %(new_inscription_right_part, description)

                if notes:
                    new_inscription_right_part = "%s (%s)" %(new_inscription_right_part, notes)

                if new_inscription and new_inscription_right_part:
                    new_inscription = "%s: %s" %(new_inscription, new_inscription_right_part)
                elif new_inscription and not new_inscription_right_part:
                    new_inscription = new_inscription
                elif not new_inscription and new_inscription_right_part:
                    new_inscription = new_inscription_right_part
                else:
                    new_inscription = new_inscription

                if new_inscription:
                    new_inscription = new_inscription.strip()
                    inscriptions.append("<li><span>"+new_inscription+"</span></li>")


        if len(inscriptions) > 3:

            text_en = ["Show more +", "Show less -"]
            text_nl = ["Toon alles +", "Toon minder -"]

            text_expand = text_nl
            if getattr(self.context, 'language', 'nl') == 'en':
                text_expand = text_en

            inscription_show = inscriptions[:3]
            inscription_hide = inscriptions[3:]
            trigger = "<p><a href='javascript:void();' class='doc-more-info' data-toggle='collapse' data-target='#inscription-list' aria-expanded='false'><span class='notariaexpanded'>%s</span><span class='ariaexpanded'>%s</span></a></p>" %(text_expand[0], text_expand[1])
            inscription_show_html = "<ul>"+"".join(inscription_show)+"</ul>"
            inscription_hide_html = "<ul>"+"".join(inscription_hide)+"</ul>"
            inscription_hide_div = "<div id='inscription-list'class='collapse' aria-expanded='false'><p>%s</p></div>" %(inscription_hide_html)

            final_value = inscription_show_html + trigger + inscription_hide_div
            return final_value

        if inscriptions:
            final_value = "<ul>"+"".join(inscriptions)+"</ul>"
        else:
            final_value = ""

        return final_value


    def generate_associated_subject_value(self, field, item):
        associated_subject_value = getattr(item, field, None)
        associated_subjects = []

        if associated_subject_value:
            for associated_subject in associated_subject_value:
                subject = associated_subject.get('subject', '')
                association = associated_subject.get('association', '')
                date = associated_subject.get('date', '')
                notes = associated_subject.get('notes', '')

                new_associated_subject = ""

                if subject:
                    new_associated_subject = "%s" %(subject)

                    if association:
                        new_associated_subject = "%s (%s)" %(new_associated_subject, association)

                    if date:
                        new_associated_subject = "%s<br>%s" %(new_associated_subject, date)

                    if notes:
                        new_associated_subject = "%s<br>%s" %(new_associated_subject, notes)
     
                    if new_associated_subject:
                        new_associated_subject = new_associated_subject.strip()

                        # Searchable
                        new_associated_subject = "<a href='/%s/zoeken#c25=%s'>%s</a>" %(getattr(self.context, 'language', 'nl'), url_quote(subject), new_associated_subject)
                        associated_subjects.append(new_associated_subject)
                else:
                    pass

        final_value = "<br>".join(associated_subjects)
        return final_value

    def generate_acquisition_value(self, field, item):
        acquisition_value = getattr(item, field, None)
        acquisitions = []

        if acquisition_value:
            for acquisition in acquisition_value:
                method = acquisition.get('method', '')
                date = acquisition.get('date', '')
                date_precision = acquisition.get('date_precision', '')
                notes = acquisition.get('notes', '')

                new_acquisition = ""

                date_split = date.split('-')
                if len(date_split) > 1:
                    date = date_split[0]

                if method:
                    method = method.replace('#', '')
                    new_acquisition = "%s" %(method)

                if date:
                    if date_precision:
                        new_date = "%s %s" %(date_precision, date)
                        new_acquisition = "%s %s" %(new_acquisition, new_date)
                    else:
                        new_acquisition = "%s %s" %(new_acquisition, date)

                if notes:
                    new_acquisition = "%s (%s)" %(new_acquisition, notes)
                
                new_acquisition = new_acquisition.strip()
 
                if new_acquisition:
                    new_acquisition = new_acquisition.strip()
                    acquisitions.append(new_acquisition)

        final_value = "<br>".join(acquisitions)
        return final_value


    def generate_handle_url_value(self, field, item):
        handle_url = getattr(item, field, None)
        
        if handle_url:
            value = "%s: <a href='%s' target='_blank'>%s</a>" %(self.context.translate(_("Handle url desc")), handle_url, handle_url)
            return value

        return ""

    def generate_production_value(self, field, item):
        production_value = getattr(item, field, None)
        productions = []

        if production_value:
            for production in production_value:
                date_start = production.get('date_start', '')
                date_start_precision = production.get('date_start_precision', '')
                date_end = production.get('date_end', '')
                date_end_precision = production.get('date_end_precision', '')
                notes = production.get('notes', '')
                
                new_production = ""

                start_date = ""

                if date_start_precision:
                    start_date = "%s" %(date_start_precision)

                if date_start:
                    date_start_split =  date_start.split("-")
                    if date_start_split:
                        date_start_year = date_start_split[0]
                        start_date = "%s %s" %(start_date, date_start_year)
                    else:
                        start_date = ""
                else:
                    start_date = ""
                start_date = start_date.strip()

                end_date = ""

                if date_end_precision:
                    end_date = "%s" %(date_end_precision)

                if date_end:
                    date_end_split =  date_end.split("-")
                    if date_end_split:
                        date_end_year = date_end_split[0]
                        end_date = "%s %s" %(end_date, date_end_year)
                    else:
                        end_date = ""
                else:
                    end_date = ""
                end_date = end_date.strip()


                if start_date and end_date:
                    if start_date == end_date:
                        new_production = "%s" %(start_date)
                    else:
                        new_production = "%s - %s" %(start_date, end_date)
                if not start_date and end_date:
                    new_production = "%s" %(end_date)
                elif start_date and not end_date:
                    new_production = "%s" %(start_date)
                else:
                    new_production = new_production

                if new_production:
                    if notes:
                        new_production = "%s (%s)" %(new_production, notes)
 
                if new_production:
                    new_production = new_production.strip()
                    productions.append(new_production)


        final_value = "<br>".join(productions)
        return final_value
        

    def generate_regular_value(self, field, item):
        value = getattr(self.context, field, None)
        if value and type(value) == list:

            subfield, separator, is_searchable = self.get_datagrid_subfield(field)

            if subfield:
                value = self.generate_regular_datagrid(field, item, subfield, separator, is_searchable)
                return value
            else:
                return None
            return None
        else:
            return value


    def get_in_museum(self):
        in_museum = getattr(self.context, 'in_museum', '')
        if in_museum not in NOT_ALLOWED:
            return True
        return False

    def get_current_location(self):
        
        locations = []
        current_location = getattr(self.context, 'current_location', '')

        if current_location:
            for location in current_location:
                name = location.get('name', '')
                if name not in NOT_ALLOWED:
                    if "EXPO" in name:
                        name_split = name.split('.')
                        if name_split:
                            new_name = name_split[0]
                            locations.append(new_name)
                        else:
                            locations.append(name)
                    else:
                        locations.append(name)

        if locations:
            locations_text = ", ".join(locations)
            return locations_text
        else:
            return None

    def get_published(self):
        published = getattr(self.context, 'record_published', '')
        if published not in NOT_ALLOWED:
            return True
        return False

    def get_fields(self):
        result = {"fields":[]}

        custom_fields = self.get_custom_fields()
        fields = self.get_schema(self.context)

        context_title = getattr(self.context, 'title', None)
        if context_title:
            new_field = {"label": self.object_templates('label', self.final_text("Title")), "value": self.object_templates('value', context_title)}
            result['fields'].append(new_field)

        for field, fieldschema in fields:
            # Check if field is allowed
            if field not in NOT_ALLOWED_FIELDS:
                title = fieldschema.title
                
                # Check if field as a custom generator
                if field in custom_fields:
                    value = custom_fields[field](field, self.context)
                else:
                    value = self.generate_regular_value(field, self.context)

                if value:
                    new_field = {"label": self.object_templates('label', self.final_text(title)), "value": self.object_templates('value', value)}
                    result['fields'].append(new_field)
            else:
                # Field is not allowed
                pass
        return result

    
def get_unique_values_for(catalog, index):
    if index == "object_name":
        return "3235"
    else:
        values = catalog.uniqueValuesFor(index)
        return len(values)

    return 0

class object_utils(BrowserView):

    def util(self):
        return



