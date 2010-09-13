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
Onion.layout.Power = function(jwin, parent, config) {
    Onion.layout.Layout.apply(this, arguments);
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

Onion.layout.Power.prototype = new Onion.layout.Layout();

Onion.layout.Power.prototype.create = function() {
    if(this.created) {
        return;
    }
    this.parent.container.append("<div id='layoutmgr" + this.parent.controlid + "'></div>");
    this.layoutcontrol = $("#layoutmgr" + this.parent.controlid);
    this.layoutcontrol.css("position", "relative");
    this.created = true;
}

Onion.layout.Power.prototype.calculate_dimensions = function() {
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
        this.calculatedrows = Math.round(this.controls.length / Math.max(this.calculatedcols, 1));
    }
    else {
        this.calculatedrows = Math.min(Math.max(this.rows, 1), this.controls.length);
        this.calculatedcols = Math.round(this.controls.length / Math.max(this.calculatedrows, 1));
    }
    
    //Onion.util.log("# calculated rows: " + this.calculatedrows);
    //Onion.util.log("# calculated cols: " + this.calculatedcols);
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
        //Onion.util.log("Positioning " + i + " row, col, rspan, cspan: " + row + ", " + col + ", " + rspan + ", " + cspan);
        
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
        //jQuery.log("Found space: " + row + ", " + col);
        for(var rr = row; rr < row+rspan; rr++) {
            for(var cc = col; cc < col+cspan; cc++) {
                //jQuery.log
                this.matrix[rr][cc] = c;
            }
        }
    }
}

Onion.layout.Power.prototype.append = function(control, data) {
    this.create();
    // this is a lot of control: control.control.control!
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

Onion.layout.Power.prototype.remove = function(control, data) {
    for (var i = 0; i < this.controls.length; i++) {
        if (this.controls[i].control == control) {
            this.controls.splice(i, 1);
        }
    }
    var factory = $("#factory");
    control.control.appendTo(factory);
    control.containingparent = null;
}

Onion.layout.Power.prototype.sumwidth = function(start, end) {
    // calculate the offset of a certain column, or the width
    // of the entire matrix (col undefined), taking fixed
    // cell size into account or not
    if(start === undefined) {
        start = 0;
    }
    if(end === undefined) {
        end = this.calculatedcols;
    }
    if(!this.flexcell) {
        return this.maxwidth * (end-start);
    }
    var s = 0;
    for(var i = start; i < end; i++) {
        s += this.col_sizes[i];
    }
    return s;
}

Onion.layout.Power.prototype.sumheight = function(start, end) {
    // calculate the offset of a certain row, or the height
    // of the entire matrix (row undefined), taking fixed
    // cell size into account or not
    var s = 0;
    if(start === undefined) {
        start = 0;
    }
    if(end === undefined) {
        end = this.calculatedrows;
    }
    if(!this.flexcell) {
        return this.maxheight * (end-start);
    }
    for(var i = start; i < end; i++) {
        s += this.row_sizes[i];
    }
    return s;
}

Onion.layout.Power.prototype.layout = function() {
    //jQuery.log("laying out " + this.parent.controlid);
    this.create(); // create if we haven't done so already
    this.calculate_dimensions();
    
    // first layout all children so we know their proper sizes
    for(var i = 0; i < this.controls.length; i++) {
        var ctr = this.controls[i].control;
        if(ctr instanceof Onion.widget.Container) {
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
            var w = Math.round(ctrl.outerWidth(true) / ctrinfo.colspan);
            var h = Math.round(ctrl.outerHeight(true) / ctrinfo.rowspan);

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
    //jQuery.log("max width, height " + this.maxwidth + ", " + this.maxheight);


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
    //jQuery.log("Scaling parent to " + parentwidth + ", " + parentheight);
}

Onion.layout.Power.prototype.layout_fase2 = function() {
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

            if(current instanceof Onion.widget.Container) {
                current.layout.layout_fase2();
                current.layout_updated();
            }
            var selector = current.control;

            var x = this.sumwidth(0, c);
            var y = this.sumheight(0, r);

            selector.css("position", "absolute");
            selector.css("top", y + "px");
            selector.css("left", x + "px");

            var layoutdata = ctrinfo.data || {};
            // get the dimensions of the cell(s) the control spans.
            var w = this.sumwidth(c, c+ctrinfo.colspan); 
            var h = this.sumheight(r, r+ctrinfo.rowspan);
            //jQuery.log("positioning: w, h " + w + "," + h);

            if(current.expand || (layoutdata && layoutdata.expand_horizontal)) {
                // XXX Keep original dimensions!
                //jQuery.log("+++ item (" + r + ", " + c + ") expands horizontally");
                //jQuery.log("scaling to " + w);
                selector.css("width", w + "px");
            }
            if(current.expand || (layoutdata && layoutdata.expand_vertical)) {
                //jQuery.log("+++ item (" + r + ", " + c + ") expands vertically");
                //jQuery.log("scaling to " + h);
                selector.css("height", h + "px");
            }
            //jQuery.log("item (" + r + ", " + c + ") positioned at " + x + ", " + y);
        }
    }

}

Onion.layout.register('power', Onion.layout.Power);

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
