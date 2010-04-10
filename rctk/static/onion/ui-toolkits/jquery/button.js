Onion.ui.Button = function() {
    Onion.ui.Base.apply(this, arguments);
}

Onion.ui.Button.prototype = new Onion.ui.Base();

Onion.ui.Button.prototype.create = function(controlid, text) {
    // perhaps not pass the factory and let the UI find it and use it
    this.factory.append('<button id="' + controlid + '">' + text + "</button>");
    this.element = $("#"+controlid);
}

Onion.ui.Button.prototype.click = function(handler) {
    this.element.click(handler)
}

Onion.ui.Button.prototype.setText = function(text) {
    this.element.html(text);
}
