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

