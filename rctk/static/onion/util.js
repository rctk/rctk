Onion.util = function() {
    return {
        hitch: function(context, method) {
            // idea taken from dojo
            var _c = context;
            var _m = method;

            return function() { return _c[_m].apply(_c, arguments || []); }
        },
         // stubs, should be overwritten with framework specific function
        log: function() { return true },
        debug: function() { return true },
        // mimic jquery 1.4
        proxy: function(a, b) { return Onion.util.hitch(b, a); }
    }
}();
