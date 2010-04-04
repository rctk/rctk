/*
 * The root is the root window, the first control where
 * everything starts with id 0
 *
 * The root is always there - there is exactly one root window,
 * not more, not less. This also means that there's no actual
 * create.
 */
Onion.widget.Root = function(jwin) {
    this.control = $("#root");
    this.container = this.control;
    this.control.width(1000);
    this.control.height(500);
    Onion.widget.Container.apply(this, [jwin, this, 0]);
}

Onion.widget.Root.prototype = new Onion.widget.Container()

Onion.widget.Root.prototype.create = function(data) {
    this.set_properties(data);
}

Onion.widget.Root.prototype.append = function(control, data) {
    //control.control.appendTo(this.container);
    this.layout.append(control, data);
}

Onion.widget.register("root", Onion.widget.Root);

