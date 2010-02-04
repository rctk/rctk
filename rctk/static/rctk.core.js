function JWinClient(){
    this.loopinterval = 1000;

    var root = new Root(this);
    root.create();

    this.controls = {0:root};
    this.root = $("#root");
    this.factory = $("#factory");
    this.toplevels = $("#toplevels");
}

JWinClient.prototype.sync = function(data) {
    $.ajax({
        type: "POST",
        url: "sync",
        data: data,
        success: function() {},
        dataTye: "json",
        async: false});
}

JWinClient.prototype.do_work = function(data) {
    jQuery.log("do_work " + data.toSource());

    var control_map = {
        "panel":Panel,
        "button":Button,
        "text":Text,
        "statictext":StaticText,
        "window":Frame,
        "checkbox":CheckBox,
        "radiobutton":RadioButton,
        "dropdown":Dropdown,
        "list":List,
        "date":DateText,
        "password":Password
    }
    var control_class = control_map[data.control];
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
        jQuery.log("Handling timer " + id + ", " + data.milliseconds);
        var callback = hitch(this, "handle_tasks");
        setTimeout(
          function() { 
             $.post("event", {"type":"timer", "id":id}, callback, "json")
           }, data.milliseconds);
        break;
    }

}

JWinClient.prototype.handle_tasks = function (data, status) {
    if(data) {
      for(var i=0; i < data.length; i++) {
        this.do_work(data[i]);
      }
    }
}

JWinClient.prototype.get_work = function() {
    $.post('pop', { 'key':'value' }, hitch(this, "handle_tasks"), "json");
}

JWinClient.prototype.start_work = function () {
    var self = this;
    var h = function(data, status)
        {
            data = data || "{}";
            if(data) {
            }
            //setInterval(hitch(self, 'get_work'), self.loopinterval);
            self.get_work();
        };
    $.post('start', {}, h, "json");
}

function boot_rctk() {
    var client = new JWinClient();
    client.start_work();
}

