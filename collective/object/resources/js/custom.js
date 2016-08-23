
/* * * * * * * * * * * */
/* Object specific JS  */
/* * * * * * * * * * * */

jQuery(function($){"use strict";var dataGridField2Functions={};dataGridField2Functions.getInputOrSelect=function(node){var inputs=node.getElementsByTagName("input");if(inputs.length>0)return inputs[0];var selects=node.getElementsByTagName("select");if(selects.length>0)return selects[0];return null;};dataGridField2Functions.getWidgetRows=function(currnode){var tbody=this.getParentByClass(currnode,"datagridwidget-body");return this.getRows(tbody);};dataGridField2Functions.getRows=function(tbody){var rows=$(tbody).children('.datagridwidget-row');return rows;};dataGridField2Functions.getVisibleRows=function(tbody){var rows=this.getRows(tbody);var filteredRows=$(rows).filter(function(){var $tr=$(this);return !$tr.hasClass("datagridwidget-empty-row");});return filteredRows;};dataGridField2Functions.onInsert=function(e){var currnode=e.currentTarget;this.autoInsertRow(currnode);},dataGridField2Functions.autoInsertRow=function(currnode,ensureMinimumRows){var dgf=$(dataGridField2Functions.getParentByClass(currnode,"datagridwidget-table-view"));var tbody=dataGridField2Functions.getParentByClass(currnode,"datagridwidget-body");var thisRow=dataGridField2Functions.getParentRow(currnode);var $thisRow=$(thisRow);var autoAppendMode=$(tbody).data("auto-append");if($thisRow.hasClass("minimum-row")){this.supressEnsureMinimum(tbody);return;}var autoAppendHandlers=dgf.find('.auto-append .datagridwidget-cell, .auto-append .datagridwidget-block-edit-cell');autoAppendHandlers.unbind('change.dgf');$thisRow.removeClass('auto-append');var newtr=dataGridField2Functions.createNewRow(thisRow),$newtr=$(newtr);$newtr.addClass('auto-append');dgf.trigger("beforeaddrowauto",[dgf,newtr]);if(ensureMinimumRows){$newtr.addClass("minimum-row");$newtr.insertBefore(thisRow);}else $newtr.insertAfter(thisRow);$(dgf).find('.auto-append .datagridwidget-cell, .auto-append .datagridwidget-block-edit-cell').bind("change.dgf",$.proxy(dataGridField2Functions.onInsert,dataGridField2Functions));dataGridField2Functions.reindexRow(tbody,newtr,'AA');dataGridField2Functions.updateOrderIndex(tbody,true,ensureMinimumRows);dgf.trigger("afteraddrowauto",[dgf,newtr]);};dataGridField2Functions.addRowAfter=function(currnode){var tbody=this.getParentByClass(currnode,"datagridwidget-body");var dgf=$(dataGridField2Functions.getParentByClass(currnode,"datagridwidget-table-view"));var thisRow=this.getParentRow(currnode);var newtr=this.createNewRow(thisRow);dgf.trigger("beforeaddrow",[dgf,newtr]);var filteredRows=this.getVisibleRows(currnode);if(thisRow.hasClass('auto-append')&&!thisRow.hasClass("minimum-row"))$(newtr).insertBefore(thisRow);else $(newtr).insertAfter(thisRow);if(thisRow.hasClass("minimum-row"))this.supressEnsureMinimum(tbody);this.updateOrderIndex(tbody,true);dgf.trigger("afteraddrow",[dgf,newtr]);};dataGridField2Functions.createNewRow=function(node){var tbody=this.getParentByClass(node,"datagridwidget-body");var emptyRow=$(tbody).children('.datagridwidget-empty-row').first();if(emptyRow.size()===0)throw new Error("Could not locate empty template row in DGF");var new_row=emptyRow.clone(true).removeClass('datagridwidget-empty-row');$(new_row.find('.select2-container')).each(function() {var data = $(this).data('select2');if (data != undefined) {var element = data.opts.element.clone(false);data.opts.element = element;$(this).attr("id", "");$(this).select2(data.opts);}});return new_row;};dataGridField2Functions.removeFieldRow=function(node){var tbody=this.getParentByClass(node,"datagridwidget-body");var row=this.getParentRow(node);$(row).remove();if($(tbody).data("auto-append")||!this.ensureMinimumRows(tbody))this.updateOrderIndex(tbody,false);};dataGridField2Functions.moveRow=function(currnode,direction){var nextRow;var dgf=$(dataGridField2Functions.getParentByClass(currnode,"datagridwidget-table-view"));var tbody=this.getParentByClass(currnode,"datagridwidget-body");var rows=this.getWidgetRows(currnode);var row=this.getParentRow(currnode);if(!row)throw new Error("Couldn't find DataGridWidget row");var idx=null;rows.each(function(i){if(this==row[0])idx=i;});if(idx==null)return;var validrows=0;rows.each(function(i){if(!$(this).hasClass('datagridwidget-empty-row')&&!$(this).hasClass('auto-append'))validrows+=1;});if(idx+1==validrows)if(direction=="down")this.moveRowToTop(row);else{nextRow=rows[idx-1];this.shiftRow(nextRow,row);}else if(idx===0)if(direction=="up")this.moveRowToBottom(row);else{nextRow=rows[parseInt(idx+1,10)];this.shiftRow(row,nextRow);}else if(direction=="up"){nextRow=rows[idx-1];this.shiftRow(nextRow,row);}else{nextRow=rows[parseInt(idx+1,10)];this.shiftRow(row,nextRow);}this.updateOrderIndex(tbody);dgf.trigger("aftermoverow",[dgf,row]);};dataGridField2Functions.moveRowDown=function(currnode){this.moveRow(currnode,"down");};dataGridField2Functions.moveRowUp=function(currnode){this.moveRow(currnode,"up");};dataGridField2Functions.shiftRow=function(bottom,top){$(top).insertBefore(bottom);};dataGridField2Functions.moveRowToTop=function(row){var rows=this.getWidgetRows(row);$(row).insertBefore(rows[0]);};dataGridField2Functions.moveRowToBottom=function(row){var rows=this.getWidgetRows(row);var insert_after=0;rows.each(function(i){if(!$(this).hasClass('datagridwidget-empty-row')&&!$(this).hasClass('auto-append'))insert_after=i;});$(row).insertAfter(rows[insert_after]);};dataGridField2Functions.reindexRow=function(tbody,row,newindex){var name_prefix=$(tbody).data('name_prefix')+'.';var id_prefix=$(tbody).data('id_prefix')+'-';var $row=$(row);var oldindex=$row.data('index');function replaceIndex(el,attr,prefix){if(el.attr(attr)){var val=el.attr(attr);var pattern=new RegExp('^'+prefix+oldindex);el.attr(attr,val.replace(pattern,prefix+newindex));if(attr.indexOf('data-')===0){var key=attr.substr(5);var data=el.data(key);el.data(key,data.replace(pattern,prefix+newindex));}}}$row.data('index',newindex);$row.attr('data-index',newindex);$row.find('[id^="formfield-'+id_prefix+'"]').each(function(i,el){replaceIndex($(el),'id','formfield-'+id_prefix);});$row.find('[name^="'+name_prefix+'"]').each(function(i,el){replaceIndex($(el),'name',name_prefix);});$row.find('[id^="'+id_prefix+'"]').each(function(i,el){replaceIndex($(el),'id',id_prefix);});$row.find('[for^="'+id_prefix+'"]').each(function(i,el){replaceIndex($(el),'for',id_prefix);});$row.find('[href*="#'+id_prefix+'"]').each(function(i,el){replaceIndex($(el),'href','#'+id_prefix);});$row.find('[data-fieldname^="'+name_prefix+'"]').each(function(i,el){replaceIndex($(el),'data-fieldname',name_prefix);});};dataGridField2Functions.supressEnsureMinimum=function(tbody){var autoAppendHandlers=$(tbody).find('.auto-append .datagridwidget-cell, .auto-append .datagridwidget-block-edit-cell');autoAppendHandlers.unbind('change.dgf');tbody.children().removeClass("auto-append");tbody.children().removeClass("minimum-row");dataGridField2Functions.updateOrderIndex(tbody,true,false);};dataGridField2Functions.updateOrderIndex=function(tbody,backwards,ensureMinimumRows){var $tbody=$(tbody);var name_prefix=$tbody.attr('data-name_prefix')+'.';var i,idx,row,$row,$nextRow;var autoAppend=false;var rows=this.getRows(tbody);for(i=0;i<rows.length;i++){idx=backwards?rows.length-i-1:i;row=rows[idx],$row=$(row);if($row.hasClass('datagridwidget-empty-row'))continue;if($row.hasClass('auto-append'))autoAppend=true;this.reindexRow(tbody,row,idx);}if(ensureMinimumRows){this.reindexRow(tbody,rows[0],"AA");autoAppend=true;}var visibleRows=this.getVisibleRows(tbody);for(i=0;i<visibleRows.length;i++){row=visibleRows[i],$row=$(row);if(i<visibleRows.length-2)$nextRow=$(visibleRows[i+1]);if(i===0)$row.addClass("datagridfield-first-filled-row");else $row.removeClass("datagridfield-first-filled-row");if(autoAppend)if($nextRow&&$nextRow.hasClass("auto-append"))$row.addClass("datagridfield-last-filled-row");else $row.removeClass("datagridfield-last-filled-row");else if(i==visibleRows.length-1)$row.addClass("datagridfield-last-filled-row");else $row.removeClass("datagridfield-last-filled-row");}var vis=this.getVisibleRows(tbody).length;$tbody.attr("data-count",this.getRows(tbody).length);$tbody.attr("data-visible-count",this.getVisibleRows(tbody).length);$tbody.attr("data-many-rows",vis>=2?"true":"false");$(document).find('input[name="'+name_prefix+'count"]').each(function(){var count=rows.length;if($(rows[count-1]).hasClass('datagridwidget-empty-row'))count--;if($(rows[count-1]).hasClass('auto-append'))count--;this.value=count;});};dataGridField2Functions.getParentElement=function(currnode,tagname){tagname=tagname.toUpperCase();var parent=currnode.parentNode;while(parent.tagName.toUpperCase()!=tagname){parent=parent.parentNode;if(parent.tagName.toUpperCase()=="BODY")return null;}return parent;};dataGridField2Functions.getParentRow=function(node){return this.getParentByClass(node,'datagridwidget-row');};dataGridField2Functions.getParentByClass=function(node,klass){var parent=$(node).closest("."+klass);if(parent.length)return parent;return null;};dataGridField2Functions.getParentElementById=function(currnode,id){id=id.toLowerCase();var parent=currnode.parentNode;while(true){var parentId=parent.getAttribute("id");if(parentId)if(parentId.toLowerCase().substring(0,id.length)==id)break;parent=parent.parentNode;if(parent.tagName.toUpperCase()=="BODY")return null;}return parent;};dataGridField2Functions.ensureMinimumRows=function(tbody){var rows=this.getRows(tbody);var filteredRows=this.getVisibleRows(tbody);var self=this;if(filteredRows.length===0){var child=rows[0];this.autoInsertRow(child,true);return true;}return false;},dataGridField2Functions.init=function(){$(".datagridwidget-body").each(function(){var $this=$(this);var aa;aa=$this.children(".auto-append").size()>0;$this.data("auto-append",aa);if(aa)$this.addClass("datagridwidget-body-auto-append");else $this.addClass("datagridwidget-body-non-auto-append");dataGridField2Functions.updateOrderIndex(this,false);if(!aa)dataGridField2Functions.ensureMinimumRows(this);});$('.auto-append .datagridwidget-cell, .auto-append .datagridwidget-block-edit-cell').bind("change.dgf",$.proxy(dataGridField2Functions.onInsert,dataGridField2Functions));$(document).trigger("afterdatagridfieldinit");};$(document).ready(dataGridField2Functions.init);window.dataGridField2Functions=dataGridField2Functions;});

var fix_textareas_height = function(elem) {
	var $ = jQuery;
    var textareas = $(elem+" textarea");
    textareas.each(function() {
        if (!$(this).hasClass("mce_editable")) {
            $(this).attr("style", "height:1px;");
            var height = $(this)[0].scrollHeight;

            if (height != 0) {
                if (height == 35) {
                    height = 34;
                }
                
                if (height != 34) {
                    height = height + 3;
                    $(this).attr("style", "height: "+height+"px;");
                } else {
                    $(this).attr("style", "height: "+height+"px;");
                }
            } else {
                $(this).attr("style", "height:34px;");
            }
        }
    });
}

var click_on_generated_link = function(obj) {
    var href = obj.attr("href");
    window.location.href = window.location.protocol + "//" + window.location.host + href;
}

function render_object_fields(schema) {
	var $ = jQuery;

	var html = "";
	var body = "";

	for (var i = 0; i < schema.length; i++) {
		if (schema[i].fields.length > 0) {
			html += "<h3 class='fieldset-header'>"+schema[i].name+"</h3>";
			for (var j = 0; j < schema[i].fields.length; j++) {
				if (schema[i].fields[j].title != "body") {
					html += "<div class='col-lg-5 col-md-5 col-sm-5 col-xs-12 object-label' style='padding-left:0px;'><span>"+schema[i].fields[j].title+"</span></div><div class='col-lg-7 col-md-7 col-sm-7 col-xs-12 object-value'><p>"+schema[i].fields[j].value+"</p></div>";
				} else {
					body = schema[i].fields[j].value;
				}
			}
		}
	}

	var no_lt = html.replace(/&lt;/g, "<");
	var res = no_lt.replace(/&gt;/g, ">");

	var jsBody = $($.parseHTML(body));
	var htmlBody = $.parseHTML(jsBody.text());
	
	$("#body-text").html('');
	$("#body-text").html(htmlBody);
	$(".object-fieldset").html(res);
};

var is_portaltype_allowed = function() {
	var $ = jQuery;
    if ($("body").hasClass("portaltype-object") || $("body").hasClass("portaltype-book") || $("body").hasClass("portaltype-image") || $("body").hasClass('portaltype-personorinstitution') || $("body").hasClass('portaltype-exhibition') || $("body").hasClass('portaltype-audiovisual') || $("body").hasClass('portaltype-treatment') || $("body").hasClass('portaltype-outgoingloan') || $("body").hasClass("portaltype-incomingloan") || $("body").hasClass("portaltype-objectentry") || $("body").hasClass("portaltype-resource") || $("body").hasClass("portaltype-taxonomie") || $("body").hasClass("portaltype-serial") || $("body").hasClass("portaltype-article")) {
        return true;
    }
    return false;
};

jQuery(document).ready(function() {
	var $ = jQuery;
	var INPUTS_QUERY = "div.template-edit input, div.template-edit select:not(.formTabs), div.template-edit textarea, div.template-edit button"

	/* Get object public fields */
	if (is_portaltype_allowed() && !$("body").hasClass("userrole-authenticated")) {
		var request_url = "get_object_fields";
		var data_url = document.location.href;

		if (document.location.search != "") {
			temp_url = data_url;
			data_url = temp_url.replace(document.location.search, '');
		}

		URL = data_url + "/" + request_url;

		$.getJSON(URL, function(data) {
			if (data) {
				if (data.schema != undefined) {
					render_object_fields(data.schema);
				}
			}
		});
	} else if (is_portaltype_allowed() && !$("body").hasClass("template-edit")) {
		$(INPUTS_QUERY).prop("disabled", true);
		$("body").addClass("fields-loaded");
		fix_textareas_height("#form");
	} else if (is_portaltype_allowed() && $("body").hasClass("template-edit")) {
		$("body").addClass("fields-loaded");
		fix_textareas_height("#form");
	}

	setTimeout(function() {
		jQuery("a.relateditems-link, a.ajaxselect-link").click(function() {
			click_on_generated_link(jQuery(this));
		});

		/*if ($("div.template-edit").length > 0) {
			jQuery(".pat-select2 .select2-search-choice div").each(function() {
				var text = $(this).html();
				var searchLink = "/search?SearchableText=" + text;
				var link = "<a href='"+searchLink+"'>"+text+"</a>";
				$(this).html(link);
				var $new_url = $($(this).find('a')[0]);
				
				$new_url.click(function() {
					click_on_generated_link($new_url);
				});
			});
		}*/

	}, 2000);
});



