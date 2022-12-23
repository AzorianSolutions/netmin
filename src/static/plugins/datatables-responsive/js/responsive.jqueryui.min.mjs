/*! jQuery UI integration for DataTables' Responsive
 * © SpryMedia Ltd - datatables.net/license
 */
import $ from"jquery";import DataTable from"datatables.net-ju";import"datatables.net-responsive";var _display=DataTable.Responsive.display,_original=_display.modal;_display.modal=function(t){return function(a,e,i){$.fn.dialog?e||$("<div/>").append(i()).appendTo("body").dialog($.extend(!0,{title:t&&t.header?t.header(a):"",width:500},t.dialog)):_original(a,e,i)}};export default DataTable;