Onion.widget.Dropdown = function(jwin, parent, controlid) {
    Onion.widget.Control.apply(this, arguments);
    this.items = [];
}

Onion.widget.Dropdown.prototype = new Onion.widget.Control();

Onion.widget.Dropdown.prototype.create = function(data) {
    var controlid = "ctrl"+this.controlid;
    this.jwin.factory.append('<select id="' + controlid + '">' + "</select>");
    this.control = $("#"+controlid);
    this.control.addClass(this.cssclass);
    this.handle_click = false;

    if(data.items) {
        for(var i = 0; i < data.items.length; i++) {
            this.append_item(data.items[i][0], data.items[i][1]);
        }
    }
    var self=this;
    this.control.change(function() { self.changed(); self.jwin.flush(); });
    this.set_properties(data);
}

Onion.widget.Dropdown.prototype.append_item = function(key, label) {
    this.control.append('<option value="' + key + '">' + label + "</option>");
    this.items.push({'key':key, 'label':label});
}

Onion.widget.Dropdown.prototype.changed = function() {
    this.jwin.add_task("sync", "sync", this.controlid, {'selection':this.control.val()});
    if(this.handle_click) {
        // find current selection.
        this.jwin.add_task("event", "click", this.controlid);
    }
}

Onion.widget.Dropdown.prototype.update = function(data) {
    Onion.widget.Control.prototype.update.apply(this, arguments);
    if(data.item) {
        this.append_item(data.item[0], data.item[1]);
    }
    if('selection' in data) {
        this.control.val(data.selection);
    }
    if('clear' in data && data.clear) {
        this.control.empty(); // doesn't work on google chrome?
        this.items = []
    }
}

// register
Onion.widget.register("dropdown", Onion.widget.Dropdown);
