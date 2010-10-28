Onion.layout.NewLayout = function(jwin, parent, config) {
    Onion.layout.Layout.apply(this, arguments);
    config = config?config:{};
    // don't care right now, wait for the calculated data when
    // layout() is called
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

// move basic append, remove to base

Onion.layout.NewLayout.prototype.append = function(control, data) {
    this.create();
    control.control.appendTo(this.layoutcontrol);
}

Onion.layout.NewLayout.prototype.remove = function(control, data) {
    control.control.appendTo($("#factory"));
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

Onion.layout.NewLayout.prototype.layout = function(config) {
    /*
     * This method can be invoked in two ways:
     * explicit, as a result from a layout() operation in python. In this
     *           case, we get a full grid configuration.
     * implicit, as a result of a recursive layout() step from our parent,
     *           in which case we already should have a config, and no new
     *           config will be available.
     */
    if(config !== undefined) {
        Onion.util.log("NEWLAYOUT: relayout setting config", config);
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

        for(var i=0; i < config.cells.length; i++) {
            var c = config.cells[i];
            var control = $("#ctrl" + c.controlid);
            var info = {control:control, row:c.row, column:c.column, rowspan:c.rowspan, colspan:c.colspan};
            info.padx = 'padx' in c? c.padx: this.padx;
            info.ipadx = 'ipadx' in c? c.ipadx: this.ipadx;
            info.pady = 'pady' in c? c.pady: this.pady;
            info.ipady = 'ipady' in c? c.ipady: this.ipady;
            info.static = 'static' in c? c.static: this.static;
            info.sticky = 'sticky' in c? c.sticky.toLowerCase(): this.sticky;

            Onion.util.log("NEWLAYOUT: info", info);
            this.children.push(info);
        }
    }
    else {
        Onion.util.log("NEWLAYOUT: relayout cascade");
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


    /*
     * Find the sizes of all children, possibly after recursively
     * laying them out if the child is a container with layout itself
     */
    for(var i=0; i<this.children.length; i++) {
        var info = this.children[i];
        var ctr = info.control;

        if(ctr instanceof Onion.widget.Container) {
            Onion.util.log("NEWLAYOUT: Recursive layout()", ctr);
            ctr.layout.layout();
        }
        /*
         * Find the size of the control, but spread it over the rows/
         * columns it has allocated.
         */
        info.width = ctr.outerWidth(true);
        info.height = ctr.outerHeight(true);

        /*
         * Calculate how big the cell should be, taking padding and spanning into account
         */
        var width = Math.round(info.width / info.colspan) + info.padx*2;
        var height = Math.round(info.height / info.rowspan) + info.pady*2;

        Onion.util.log("NEWLAYOUT: size: " + width + ", " + height);

        /* 
         * Keep track of max width height, overall and per row/column
         */
        this.maxcellwidth = Math.max(this.maxcellwidth, width);
        this.maxcellheight = Math.max(this.maxcellheight, height);

        /*
         * colspans/rowspans are a bit tricky, esp. when they're empty besides
         * the current child. Currently, the child will be spread evenly over the
         * columns/rows
         */
        for(var r=0; r < info.rowspan; r++) {
            this.row_sizes[info.row+r] = Math.max(this.row_sizes[info.row+r], height);
        }
        for(var c=0; c < info.colspan; c++) {
            this.col_sizes[info.column+c] = Math.max(this.col_sizes[info.column+c], width);
        }
    }
    Onion.util.log("NEWLAYOUT: rows", this.row_sizes);
    Onion.util.log("NEWLAYOUT: cols", this.col_sizes);

    /*
     * resize the container we're laying out to fit all children. Whether
     * we do this should probably be configurable.
     */
    this.totalwidth = this.sumwidth();
    this.totalheight = this.sumheight();
    Onion.util.log("NEWLAYOUT container size: " + this.totalwidth + ", " + this.totalheight);
    this.layoutcontrol.css("width", this.totalwidth + "px");
    this.layoutcontrol.css("height", this.totalheight + "px");
    this.parent.resize(this.totalwidth, this.totalheight);
    // resize this.layoutcontrol, if we still need it/have it.
}

Onion.layout.NewLayout.prototype.layout_fase2 = function() {
    Onion.util.log("NEWLAYOUT: New layout 2");
    for(var i=0; i<this.children.length; i++) {
        var info = this.children[i];
        var ctr = info.control;
        if(ctr instanceof Onion.widget.Container) {
            Onion.util.log("NEWLAYOUT: Recursive layout_fase2()", ctr);
            ctr.layout.layout_fase2();
        }

        var x = this.sumwidth(0, info.column);
        var y = this.sumheight(0, info.row);
        var w = this.sumwidth(info.column, info.column+info.colspan);
        var h = this.sumheight(info.row, info.row+info.rowspan);


        /*
         * The default behaviour is to center the control
         * in its cell
         */
        ctr.css("position", "absolute");
        ctr.css("top", (y+(h-info.height)/2) + "px");
        ctr.css("left", (x+(w-info.width)/2) + "px");

        if(info.sticky != "center") {
            var N = info.sticky.indexOf('n') != -1;
            var E = info.sticky.indexOf('e') != -1;
            var S = info.sticky.indexOf('s') != -1;
            var W = info.sticky.indexOf('w') != -1;
            // handle expanding
            if(N && S) {
                ctr.css("height", h - info.pady*2);
            }
            if(E && W) {
                ctr.css("width", w - info.padx*2);
            }
            // handle positioning
            if(N) {
                ctr.css("top", (y+info.pady) + "px");
            }
            else if(S) {
                ctr.css("top", (y+h-info.height-info.pady) + "px");
            }
            if(W) {
                ctr.css("left", (x+info.padx) + "px");
            }
            else if(E) {
                ctr.css("left", (x+w-info.width-info.padx) + "px");
            }
        }
    }
}

Onion.layout.register('new', Onion.layout.NewLayout);

