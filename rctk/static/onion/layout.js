Onion.layout = function() {
    var map = [];
    
    return {
        /* Register a layout in order to map widget names to classes. */
        register: function(name, class) {
            if (!map[name]) {
                map[name] = class;
            }
        },
        /* Lookup the class of a layout */
        map: function(name) {
            return map[name] || null;
        }
    }
}();