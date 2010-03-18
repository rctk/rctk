Onion.widget.Password = function(jwin, parent, controlid) {
    Onion.widget.Text.apply(this, arguments);
}

Onion.widget.Password.prototype = new Onion.widget.Text();

Onion.widget.Password.prototype.create = function(data) {
    var controlid = "ctrl"+this.controlid;
    this.jwin.factory.append('<input type="password" name="' + controlid + '" id="' + controlid + '">');
    this.control = $("#"+controlid);
    this.control.addClass(this.cssclass);

    var self = this;
    this.control.change(function() {
        self.changed();
    });
    this.set_properties(data);
}
