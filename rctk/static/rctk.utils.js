// more goodies: http://getfirebug.com/console.html

jQuery.log = function() {
        if (typeof window.console != 'undefined') {
                window.console.log.apply(this, arguments);
        }
}
jQuery.debug = function() {
        if (typeof window.console != 'undefined') {
                window.console.debug.apply(this, arguments);
        }
}

jQuery.fn.log = function(msg) {
        msg = msg || "log";
        jQuery.log("%s: %o", msg, this);
        return this;
};

jQuery.fn.debug = function(msg) {
        msg = msg || "log";
        jQuery.debug("%s: %o", msg, this);
        return this;
}
