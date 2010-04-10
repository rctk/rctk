Onion.widget.Button = function(jwin, parent, controlid) {
    Onion.widget.Control.apply(this, arguments);
    this.ui = null;
}

Onion.widget.Button.prototype = new Onion.widget.Control();

Onion.widget.Button.prototype.create = function(data) {
    var controlid = "ctrl"+this.controlid;
    this.ui = new Onion.ui.Button(this.jwin.factory);
    this.ui.create(controlid, data.text);

    this.control = $("#"+controlid);
    this.control.addClass(this.cssclass);
    this.handle_click = false;

    var self=this;
    this.ui.click(function() { self.clicked(); self.jwin.flush(); });
    this.set_properties(data);
}

Onion.widget.Button.prototype.clicked = function() {
    if(this.handle_click) {
        this.jwin.add_task("event", "click", this.controlid);
    }
}

Onion.widget.Button.prototype.update = function(data) {
    Onion.widget.Control.prototype.update.apply(this, arguments);
    if(data.text) {
        this.ui.setText(data.text);
    }
}

// register
Onion.widget.register("button", Onion.widget.Button);
