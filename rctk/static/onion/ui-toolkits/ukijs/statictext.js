Onion.ui.StaticText = function() {
    Onion.ui.Base.apply(this, arguments);
}

Onion.ui.StaticText.prototype = new Onion.ui.Base();

Onion.ui.StaticText.prototype.create = function(controlid, text) {
    // perhaps not pass the factory and let the UI find it and use it
    Onion.util.log("Label", controlid, text);
    this.factory.append("<div id='" + controlid + "'></div>");
    this.element = $("#"+controlid);
    this.ui = uki({
        view: 'Label',
        rect: '0 0 200 24', // required?
        anchors: 'left top',
        fontSize: '12px',
        text: text
    });
    this.ui.attachTo(this.element.get(0), '0 0');
}


Onion.ui.StaticText.prototype.setText = function(text) {
    this.ui.attr('text', text);
}
