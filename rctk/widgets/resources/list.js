/*
 * TODO:
 *
 * Support insertion at any position
 * Support deletion
 */
Onion.widget.List = function(jwin, parent, controlid) {
    Onion.widget.Dropdown.apply(this, arguments);
    this.size = 5; // default
    this.name = "list";
}

Onion.widget.List.prototype = new Onion.widget.Dropdown();

Onion.widget.List.prototype.create = function(data) {
    Onion.widget.Dropdown.prototype.create.apply(this, arguments);
    if(data.size) {
        this.size = Math.max(2, data.size);
    }
    this.setsize();
}

Onion.widget.List.prototype.append_item = function(key, label) {
    Onion.widget.Dropdown.prototype.append_item.apply(this, arguments);
    this.setsize();
}

Onion.widget.List.prototype.setsize = function() {
    this.control.attr('size', this.size);
}

Onion.widget.List.prototype.set_properties = function(data) {
    Onion.widget.Dropdown.prototype.set_properties.apply(this, arguments);

    if(data.size) {
        this.size = Math.max(2, data.size);
        this.setsize();
    }
}

// register
Onion.widget.register("list", Onion.widget.List);
