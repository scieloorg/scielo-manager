/*
 * Alternate Select Multiple (asmSelect) 1.0.1 beta - jQuery Plugin
 * http://www.ryancramer.com/projects/asmselect/
 * 
 * Copyright (c) 2008 by Ryan Cramer - http://www.ryancramer.com
 * 
 * Licensed under the GPL (gpl-2.0.txt) license.
 *
 */

(function($) {

	$.fn.asmSelect = function(customOptions) {

		var options = {

			listType: 'ol',						// Ordered list 'ol', or unordered list 'ul'
			sortable: false, 					// Should the list be sortable?
			highlight: true,					// Use the highlight feature? 
			animate: true,						// Animate the the adding/removing of items in the list?
			hideWhenAdded: true,					// Stop showing in select after after item has been added?
			addItemTarget: 'bottom',				// Where to place new selected items in list: top or bottom
			debugMode: false,					// Debug mode keeps original select visible 

			removeLabel: 'remove',					// Text used in the "remove" link
			highlightAddedLabel: 'Added: ',				// Text that precedes highlight of added item
			highlightRemovedLabel: 'Removed: ',			// Text that precedes highlight of removed item

			containerClass: 'asmContainer',				// Class for container that wraps this widget
			selectClass: 'asmSelect',				// Class for the newly created <select>
			listClass: 'asmList',					// Class for the list ($ol)
			listSortableClass: 'asmListSortable',			// Another class given to the list when it is sortable
			listItemClass: 'asmListItem',				// Class for the <li> list items
			listItemLabelClass: 'asmListItemLabel',			// Class for the label text that appears in list items
			removeClass: 'asmListItemRemove',			// Class given to the "remove" link
			highlightClass: 'asmHighlight'				// Class given to the highlight <span>

			};

		$.extend(options, customOptions); 

		return this.each(function(index) {

			var $original = $(this); 				// the original select multiple
			var $container; 					// a container that is wrapped around our widget
			var $select; 						// the new select we've created
			var $ol; 						// the list that we are manipulating
			var buildingSelect = false; 				// is the new select being constructed right now?

			function init() {

				// initialize the alternate select multiple

				$select = $("<select></select>")
					.addClass(options.selectClass)
					.attr('id', options.selectClass + index); 

				$ol = $("<" + options.listType + "></" + options.listType + ">")
					.addClass(options.listClass)
					.attr('id', options.listClass + index); 

				$container = $("<div></div>")
					.addClass(options.containerClass) 
					.attr('id', options.containerClass + index); 

				buildSelect();

				$select.change(function() {
					var id = $(this).children("option:selected").slice(0,1).attr('rel'); 
					addListItem(id); 	
				}); 

				$original.change(originalChangeEvent)
					.wrap($container).before($select).before($ol);

				if(options.sortable) makeSortable();
				if($.browser.msie) $ol.css('display', 'inline-block'); 
				if(!options.debugMode) $original.hide();
			}

			function makeSortable() {

				// make any items in the selected list sortable
				// requires jQuery UI sortables, draggables, droppables

				$ol.sortable({
					items: 'li.' + options.listItemClass,
					handle: '.' + options.listItemLabelClass,
					axis: 'y',
					update: function() {
						$(this).children("li").each(function(n) {
							if($(this).is(".ui-sortable-helper")) return;
							$option = $('#' + $(this).attr('rel')); 
							$original.append($option); 
						}); 
					}
				}).addClass(options.listSortableClass); 
			}

			function originalChangeEvent(e) {

				// select or option change event manually triggered
				// on the original <select multiple>, so rebuild ours

				$select.empty();
				$ol.empty();
				buildSelect();
			}

			function buildSelect() {

				// build or rebuild the new select that the user
				// will select items from

				buildingSelect = true; 

				// add a first option to be the home option / default selectLabel
				$select.prepend("<option>" + $original.attr('title') + "</option>"); 

				$original.children("option").each(function(n) {

					var $t = $(this); 
					var id; 


					if(!$t.attr('id')) $t.attr('id', 'asm' + index + 'option' + n); 
					id = $t.attr('id'); 

					if($t.is(":selected")) {
						addListItem(id); 
						addSelectOption(id, options.hideWhenAdded); 						
					} else {
						addSelectOption(id); 
					}
				});

				$selectLabel = $select.children().slice(0,1);
				buildingSelect = false; 
			}

			function addSelectOption(optionId, hide) {

				// add an <option> to the <select>
				// used only by buildSelect()

				if(hide == undefined) var hide = false; 

				var $O = $('#' + optionId); 
				var $option = $("<option>" + $O.text() + "</option>")
					.val($O.val())
					.attr('rel', optionId);

				if(hide) $option.hide().attr('disabled', true); 

				$select.append($option); 
			}

			function addListItem(optionId) {

				// add a new item to the html list

				var $O = $('#' + optionId); 

				if(!$O) return; // this is the first item, selectLabel

				var $removeLink = $("<a></a>")
					.attr("href", "#")
					.addClass(options.removeClass)
					.prepend(options.removeLabel)
					.click(function() { 
						dropListItem($(this).parent('li').attr('rel')); 
						return false; 
					}); 

				var $itemLabel = $("<span></span>")
					.addClass(options.listItemLabelClass)
					.html($O.html()); 

				var $item = $("<li></li>")
					.attr('rel', optionId)
					.addClass(options.listItemClass)
					.append($itemLabel)
					.append($removeLink)
					.hide();

				if(!buildingSelect) {
					if($O.is(":selected")) return; // already have it
					$O.attr('selected', true); 
				}

				if(options.addItemTarget == 'top' && !buildingSelect) {
					$ol.prepend($item); 
					if(options.sortable) $original.prepend($O); 
				} else {
					$ol.append($item); 
					if(options.sortable) $original.append($O); 
				}

				addListItemShow($item); 

				if(options.hideWhenAdded) {
					$select.find("[rel=" + optionId + "]").attr("disabled", true).hide();
					$select.children().slice(0,1).attr("selected", true); 
				}

				if(!buildingSelect) {
					setHighlight($item, options.highlightAddedLabel); 
					if(options.sortable) $ol.sortable("refresh"); 	
				}

			}

			function addListItemShow($item) {

				// reveal the currently hidden item with optional animation
				// used only by addListItem()

				if(options.animate && !buildingSelect) {
					$item.animate({
						opacity: "show",
						height: "show"
					}, 100, "swing", function() { 
						$item.animate({
							height: "+=2px"
						}, 50, "swing", function() {
							$item.animate({
								height: "-=2px"
							}, 25, "swing"); 
						}); 
					}); 
				} else {
					$item.show();
				}
			}

			function dropListItem(optionId, highlightItem) {

				// remove an item from the html list

				if(highlightItem == undefined) var highlightItem = true; 
				var $O = $('#' + optionId); 

				$O.attr('selected', false); 
				$item = $ol.children("li[rel=" + optionId + "]");

				dropListItemHide($item); 

				if(options.hideWhenAdded) $select.find("[rel=" + optionId + "]").show().attr("disabled", false);
				if(highlightItem) setHighlight($item, options.highlightRemovedLabel); 
				
			}

			function dropListItemHide($item) {

				// remove the currently visible item with optional animation
				// used only by dropListItem()

				$prevItem = $item.prev("li");

				if(options.animate && !buildingSelect) {

					$item.animate({
						opacity: "hide",
						height: "hide"
					}, 100, "linear", function() {
						$prevItem.animate({
							height: "-=2px"
						}, 50, "swing", function() {
							$prevItem.animate({
								height: "+=2px"
							}, 100, "swing"); 
						}); 
						$item.remove(); 
					}); 
					
				} else {
					$item.remove(); 
				}

				
			}

			function setHighlight($item, label) {

				// set the contents of the highlight area that appears
				// directly after the <select> single
				// fade it in quickly, then fade it out

				if(!options.highlight) return; 

				$select.next("#" + options.highlightClass + index).remove();

				var $highlight = $("<span></span>")
					.hide()
					.addClass(options.highlightClass)
					.attr('id', options.highlightClass + index)
					.html(label + $item.children("." + options.listItemLabelClass).slice(0,1).text()); 
					
				$select.after($highlight); 

				$highlight.fadeIn("fast", function() {
					setTimeout(function() { $highlight.fadeOut("slow"); }, 50); 
				}); 
			}

			init();
		});
	};

})(jQuery); 
