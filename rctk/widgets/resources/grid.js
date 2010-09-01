Onion.widget.Grid = function(jwin, parent, controlid) {
    Onion.widget.Control.apply(this, arguments);
    this.items = [];
    this.name = "grid";
}

Onion.widget.Grid.prototype = new Onion.widget.Control();

Onion.widget.Grid.prototype.create = function(data) {
    var controlid = "ctrl"+this.controlid;
    this.jwin.factory.append('<table id="' + controlid + '">' + "</table>");
    this.container = $("#"+controlid);
    this.container.addClass(this.cssclass);
    this.container.addClass(this.name);
    // this.set_properties(data);
    this.container.jqGrid({
        datatype: 'local',
        colNames:data.colNames,
        colModel :data.colModel,
        // rowNum:10,
        //rowList:[10,20,30],
        //sortname: 'invid',
        //sortorder: 'desc',
        viewrecords: false,
        caption: '',
        loadui: 'disabled',
        scroll: false // see remark below
    }); 
    // setting scroll to 1 will allow dynamic loading of batches of
    // rows. I.e. "static" vs "virtual". 
    // However, this currently has odd side effects on firefox, perhaps
    // we need some handler to feed / restore data. Actual deletion takes
    // place in grid.base.js, line 300 (populateVisible)
    this.control = $("#gbox_"+controlid);

}

Onion.widget.Grid.prototype.update = function(data) {
    Onion.widget.Control.prototype.update.apply(this, arguments);
    if(data && 'addrow' in data) {
        this.container.addRowData(data.addrow.id, data.addrow.data, data.addrow.position);
    }
    if('clear' in data && data.clear) {
        this.container.clearGridData(true); 
    }
}

// register
Onion.widget.register("grid", Onion.widget.Grid);
