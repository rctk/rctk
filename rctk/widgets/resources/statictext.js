Onion.widget.StaticText = function(jwin, parent, controlid) {
    Onion.widget.Control.apply(this, arguments);
    this.name = "statichtml";
}

Onion.widget.StaticText.prototype = new Onion.widget.Control();

Onion.widget.StaticText.prototype.create = function(data) {
    var controlid = "ctrl"+this.controlid;
    this.jwin.factory.append('<div id="' + controlid + '">' + data.text + "</div>");

    this.control = $("#"+controlid);
    this.control.addClass(this.cssclass);
    this.control.addClass(this.name);
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
        Onion.util.log("########## before", this.control.outerWidth(true));
        this.control.html(data.text);
        Onion.util.log("########## after 1", this.control.outerWidth(true));
        // Respect width/height settings.
        if(this.width) {
            Onion.util.log("######## scaling to", this.width);
            this.control.width(this.width);
            Onion.util.log("########## after 2", this.control.outerWidth(true));
        }
        //else if(this.maxwidth && this.control.width() > this.maxwidth) {
        //    this.control.width(this.maxwidth + "px"); 
       // }
       // if(this.height) {
       //     this.control.height(this.height + "px");
       // }
       // else if(this.maxheight && this.control.height() > this.maxheight) {
       //     this.control.height(this.maxheight + "px"); 
       // }
    }
}

Onion.widget.StaticHTMLText = function(jwin, parent, controlid) {
    Onion.widget.StaticText.apply(this, arguments);
    this.name = "statichtmltext";
}

Onion.widget.StaticHTMLText.prototype = new Onion.widget.StaticText();

Onion.widget.StaticHTMLText.prototype.create = function(data) {
    var controlid = "ctrl"+this.controlid;
    this.jwin.factory.append('<div id="' + controlid + '">' + data.text + "</div>");

    this.control = $("#"+controlid);
    this.control.addClass(this.cssclass);
    this.set_properties(data);
    this.control.addClass(this.name);

    // we're not supporting any of the specific statictext properties
}

// register
Onion.widget.register("statictext", Onion.widget.StaticText);
Onion.widget.register("statichtmltext", Onion.widget.StaticHTMLText);
