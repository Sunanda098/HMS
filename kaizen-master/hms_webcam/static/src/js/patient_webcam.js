
openerp.hms_webcam = function(instance) {
    
    // client action hook
    instance.web.client_actions.add("photo.action", "instance.hms_webcam.action");
    instance.hms_webcam.action = instance.web.Widget.extend({
           
        template: 'photo_action',
           
        events: {
            'click .oe_patient_webcam_close a': 'window_close'
        },
            
        window_close: function() {
            var self = this;
            self.getParent().history_back();
            self.destroy();
        },
            
        init: function(parent, action) {
            this._super(parent, action);
            this.patient_id = action.params.patient_id;
        },
        
        start: function() {
            this._super();
            var pos = 0;
            var ctx = null;
            var cam = null;
            var image = null;
            var patient_id = this.patient_id;
            this.$el.find('#webcam').webcam({
                width: 320,
                height: 240,
                mode: "callback",
                swffile: "/hms_webcam/static/jscam_canvas_only.swf",
                onTick: function() {},
                    
                onSave: function(data) {
                    var col = data.split(";");
                    var canvas = document.getElementById("canvas");
                    var ctx = canvas.getContext("2d");
                    var img = image;
                    if (img == null && ctx) {
                        ctx.clearRect(0, 0, 320, 240);
                        img = ctx.getImageData(0, 0, 320, 240);
                    }
                    for(var i = 0; i < 320; i++) {
                        var tmp = parseInt(col[i]);
                        img.data[pos + 0] = (tmp >> 16) & 0xff;
                        img.data[pos + 1] = (tmp >> 8) & 0xff;
                        img.data[pos + 2] = tmp & 0xff;
                        img.data[pos + 3] = 0xff;
                        pos+= 4;
                    }
                    image = img
                    
                    if (pos >= 4 * 320 * 240) {
                        ctx.putImageData(img, 0, 0);
                        vals = {'image': canvas.toDataURL("image/png").replace(/^data:image\/(png|jpg);base64,/, "")};
                        model = new instance.web.Model("hms.patient")
                        if (patient_id)
                            model.call('write', [patient_id, vals]).then(null);
                        pos = 0;
                    }
                },
                
                onCapture: function() {
                    webcam.save();
                },
                
                debug: function (type, string) {
                    jQuery("#status").html(type + ": " + string);
                },
            
                onLoad: function () {
            
                    var cams = webcam.getCameraList();
                    for(var i in cams) {
                        jQuery("#cams").append("<li>" + cams[i] + "</li>");
                    }
                },
            });
        },
    });
};
