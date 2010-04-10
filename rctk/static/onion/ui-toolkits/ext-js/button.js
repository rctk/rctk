/*
 * This is an example implementation of a UI Button using ext-js.
 * Because of ext-js's commercial nature
 * - you need a license if you want to do something commercially with RCTK
 * - we can't bundle ext-js with RCTK
 * there's no real purpose to add any other support besides this demo.
 * Add the following code to main.html, just before the document-ready snippet:

 <script type="text/javascript" src="/static/extjs/ext-base.js"></script>
 <script type="text/javascript" src="/static/extjs/ext-all.js"></script>
 <script type="text/javascript" src="/static/onion/ui-toolkits/ext-js/base.js"></script>
 <script type="text/javascript" src="/static/onion/ui-toolkits/ext-js/button.js"></script>
 * and make sure you have the relevant parts of ext-js in static/ including
 * the ext-js resources/images directory.
 */
Onion.ui.Button = function() {
    Onion.ui.Base.apply(this, arguments);
}

Onion.ui.Button.prototype = new Onion.ui.Base();

Onion.ui.Button.prototype.create = function(controlid, text) {
    // perhaps not pass the factory and let the UI find it and use it
    this.factory.append("<div id='" + controlid + "'></div>");
    this.ui = new Ext.Button({
        'renderTo':controlid,
	    iconCls:'x-plain',
	    text:text})
    this.element = $("#"+controlid);
}

Onion.ui.Button.prototype.click = function(handler) {
    this.ui.addListener("click", handler)
}

Onion.ui.Button.prototype.setText = function(text) {
    this.ui.setText(text);
}
