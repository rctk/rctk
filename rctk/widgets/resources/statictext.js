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

Onion.widget.StaticText.prototype.set_properties = function(data) {
    Onion.widget.Control.prototype.set_properties.apply(this, arguments);
    if('text' in data) {
        this.control.html(data.text);
        // Respect width/height settings.
        if(this.width) {
            this.control.width(this.width);
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

}

Onion.widget.StaticHTMLText.prototype.set_properties = function(data) {
    Onion.widget.StaticText.prototype.set_properties.apply(this, arguments);
    // text has been updated; update clickhandlers on a's
    if('text' in data) {
        this.handle_links()
    }
}

Onion.widget.StaticHTMLText.prototype.handle_links = function() {
    Onion.util.log("Installing clickhandler on statictext", $("#ctrl" + this.controlid + " a"));
    var self=this;
    $("#ctrl" + this.controlid + " a").click(function() {
        Onion.util.log("Click!", $(this).attr('href'));
        self.jwin.add_task("event", "click", self.controlid, {link:$(this).attr('href')});
        self.jwin.flush();
        return false;
    });
}

Onion.widget.register("statictext", Onion.widget.StaticText);
Onion.widget.register("statichtmltext", Onion.widget.StaticHTMLText);
