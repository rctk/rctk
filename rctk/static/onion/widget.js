Onion.widget = function() {
    var map = [];
    
    return {
        /* Register a widget in order to map widget names to classes. */
        register: function(name, class) {
            if (!map[name]) {
                map[name] = class;
            }
        },
        /* Lookup the class of a widget */
        map: function(name) {
            return map[name];
        }
    }
}();