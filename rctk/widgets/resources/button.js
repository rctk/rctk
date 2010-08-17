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
    this.control.click(function() { 
         // being busy means we've been clicked and the handler
         // is still busy handling. Don't accept clicks untill
         // it's finished.
         if(!self.busy) {
            self.clicked(); 
            self.jwin.flush(); 
            self.jwin.register_busy(self);
         }
         else {
            Onion.util.log("Control busy", self);
         }
    });
    this.set_properties(data);
}

Onion.widget.Button.prototype.clicked = function() {
    if(this.handle_click) {
        this.jwin.add_task("event", "click", this.controlid);
    }
}

Onion.widget.Button.prototype.update = function(data) {
    Onion.widget.Control.prototype.update.apply(this, arguments);
    if('text' in data) {
        this.control.html(data.text);
    }
}

// register
Onion.widget.register("button", Onion.widget.Button);
