/*
 * Simple collection widget
 */
Onion.widget.Collection = function(jwin, parent, controlid) {
    Onion.widget.Container.apply(this, arguments);
    this.cssclass="panel-control";
    this.expand = true; // expand in layout by default
}

Onion.widget.Collection.prototype = new Onion.widget.Panel();

// register
Onion.widget.register("collection", Onion.widget.Collection);

