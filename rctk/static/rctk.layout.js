function Layout(jwin, parent, config) {
    this.jwin = jwin;
    this.parent = parent;
    this.config = config
    this.created = false;
}

Layout.prototype.create = function() {
    if(this.created) {
        return;
    }
    this.parent.container.append("<div id='layoutmgr" + this.parent.controlid + "'></div>");
    this.layoutcontrol = $("#layoutmgr" + this.parent.controlid);
    this.layoutcontrol.layout(this.config);
    this.created = true;
}

// no-cell version
Layout.prototype.append = function(control, options) {
    this.create();
    control.control.appendTo(this.layoutcontrol);
    control.containingparent = this.parent;

    this.layoutcontrol.layout(this.config);
}
Layout.prototype.xappend = function(control) {
    this.create();
    this.layoutcontrol.append("<div id='layoutctr" + control.controlid + "'></div>");
    var ctr = $("#layoutctr" + control.controlid);
    ctr.append(control);
    control.control.appendTo(ctr);
    ctr.addClass("cell");
    this.layoutcontrol.layout(this.config);
}

/*
 * The tabbed layout comes from jqueryui. It's not JLayout based, which is
 * why it currently can't use everything from the JLayout baseclass.
 * XXX needs refactoring!
 */
function TabbedLayout(jwin, parent, config) {
    Layout.apply(this, arguments);
    this.controls = [];
}

TabbedLayout.prototype = new Layout();

TabbedLayout.prototype.create = function() {
    // don't inherit - assumes jlayout's .layout()
    if(this.created) {
        return;
    }
    this.parent.container.append("<div id='layoutmgr" + this.parent.controlid + "'></div>");
    this.layoutcontrol = $("#layoutmgr" + this.parent.controlid);
    this.layoutcontrol.append("<ul id='tabs" + this.parent.controlid + "' />");
    this.tabs = $("#tabs" + this.parent.controlid);
    this.layoutcontrol.tabs();
    this.created = true;
}

/*
 * Perhaps too primitive for tabs - you want to get hold of the tab
 */
TabbedLayout.prototype.append = function(control, data) {
    this.create();

    var title = data.title
    this.layoutcontrol.append("<div id='layoutctr" + control.controlid + "'></div>");
    var ctr = $("#layoutctr" + control.controlid);
    ctr.addClass("tab");
    control.control.appendTo(ctr);
    control.containingparent = this.parent;
    this.layoutcontrol.tabs('add', '#layoutctr' + control.controlid, title);
    this.controls.push(control);

}

TabbedLayout.prototype.layout = function() {
    // first layout all children so we know their proper sizes
    for(var i = 0; i < this.controls.length; i++) {
        var ctr = this.controls[i];
        if(ctr.layout && ctr.layout.layout) {
            ctr.layout.layout();
        }
    }
}

TabbedLayout.prototype.layout_fase2 = function() {
    for(var i = 0; i < this.controls.length; i++) {
        var ctr = this.controls[i];
        if(ctr.layout && ctr.layout.layout_fase2) {
            ctr.layout.layout_fase2();
        }
    }

}

/*
 * Experimental new, full featured and flexible layoutmanager.
 *
 * TODO
 *
 * - allow explicit rows/cols as hint on how to render/size.
 * - allow expanding (h/v) of controls within available space
 * - allow layoutmanager to expand to available space (in stead of just using what it needs)

 2 phases:
 - first calculate all sizes and try to layout things
 - then let all controls resize themself to the available space.
 */
function PowerLayout(jwin, parent, config) {
    Layout.apply(this, arguments);
    config = config?config:{};

    this.controls = [];

    /*
     * Configure gridsize. All we need to know is either
     * the number of columns or the number of rows,
     * the other follows automatically from the number of 
     * added * controls.
     *
     * If neither is defined, default to 1 row
     */
    this.cols = parseInt(config.columns?config.columns:0);
    this.rows = parseInt(config.rows?config.rows:0);
    this.expand_horizontal = config.expand_horizontal;
    this.expand_vertical = config.expand_vertical;

    // the actually required columns/rows
    this.calculatedcols = 0;
    this.calculatedrows = 0;

    // fixed cell size or not
    this.flexcell = config.flex;
    this.row_sizes = [];
    this.col_sizes = [];
}

PowerLayout.prototype = new Layout();

PowerLayout.prototype.create = function() {
    if(this.created) {
        return;
    }
    this.parent.container.append("<div id='layoutmgr" + this.parent.controlid + "'></div>");
    this.layoutcontrol = $("#layoutmgr" + this.parent.controlid);
    this.layoutcontrol.css("position", "relative");
    this.created = true;
}

PowerLayout.prototype.calculate_dimensions = function() {
    if(this.cols && this.rows) {
        // this is how the user wants it. If inproperly configured,
        // may cause weird behaviour
        this.calculatedcols = this.cols;
        this.calculatedrows = this.rows;
    }

    /*
     * derive from either rows/cols and number of controls
     * if we ever support it: use rowspans/colspans for dynamic
     * dimension calculation. Possibly build an actual matrix and
     * assign controls appropriately (possibly even taking (x,y) into
     * account)
     */
    else if(this.cols) {
        this.calculatedcols = Math.min(this.cols, this.controls.length);
        this.calculatedrows = Math.round(this.controls.length / this.calculatedcols);
    }
    else {
        this.calculatedrows = Math.min(Math.max(this.rows, 1), this.controls.length);
        this.calculatedcols = Math.round(this.controls.length / this.calculatedrows);
    }

    jQuery.log("# calculated rows: " + this.calculatedrows);
    jQuery.log("# calculated cols: " + this.calculatedcols);
    this.row_sizes = [];
    this.col_sizes = [];
    for(var i = 0; i < this.calculatedrows; i++) {
        this.row_sizes.push(0);
    }
    for(var i = 0; i < this.calculatedcols; i++) {
        this.col_sizes.push(0);
    }

    this.matrix = new Array(this.calculatedrows);
    for(var i = 0; i < this.calculatedrows; i++) {
        this.matrix[i] = new Array(this.calculatedcols);
    }
    // cells: row, col (default -1)
    // rowspan, colspan: default 1

    for(var i = 0; i < this.controls.length; i++) {
        var c = this.controls[i];
        var row = c.row;
        var col = c.col;
        var rspan = c.rowspan;
        var cspan = c.colspan;
        jQuery.log("Positioning " + i + " row, col, rspan, cspan: " + row + ", " + col + ", " + rspan + ", " + cspan);
        
        if(row == -1 || col == -1) {
            for(var j=0, row=0, col=0; j < this.calculatedrows*this.calculatedcols; 
                j++, row=Math.floor(j/this.calculatedcols), col=j%this.calculatedcols) {
                if(this.matrix[row][col] === undefined) {
                    break;
                }
            }
            // no entry found? Then the matrix is full, no need to continue
            if(j >= this.calculatedrows*this.calculatedcols) {
                return;
            }
        }


        if(row+rspan-1 >= this.calculatedrows || col+cspan-1 >= this.calculatedcols) {
            continue;
        }
        jQuery.log("Found space: " + row + ", " + col);
        for(var rr = row; rr < row+rspan; rr++) {
            for(var cc = col; cc < col+cspan; cc++) {
                //jQuery.log
                this.matrix[rr][cc] = c;
            }
        }
    }
}

PowerLayout.prototype.append = function(control, data) {
    this.create();
    // this is alot of control: control.control.control!
    var controlinfo = {row:-1, col:-1, rowspan:1, colspan:1, control:control, data:data || {}}

    if("row" in data) {
        controlinfo.row = data.row;
    }
    if("col" in data) {
        controlinfo.col = data.col;
    }
    if("rowspan" in data) {
        controlinfo.rowspan = data.rowspan;
    }
    if("colspan" in data) {
        controlinfo.colspan = data.colspan;
    }

    this.controls.push(controlinfo);
    control.control.appendTo(this.layoutcontrol);
    control.containingparent = this.parent;

}

PowerLayout.prototype.sumwidth = function(col) {
    // calculate the offset of a certain column, or the width
    // of the entire matrix (col undefined), taking fixed
    // cell size into account or not
    var s = 0;
    if(col === undefined) {
        col = this.calculatedcols;
    }
    if(!this.flexcell) {
        return this.maxwidth * col;
    }
    for(var i = 0; i < col; i++) {
        s += this.col_sizes[i];
    }
    return s;
}

PowerLayout.prototype.sumheight = function(row) {
    // calculate the offset of a certain row, or the height
    // of the entire matrix (row undefined), taking fixed
    // cell size into account or not
    var s = 0;
    if(row === undefined) {
        row = this.calculatedrows;
    }
    if(!this.flexcell) {
        return this.maxheight * row;
    }
    for(var i = 0; i < row; i++) {
        s += this.row_sizes[i];
    }
    return s;
}

PowerLayout.prototype.layout = function() {
    jQuery.log("laying out " + this.parent.controlid);
    this.create(); // create if we haven't done so already
    this.calculate_dimensions();
    
    // first layout all children so we know their proper sizes
    for(var i = 0; i < this.controls.length; i++) {
        var ctr = this.controls[i].control;
        // only relevant for Panels?
        if(ctr.layout && ctr.layout.layout) {
            ctr.layout.layout();
        }
    }
    // find the max height/width for all widgets
    this.maxwidth = 0;
    this.maxheight = 0;

    for(var r = 0; r < this.calculatedrows; r++) {
        for(var c = 0; c < this.calculatedcols; c++) {
            if(this.matrix[r][c] === undefined) {
                continue;
            }
            var ctrinfo = this.matrix[r][c];
            ctrinfo.laidout = false; // initialize/clear for the actual layout-step
            var ctr = ctrinfo.control;
            var ctrl = ctr.control;
            var w = Math.round(ctrl.outerWidth() / ctrinfo.colspan);
            var h = Math.round(ctrl.outerHeight() / ctrinfo.rowspan);

            //if(!ctr.scrolling) {
                this.maxwidth = Math.max(this.maxwidth, w);
                this.maxheight = Math.max(this.maxheight, h);

                this.row_sizes[r] = Math.max(this.row_sizes[r], h);
                this.col_sizes[c] = Math.max(this.col_sizes[c], w);
            //}
            //else {
            //    jQuery.log(" /// ctrl " + ctr.controlid + " is scrolling");
            //}
        }
    }
    jQuery.log("max width, height " + this.maxwidth + ", " + this.maxheight);


    // check if the layout need to expand to fit the parent
    if(this.expand_horizontal) {
        var exp_width = this.parent.containingparent.container.width() / this.calculatedcols;
        if(exp_width > this.maxwidth) {
            this.maxwidth = Math.round(exp_width);
        }
    }
    if(this.expand_vertical) {
        var exp_height = this.parent.containingparent.container.height() / this.calculatedrows;
        if(exp_height > this.maxheight) {
            this.maxheight = Math.round(exp_height);
        }
    }


    var parentwidth = this.sumwidth();
    var parentheight = this.sumheight();

    this.layoutcontrol.css("width", parentwidth + "px");
    this.layoutcontrol.css("height", parentheight + "px");
    jQuery.log("Scaling parent to " + parentwidth + ", " + parentheight);
}

PowerLayout.prototype.layout_fase2 = function() {
    // can't think of a better name.
    // everything has been sized. Now go scale everything that needs to be scaled.
    // shouldn't influence the sizes, so no explicit order is required
    // first layout all children so we know their proper sizes
    for(var r = 0; r < this.calculatedrows; r++) {
        for(var c = 0; c < this.calculatedcols; c++) {
            if(this.matrix[r][c] === undefined) {
                continue;
            }
            var ctrinfo = this.matrix[r][c];

            /*
             * We're visiting each cell, which means visiting controls
             * that span multiple rows/columns more than once. Don't
             * reposition them!
             */
            if(ctrinfo.laidout) {
                continue;
            }
            ctrinfo.laidout = true;

            var current = ctrinfo.control;

            // only panels?
            if(current.layout && current.layout.layout_fase2) {
                current.layout.layout_fase2();
            }
            var selector = current.control;

            var x = this.sumwidth(c);
            var y = this.sumheight(r);

            selector.css("position", "absolute");
            selector.css("top", y + "px");
            selector.css("left", x + "px");

            var layoutdata = ctrinfo.data || {};
            var w = this.col_sizes[c];
            var h = this.row_sizes[r];
            if(!this.flexcell) {
                w = this.maxwidth;
                h = this.maxheight;
            }
            jQuery.log("positioning: w, h " + w + "," + h);

            if(current.expand || (layoutdata && layoutdata.expand_horizontal)) {
                // XXX Keep original dimensions!
                jQuery.log("+++ item (" + r + ", " + c + ") expands horizontally");
                jQuery.log("scaling to " + w);
                selector.css("width", w + "px");
            }
            if(current.expand || (layoutdata && layoutdata.expand_vertical)) {
                jQuery.log("+++ item (" + r + ", " + c + ") expands vertically");
                jQuery.log("scaling to " + h);
                selector.css("height", h + "px");
            }
            jQuery.log("item (" + r + ", " + c + ") positioned at " + x + ", " + y);
        }
    }

}

/*
 * Stuff to keep in mind:
 *
 * Controls have a default, initial size but may be resized to to layout
 * constraints. This will change their "reported" size.
 * If the layout itself resized, it may do this on wrong control size. This
 * means we need to keep track of the default/initial/minimal size - it might
 * be possible/required to actually shrink controls!
 *
 * Calculate appropriate sizes based on the rowspan/colspan (!)
 */
