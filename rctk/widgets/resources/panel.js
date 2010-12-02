/*
 * A panel is a simple container-control. Mostly used to
 * nest layoutmanagers. It support scrolling (horizontally
 * for now, using defaults), but we're not using the default
 * html/css "overflow" scrolling because we can't properly 
 * predict the exact size of the panel:
 * - the width of the panel will be the outer width of the entire
 *   panel includign scrollbar, so the available area will be smaller
 * - scrollbars won't be shown until really necessary which means either
 *   the panel will expand or the inner area will shrink.
 * using jScrollingPane makes all of this predictable.
 *
 * See also: http://stackoverflow.com/questions/4334366/
 */
Onion.widget.Panel = function(jwin, parent, controlid) {
    Onion.widget.Container.apply(this, arguments);
    this.name = "panel";
}

Onion.widget.Panel.prototype = new Onion.widget.Container();

Onion.widget.Panel.prototype.create = function(data) {
    Onion.widget.Container.prototype.create.apply(this, arguments);

    if(data.scrolling) {
        Onion.util.log("+__++_+_+_+_+_+_+_ scrolling", this.control);
        this.scrolling = true;

        this.control.jScrollPane();
        this.container = this.control;
        this.control = this.control.parent();
    }
    else {
        this.scrolling = false;
    }

}

Onion.widget.Panel.prototype.update_scrolling = function() {
    if(this.scrolling) {
        this.container.jScrollPane();
        Onion.util.log("+__++_+_+_+_+_+_+_ update", this.container, this.control);
    }
}

Onion.widget.Panel.prototype.append = function(control, data) {
    Onion.widget.Container.prototype.append.apply(this, arguments);
    this.control.scrollTop(this.control.attr("scrollHeight"));
    this.update_scrolling();
}

Onion.widget.Panel.prototype.layout_updated = function() {
    Onion.widget.Container.prototype.layout_updated.apply(this, arguments);
    this.control.scrollTop(this.control.attr("scrollHeight"));
    this.update_scrolling();
}

Onion.widget.register("panel", Onion.widget.Panel);
