Onion.widget.Grid = function(jwin, parent, controlid) {
    Onion.widget.Control.apply(this, arguments);
    this.items = [];
}

Onion.widget.Grid.prototype = new Onion.widget.Control();

Onion.widget.Grid.prototype.create = function(data) {
    var controlid = "ctrl"+this.controlid;
    this.jwin.factory.append('<table id="' + controlid + '">' + "</table>");
    this.container = $("#"+controlid);
    this.container.addClass(this.cssclass);
    // this.set_properties(data);
    this.container.jqGrid({
    datatype: 'clientSide',
    colNames:data.colNames,
    colModel :data.colModel,
    rowNum:10,
    rowList:[10,20,30],
    sortname: 'invid',
    sortorder: 'desc',
    viewrecords: true,
    caption: '',
    loadui: 'disabled',
    scroll: true
    }); 
    this.control = $("#gbox_"+controlid);

}

// register
Onion.widget.register("grid", Onion.widget.Grid);
