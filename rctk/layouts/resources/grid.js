/*
 * Layouts are very hard to do right. Some of the things you need to take
 * into account:
 * - different controls have different sizes, they need to be aligned nicely
 *   in a grid
 * - a layout can calculate what size it needs, or it can be instructed to use the vailable size, in which case rows/columns need to expand, somehow. Not all rows/columns may need to scale equally (or at all)
 * - all kinds of padding, inside and between cells
 * - the overall grid (rows, cols, spans) are calculated serverside, the
 *   complete configuration isn't known until the actual layout() call,
 *   and if children haven't been laid out, they can't be invoked recursively.
 * - alignment and expanding of controls, which in turn need relayouting
 *
 * esp. this last part is where the current implementation fails.
 */
/*
 * Thoughts on resizing, scaling:
 * Rows and columns can have a scaling factor. 1 means no scaling
 * (default size calulation), any other number determines how much the
 * rows/columns will scale when extra space is available.
 *
 * Example: three columns, scaling factors 1,2,3
 * available width is 100, column one takes 20px
 * remaining size is 80, which means 32px for column 2 and 48px for 3
 * If column 32 requires more than 32px, this space is taken from column 3.
 */
Onion.layout.NewLayout = function(jwin, parent, config) {
    Onion.layout.Layout.apply(this, arguments);
    config = config?config:{};
}

Onion.layout.NewLayout.prototype = new Onion.layout.Layout();

Onion.layout.NewLayout.prototype.create = function() {
    if(this.created) {
        return;
    }
    // not sure if we need this extra div.
    this.parent.container.append("<div id='layoutmgr" + this.parent.controlid + "'></div>");
    this.layoutcontrol = $("#layoutmgr" + this.parent.controlid);
    this.layoutcontrol.css("position", "relative");
    this.created = true;
    this.children = [];
    this.maxcellwidth = 0;
    this.maxcellheight = 0;
    this.row_sizes = [];
    this.col_sizes = [];

    this.static = false; // no fixed cell size; scale rows/cols nicely
    this.padx = 0;
    this.pady = 0;
    this.ipadx = 0;
    this.ipady = 0;
    this.sticky = "center"; // default stickyness
}

Onion.layout.NewLayout.prototype.append = function(control, data) {
    this.create();
    control.control.appendTo(this.layoutcontrol);
    control.containingparent = this.parent;
}

Onion.layout.NewLayout.prototype.sumwidth = function(start, end) {
    if(start === undefined) {
        start = 0;
    }
    if(end === undefined) {
        end = this.columns;
    }
    if(this.static) {
        return this.maxcellwidth * (end-start);
    }
    var s = 0;
    for(var i = start; i < end; i++) {
        s += this.col_sizes[i];
    }
    return s;
}

Onion.layout.NewLayout.prototype.sumheight = function(start, end) {
    var s = 0;
    if(start === undefined) {
        start = 0;
    }
    if(end === undefined) {
        end = this.rows;
    }
    if(this.static) {
        return this.maxcellheight * (end-start);
    }
    for(var i = start; i < end; i++) {
        s += this.row_sizes[i];
    }
    return s;
}

Onion.layout.NewLayout.prototype.initialize = function(config) {
    this.create();
    this.rows = config.size[0];
    this.columns = config.size[1];
    if('options' in config) {
        var options = config.options;
        if('padx' in options) {
            this.padx = options.padx;
        }
        if('pady' in options) {
            this.pady = options.pady;
        }
        if('ipadx' in options) {
            this.ipadx = options.ipadx;
        }
        if('ipady' in options) {
            this.ipady = options.ipady;
        }
        if('static' in options) {
            this.static = options.static;
        }
        if('sticky' in options) {
            this.sticky = options.sticky.toLowerCase();
        }
    }

    // avoid duplicates
    this.children = [];
    for(var i=0; i < config.cells.length; i++) {
        var c = config.cells[i];
        var control = this.jwin.controls[c.controlid];
        var info = {id:c.controlid, control:control, row:c.row, column:c.column, rowspan:c.rowspan, colspan:c.colspan};
        info.padx = 'padx' in c? c.padx: this.padx;
        info.ipadx = 'ipadx' in c? c.ipadx: this.ipadx;
        info.pady = 'pady' in c? c.pady: this.pady;
        info.ipady = 'ipady' in c? c.ipady: this.ipady;
        info.static = 'static' in c? c.static: this.static;
        info.sticky = 'sticky' in c? c.sticky.toLowerCase(): this.sticky;

        this.children.push(info);
    }

    /*
     * We need to keep track of the max height per row
     * and max width per column.
     */
    for(var c=0; c < this.columns; c++) {
        this.col_sizes[c] = 0;
    }
    for(var r=0; r < this.rows; r++) {
        this.row_sizes[r] = 0;
    }
    this.maxcellwidth = 0;
    this.maxcellheight = 0;
}

Onion.layout.NewLayout.prototype.layout = function(config) {
    Onion.util.log("NEWLAYOUT: relayout setting config", config);

    this.initialize(config);

    /*
     * Find the sizes of all children, possibly after recursively
     * laying them out if the child is a container with layout itself
     */
    for(var i=0; i<this.children.length; i++) {
        var info = this.children[i];
        var ctr = info.control;

        /*
         * Find the size of the control, but spread it over the rows/
         * columns it has allocated.
         */
        info.width = ctr.control.outerWidth(true);
        info.height = ctr.control.outerHeight(true);

        /*
         * Calculate how big the cell should be, taking padding and spanning into account
         */
        var width = Math.round(info.width / info.colspan) + info.padx*2;
        var height = Math.round(info.height / info.rowspan) + info.pady*2;

        /* 
         * Keep track of max width height, overall and per row/column
         */
        this.maxcellwidth = Math.max(this.maxcellwidth, width);
        this.maxcellheight = Math.max(this.maxcellheight, height);

        /*
         * colspans/rowspans are a bit tricky, esp. when they're empty besides
         * the current child. Currently, the child will be spread evenly over 
         * the columns/rows
         */
        for(var r=0; r < info.rowspan; r++) {
            this.row_sizes[info.row+r] = Math.max(this.row_sizes[info.row+r], height);
        }
        for(var c=0; c < info.colspan; c++) {
            this.col_sizes[info.column+c] = Math.max(this.col_sizes[info.column+c], width);
        }
    }

    /*
     * resize the container we're laying out to fit all children. Whether
     * we do this should probably be configurable.
     */
    this.totalwidth = this.sumwidth();
    this.totalheight = this.sumheight();

    var parentmax = this.parent.max_size()
    var maxwidth = Math.min(this.totalwidth, parentmax.width) || this.totalwidth;
    var maxheight = Math.min(this.totalheight, parentmax.height) || this.totalheight;

    this.layoutcontrol.css("width", maxwidth + "px");
    this.layoutcontrol.css("height", maxheight + "px");
    this.parent.resize(maxwidth, maxheight);

    for(var i=0; i<this.children.length; i++) {
        var info = this.children[i];
        var ctr = info.control;

        var x = this.sumwidth(0, info.column);
        var y = this.sumheight(0, info.row);
        var w = this.sumwidth(info.column, info.column+info.colspan);
        var h = this.sumheight(info.row, info.row+info.rowspan);



        /*
         * The default behaviour is to center the control
         * in its cell
         */
        ctr.control.css("position", "absolute");
        ctr.control.css("top", (y+(h-info.height)/2) + "px");
        ctr.control.css("left", (x+(w-info.width)/2) + "px");

        if(info.sticky != "center") {
            var N = info.sticky.indexOf('n') != -1;
            var E = info.sticky.indexOf('e') != -1;
            var S = info.sticky.indexOf('s') != -1;
            var W = info.sticky.indexOf('w') != -1;
            var expanded = false;

            // handle expanding
            if(N && S) {
                ctr.control.css("height", h - info.pady*2);
                expanded = true;
            }
            if(E && W) {
                ctr.control.css("width", w - info.padx*2);
                expanded = true;
            }
            //if(expanded && (ctr instanceof Onion.widget.Container)) {
            //    Onion.util.log("Expanding!!!!!", ctr);
            //    ctr.relayout();
            //    Onion.util.log("-------- DONE -------");
            //}
            // handle positioning
            if(N) {
                ctr.control.css("top", (y+info.pady) + "px");
            }
            else if(S) {
                ctr.control.css("top", (y+h-info.height-info.pady) + "px");
            }
            if(W) {
                ctr.control.css("left", (x+info.padx) + "px");
            }
            else if(E) {
                ctr.control.css("left", (x+w-info.width-info.padx) + "px");
            }
        }
    }
}

Onion.layout.register('new', Onion.layout.NewLayout);

