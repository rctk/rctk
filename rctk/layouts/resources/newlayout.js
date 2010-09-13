Onion.layout.NewLayout = function(jwin, parent, config) {
    Onion.layout.Layout.apply(this, arguments);
    config = config?config:{};
}

Onion.layout.NewLayout.prototype = new Onion.layout.Layout();

Onion.layout.NewLayout.prototype.create = function() {
    if(this.created) {
        return;
    }
}

// move basic append, remove to base

Onion.layout.NewLayout.prototype.append = function(control, data) {
    this.create();
    // this is alot of control: control.control.control!
    var controlinfo = {row:-1, col:-1, rowspan:1, colspan:1, control:control, data:data || {}}
}

Onion.layout.NewLayout.prototype.layout = function() {
    Onion.util.log("New layout");
}

Onion.layout.NewLayout.prototype.layout_fase2 = function() {
    Onion.util.log("New layout 2");
}

Onion.layout.register('new', Onion.layout.NewLayout);

