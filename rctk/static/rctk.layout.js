/*
 * Layouts manage the positioning of controls in a container. Containers 
 * usually have a default layout that can be overridden before the first
 * control is added. Once a control is added, the layout will be created,
 * no further changes are possible then.
 *
 * This is due to the fact that the div that becomes the layout gets all
 * kinds of styling information set, so changing the layout after creation
 * will result in messed up layouts.
 *
 *
 */

/*
 * Layout is the base Layout. It doesn't implement an actual layout
 * It currently somewhat assumes the layouts are JLayout based (it calls
 * layoutcontrol.layout()), which doesn't work for all layouts. 
 * XXX This needs refactoring!
 *
 * After each modification on JLayout based layouts, the layout() method
 * needs to be called to reorganize the controls.
 */
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
Layout.prototype.append = function(control) {
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
 * A Grid layout can be a single row (columns=1), a single
 * column (rows=1) or an NxM matrix of controls
 */
function GridLayout(jwin, parent, config) {
    Layout.apply(this, arguments);
    if(config) {
        this.config = {
            'type':'grid',
            'columns':config.columns?config.columns:1,
            'rows':config.rows?config.rows:1
        };
    }
}

GridLayout.prototype = new Layout();

function FlexGridLayout(jwin, parent, config) {
    Layout.apply(this, arguments);
    if(config) {
        this.config = {
            'type':'flex-grid',
            'columns':config.columns?config.columns:1,
            'rows':config.rows?config.rows:1
        };
    }
}

FlexGridLayout.prototype = new Layout();

function FlowLayout(jwin, parent, config) {
    Layout.apply(this, arguments);
    if(config) {
        this.config = {
            'type':'flow',
            'columns':config.columns?config.columns:1,
            'rows':config.rows?config.rows:1,
            'alignment':config.alignment!=undefined?config.alignment:'left'
        };
    }
}

FlowLayout.prototype = new Layout();

function BorderLayout(jwin, parent, config) {
    Layout.apply(this, arguments);
    this.config = {
        'type':'border',
    };
}

BorderLayout.prototype = new Layout();

BorderLayout.prototype.append = function(control, data) {
    this.create();

    var direction = data.direction;

    if(this[direction] == undefined) {
        this.layoutcontrol.append("<div id='layoutctr" + control.controlid + "'></div>");
        this[direction] = $("#layoutctr" + control.controlid);
        this[direction].addClass(direction);
        this[direction].addClass("cell");
    }
    // XXX remove old!
    control.control.appendTo(this[direction]);
    control.containingparent = this.parent;
    // this[direction].append(control);
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

 2 fase:
 - first calculate all sizes and try to layout things
 - then let all controls resize themself to the available space.
 */
function IvoLayout(jwin, parent, config) {
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
    this.columns = parseInt(config.columns?config.columns:0);
    this.rows = parseInt(config.rows?config.rows:1);
    this.expand_horizontal = config.expand_horizontal;
    this.expand_vertical = config.expand_vertical;

    // the actually required columns/rows
    this.calculatedcols = 0;
    this.calculatedrows = 0;

}

IvoLayout.prototype = new Layout();

IvoLayout.prototype.create = function() {
    if(this.created) {
        return;
    }
    this.parent.container.append("<div id='layoutmgr" + this.parent.controlid + "'></div>");
    this.layoutcontrol = $("#layoutmgr" + this.parent.controlid);
    this.layoutcontrol.css("position", "relative");
    this.created = true;
}

IvoLayout.prototype.append = function(control, data) {
    this.create();
    this.controls.push(control);
    control.control.appendTo(this.layoutcontrol);
    control.containingparent = this.parent;
    if(data.layout) {
        control.control.data("layout", data.layout);
    }

    // update the number of calculated rows/cols
    if(this.cols) {
        this.calculatedcols = Math.min(this.columns, this.controls.length);
        this.calculatedrows = Math.round(this.controls.length / this.calculatedcols);
    }
    else {
        this.calculatedrows = Math.min(this.rows, this.controls.length);
        this.calculatedcols = Math.round(this.controls.length / this.calculatedcols);
    }
}

IvoLayout.prototype.layout = function() {
    jQuery.log("laying out " + this.parent.controlid);
    this.create(); // create if we haven't done so already
    
    // first layout all children so we know their proper sizes
    for(var i = 0; i < this.controls.length; i++) {
        var ctr = this.controls[i];
        // only relevant for Panels?
        if(ctr.layout && ctr.layout.layout) {
            ctr.layout.layout();
        }
    }
    // find the max height/width for all widgets
    this.maxwidth = 0;
    this.maxheight = 0;

    for(var i = 0; i < this.controls.length; i++) {
        var ctr = this.controls[i];
        var ctrl = ctr.control;
        if(!ctr.scrolling) {
            this.maxwidth = Math.max(this.maxwidth, ctrl.outerWidth());
            this.maxheight = Math.max(this.maxheight, ctrl.outerHeight());
        }
        else {
            jQuery.log(" /// ctrl " + ctr.controlid + " is scrolling");
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


    var parentwidth = this.calculatedcols * this.maxwidth;
    var parentheight = this.calculatedrows * this.maxheight;

    this.layoutcontrol.css("width", parentwidth + "px");
    this.layoutcontrol.css("height", parentheight + "px");
}

IvoLayout.prototype.layout_fase2 = function() {
    // can't think of a better name.
    // everything has been sized. Now go scale everything that needs to be scaled.
    // shouldn't influence the sizes, so no explicit order is required
    // first layout all children so we know their proper sizes
    for(var r = 0; r < this.calculatedrows; r++) {
        for(var c = 0; c < this.calculatedcols; c++) {
            var idx = r*this.calculatedcols+c

            // the grid may contain more cells than there are controls!
            if(idx >= this.controls.length) {
                break;
            }

            var current = this.controls[idx];

            // only panels?
            if(current.layout && current.layout.layout_fase2) {
                current.layout.layout_fase2();
            }
            var selector = current.control;

            var x = r * this.maxheight;
            var y = c * this.maxwidth;

            selector.css("position", "absolute");
            selector.css("top", x + "px");
            selector.css("left", y) + "px";

            var layoutdata = selector.data("layout") || {};
            if(current.expand || (layoutdata && layoutdata.expand_horizontal)) {
                jQuery.log("+++ item " + idx + " expands horizontally");
                jQuery.log("scaling to " + this.maxwidth);
                selector.css("width", this.maxwidth + "px");
            }
            if(current.expand || (layoutdata && layoutdata.expand_vertical)) {
                jQuery.log("+++ item " + idx + " expands vertically");
                jQuery.log("scaling to " + this.maxheight);
                selector.css("height", this.maxheight + "px");
            }
            jQuery.log("item " + idx + " positioned at " + y + ", " + x);
        }
    }

}

/*
 * Stuff to keep in mind:
 *
 * Controls have a default, initial size but may be resized to to layout
 * constriants. This will change their "reported" size.
 * If the layout itself resized, it may do this on wrong control size. This
 * means we need to keep track of the default/initial/minimal size - it might
 * be possible/required to actually shrink controls!
 */
/*
 * fase 1 bepaalt de globale cell size (dus static), fase 2 gaat vervolgens de
 * controls expanden om (indien nodig) de beschikbare size te gebruiken.
 *
 * Voor een niet-static variant moet fase 1 dus aangepast worden en per row/
 * col de size bepaald worden. Er moet:
 * - een registratie per row en per col komen (row_sizes, col_sizes). Initieel
 *   is deze 0 (los van padding)
 * - bij het bepalen van iedere controlsize moet deze rowsize vergroot worden
 *   indien nodig. Maar niet verkleind! Idem voor colsize
 * - generiek werken met row_sizes en col_sizes? Er is geen maxwidth/height met
 *   flexibele cellen!
 * - support voor rowspan/colspan. Cellen expliciet definieren, koppelen
 *   aan controls die er in zitten, incl. dimensions (gebaseerd op row/col
 *   dims?)
 */
function IvoGridLayout(jwin, parent, config) {
    IvoLayout.apply(this, arguments);
    this.row_sizes = [];
    this.col_sizes = [];
}

IvoGridLayout.prototype = new IvoLayout();

IvoGridLayout.layout = function()  { // fase 1

}

