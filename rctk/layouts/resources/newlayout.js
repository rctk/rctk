Onion.layout.NewLayout = function(jwin, parent, config) {
    Onion.layout.Layout.apply(this, arguments);
    config = config?config:{};
    // don't care right now, wait for the calculated data when
    // layout() is called
}

Onion.layout.NewLayout.prototype = new Onion.layout.Layout();

Onion.layout.NewLayout.prototype.create = function() {
    if(this.created) {
        return;
    }
    this.parent.container.append("<div id='layoutmgr" + this.parent.controlid + "'></div>");
    this.layoutcontrol = $("#layoutmgr" + this.parent.controlid);
    this.layoutcontrol.css("position", "relative");
    this.created = true;
}

// move basic append, remove to base

Onion.layout.NewLayout.prototype.append = function(control, data) {
    this.create();
    control.control.appendTo(this.layoutcontrol);
}

Onion.layout.NewLayout.prototype.remove = function(control, data) {
    control.control.appendTo($("#factory"));
}


Onion.layout.NewLayout.prototype.layout = function(config) {
    // the relayout may be explicit (from pythoncode) or an implicit
    // cascade from a parent. In the latter case, we won't receive new
    // configuration data, so use the existing data
    if(config !== undefined) {
        Onion.util.log("relayout setting config", config);
        this.config = config;
    }
    else {
        Onion.util.log("relayout cascade");
    }

    Onion.util.log("New layout", this.config);
    // iterate over all controls, get their size (possibly cached
    // if resized for padding). Get the largest component, relayout
}

Onion.layout.NewLayout.prototype.layout_fase2 = function() {
    Onion.util.log("New layout 2");
}

Onion.layout.register('new', Onion.layout.NewLayout);

