function hitch(context, method) {
    // idea taken from dojo
    var _c = context;
    var _m = method;

    return function() { return _c[_m].apply(_c, arguments || []); }
}

function Control(jwin, parent, controlid) {
    this.cssclass = "control";
    this.jwin = jwin;
    this.controlid = controlid;
    this.parent = parent;
}

Control.prototype.update = function(data) {
    /* 
     * a control has been updated (changed) on the serverside,
     * this change needs to be reflected locally.
     * "sync" may be more consistent, controls on the serverside
     * implement a sync() method for changes from the clientside
     */
}

Control.prototype.set_properties = function(data) {
    if(data === undefined) {
        return;
    }
    // handle base properties
    if('width' in data && data.width) {
        this.control.css("width", data.width + "px");
    }
    if('height' in data && data.height) {
        this.control.css("height", data.height + "px");
    }
    if('foreground' in data && data.foreground) {
        this.control.css("color", data.foreground);
    }
    if('background' in data && data.background) {
        this.control.css("background-color", data.background);
    }
}
Control.prototype.create = function(data) {
    var controlid = "ctrl"+this.controlid;
    this.jwin.factory.append('<div id="' + controlid + '"></div>');
    this.control = $("#"+controlid);
    this.control.addClass(this.cssclass);
    this.set_properties(data);

}

/*
 * A container is a control that can contain controls, i.e. a window,
 * a layout manager. Its control may be different from its container
 * (i.e. a window, which has outer divs as decoration)
 */
function Container(jwin, parent, controlid) {
    Control.apply(this, arguments);
    // default layout manager
    this.layout = new PowerLayout(this.jwin, this);
}

Container.prototype = new Control();

Container.prototype.create = function(data) {
    Control.prototype.create.apply(this, arguments);

    this.container = this.control;
}

Container.prototype.append = function(control, data) {
    this.layout.append(control, data);
}

Container.prototype.setLayout = function(type, config) {
    // unimplemented options:
    // hgap, vgap, resize (default true)
    switch(type) {
    case 'tabbed':
        this.layout = new TabbedLayout(this.jwin, this, config);
        this.layout.create();
        break;
    case 'power':
        this.layout = new PowerLayout(this.jwin, this, config);
        this.layout.create();
        break;
    }
}

Container.prototype.relayout = function() {
    this.layout.layout();
    this.layout.layout_fase2();
    this.layout_updated();
}

Container.prototype.layout_updated = function() {
}

/*
 * A panel is a simple container-control. Mostly used to
 * nest layoutmanagers
 */
function Panel(jwin, parent, controlid) {
    Container.apply(this, arguments);
    this.cssclass="panel-control";
    this.expand = true; // expand in layout by default
}

Panel.prototype = new Container();

Panel.prototype.create = function(data) {
    Container.prototype.create.apply(this, arguments);

    if(data.scrolling) {
        this.control.css("overflow", "auto");
        this.scrolling = true;
    }
    else {
        this.scrolling = false;
    }

}

Panel.prototype.append = function(control, data) {
    Container.prototype.append.apply(this, arguments);
    jQuery.log("scrolling " + this.control.attr("scrollTop") + ", " + this.control.attr("scrollHeight"));
    this.control.scrollTop(this.control.attr("scrollHeight"));
    jQuery.log("scrolling " + this.control.attr("scrollTop"));
}

Panel.prototype.layout_updated = function() {
    Container.prototype.layout_updated.apply(this, arguments);
    this.control.scrollTop(this.control.attr("scrollHeight"));
}

/*
 * The root is the root window, the first control where
 * everything starts with id 0
 *
 * It should be singletonish. There's no actual create()
 */
function Root(jwin) {
    this.control = $("#root");
    this.container = this.control;
    this.control.width(1000);
    this.control.height(500);
    Container.apply(this, [jwin, this, 0]);
}

Root.prototype = new Container()

Root.prototype.create = function(data) {
    this.set_properties(data);
}

Root.prototype.append = function(control, data) {
    //control.control.appendTo(this.container);
    this.layout.append(control, data);
}

function Button(jwin, parent, controlid) {
    Control.apply(this, arguments);
}

Button.prototype = new Control();

Button.prototype.create = function(data) {
    var controlid = "ctrl"+this.controlid;
    this.jwin.factory.append('<button id="' + controlid + '">' + data.text + "</button>")
    this.control = $("#"+controlid);
    this.control.addClass(this.cssclass);
    this.handle_click = false;

    var self=this;
    this.control.click(function() { self.clicked() });
    this.set_properties(data);
}

Button.prototype.clicked = function() {
    if(this.handle_click) {
        $.post("event", {'type':"click", 'id':this.controlid}, hitch(this.jwin, "handle_tasks"), "json");
    }
}


function Dropdown(jwin, parent, controlid) {
    Control.apply(this, arguments);
    this.items = [];
}

Dropdown.prototype = new Control();

Dropdown.prototype.create = function(data) {
    var controlid = "ctrl"+this.controlid;
    this.jwin.factory.append('<select id="' + controlid + '">' + "</select>");
    this.control = $("#"+controlid);
    this.control.addClass(this.cssclass);
    this.handle_click = false;

    if(data.items) {
        for(var i = 0; i < data.items.length; i++) {
            this.append_item(data.items[i][0], data.items[i][1]);
        }
    }
    var self=this;
    this.control.change(function() { self.changed() });
    this.set_properties(data);
}

Dropdown.prototype.append_item = function(key, label) {
    this.control.append('<option value="' + key + '">' + label + "</option>");
    this.items.push({'key':key, 'label':label});
}

Dropdown.prototype.changed = function() {
    this.jwin.sync({'id':this.controlid, 'selection':this.control.val()});
    if(this.handle_click) {
        // find current selection.
        $.post("event", {'type':"click", 'id':this.controlid}, hitch(this.jwin, "handle_tasks"), "json");
    }
        
}

Dropdown.prototype.update = function(data) {
    if(data.item) {
        this.append_item(data.item[0], data.item[1]);
    }
    if(data.selection) {
        this.control.val(data.selection);
    }
    if(data.clear) {
        this.control.empty(); // doesn't work on google chrome?
        this.items = []
    }
}

/*
 * TODO:
 *
 * Support insertion at any position
 * Support deletion
 */
function List(jwin, parent, controlid) {
    Dropdown.apply(this, arguments);
    this.size = 5; // default
}

List.prototype = new Dropdown();

List.prototype.create = function(data) {
    Dropdown.prototype.create.apply(this, arguments);
    if(data.size) {
        this.size = Math.max(2, data.size);
    }
    this.setsize();
}

List.prototype.append_item = function(key, label) {
    Dropdown.prototype.append_item.apply(this, arguments);
    this.setsize();
}

List.prototype.setsize = function() {
    this.control.attr('size', this.size);
}

List.prototype.update = function(data) {
    Dropdown.prototype.update.apply(this, arguments);

    if(data.size) {
        this.size = Math.max(2, data.size);
        this.setsize();
    }
}

function StaticText(jwin, parent, controlid) {
    Control.apply(this, arguments);
}

StaticText.prototype = new Control();

StaticText.prototype.create = function(data) {
    var controlid = "ctrl"+this.controlid;
    this.jwin.factory.append('<div id="' + controlid + '">' + data.text + "</div>")
    this.control = $("#"+controlid);
    this.control.addClass(this.cssclass);
    this.set_properties(data);

    if('wrap' in data) {
        if(data.wrap) {
            this.control.css("white-space", "wrap");
        }
        else {
            this.control.css("white-space", "nowrap");
        }
    }
    if('bold' in data) {
        if(data.bold) {
            this.control.css("font-weight", "bold");
        }
        else {
            this.control.css("font-weight", "")
        }
    }
    if('italic' in data) {
        if(data.italic) {
            this.control.css("font-style", "italic");
        }
        else {
            this.control.css("font-style", "");
        }
    }

    if('decoration' in data) {
        if(data.decoration == "underline") {
            this.control.css("text-decoration", "underline");
        }
        else if(data.decoration == "overstrike") {
            this.control.css("text-decoration", "line-through");
        }
        else {
            this.control.css("text-decoration", "");
        }
    }
        
}

StaticText.prototype.update = function(data) {
    if(data.text) {
        this.control.html(data.text);
    }
}

/*
 * Text is a simple text input. The serverside needs to be informed
 * of changes so we need to regularly submit changes, esp. for actions
 * that depend on it. An explicit <enter> is not sufficient, eventhandlers
 * may want to read the current value at any moment
 *
 * For now, use onchange to submit changes.
 */

function Text(jwin, parent, controlid) {
    Control.apply(this, arguments);
}

Text.prototype = new Control();

Text.prototype.create = function(data) {
    var controlid = "ctrl"+this.controlid;
    this.jwin.factory.append('<input type="text" name="' + controlid + '" id="' + controlid + '">');
    this.control = $("#"+controlid);
    this.control.addClass(this.cssclass);

    var self = this;
    this.control.change(function() {
        self.changed();
    });
    this.control.keypress(function(e) {
        self.keypressed(e);
    });
    this.set_properties(data);
}

Text.prototype.changed = function() {
    this.jwin.sync({'id':this.controlid, 'value':this.control.val()});
    if(this.handle_change) {
        $.post("event", {'type':"change", 'id':this.controlid}, hitch(this.jwin, "handle_tasks"), "json");
    }
}
Text.prototype.keypressed = function(e) {
    // if this.handle_keypress: jwin.sync, post event
    // could use some optimization
    if(this.handle_submit) {
        if(e.which == 13) {
            this.jwin.sync({'id':this.controlid, 'value':this.control.val()});
            $.post("event", {'type':"submit", 'id':this.controlid}, hitch(this.jwin, "handle_tasks"), "json");
            return false;
        }
    }
}

Text.prototype.val = function() {
    return this.control.val();
}

Text.prototype.update = function(update) {
    if(update.value != undefined) {
        this.control.val(update.value);
    }
}

function Password(jwin, parent, controlid) {
    Text.apply(this, arguments);
}

Password.prototype = new Text();

Password.prototype.create = function(data) {
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

/*
 * Date is reserved in javascript (or at least already used)
 */
function DateText(jwin, parent, controlid) {
    Text.apply(this, arguments);
}

DateText.prototype = new Text();

DateText.prototype.create = function(data) {
    Text.prototype.create.apply(this, arguments);
    this.control.datepicker(data.pickerconfig);
}

function CheckBox(jwin, parent, controlid) {
    Control.apply(this, arguments);
}

CheckBox.prototype = new Control();

CheckBox.prototype.create = function(data) {
    var controlid = "ctrl" + this.controlid;
    this.jwin.factory.append('<input type="checkbox" id="' + controlid + '"></input>')
    this.control = $("#" + controlid);
    this.control.attr('defaultChecked', data.defaultChecked);
    this.handle_click = false;

    var self=this;
    this.control.change(
        function() { self.changed() }
    );
    this.set_properties(data);
}

/*
 * Handle change events, which means syncing the updated state and possibly
 * firing the 'click' event. By (ab)using change to detect clicks we can
 * guarantee sync will take place before click
 */
CheckBox.prototype.changed = function() {
    this.jwin.sync({'id':this.controlid, 'checked':this.control.attr('checked')});

    if(this.handle_click) {
        $.post("event", {'type':"click", 'id':this.controlid}, hitch(this.jwin, "handle_tasks"), "json");
    }
}

CheckBox.prototype.update = function(data) {
    // use === operator because we're testing a boolean
    if(data.checked !== undefined) {
        this.control.attr('checked', data.checked);
    }
}

function RadioButton(jwin, parent, controlid) {
    Control.apply(this, arguments);
}

RadioButton.prototype = new Control();

RadioButton.prototype.create = function(data) {
    var controlid = "ctrl" + this.controlid;
    this.jwin.factory.append('<input type="radio" id="' + controlid + '"></input>')
    this.control = $("#" + controlid);
    this.control.attr('name', data.name);
    this.control.attr('value', data.value);
    this.control.attr('defaultChecked', data.defaultChecked);
    this.handle_click = false;
    
    var self=this;
    this.control.change( function() { self.changed() });
    this.set_properties(data);
}

RadioButton.prototype.changed = function() {
    this.jwin.sync({'id':this.controlid, 'checked':this.control.attr('checked') });

    if(this.handle_click) {
        $.post("event", {'type':"click", 'id':this.controlid}, hitch(this.jwin, "handle_tasks"), "json");
    }
}
RadioButton.prototype.update = function(data) {
    if(data.group) {
        this.control.attr('name', data.name);
    }
    if(data.value) {
        this.control.attr('value', data.value);
    }
    if(data.checked !== undefined) {
        this.control.attr('checked', data.checked);
    }
}

function Frame(jwin, parent, controlid) {
    Container.apply(this, arguments);
}

Frame.prototype = new Container();

Frame.prototype.create = function(data) {

    var controlid = "ctrl"+this.controlid;

    this.jwin.factory.append('<div id="' + controlid + '" title="' + data.title + '"></div>');
    this.control = $("#"+controlid);
    this.control.dialog({'autoOpen':true, 'modal':false, 'resize':false}); // width, position, modal, etc.
    this.control = $("#"+controlid).parent();
    this.container = $("#"+controlid);
    // dialogBox class not currently used
    this.container.addClass(this.cssclass);
    
    // windows aren't appended, they appear immediately
    this.control.appendTo(this.jwin.toplevels);
    this.set_properties(data);
}

Frame.prototype.setLayout = function(type, config) {
    Container.prototype.setLayout.apply(this, arguments);
    // dialogInner class not currently used
    //this.layout.layoutcontrol.addClass("dialogInner");
}

Frame.prototype.update = function(data) {
    if(data.state) {
        jQuery.log("Window state update ", data);
        if(data.state == "open") {
            this.container.dialog('open');
        }
        else if(data.state == "close") {
            jQuery.log("Closing");
            this.container.dialog('close');
        }
    }
}

