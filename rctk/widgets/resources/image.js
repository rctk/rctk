Onion.widget.Image = function(jwin, parent, controlid) {
    Onion.widget.Control.apply(this, arguments);
}

Onion.widget.Button.prototype = new Onion.widget.Control();

Onion.widget.Button.prototype.create = function(data) {
    var controlid = "ctrl"+this.controlid;
    this.jwin.factory.append('<img id="' + controlid + '" />');
    this.control = $("#"+controlid);
    this.control.attr('src', data.src);
    this.control.attr('title', data.title);
    this.set_properties(data);
}

Onion.widget.Button.prototype.update = function(data) {
    Onion.widget.Control.prototype.update.apply(this, arguments);
    if(data.title) {
        this.control.attr('title', data.title);
    }
    this.set_properties(data);
}

// register
Onion.widget.register("image", Onion.widget.Button);
