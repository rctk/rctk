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
    var html = '<input type="text" name="' + controlid + '" id="' + controlid + '">';
    if (data.rows > 1) {
        html = '<textarea name="' + controlid + '" id="' + controlid + '"></textarea>';
    }
    this.jwin.factory.append(html);
    this.control = $("#"+controlid);
    this.control.val(data.value);
    this.control.attr('rows', data.rows);
    this.control.attr('cols', data.columns);
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
        if(!this.busy) {
            /*
             * Does it make sense to handle busy-ness here? This would mean
             * double-hitting enter..
             */
            if(e.which == 13) {
                this.jwin.register_busy(this);
                this.jwin.add_task("sync", "sync", this.controlid, {'value':this.control.val()});
                this.jwin.add_task("event", "submit", this.controlid);
                return false;
            }
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
