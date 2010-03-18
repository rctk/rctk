Onion.widget.Button = function(jwin, parent, controlid) {
    Onion.widget.Control.apply(this, arguments);
}

Onion.widget.Button.prototype = new Onion.widget.Control();

Onion.widget.Button.prototype.create = function(data) {
    var controlid = "ctrl"+this.controlid;
    this.jwin.factory.append('<button id="' + controlid + '">' + data.text + "</button>")
    this.control = $("#"+controlid);
    this.control.addClass(this.cssclass);
    this.handle_click = false;

    var self=this;
    this.control.click(function() { self.clicked() });
    this.set_properties(data);
}

Onion.widget.Button.prototype.clicked = function() {
    if(this.handle_click) {
        $.post("event", {'type':"click", 'id':this.controlid}, Onion.util.hitch(this.jwin, "handle_tasks"), "json");
    }
}