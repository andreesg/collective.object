#!/usr/bin/python
# -*- coding: utf-8 -*-

#from collective.leadmedia.adapters import ICanContainMedia
from zope.component import getMultiAdapter, getUtility
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFCore.utils import getToolByName

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

NOT_ALLOWED = [None, '', ' ', 'None']
NOT_ALLOWED_FIELDS = ['priref', 'collection', 'in_museum', 'record_published', 'current_location']

# # # # # # # # # # # # #
# View specific methods #
# # # # # # # # # # # # #



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
            "label":"<div class='col-lg-5 col-md-5 col-sm-5 col-xs-12 object-label'><p>%s</p></div>",
            "value":"<div class='col-lg-7 col-md-7 col-sm-7 col-xs-12 object-value'><p>%s</p></div>"
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
            "documentation": self.generate_documentation_value
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

        separator = ", "
        if field in SEPARATORS:
            separator = SEPARATORS[field]

        if field in DATAGRID_SUBFIELDS:
            return DATAGRID_SUBFIELDS[field], separator
        else:
            return None, separator

    def generate_regular_datagrid(self, field, item, subfield, separator=', '):
        value = getattr(item, field, None)

        values = []

        if subfield:
            if value:
                for subitem in value:
                    if subfield in subitem:
                        subfield_value = subitem.get(subfield, '')
                        if subfield_value:
                            if separator == "<br>":
                                values.append("<span>%s</span>" %(subfield_value))
                            else:
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

                url = creator.get('url', '')

                # Create name
                if name:
                    name_split = name.split(",")
                    if len(name_split) > 1:
                        firstname = name_split[1]
                        lastname = name_split[0]
                        name = "%s %s" %(firstname, lastname)
                    new_creator = "%s" %(name)

                if qualifier:
                    new_creator = "%s %s" %(qualifier, new_creator)

                if role:
                    new_creator = "%s (%s)" %(new_creator, role)

                start_date = ""
                end_date = ""
                creator_date_range = ""

                if birth_date_start:
                    dates = birth_date_start.split("-")
                    if dates:
                        start_date = dates[0]

                if birth_date_end and not start_date:
                    dates = birth_date_end.split("-")
                    if dates:
                        start_date = dates[0]

                if death_date_start:
                    death_dates = death_date_start.split("-")
                    if death_dates:
                        end_date = death_dates[0]

                if death_date_end and not end_date:
                    death_dates = death_date_end.split("-")
                    if death_dates:
                        end_date = death_dates[0]

                if start_date:
                    creator_date_range = "%s" %(start_date)

                if start_date and end_date:
                    creator_date_range = "%s - %s" %(start_date, end_date)

                if not start_date and end_date:
                    creator_date_range = "%s" %(end_date)

                if creator_date_range:
                    creator_date_range = "(%s)" %(creator_date_range)
                    new_creator = "%s %s" %(new_creator, creator_date_range)

                if birth_place:
                    new_creator = "%s<br>%s: %s" %(new_creator, self.context.translate(_("Birth place")), birth_place)
                if death_place:
                    new_creator = "%s<br>%s: %s" %(new_creator, self.context.translate(_("Death place")), death_place)

                if url:
                    new_creator = "%s<br><a href='%s' target='_blank'>%s</a>" %(new_creator, url, self.context.translate(_("Read more")))
                
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

    def generate_documentation_value(self, field, item):
        value = getattr(item, field, None)
        documentations = []

        if value:
            # Check if DataGridField
            for doc in value:
                new_doc = ""

                title = doc.get('title', '')
                lead_word = doc.get('lead_word', '')
                author = doc.get('author', '')
                statement_of_responsibility = doc.get('statement_of_responsibility', '')
                place_of_publication = doc.get('place_of_publication', '')
                year_of_publication = doc.get('year_of_publication', '')


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

                documentations.append("<span>"+new_doc+"</span>")


        if len(documentations) > 3:

            text_en = ["Show more", "Show less"]
            text_nl = ["Toon alle documentatie waarin dit object voorkomt", "Toon minder documentatie"]

            text_expand = text_nl
            if getattr(self.context, 'language', 'nl') == 'en':
                text_expand = text_en

            documentation_show = documentations[:3]
            documentation_hide = documentations[3:]
            trigger = "<p><a href='javascript:void();' class='doc-more-info' data-toggle='collapse' data-target='#doc-list' aria-expanded='false'><span class='notariaexpanded'>%s</span><span class='ariaexpanded'>%s</span></a></p>" %(text_expand[0], text_expand[1])
            documentation_show_html = "<br>".join(documentation_show)
            documentation_hide_html = "<br>".join(documentation_hide)
            documentation_hide_div = "<div id='doc-list'class='collapse' aria-expanded='false'><p>%s</p></div>" %(documentation_hide_html)

            final_value = documentation_show_html + documentation_hide_div + trigger
            return final_value

        final_value = "<br>".join(documentations)
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
                    new_dimension = "%s<br>%s" %(new_dimension, notes)

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
                    inscriptions.append(new_inscription)

        final_value = "<br>".join(inscriptions)
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

                new_acquisition = ""

                date_split = date.split('-')
                if len(date_split) > 1:
                    date = date_split[0]

                if method:
                    new_acquisition = "%s" %(method)

                if date:
                    if date_precision:
                        new_date = "%s %s" %(date_precision, date)
                        new_acquisition = "%s (%s)" %(new_acquisition, new_date)
                    else:
                        new_acquisition = "%s (%s)" %(new_acquisition, date)
                
                new_acquisition = new_acquisition.strip()
 
                if new_acquisition:
                    new_acquisition = new_acquisition.strip()
                    acquisitions.append(new_acquisition)

        final_value = "<br>".join(acquisitions)
        return final_value

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

            subfield, separator = self.get_datagrid_subfield(field)

            if subfield:
                value = self.generate_regular_datagrid(field, item, subfield, separator)
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

    


class object_utils(BrowserView):

    def util(self):
        return



