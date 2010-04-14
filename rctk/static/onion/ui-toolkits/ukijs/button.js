Onion.ui.Button = function() {
    Onion.ui.Base.apply(this, arguments);
}

Onion.ui.Button.prototype = new Onion.ui.Base();

Onion.ui.Button.prototype.create = function(controlid, text) {
    // perhaps not pass the factory and let the UI find it and use it
    this.factory.append("<div id='" + controlid + "'></div>");
    this.element = $("#"+controlid);
    this.ui = uki({
        view: 'Button',
        rect: '0 0 200 24', // required?
        text: text
    });
    // resizing is a bit drastic atm
    // this.ui.resizeToContents('width height');
    this.ui.attachTo(this.element.get(0), '0 0');
}

Onion.ui.Button.prototype.click = function(handler) {
    Onion.util.log("uki button click", handler, this.ui);
    this.ui.bind("click", handler)
}

Onion.ui.Button.prototype.setText = function(text) {
    this.ui.attr('text', text);
    // this.ui.resizeToContents('width height');
}
