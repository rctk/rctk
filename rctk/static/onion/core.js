
Onion.core.JWinClient = function() {
    this.poll = false; // poll for new tasks
    this.interval = 1000; // if so, how often
    this.debug = false;
    this.crashed = false;

    var root = new Onion.widget.Root(this);
    root.create();

    this.controls = {0:root};
    // references to the actual div's
    this.root = $("#root");
    this.factory = $("#factory");
    this.toplevels = $("#toplevels");
    this.queue = []
    this.busy = []
}

Onion.core.JWinClient.prototype.do_work = function(data) {
    //Onion.util.log("do_work ", data);
    
    var control_class = Onion.widget.map(data.control);
    var parent = this.controls[data.parentid];
    var id = data.id;
                       
    if(this.crashed) {
        return;
    }

    if('crash' in data && data.crash) {
        if(this.debug) {
            this.root.append('<div id="system" class="jqmWindow" style="width: 600px; height: 600px"><b>The application ' + data.application + ' has crashed. </b><br><p>Click <a href="/">here</a> to restart</p><br><div style="overflow: auto; width: 600px; height: 500px;">' + data.traceback + '</div></div>');
        }
        else {
            this.root.append('<div id="system" class="jqmWindow" style="width: 600px; height: 300px"><b>The application ' + data.application + ' has crashed. </b><br><p>Click <a href="/">here</a> to restart</p></div>');

        }
        $("#system").jqm({'modal':true});
        $("#system").jqmShow();
        this.crashed = true;
        return;
    }
    switch(data.action) {
    case "append":
        var container = this.controls[data.id];
        var child = this.controls[data.child];
        container.append(child, data);
        break;
    case "remove":
        var container = this.controls[data.id];
        var child = this.controls[data.child];
        container.remove(child, data);
        break;
    case "show":
        // Can this be removed? Doesn't seem to be a show task anymore.
        // show all - hack!
        for(var i = 0; i < this.controls.length; i++) {
            this.controls[i].css("display", "inline");
        }
        break;
    case "create":
        // TODO?: if this fails 'the other side' is not informed!
        if(control_class) {
           c = new control_class(this, parent, id);
           c.create(data);
           this.controls[id] = c;
        }
        break;
    case "destroy":
        var control = this.controls[id];
        control.destroy();
        this.controls[id] = null
        break;
    case "update":
        // update a control. Rename to sync?
        var control = this.controls[id];
        control.update(data.update);
        break;
    case "handler":
        var control = this.controls[id];
        control["handle_"+data.type] = true;
        break;
    case "layout":
        var container = this.controls[id];
        container.setLayout(data.type, data.config);
        break;
    case "relayout":
        var container = this.controls[id];
        container.relayout();
        break;
    case "timer":
        Onion.util.log("Handling timer " + id + ", " + data.milliseconds);
        var callback = Onion.util.hitch(this, "handle_tasks");
        var self=this;
        setTimeout(
          function() { 
             self.add_task("event", "timer", id);
             self.flush();
           }, data.milliseconds);
        break;
    }

}

Onion.core.JWinClient.prototype.handle_tasks = function (data, status) {
    if(data) {
      for(var i=0; i < data.length; i++) {
        this.do_work(data[i]);
      }
    }

    /*
     * time to enable busy controls again
     */
    for(var i in this.busy) {
        Onion.log("Control no longer busy", c);
        this.busy[i].busy = false;
    }
    this.busy = [];

    this.flush();

    if(this.poll) {
        setInterval(Onion.util.hitch(this, 'get_work'), this.interval);
    }
}

Onion.core.JWinClient.prototype.get_work = function() {
    $.post('pop', { 'key':'value' }, Onion.util.hitch(this, "handle_tasks"), "json");
}

Onion.core.JWinClient.prototype.start_work = function () {
    var self = this;
    var h = function(data, status) {
        data = data || "{}";
        if('config' in data) {
            var config = data.config;

            if('poll' in config) {
                self.poll = config.poll;
            }
            if('interval' in config) {
                self.interval = config.interval;
            }
            if('debug' in config) {
                self.debug = config.debug;
            }
        }
        self.get_work();
    };
    $.post('start', {}, h, "json");
}

Onion.core.JWinClient.prototype.flush = function() {
    if(this.queue.length > 0) {
        $.post("task", {'queue':JSON.stringify(this.queue)}, Onion.util.hitch(this, "handle_tasks"), "json");
        this.queue = []
    }
}

Onion.core.JWinClient.prototype.add_task = function(method, type, id, data) {
    this.queue.push({'method':method, 'type':type, 'id':id, 'data':data});
}

Onion.core.JWinClient.prototype.register_busy = function(control) {
    /*
     * A busy control cannot handle new events until the current
     * handler has finished handling. This means a control is marked
     * busy once it's clicked and marked unbusy once the (optional)
     * tasks generated by its handler have been handled.
     */
    control.busy = true;
    this.busy.push(control);
}
