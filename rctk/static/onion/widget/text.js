/*
 * Text is a simple text input. The serverside needs to be informed
 * of changes so we need to regularly submit changes, esp. for actions
 * that depend on it. An explicit <enter> is not sufficient, eventhandlers
 * may want to read the current value at any moment
 *
 * For now, use onchange to submit changes.
 */

Onion.widget.Text = function(jwin, parent, controlid) {
    Onion.widget.Control.apply(this, arguments);
}

Onion.widget.Text.prototype = new Onion.widget.Control();

Onion.widget.Text.prototype.create = function(data) {
    var controlid = "ctrl"+this.controlid;
    this.jwin.factory.append('<input type="text" name="' + controlid + '" id="' + controlid + '">');
    this.control = $("#"+controlid);
    this.control.val(data.value);
    this.control.addClass(this.cssclass);

    var self = this;
    this.control.change(function() {
        self.changed();
        self.jwin.flush();
    });
    this.control.keypress(function(e) {
        self.keypressed(e);
        self.jwin.flush();
    });
    this.set_properties(data);
}

Onion.widget.Text.prototype.changed = function() {
    this.jwin.add_task("sync", "sync", this.controlid, {'value':this.control.val()});
    if(this.handle_change) {
        this.jwin.add_task("event", "change", this.controlid);
    }
}

Onion.widget.Text.prototype.keypressed = function(e) {
    // if this.handle_keypress: jwin.sync, post event
    // could use some optimization
    if(this.handle_submit) {
        if(e.which == 13) {
            this.jwin.add_task("sync", "sync", this.controlid, {'value':this.control.val()});
            this.jwin.add_task("event", "submit", this.controlid);
            return false;
        }
    }
}

Onion.widget.Text.prototype.val = function() {
    return this.control.val();
}

Onion.widget.Text.prototype.update = function(update) {
    if(update.value != undefined) {
        this.control.val(update.value);
    }
}

// register
Onion.widget.register("text", Onion.widget.Text);
