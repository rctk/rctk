Onion.ui.StaticText = function() {
    Onion.ui.Base.apply(this, arguments);
}

Onion.ui.StaticText.prototype = new Onion.ui.Base();

Onion.ui.StaticText.prototype.create = function(controlid, text) {
    this.factory.append('<div id="' + controlid + '">' + text + "</div>");
    this.element = $("#"+controlid);
}

Onion.ui.StaticText.prototype.setText = function(text) {
    this.element.html(text);
}
