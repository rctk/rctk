/*
 * The root is the root window, the first control where
 * everything starts with id 0
 *
 * The root is always there - there is exactly one root window,
 * not more, not less. This also means that there's no actual
 * create.
 */
Onion.widget.Root = function(jwin) {
    this.control = $("#root");
    this.container = this.control;
    Onion.widget.Container.apply(this, [jwin, this, 0]);
}

Onion.widget.Root.prototype = new Onion.widget.Container()

Onion.widget.Root.prototype.create = function(data) {
    this.set_properties(data);
}

Onion.widget.Root.prototype.append = function(control, data) {
    //control.control.appendTo(this.container);
    this.layout.append(control, data);
}

Onion.widget.Root.prototype.update = function(data) {
    Onion.widget.Container.prototype.update.apply(this, arguments);
    if('title' in data) {
        $("title").html(data.title);
    }
    // properly resizing the actual window is tricky (and usually blocked
    // anyway)
    if('width' in data && data.width) {
        $("#root").width(data.width);
        //window.resizeTo(data.width, $(window).height());
    }
    if('height' in data && data.height) {
        $("#root").height(data.width);
        //window.resizeTo($(window).width(), data.height);
    }
}
Onion.widget.register("root", Onion.widget.Root);

