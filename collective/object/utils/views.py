#!/usr/bin/python
# -*- coding: utf-8 -*-

from collective.leadmedia.adapters import ICanContainMedia
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

_ = MessageFactory('collective.object')

# # # # # # # # # # # # #
# View specific methods #
# # # # # # # # # # # # #

class ObjectView(DefaultView):
    """ View class """

    """
    MultiContentTreeWidget
    TextWidget
    BlockDataGridField
    DataGridField
    TextAreaWidget
    SelectWidget

    """
    def get_fieldtype_by_schema(self, field):
        f = str(field)

        type_field = ""
        if "MultiContentTreeWidget" in f:
            type_field = "relation"
        elif "TextWidget" in f:
            type_field = "text"
        elif "BlockDataGridField" in f:
            type_field = "datagrid"
        elif "DataGridField" in f:
            type_field = "datagrid"
        elif "TextAreaWidget" in f:
            type_field = "text"
        elif "SelectWidget" in f:
            type_field = "select"
        else:
            type_field = "unknown"

        return type_field

    def checkUserPermission(self):
        sm = getSecurityManager()
        if sm.checkPermission(ModifyPortalContent, self.context):
            return True
        return False

    def transform_value(self, value):

        if 'collective.exhibition.exhibition.Exhibition' in str(type(value)):
            uid = value.UID()

            url = self.get_url_by_uid(uid)
            value = "<a href='%s'>%s</a>" %(url, value.title)
            return value

        elif 'collective.' in str(type(value)):
            uid = value.UID()

            url = self.get_url_by_uid(uid)
            value = "<a href='%s'>%s</a>" %(url, value.title)
            return value

        if value == "selected":
            value = "Ja"

        if value == False:
            value = "Nee"

        if value == True:
            value = "Ja"

        return value

    def show_fieldset(self, fieldset):
        for widget in fieldset.widgets.values():
            if widget.value:
                return True
        return False

    def get_url_by_uid(self, uid):
        catalog = self.context.portal_catalog
        brains = catalog(UID=uid)
        if brains:
            obj = brains[0]
            return obj.getURL()

        return ""

    def append_value(self, _list, value, subfield=False):
      
        if 'collective.exhibition.exhibition.Exhibition' in str(type(value)):
            uid = value.UID()

            url = self.get_url_by_uid(uid)
            value = "<a href='%s'>%s</a>" %(url, value.title)
            _list.append(value)
            return

        elif 'collective.' in str(type(value)):
            uid = value.UID()

            url = self.get_url_by_uid(uid)
            value = "<a href='%s'>%s</a>" %(url, value.title)
            _list.append(value)
            return

        if value != "" and value != None and value != " " and value != []:
            if subfield:
                subfield_translation = _(subfield)
                value = "%s: %s" %(self.context.translate(subfield_translation), self.transform_value(value))

            _list.append(self.transform_value(value))

    def generate_value_from_item(self, item, line):
        if type(item) is str:
            self.append_value(line, self.transform_value(item))
        
        elif type(item) is list:
            for elem in item:
                if type(elem) is dict:
                    for key in elem.keys():
                        #val = "%s: %s<p>" %(key, elem[key])
                        val = elem[key]
                        self.append_value(line, val, key)
                
                elif type(elem) is list:
                    for e in elem:
                        self.append_value(line, e)
                else:
                    self.append_value(line, elem)
                
                self.append_value(line, '<p>')
        else:
            for key in item.keys():
                if type(item[key]) is list:
                    for val in item[key]:
                        vals = []
                        if val:
                            vals.append(self.transform_value(val))
                        vals = ', '.join(vals)

                        self.append_value(line, vals, key)
                else:
                    #val = "%s: %s<p>" %(key, item[key])
                    val = item[key]
                    self.append_value(line, val, key)

    def get_field_value(self, value, widget):
        _type = self.get_fieldtype_by_schema(widget)

        if value == None:
            return ""

        if _type in ["datagrid", "select"]:
            try:
                result = []
                for item in value:
                    line = []
                    self.generate_value_from_item(item, line)
                    #print line
                    line = '<p>'.join(line)
                    
                    result.append(line)
                result = '<p>'.join(result)
                return result
            except:
                raise
                return ""

        elif _type == "relation":
            return ""


        return value

    def trim_white_spaces(self, text):
        if text != "" and text != None:
            if len(text) > 0:
                if text[0] == " ":
                    text = text[1:]
                if len(text) > 0:
                    if text[-1] == " ":
                        text = text[:-1]
                return text
            else:
                return ""
        else:
            return ""

    def create_author_name(self, value):
        comma_split = value.split(",")

        for i in range(len(comma_split)):       
            name_split = comma_split[i].split('(')
            
            raw_name = name_split[0]
            name_split[0] = self.trim_white_spaces(raw_name)
            name_artist = name_split[0]
            
            name_artist_link = '<a href="/'+self.context.language+'/search?SearchableText=%s">%s</a>' % (name_artist, name_artist)
            name_split[0] = name_artist_link

            if len(name_split) > 1:
                if len(name_split[1]) > 0:
                    name_split[0] = name_artist_link + " "
        
            comma_split[i] = '('.join(name_split)

        _value = ", ".join(comma_split)

        return _value

    def create_materials(self, value):
        materials = value.split(',')
        _value = ""
        for i, mat in enumerate(materials):
            if i == (len(materials)-1):
                _value += '<a href="/'+self.context.language+'/search?SearchableText=%s">%s</a>' % (mat, mat)
            else:
                _value += '<a href="/'+self.context.language+'/search?SearchableText=%s">%s</a>, ' % (mat, mat)

        return _value

    def getSearchableValue(self, name, value):
        _value = ""

        if (name == 'artist') or (name == 'author'):
            _value = self.create_author_name(value)
        elif (name == 'material') or (name == 'technique'):
            _value = self.create_materials(value)
        else:
            _value = '<a href="/'+self.context.language+'/search?SearchableText=%s">%s</a>' % (value, value)

        return _value

    def getFBdetails(self):
        item = self.context
        
        state = getMultiAdapter(
                (item, self.request),
                name=u'plone_context_state')

        # Check view type
        view_type = state.view_template_id()

        obj = ICanContainMedia(item)

        details = {}
        details["title"] = item.Title()
        details["type"] = "article"
        details["site_name"] = "ZM"
        details["url"] = item.absolute_url()
        details["description"] = item.Description()
        details["double_image"] = ""
        details["image"] = ""
        
        if view_type == "instruments_view":
            if hasattr(item, 'slideshow'):
                catalog = getToolByName(self.context, 'portal_catalog')
                slideshow = item['slideshow']
                path = '/'.join(slideshow.getPhysicalPath())
                results = catalog.searchResults(path={'query': path, 'depth': 1, 'portal_type': 'Image'}, sort_on='sortable_title')
                if len(results) > 0:
                    lead_image = results[0]
                    if lead_image.portal_type == "Image":
                        details["image"] = lead_image.getObject().absolute_url()+"/@@images/image/large"
                else:
                    details["image"] = ""
                

        if details["image"] == "":
            if obj.hasMedia():
                image = obj.getLeadMedia()
                details["image"] = image.absolute_url()+"/@@images/image/large"
                
                if view_type == "double_view":
                    if hasattr(item, 'slideshow'):
                        slideshow = item['slideshow']
                        if len(slideshow.objectIds()) > 1:
                            double_image = slideshow[slideshow.objectIds()[1]]
                            if double_image.portal_type == "Image":
                                details["double_image"] = double_image.absolute_url()+"/@@images/image/large"
            else:
                details["image"] = ""

        return details
