
Onion.core.JWinClient = function() {
    this.poll = false; // poll for new tasks
    this.interval = 1000; // if so, how often

    var root = new Onion.widget.Root(this);
    root.create();

    this.controls = {0:root};
    // references to the actual div's
    this.root = $("#root");
    this.factory = $("#factory");
    this.toplevels = $("#toplevels");
    this.queue = []
}

Onion.core.JWinClient.prototype.sync = function(data) {
    $.ajax({
        type: "POST",
        url: "sync",
        data: data,
        success: function() {},
        dataTye: "json",
        async: false});
}

Onion.core.JWinClient.prototype.do_work = function(data) {
    Onion.util.log("do_work ", data);
    
    var control_class = Onion.widget.map(data.control);
    var parent = this.controls[data.parentid];
    var id = data.id;
                       
    switch(data.action) {
    case "append":
        var container = this.controls[data.id];
        var child = this.controls[data.child];
        container.append(child, data);
        break;
    case "show":
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
                this.poll = config.poll;
            }
            if('interval' in config) {
                this.interval = config.interval;
            }
        }
        self.get_work();
    };
    $.post('start', {}, h, "json");
}

Onion.core.JWinClient.prototype.flush = function() {
    if(this.queue.length > 0) {
        Onion.util.log("tasks: ", $.param(this.queue));
        $.post("task", {'queue':JSON.stringify(this.queue)}, Onion.util.hitch(this, "handle_tasks"), "json");
        this.queue = []
    }
}

Onion.core.JWinClient.prototype.add_task = function(method, type, id) {
    this.queue.push({'method':method, 'type':type, 'id':id});
}
