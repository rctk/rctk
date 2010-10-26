Onion.widget.Frame = function(jwin, parent, controlid) {
    Onion.widget.Container.apply(this, arguments);
    this.name = "frame";
}

Onion.widget.Frame.prototype = new Onion.widget.Container();

Onion.widget.Frame.prototype.create = function(data) {
    var controlid = "ctrl"+this.controlid;

    this.jwin.factory.append('<div id="' + controlid + '" title="' + data.title + '"></div>');
    this.control = $("#"+controlid);
    this.control.dialog({'autoOpen':true, 'modal':false, 'resize':false}); // width, position, modal, etc.
    this.control = $("#"+controlid).parent();
    this.container = $("#"+controlid);
    // dialogBox class not currently used
    this.container.addClass(this.cssclass);
    this.container.addClass(this.name);
    
    // windows aren't appended, they appear immediately
    this.control.appendTo(this.jwin.toplevels);
    this.set_properties(data);
}

Onion.widget.Frame.prototype.setLayout = function(type, config) {
    Onion.widget.Container.prototype.setLayout.apply(this, arguments);
    // dialogInner class not currently used
    //this.layout.layoutcontrol.addClass("dialogInner");
}

Onion.widget.Frame.prototype.update = function(data) {
    Onion.widget.Container.prototype.update.apply(this, arguments);
    if(data.state) {
        Onion.util.log("Window state update", data);
        if(data.state == "open") {
            this.container.dialog('open');
        }
        else if(data.state == "close") {
            Onion.util.log("Closing");
            this.container.dialog('close');
        }
    }
}

Onion.widget.Frame.prototype.resize = function(width, height) {
    this.container.dialog({width:width, height: height});
    //this.container.dialog({minWidth:width, minHeight: height});
}
// register
Onion.widget.register("window", Onion.widget.Frame);
