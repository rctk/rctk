/*
 * A panel is a simple container-control. Mostly used to
 * nest layoutmanagers
 */
Onion.widget.Panel = function(jwin, parent, controlid) {
    Onion.widget.Container.apply(this, arguments);
    this.cssclass="panel-control";
    this.expand = true; // expand in layout by default
}

Onion.widget.Panel.prototype = new Onion.widget.Container();

Onion.widget.Panel.prototype.create = function(data) {
    Onion.widget.Container.prototype.create.apply(this, arguments);

    if(data.scrolling) {
        this.control.css("overflow", "auto");
        this.scrolling = true;
    }
    else {
        this.scrolling = false;
    }

}

Onion.widget.Panel.prototype.append = function(control, data) {
    Onion.widget.Container.prototype.append.apply(this, arguments);
    //Onion.util.log("scrolling " + this.control.attr("scrollTop") + ", " + this.control.attr("scrollHeight"));
    this.control.scrollTop(this.control.attr("scrollHeight"));
    //Onion.util.log("scrolling " + this.control.attr("scrollTop"));
}

Onion.widget.Panel.prototype.layout_updated = function() {
    Onion.widget.Container.prototype.layout_updated.apply(this, arguments);
    this.control.scrollTop(this.control.attr("scrollHeight"));
}

// register
Onion.widget.register("panel", Onion.widget.Panel);
