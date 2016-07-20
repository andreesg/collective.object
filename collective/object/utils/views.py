#!/usr/bin/python
# -*- coding: utf-8 -*-

#from collective.leadmedia.adapters import ICanContainMedia
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from collective.object import MessageFactory as _
from plone.dexterity.browser.view import DefaultView
from AccessControl import getSecurityManager
from Products.CMFCore.permissions import ModifyPortalContent
from zope.schema.interfaces import IChoice, ITextLine, IList, IText, IBool
from collective.z3cform.datagridfield.interfaces import IDataGridField
from plone.app.textfield.interfaces import IRichText
from collective.object.utils.interfaces import IListField
from z3c.relationfield.interfaces import IRelationList
from zope.i18nmessageid import MessageFactory
from zope.schema import getFields, getFieldsInOrder
from collective.object.utils.variables import GENERAL_WIDGETS
from plone.app.z3cform.widget import AjaxSelectFieldWidget, AjaxSelectWidget, SelectWidget, DatetimeFieldWidget, IAjaxSelectWidget, RelatedItemsFieldWidget
from zope.interface import alsoProvides
from .interfaces import IFormWidget
from plone.dexterity.browser import add, edit
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.uuid.utils import uuidToCatalogBrain, uuidToObject


_ = MessageFactory('collective.object')

# # # # # # # # # # # # #
# View specific methods #
# # # # # # # # # # # # #

class ObjectView(edit.DefaultEditForm):
    """ View class """

    general_widgets = {}
    general_widgets_order = GENERAL_WIDGETS

    template = ViewPageTemplateFile('../object_templates/view.pt')

    def update(self):
        super(ObjectView, self).update()
        for group in self.groups:
            for widget in group.widgets.values():
                if IDataGridField.providedBy(widget):
                    widget.auto_append = False
                    widget.allow_reorder = True
                alsoProvides(widget, IFormWidget)

        for widget in self.widgets.values():
            if IDataGridField.providedBy(widget) or IAjaxSelectWidget.providedBy(widget):
                widget.auto_append = False
                widget.allow_reorder = True
                alsoProvides(widget, IFormWidget)

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

        brain = uuidToCatalogBrain(item_uid)
        #if brain:
        #    leadmedia_uid = brain.leadMedia
        #    if leadmedia_uid:
        #        lead_media = uuidToCatalogBrain(leadmedia_uid)
        #        details['image'] = lead_media.getURL() + "/@@images/image/large"

        return details

