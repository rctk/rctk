(function($) {
    jQuery.extend({
        "log": function() {
            if (typeof window.console != 'undefined') {
                window.console.log.apply(window.console, arguments);
            }
        },
        "debug": function() {
            if (typeof window.console != 'undefined') {
                window.console.debug.apply(window.console, arguments);
            }
        }
    });
    // $.fn.extend... ?
})(jQuery);

// attach jQuery to Onion
Onion.env.framework = jQuery;
Onion.util.log = jQuery.log;
Onion.util.debug = jQuery.debug;

jQuery.fn.log = function(msg) {
    msg = msg || "log";
    jQuery.log("%s: %o", msg, this);
    return this;
};

jQuery.fn.debug = function(msg) {
    msg = msg || "log";
    jQuery.debug("%s: %o", msg, this);
    return this;
};
