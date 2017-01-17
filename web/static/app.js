(function(ctx) {

    var config = new Backbone.Model();

    var Printers = Backbone.View.extend({
        events: {
            "click .save":"save",
            "click .add":"add"
        },
        render:function() {
            this.setElement($("#options"));

            var $this = this;
            config.url = "/config/"+window.secret;
            config.fetch({
                success:function() {
                    $this.renderPrinters();
                },
                error:function(err) {
                    alert("Error loading printers: " + err)
                }
            });
            return this;
        },
        dirty:function() {
            $(".save").addClass("enabled");
            this.isDirty = true;
        },
        clean:function() {
            $(".save").removeClass("enabled");
            this.isDirty = false;
        },
        add:function() {
            var printers = config.get('printers');
            printers.push({
                isWindows: true,
                connected: true,
                share_name: 'localhost',
                serial: (Math.floor(Math.random() * 100000))+"",
                name: 'New Printer'
            });
            this.dirty();
            this.renderPrinters();
        },
        save:function() {
            var $this = this;
            if(!this.isDirty) return;
            config.save({},{
                success:function() {
                    $this.clean();
                },
                error:function(err) {
                    alert('Failed saving: ' + err);
                }
            })
        },
        renderPrinters:function() {
            var $this = this;
            var printers = new Backbone.Collection(config.get('printers'));

            printers.each(function(p) {
                p.on("change", function() {
                    config.set({printers:printers.toJSON()});
                    $this.dirty();
                });
            });
            printers.on("remove", function() {
                config.set({printers:printers.toJSON()});
                $this.dirty();
            });

            var columns = [
                {name:"name", label:'Name', editable:true, cell: "string"},
                {name:"share_name", label:'Share', editable:true, cell: "string"},
                {name:"type", label:'Type', editable:false, cell: Backgrid.Cell.extend({
                    render: function () {
                        this.$el.empty();
                        if (this.model.get('isWindows')) {
                            this.$el.append($("<span>").text("Windows Shared Printer"));
                        } else {
                            this.$el.append($("<span>").text(this.model.get('manufacturer') + " " + this.model.get('model')));
                        }
                        return this;
                    }
                })},
                {name:"serial", label:'Serial #', editable:false, cell: "string"},
                {name:"connected", label:'Connected', editable:true, cell: "boolean"},
                {name:"identify", label:'', editable:false, cell: Backgrid.Cell.extend({
                    render: function () {
                        var _this = this;
                        this.$el.empty();

                        this.$el.append($("<a>")
                            .addClass("btn btn-sm btn-info pull-right spacer")
                            .html("<i class=\"fa fa-trash-o\"></i>")
                            .attr("title", "Remove printer")
                            .on("click", function(){ printers.remove(_this.model)  }));

                        this.$el.append($("<a>")
                            .addClass("btn btn-xs btn-info pull-right spacer")
                            .text("Print test page")
                            .on("click", function(){ $this.testpage(_this.model) }));

                        this.$el.append($("<a>")
                            .addClass("btn btn-xs btn-info pull-right spacer")
                            .text("Identify")
                            .on("click", function(){ $this.identify(_this.model) }));

                        this.$el.append($("<a>")
                            .addClass("btn btn-xs btn-info pull-right spacer")
                            .text("Open Cash Drawer")
                            .on("click", function(){ $this.cashbox(_this.model) }));

                        return this;
                    }
                })}
            ];
            this.grid = new Backgrid.Grid({
                columns:columns,
                collection:printers
            });

            this.$el.find("#printers").empty().append(this.grid.render().el);
        },
        identify:function(printer) {
            var ps = this.model;
            var url = "/helloprinter/" + printer.get('serial') + "/" + window.secret;
            $.get(url);
        },
        cashbox:function(printer) {
            var ps = this.model;
            var url = "/opencashbox/" + printer.get('serial') + "/" + window.secret;
            $.get(url);
        },
        testpage:function(printer) {
            var ps = this.model;
            var url = "/test/" + printer.get('serial') + "/" + window.secret;
            $.get(url);
        }
    });

    ctx.Printers = Printers;

})(window);