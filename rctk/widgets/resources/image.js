Onion.widget.Image = function(jwin, parent, controlid) {
    Onion.widget.Control.apply(this, arguments);
}

Onion.widget.Image.prototype = new Onion.widget.Control();

Onion.widget.Image.prototype.create = function(data) {
    var controlid = "ctrl"+this.controlid;
    this.jwin.factory.append('<img id="' + controlid + '" />');
    this.control = $("#"+controlid);
    if('resource' in data && data.resource) {
        this.control.attr('src', 'resources/' + data.resource);
    }
    if('url' in data && data.url) {
        this.control.attr('src', data.url);
    }
    this.control.attr('title', data.title);
    this.control.attr('alt', data.resource);
    this.set_properties(data);
}

Onion.widget.Image.prototype.set_properties = function(data) {
    Onion.widget.Control.prototype.set_properties.apply(this, arguments);
    if ('title' in data) {
        this.control.attr('title', data.title);
    }
    if ('resource' in data && data.resource) {
        this.control.attr('src', 'resources/' + data.resource);
    }
    if ('url' in data && data.url) {
        this.control.attr('src', data.url);
    }
}

// register
Onion.widget.register("image", Onion.widget.Image);
