
#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from collective.object import MessageFactory as _
from zope.schema.interfaces import ISource, IContextSourceBinder, IVocabularyFactory
from zope.interface import implements, classProvides
from Products.CMFCore.utils import getToolByName
from plone import api
from zope.component.hooks import getSite
from binascii import b2a_qp
from Products.CMFPlone.utils import safe_unicode
from plone.app.vocabularies.catalog import CatalogVocabulary
from plone.app.querystring import queryparser
from eea.faceted.vocabularies.utils import IVocabularyFactory as IVocabularyFactoryEEA
from zope.interface import implementer
from plone.app.vocabularies.terms import safe_encode as safe_enc, safe_simpleterm_from_value
import datetime
from plone.memoize.view import memoize, memoize_contextless
from plone.memoize import ram
from time import time
from operator import itemgetter

def safe_simplevocabulary_from_values(values, query=None):
    """Creates (filtered) SimpleVocabulary from iterable of untrusted values.
    """
    items = [
        safe_simpleterm_from_value(i[0])
        for i in values
        if query is None or safe_enc(query) in safe_enc(i[0])
    ]
    return SimpleVocabulary(items)

@implementer(IVocabularyFactory)
class CreatorNameVocabulary(object):
    """Vocabulary factory for sortable_creator_name index.
    """
    
    def get_values(self, context, query=None):
        site = getSite()
        self.catalog = getToolByName(site, 'portal_catalog', None)
        if self.catalog is None:
            return SimpleVocabulary([])
        """index = self.catalog._catalog.getIndex('creatorname')
        values = safe_simplevocabulary_from_values(index._index, query=query)"""
        indexes = list(self.catalog.Indexes.get('creatorname', []).uniqueValues(withLengths=True))
        indexes.sort(key=itemgetter(1), reverse=True)
        values = safe_simplevocabulary_from_values(indexes, query=query)
        return values

    def __call__(self, context, query=None):
        values = self.get_values(context, query)
        return values

@implementer(IVocabularyFactory)
class CreatorNameIndexVocabulary(object):
    """Vocabulary factory for sortable_creator_name index.
    """
    
    def get_values(self, context, query=None):
        site = getSite()
        self.catalog = getToolByName(site, 'portal_catalog', None)
        if self.catalog is None:
            return SimpleVocabulary([])
        """index = self.catalog._catalog.getIndex('creatorname')
        values = safe_simplevocabulary_from_values(index._index, query=query)"""
        indexes = list(self.catalog.Indexes.get('creator_name_index', []).uniqueValues(withLengths=True))
        indexes.sort(key=itemgetter(1), reverse=True)
        values = safe_simplevocabulary_from_values(indexes, query=query)
        return values

    def __call__(self, context, query=None):
        values = self.get_values(context, query)
        return values

@implementer(IVocabularyFactory)
class ObjectNameVocabulary(object):
    """Vocabulary factory for sortable_creator_name index.
    """
    
    def get_values(self, context, query=None):
        site = getSite()
        self.catalog = getToolByName(site, 'portal_catalog', None)
        if self.catalog is None:
            return SimpleVocabulary([])
        """index = self.catalog._catalog.getIndex('creatorname')
        values = safe_simplevocabulary_from_values(index._index, query=query)"""
        indexes = list(self.catalog.Indexes.get('object_name_index', []).uniqueValues(withLengths=True))
        indexes.sort(key=itemgetter(1), reverse=True)
        values = safe_simplevocabulary_from_values(indexes, query=query)
        return values

    def __call__(self, context, query=None):
        values = self.get_values(context, query)
        return values

@implementer(IVocabularyFactory)
class TechniqueVocabulary(object):
    """Vocabulary factory for sortable_creator_name index.
    """
    
    def get_values(self, context, query=None):
        site = getSite()
        self.catalog = getToolByName(site, 'portal_catalog', None)
        if self.catalog is None:
            return SimpleVocabulary([])
        """index = self.catalog._catalog.getIndex('creatorname')
        values = safe_simplevocabulary_from_values(index._index, query=query)"""
        indexes = list(self.catalog.Indexes.get('technique_index', []).uniqueValues(withLengths=True))
        indexes.sort(key=itemgetter(1), reverse=True)
        values = safe_simplevocabulary_from_values(indexes, query=query)
        return values

    def __call__(self, context, query=None):
        values = self.get_values(context, query)
        return values

@implementer(IVocabularyFactory)
class MaterialVocabulary(object):
    """Vocabulary factory for sortable_creator_name index.
    """
    
    def get_values(self, context, query=None):
        site = getSite()
        self.catalog = getToolByName(site, 'portal_catalog', None)
        if self.catalog is None:
            return SimpleVocabulary([])
        """index = self.catalog._catalog.getIndex('creatorname')
        values = safe_simplevocabulary_from_values(index._index, query=query)"""
        indexes = list(self.catalog.Indexes.get('material_index', []).uniqueValues(withLengths=True))
        indexes.sort(key=itemgetter(1), reverse=True)
        values = safe_simplevocabulary_from_values(indexes, query=query)
        return values

    def __call__(self, context, query=None):
        values = self.get_values(context, query)
        return values


@implementer(IVocabularyFactory)
class CreatorPlaceVocabulary(object):
    """Vocabulary factory for sortable_creator_name index.
    """
    
    def get_values(self, context, query=None):
        site = getSite()
        self.catalog = getToolByName(site, 'portal_catalog', None)
        if self.catalog is None:
            return SimpleVocabulary([])
        """index = self.catalog._catalog.getIndex('creatorname')
        values = safe_simplevocabulary_from_values(index._index, query=query)"""
        indexes = list(self.catalog.Indexes.get('creator_place_index', []).uniqueValues(withLengths=True))
        indexes.sort(key=itemgetter(1), reverse=True)
        values = safe_simplevocabulary_from_values(indexes, query=query)
        return values

    def __call__(self, context, query=None):
        values = self.get_values(context, query)
        return values


@implementer(IVocabularyFactory)
class PlaceVocabulary(object):
    """Vocabulary factory for sortable_creator_name index.
    """
    
    def get_values(self, context, query=None):
        site = getSite()
        self.catalog = getToolByName(site, 'portal_catalog', None)
        if self.catalog is None:
            return SimpleVocabulary([])
        """index = self.catalog._catalog.getIndex('creatorname')
        values = safe_simplevocabulary_from_values(index._index, query=query)"""
        indexes = list(self.catalog.Indexes.get('place_index', []).uniqueValues(withLengths=True))
        indexes.sort(key=itemgetter(1), reverse=True)
        values = safe_simplevocabulary_from_values(indexes, query=query)
        return values

    def __call__(self, context, query=None):
        values = self.get_values(context, query)
        return values

@implementer(IVocabularyFactory)
class WebsiteCollectionExhibitionVocabulary(object):
    """Vocabulary factory for sortable_creator_name index.
    """
    
    def get_values(self, context, query=None):
        site = getSite()
        self.catalog = getToolByName(site, 'portal_catalog', None)
        if self.catalog is None:
            return SimpleVocabulary([])
        """index = self.catalog._catalog.getIndex('creatorname')
        values = safe_simplevocabulary_from_values(index._index, query=query)"""
        indexes = list(self.catalog.Indexes.get('website_collection_exhibition_index', []).uniqueValues(withLengths=True))
        indexes.sort(key=itemgetter(1), reverse=True)
        values = safe_simplevocabulary_from_values(indexes, query=query)
        return values

    def __call__(self, context, query=None):
        values = self.get_values(context, query)
        return values

@implementer(IVocabularyFactory)
class PeriodVocabulary(object):
    """Vocabulary factory for sortable_creator_name index.
    """
    
    def get_values(self, context, query=None):
        site = getSite()
        self.catalog = getToolByName(site, 'portal_catalog', None)
        if self.catalog is None:
            return SimpleVocabulary([])
        """index = self.catalog._catalog.getIndex('creatorname')
        values = safe_simplevocabulary_from_values(index._index, query=query)"""
        indexes = list(self.catalog.Indexes.get('period_index', []).uniqueValues(withLengths=True))
        indexes.sort(key=itemgetter(1), reverse=True)
        values = safe_simplevocabulary_from_values(indexes, query=query)
        return values

    def __call__(self, context, query=None):
        values = self.get_values(context, query)
        return values

@implementer(IVocabularyFactory)
class ObjectPeriodVocabulary(object):
    """Vocabulary factory for sortable_creator_name index.
    """
    
    def get_values(self, context, query=None):
        site = getSite()
        self.catalog = getToolByName(site, 'portal_catalog', None)
        if self.catalog is None:
            return SimpleVocabulary([])
        """index = self.catalog._catalog.getIndex('creatorname')
        values = safe_simplevocabulary_from_values(index._index, query=query)"""
        indexes = list(self.catalog.Indexes.get('object_period_index', []).uniqueValues(withLengths=True))
        indexes.sort(key=itemgetter(1), reverse=True)
        values = safe_simplevocabulary_from_values(indexes, query=query)
        return values

    def __call__(self, context, query=None):
        values = self.get_values(context, query)
        return values


class ObjectVocabulary(object):

    implements(IVocabularyFactory)

    def __init__(self, index):
        self.index = index

    def __call__(self, context, query=None):
        self.context = context
        
        site = getSite()

        if not context:
        	self.context = site
        	
        self.catalog = getToolByName(site, "portal_catalog")
        if self.catalog is None:
            return SimpleVocabulary([])
        index = self.catalog._catalog.getIndex(self.index)
        
        def safe_encode(term):
            if isinstance(term, unicode):
                # no need to use portal encoding for transitional encoding from
                # unicode to ascii. utf-8 should be fine.
                term = term.encode('utf-8')
            return term

        items = []

        for i in index._index:
            if type(i) != list and (query is None or safe_encode(query).lower() in safe_encode(i).lower()):
                items.append(SimpleTerm(i, b2a_qp(safe_encode(i)), safe_unicode(i)))

        items.sort(key=lambda x: x.token.lower())

        return SimpleVocabulary(items)

AuthorVocabularyFactory = ObjectVocabulary('documentation_author')
AssociationSubjectVocabularyFactory = ObjectVocabulary('association_subject')
AcquisitionMethodVocabularyFactory = ObjectVocabulary('acquisition_method')
CreatorRoleVocabularyFactory = ObjectVocabulary('creator_role')
CreatorQualifierVocabularyFactory = ObjectVocabulary('creator_qualifier')
CreatorPlaceVocabularyFactory = ObjectVocabulary('creator_place')
CreatorNameVocabularyFactory = ObjectVocabulary('sortable_creator_name')
CollectionVocabularyFactory = ObjectVocabulary('collection')
ObjectNameVocabularyFactory = ObjectVocabulary('objectname')

CollectionIndexVocabularyFactory = ObjectVocabulary('collection_index')

