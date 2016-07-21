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
from collective.object.utils.variables import GENERAL_WIDGETS
from plone.app.z3cform.widget import AjaxSelectFieldWidget, AjaxSelectWidget, SelectWidget, DatetimeFieldWidget, IAjaxSelectWidget, RelatedItemsFieldWidget
from zope.interface import alsoProvides
from .interfaces import IFormWidget
from plone.dexterity.browser import add, edit
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.uuid.utils import uuidToCatalogBrain, uuidToObject
from Products.Five import BrowserView
import json
from collective.object import MessageFactory as _

NOT_ALLOWED = [None, '', ' ', 'None']

# # # # # # # # # # # # #
# View specific methods #
# # # # # # # # # # # # #

class ObjectFields(BrowserView):
    def get_object_body(self, object):
        if hasattr(object, 'text') and object.text != None:
            return object.text.output
        else:
            return ""

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
            
            name_artist_link = '<a href="/search?SearchableText=%s">%s</a>' % (name_artist, name_artist)
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
                _value += '<a href="/search?SearchableText=%s">%s</a>' % (mat, mat)
            else:
                _value += '<a href="/search?SearchableText=%s">%s</a>, ' % (mat, mat)

        return _value

    def get_field_from_object(self, field, object):
        
        empty_field = ""
        
        value = getattr(object, field, "")
        if value != "" and value != None:
            return value
        
        return empty_field

    def get_field_from_schema(self, fieldname, schema):
        for name, field in schema:
            if name == fieldname:
                return field

        return None

    def transform_schema_field(self, name, field_value, choice=None, restriction=None, not_show=[]):
        try:
            if type(field_value) is list:
                new_val = []
                if choice == None:
                    for val in field_value:
                        if type(val) is unicode:
                            new_val.append(val)
                        elif type(val) is str:
                            new_val.append(val)
                        else:
                            for key, value in val.iteritems():
                                if key not in not_show:
                                    if value != "" and value != None and value != " ":
                                        if restriction != None:
                                            if value != restriction:
                                                if key in "name" and name not in ['exhibitions_exhibition','identification_objectName_objectname']:
                                                    value = self.create_maker(value)
                                                if type(value) is list: 
                                                    new_val.append(value[0])
                                                else:
                                                    new_val.append(value)
                                        else:
                                            if key == "name" and name not in ['exhibitions_exhibition','identification_objectName_objectname']:
                                                value = self.create_maker(value)
                                            if type(value) is list: 
                                                new_val.append(value[0])
                                            else:
                                                new_val.append(value)
                else:
                    for val in field_value:
                        if val[choice] != "" and val[choice] != None and val[choice] != " ":
                            if restriction != None:
                                if val[choice] != restriction:
                                    if choice == "name" and name not in ['exhibitions_exhibition','identification_objectName_objectname']:
                                        new_val.append(self.create_maker(val[choice]))
                                    else:
                                        
                                        if type(val[choice]) is list: 
                                            if val[choice]:
                                                new_val.append(val[choice][0])
                                        else:
                                            new_val.append(val[choice])
                            else:
                                if choice in ["name", "author"] and name not in ['exhibitions_exhibition','identification_objectName_objectname']:
                                    new_val.append(self.create_maker(val[choice]))
                                else:
                                    if type(val[choice]) is list: 
                                        if val[choice]:
                                            new_val.append(val[choice][0])
                                    else:
                                        new_val.append(val[choice])

                if len(new_val) > 0:
                    if name in ["exhibitions_exhibition", "productionDating_production", "labels", "seriesNotesISBN_notes_bibliographicalNotes",
                                "abstractAndSubjectTerms_notes", "abstractAndSubjectTerms_abstract_abstract",
                                "exhibitionsAuctionsCollections_exhibition", "exhibitionsAuctionsCollections_auction",
                                "exhibitionsAuctionsCollections_collection"]:
                        return '<p>'.join(new_val)
                    else:
                        for index, single_value in enumerate(new_val):
                            single_value = "<a href='/search?SearchableText=%s'>%s</a>" %(single_value, single_value)
                            new_val[index] = single_value
                        return ', '.join(new_val)
                else:
                    return ""
            else:
                return field_value
        except:
            return ""


    def generate_identification_tab(self, identification_tab, object_schema, fields, object, field_schema):
        for field, choice in identification_tab:
            # Title field
            if field in ['title']:
                value = getattr(object, field, "")
                if value != "" and value != None and value != " ":
                    object_schema[field_schema]['fields'].append({"title": self.context.translate(_('Title')), "value": value})

            elif field in ['text']:
                val = getattr(object, field, "")
                if val:
                    value = val.output
                else:
                    value = ""
                if value != "" and value != None and value != " ":
                    object_schema[field_schema]['fields'].append({"title": "body", "value": value})
            
            # Regular fields
            elif field not in ['identification_taxonomy']:
                fieldvalue = self.get_field_from_schema(field, fields)
                if fieldvalue != None:
                    title = fieldvalue.title
                    value = self.get_field_from_object(field, object)

                    schema_value = self.transform_schema_field(field, value, choice)

                    if schema_value != "" and schema_value != " ":
                        object_schema[field_schema]['fields'].append({"title": self.context.translate(_(title)), "value": schema_value})

            # Taxonomy special case
            else:
                taxonomy = self.get_field_from_object(field, object)
                if len(taxonomy) > 0:
                    scientific_names = []
                    common_names_list = []

                    for taxonomy_elem in taxonomy:
                        scientific_name = taxonomy_elem['scientific_name']
                        if scientific_name:
                            tax = scientific_name[0]
                            tax_obj = None
                            if IRelationValue.providedBy(tax):
                                tax_obj = tax.to_object
                            else:
                                tax_obj = tax

                            if tax_obj:
                                tax_title = getattr(tax_obj, 'title', '')
                                if tax_title:
                                    scientific_names.append(tax_title)

                                common_name = getattr(tax_obj, 'taxonomicTermDetails_commonName', '')
                                if common_name:
                                    common_names = []
                                    for line in common_name:
                                        if line['commonName'] not in [None, '', ' ']:
                                            common_names.append(line['commonName'])

                                    common_names_list.extend(common_names)
                    
                    if scientific_names:     
                        object_schema[field_schema]['fields'].append({"title": self.context.translate(_('Scient. name')), "value": ', '.join(scientific_names)})
                    
                    if common_names_list:
                        object_schema[field_schema]['fields'].append({"title": self.context.translate(_('Common name')), "value": ', '.join(common_names_list)})


    def create_maker(self, name, url=False):
        maker = []
        name_split = name.split(",")

        if len(name_split) > 0:
            if len(name_split) > 1:
                maker.append(name_split[-1])
                maker.append(name_split[0])
            else:
                maker.append(name_split[0])

        new_maker = ' '.join(maker)
        if url:
            new_maker = new_maker

        return new_maker

    def create_production_field(self, field, url=False):
        production = ""

        maker = field['maker']
        qualifier = field['qualifier']
        role = field['role']
        place = field['place']

        production = self.create_maker(maker, url)

        if qualifier not in NOT_ALLOWED:
            if production:
                production = "%s, %s" %(qualifier, production)
            else:
                production = "%s" %(qualifier)

        if role not in NOT_ALLOWED:
            if production:
                production = "(%s) %s" %(role, production)
            else:
                production = "(%s)" %(role)

        if place not in NOT_ALLOWED:
            if production:
                production = "%s, %s" %(production, place)
            else:
                production = "%s" %(place)

        return production

    def create_period_field(self, field):
        period = field['period']
        start_date = field['date_early']
        start_date_precision = field['date_early_precision']
        end_date = field['date_late']
        end_date_precision = field['date_late_precision']

        result = ""

        if period != "" and period != None and period != " ":
            result = "%s" %(period)

        if start_date != "" and start_date != " ":
            if result:
                if start_date_precision != "" and start_date_precision != " ":
                    result = "%s, %s %s" %(result, start_date_precision, start_date)
                else:
                    result = "%s, %s" %(result, start_date)
            else:
                if start_date_precision != "" and start_date_precision != " ":
                    result = "%s %s" %(start_date_precision, start_date)
                else:
                    result = "%s" %(start_date)
    

        if end_date != "" and end_date != " ":
            if result:
                if end_date_precision != "" and end_date_precision != " ":
                    result = "%s - %s %s" %(result, end_date_precision, start_date)
                else:
                    result = "%s - %s" %(result, end_date)
            else:
                if end_date_precision != "" and end_date_precision != " ":
                    result = "%s %s" %(end_date_precision, start_date)
                else:
                    result = "%s" %(end_date)

        return result

    def get_url_by_uid(self, uid):
        brains = uuidToCatalogBrain(uid)
        if brains:
            return brains.getURL()

        return ""


    def generate_production_dating(self, production_dating_tab, object_schema, fields, object, field_schema):
        production_field = self.get_field_from_object('productionDating_productionDating', object)

        production_result = []
        # Generate production
        url = ""
        for field in production_field:
            production = {}
            if field['makers']:
                production['maker'] = field["makers"][0].title
                url = self.get_url_by_uid(field["makers"][0].UID())
            else:
                production['maker'] = ""

            production['qualifier'] = field['qualifier']

            if field['role']:
                production['role'] = field['role'][0]
            else:
                production['role'] = ""

            if field['place']:
                production['place'] = field['place'][0]
            else:
                production['place'] = ""

            result = self.create_production_field(production, url)
            if result not in NOT_ALLOWED:
                production_result.append(result)

        if len(production_result) > 0:
            production_value = '<p>'.join(production_result)
            object_schema[field_schema]['fields'].append({"title": self.context.translate(_('Maker')), "value": production_value})

        ## Generate Period
        period_field = self.get_field_from_object('productionDating_dating_period', object)

        period = []
        for field in period_field:
            result = self.create_period_field(field)
            if result not in NOT_ALLOWED:
                period.append(result)

        if len(period) > 0:
            period_value = ', '.join(period)
            object_schema[field_schema]['fields'].append({"title": self.context.translate(_('Period')), "value": period_value})

    def generate_production_dating_tab(self, production_dating_tab, object_schema, fields, object, field_schema):

        ## Generate Author
        production_field = self.get_field_from_object('productionDating_production', object)
        production = []
        for field in production_field:
            result = self.create_production_field(field)
            if result not in NOT_ALLOWED:
                production.append(result)

        if len(production) > 0:
            production_value = '<p>'.join(production)
            object_schema[field_schema]['fields'].append({"title": self.context.translate(_('Maker')), "value": production_value})

        ## Generate Period
        period_field = self.get_field_from_object('productionDating_dating_period', object)

        period = []
        for field in period_field:
            result = self.create_period_field(field)
            if result not in NOT_ALLOWED:
                period.append(result)

        if len(period) > 0:
            period_value = ', '.join(period)
            object_schema[field_schema]['fields'].append({"title": self.context.translate(_('Period')), "value": period_value})

    def create_dimension_field(self, field):
        new_dimension_val = []
        dimension_result = ""

        for val in field:
            dimension = ""
            if val['value'] != "":
                dimension = "%s" %(val['value'])
            if val['units'] != "":
                dimension = "%s %s" %(dimension, val['units'])
            if val['dimension'] != "" and val['dimension'] != []:
                dimension = "%s: %s" %(val['dimension'][0], dimension)

            new_dimension_val.append(dimension)

        dimension_result = '<p>'.join(new_dimension_val)
        
        return dimension_result

    def generate_physical_characteristics_tab(self, physical_characteristics_tab, object_schema, fields, object, field_schema):
        
        for field, choice, restriction in physical_characteristics_tab:
            if field == 'physicalCharacteristics_dimension':
                dimension_field = getattr(object, 'physicalCharacteristics_dimension', None)
                if dimension_field != None:
                    dimension = self.create_dimension_field(dimension_field)
                    ## add to schema
                    if dimension != "" and dimension != None:
                        object_schema[field_schema]['fields'].append({"title": self.context.translate(_('Dimensions')), "value": dimension})
            else:
                fieldvalue = self.get_field_from_schema(field, fields)
                if fieldvalue != None:
                    title = fieldvalue.title
                    value = self.get_field_from_object(field, object)

                    schema_value = self.transform_schema_field(field, value, choice)

                    if schema_value != "":
                        object_schema[field_schema]['fields'].append({"title": self.context.translate(_(title)), "value": schema_value})


    def generate_associations_tab(self, associations_tab, object_schema, fields, object, field_schema):
        for field, choice, restriction in associations_tab:
            if field == "associations_associatedPersonInstitutions":
                fieldvalue = self.get_field_from_schema(field, fields)
                if fieldvalue:
                    title = fieldvalue.title
                    associations_field = self.get_field_from_object('associations_associatedPersonInstitutions', object)

                    result = []
                    for line in associations_field:
                        names = line["names"]
                        if names:
                            name = names[0].title
                            url = self.get_url_by_uid(names[0].UID())
                            new_name = self.create_maker(name, url)
                            result.append(new_name)

                    final_result = "<p>".join(result)
                    if final_result != "":
                        object_schema[field_schema]['fields'].append({"title": self.context.translate(_(title)), "value": final_result})

            else:
                fieldvalue = self.get_field_from_schema(field, fields)
                if fieldvalue != None:
                    title = fieldvalue.title
                    value = self.get_field_from_object(field, object)

                    schema_value = self.transform_schema_field(field, value, choice)

                    if schema_value != "":
                        object_schema[field_schema]['fields'].append({"title": self.context.translate(_(title)), "value": schema_value})
    
    def generate_reproductions_tab(self, reproductions_tab, object_schema, fields, object, field_schema):
        for field, choice, restriction in reproductions_tab:
            fieldvalue = self.get_field_from_schema(field, fields)
            if fieldvalue != None:
                title = fieldvalue.title
                value = self.get_field_from_object(field, object)

                schema_value = self.transform_schema_field(field, value, choice)

                if schema_value != "":
                    if field == "reproductions_reproduction":
                        title = "Reference"
                    object_schema[field_schema]['fields'].append({"title": self.context.translate(_(title)), "value": schema_value})    

    def generate_recommendations_tab(self, recommendations_tab, object_schema, fields, object, field_schema):
        for field, choice, restriction in recommendations_tab:
            fieldvalue = self.get_field_from_schema(field, fields)
            if fieldvalue != None:
                title = fieldvalue.title
                value = self.get_field_from_object(field, object)

                schema_value = self.transform_schema_field(field, value, choice)

                if schema_value != "":
                    object_schema[field_schema]['fields'].append({"title": self.context.translate(_(title)), "value": schema_value})     

    def generate_location_tab(self, location_tab, object_schema, fields, object, field_schema):
        for field, choice, restriction in location_tab:
            fieldvalue = self.get_field_from_schema(field, fields)
            if fieldvalue != None:
                title = fieldvalue.title
                value = self.get_field_from_object(field, object)

                schema_value = self.transform_schema_field(field, value, choice)

                if schema_value != "":
                    object_schema[field_schema]['fields'].append({"title": self.context.translate(_(title)), "value": schema_value})


    def generate_fieldcollection_tab(self, fieldcollection_tab, object_schema, fields, object, field_schema):
        for field, choice, restriction in fieldcollection_tab:
            fieldvalue = self.get_field_from_schema(field, fields)
            if fieldvalue != None:
                title = fieldvalue.title
                value = self.get_field_from_object(field, object)

                schema_value = self.transform_schema_field(field, value, choice)

                if schema_value != "":
                    if field == 'fieldCollection_habitatStratigraphy_stratigraphy':
                        object_schema[field_schema]['fields'].append({"title": self.context.translate(_('Geologisch tijdvak')), "value": schema_value})
                    else:
                        object_schema[field_schema]['fields'].append({"title": self.context.translate(_(title)), "value": schema_value})


    def generate_exhibitions_tab_temp(self, exhibitions_tab, object_schema, fields, object, field_schema):
        for field, choice, restriction, not_show in exhibitions_tab:
            fieldvalue = self.get_field_from_schema(field, fields)
            if fieldvalue != None:
                title = fieldvalue.title
                value = self.get_field_from_object(field, object)

                schema_value = self.transform_schema_field(field, value, choice, restriction, not_show)

                if schema_value != "":
                    object_schema[field_schema]['fields'].append({"title": self.context.translate(_(title)), "value": schema_value})

    def generate_exhibition_tab(self, exhibitions_tab, object_schema, fields, object, field_schema):

        relations = []
        related_exhibitions = []

        def get_url_by_uid(context, uid):
            brain = uuidToCatalogBrain(uid)
            if brain:
                return brain.getURL()

            return ""

        for field, choice, restriction, not_show in exhibitions_tab:
            fieldvalue = self.get_field_from_schema(field, fields)
            if fieldvalue != None:
                title = fieldvalue.title
                value = self.get_field_from_object(field, object)
                if value:
                    for val in value:
                        exhibition = val['exhibitionName']
                        if exhibition:
                            rel = exhibition[0]
                            rel_obj = None
                            if IRelationValue.providedBy(rel):
                                rel_obj = rel.to_object
                            else:
                                rel_obj = rel

                            if rel_obj:
                                rel_url = get_url_by_uid(self.context, rel_obj.UID())
                                rel_title = rel_obj.title
                                related_exhibitions.append("<a href='%s'>%s</a>"%(rel_url, rel_title))

                                rel_date_start = ""
                                rel_date_end = ""
                                if hasattr(rel_obj, 'start_date'):
                                    rel_date_start = rel_obj.start_date

                                if hasattr(rel_obj, 'end_date'):
                                    rel_date_end = rel_obj.end_date

                                if rel_date_start != "":
                                    try:
                                        date_start = rel_date_start.strftime('%Y-%m-%d')
                                    except:
                                        rel_date_start = ""

                                if rel_date_end != "":
                                    try:
                                        date_end = rel_date_end.strftime('%Y-%m-%d')
                                    except:
                                        rel_date_end = ""


                                final_date = ""
                                if rel_date_start != "" and rel_date_end != "":
                                    final_date = "%s t/m %s" %(date_start, date_end)

                                if final_date != "":
                                    related_exhibitions.append(final_date)

                                # organisator
                                orgs = []
                                locations = []
                                places = []

        if len(related_exhibitions) > 0:
            related_exhibitions_value = '<p>'.join(related_exhibitions)
            object_schema[field_schema]['fields'].append({'title': self.context.translate(_('Exhibition name')), 'value': related_exhibitions_value})


    def generate_exhibitions_tab(self, exhibitions_tab, object_schema, fields, object, field_schema):
        relations = getattr(object, 'exhibitions_exhibition', None)

        if relations:
            related_exhibitions = []
            for rel in relations:
                rel_obj = None
                if IRelationValue.providedBy(rel):
                    rel_obj = rel.to_object
                else:
                    rel_obj = rel

                rel_url = rel_obj.absolute_url()
                rel_title = rel_obj.title
                related_exhibitions.append("<a href='%s'>%s</a>"%(rel_url, rel_title))

                rel_date_start = ""
                rel_date_end = ""
                if hasattr(rel_obj, 'start_date'):
                    rel_date_start = rel_obj.start_date

                if hasattr(rel_obj, 'end_date'):
                    rel_date_end = rel_obj.end_date

                if rel_date_start != "":
                    date_start = rel_date_start.strftime('%Y-%m-%d')

                if rel_date_end != "":
                    date_end = rel_date_start.strftime('%Y-%m-%d')

                final_date = ""
                if rel_date_start != "" and rel_date_end != "":
                    final_date = "%s t/m %s" %(date_start, date_end)

                if final_date != "":
                    related_exhibitions.append(final_date)

        if len(related_exhibitions) > 0:
            related_exhibitions_value = '<p>'.join(related_exhibitions)
            object_schema[field_schema]['fields'].append({'title': self.context.translate(_('Exhibitions')), 'value': related_exhibitions_value})

    def generate_labels_tab(self, labels_tab, object_schema, fields, object, field_schema):
        for field, choice, restriction in labels_tab:
            fieldvalue = self.get_field_from_schema(field, fields)
            if fieldvalue != None:
                title = fieldvalue.title
                value = self.get_field_from_object(field, object)

                schema_value = self.transform_schema_field(field, value, choice, restriction)

                if schema_value != "":
                    object_schema[field_schema]['fields'].append({"title": self.context.translate(_(title)), "value": schema_value})

    def generate_related_books_tab(self, object_schema, fields, object, field_schema):
        if checkPermission('cmf.ManagePortal', self.context):
            intids = getUtility(IIntIds)
            catalog = getUtility(ICatalog)

            relations = sorted(catalog.findRelations({'to_id': intids.getId(object), 'from_attribute':'relations_relatedMuseumObjects'}))
            related_exhibitions = []
            for rel in relations:
                rel_obj = rel.from_object
                rel_url = rel_obj.absolute_url()
                rel_title = rel_obj.title
                related_exhibitions.append("<a href='%s'>%s</a>"%(rel_url, rel_title))
            
            if len(related_exhibitions) > 0:
                related_exhibitions_value = '<p>'.join(related_exhibitions)
                object_schema[field_schema]['fields'].append({'title': self.context.translate(_('Books')), 'value': related_exhibitions_value})


    def generate_documentation_tab(self, object_schema, fields, object, field_schema):
        if hasattr(object, 'documentation_documentation'):
            documentation = object.documentation_documentation
            docs = []

            if documentation:
                for doc in documentation:
                    try:
                        if doc['title'] != "":
                            new_doc = "%s" %(doc['title'])

                            if doc['pageMark'] != "":
                                new_doc = "%s, %s" %(new_doc, doc['pageMark'])

                            if doc['notes'] != "":
                                new_doc = "%s, %s" %(new_doc, doc['notes'])

                            docs.append(new_doc)
                    except:
                        pass

            if len(docs) > 0:
                schema_value = '<p>'.join(docs)
                object_schema[field_schema]['fields'].append({'title': self.context.translate(_('Documentation')), 'value': schema_value})


    def get_all_fields_object(self, object):
        object_schema = {}

        object_schema["identification"] = {
            "fields": [],
            "name": self.context.translate(_("Identification"))
        }

        object_schema["production_dating"] = {
            "fields": [],
            "name": self.context.translate(_("Production & Dating"))
        }

        object_schema["physical_characteristics"] = {
            "fields": [],
            "name": self.context.translate(_("Physical Characteristics"))
        }

        object_schema["associations"] = {
            "fields": [],
            "name": self.context.translate(_("Associations"))
        }

        object_schema["reproductions"] = {
            "fields": [],
            "name": self.context.translate(_("Reproductions"))
        }

        object_schema["recommendations_requirements"] = {
            "fields": [],
            "name": self.context.translate(_("Recommendations/requirements"))
        }

        object_schema["location"] = {
            "fields": [],
            "name": self.context.translate(_("Location"))
        }

        object_schema["field_collection"] = {
            "fields": [],
            "name": self.context.translate(_("Field Collection"))
        }

        object_schema["exhibitions"] = {
            "fields": [],
            "name": self.context.translate(_("Exhibitions"))
        }

        object_schema["labels"] = {
            "fields": [],
            "name": self.context.translate(_("Labels"))
        }

        object_schema["books"] = {
            "fields": [],
            "name": self.context.translate(_("Books"))
        }

        object_schema["documentation"] = {
            "fields": [],
            "name": self.context.translate(_("Documentation"))
        }


        schema = getUtility(IDexterityFTI, name='Object').lookupSchema()
        fields = getFieldsInOrder(schema)

        identification_tab = [('identification_identification_collections', None), ('identification_identification_objectNumber', None),
                                ('identification_objectName_category', None), ('identification_objectName_objectname', 'name'),
                                ('title', None), ('identification_taxonomy', 'scientific_name'), ('text', None)]

        production_dating_tab = ['productionDating_production', 'productionDating_dating_period']

        physical_characteristics_tab = [('physicalCharacteristics_technique', 'technique', None), ('physicalCharacteristics_material', 'material', None),
                                        ('physicalCharacteristics_dimension', None, None)]

        associations_tab = [('associations_associatedPersonInstitutions', 'names', None), ('associations_associatedSubjects', 'subject', None)]

        reproductions_tab = [('reproductions_reproduction', 'reference', None)]

        recommendations_tab = [('recommendationsRequirements_creditLine_creditLine', None, None)]

        location_tab = [('location_current_location', 'location_type', None)]

        fieldcollection_tab = [('fieldCollection_fieldCollection_places', None, None), ('fieldCollection_habitatStratigraphy_stratigrafie', 'unit', None)]

        exhibitions_tab = [('exhibitions_exhibition', None, 'Zeeuws Museum', ['catObject'])]

        labels_tab = [('labels', 'text', None)]


        ## Identification tab
        try:
            self.generate_identification_tab(identification_tab, object_schema, fields, object, "identification")
        except:
            pass
            
        ## Vervaardiging & Datering tab
        #self.generate_production_dating_tab(production_dating_tab, object_schema, fields, object, "production_dating")
        try:
            self.generate_production_dating(production_dating_tab, object_schema, fields, object, "production_dating")
        except:
            pass
            
        ## Physical Characteristics
        try:
            self.generate_physical_characteristics_tab(physical_characteristics_tab, object_schema, fields, object, "physical_characteristics")
        except:
            pass

        ## Associations
        try:
            self.generate_associations_tab(associations_tab, object_schema, fields, object, "associations")
        except:
            pass
        ## Reproductions
        try:
            self.generate_reproductions_tab(reproductions_tab, object_schema, fields, object, "reproductions")
        except:
            pass
        ## Recommendations
        try:
            self.generate_recommendations_tab(recommendations_tab, object_schema, fields, object, "recommendations_requirements")
        except:
            pass
        ## Location
        try:
            self.generate_location_tab(location_tab, object_schema, fields, object, "location")
        except:
            pass
        ## Field collection
        try:
            self.generate_fieldcollection_tab(fieldcollection_tab, object_schema, fields, object, "field_collection")
        except:
            pass
        ## Exhibtions
        #self.generate_exhibitions_tab(exhibitions_tab, object_schema, fields, object, "exhibitions")
        try:
            self.generate_exhibition_tab(exhibitions_tab, object_schema, fields, object, "exhibitions")
        except:
            pass

        ## Labels
        try:
            self.generate_labels_tab(labels_tab, object_schema, fields, object, "labels")
        except:
            pass

        ## Books
        try:
            self.generate_related_books_tab(object_schema, fields, object, "books")
        except:
            pass

        ## Documentation
        try:
            self.generate_documentation_tab(object_schema, fields, object, "documentation")
        except:
            pass

        new_object_schema = []
        new_object_schema.append(object_schema['identification'])
        new_object_schema.append(object_schema['production_dating'])
        new_object_schema.append(object_schema['physical_characteristics'])
        new_object_schema.append(object_schema['associations'])
        new_object_schema.append(object_schema['reproductions'])
        new_object_schema.append(object_schema['recommendations_requirements'])
        new_object_schema.append(object_schema['location'])
        new_object_schema.append(object_schema['field_collection'])
        new_object_schema.append(object_schema['exhibitions'])
        new_object_schema.append(object_schema['labels'])
        new_object_schema.append(object_schema['books'])
        new_object_schema.append(object_schema['documentation'])

        return new_object_schema

    def getJSON(self):
        schema = []
        if self.context.portal_type == "Object":
            obj = self.context
            schema = self.get_all_fields_object(obj)
        else:
            schema = []

        return json.dumps({'schema':schema})


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

        #brain = uuidToCatalogBrain(item_uid)
        #if brain:
        #    leadmedia_uid = brain.leadMedia
        #    if leadmedia_uid:
        #        lead_media = uuidToCatalogBrain(leadmedia_uid)
        #        details['image'] = lead_media.getURL() + "/@@images/image/large"

        return details

