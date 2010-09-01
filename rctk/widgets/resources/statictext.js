Onion.widget.StaticText = function(jwin, parent, controlid) {
    Onion.widget.Control.apply(this, arguments);
}

Onion.widget.StaticText.prototype = new Onion.widget.Control();

Onion.widget.StaticText.prototype.create = function(data) {
    var controlid = "ctrl"+this.controlid;
    this.jwin.factory.append('<div id="' + controlid + '">' + data.text + "</div>");

    this.control = $("#"+controlid);
    this.control.addClass(this.cssclass);
    this.set_properties(data);

    if('wrap' in data) {
        if(data.wrap) {
            this.control.css("white-space", "pre-wrap");
        }
        else {
            this.control.css("white-space", "pre");
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

Onion.widget.StaticText.prototype.update = function(data) {
    Onion.widget.Control.prototype.update.apply(this, arguments);
    if('text' in data) {
        this.control.html(data.text);
    }
}

Onion.widget.StaticHTMLText = function(jwin, parent, controlid) {
    Onion.widget.StaticText.apply(this, arguments);
}

Onion.widget.StaticHTMLText.prototype = new Onion.widget.StaticText();

Onion.widget.StaticHTMLText.prototype.create = function(data) {
    var controlid = "ctrl"+this.controlid;
    this.jwin.factory.append('<div id="' + controlid + '">' + data.text + "</div>");

    this.control = $("#"+controlid);
    this.control.addClass(this.cssclass);
    this.set_properties(data);

    // we're not supporting any of the specific statictext properties
}

// register
Onion.widget.register("statictext", Onion.widget.StaticText);
Onion.widget.register("statichtmltext", Onion.widget.StaticHTMLText);
