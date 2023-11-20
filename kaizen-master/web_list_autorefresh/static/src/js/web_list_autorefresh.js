odoo.define('web_list_autorefresh.list_autorefresh', function (require) {
"use strict";

var core = require('web.core');
var common = require('web.form_common');
var Model = require('web.Model');
var time = require('web.time');
var ListView = require('web.ListView');
var session = require('web.session');

var _t = core._t;

var data = require('web.data');

    ListView.include({
      init: function(parent, dataset, view_id, options) {
         var self = this;
         parent.autorefresh = 1
         this._super.apply(this, arguments);
         this.background_colors = null;
         if(options.action && options.action.auto_refresh && parent.autorefresh > 0){
            self.refresh_interval = setInterval(_.bind(function(){
                var controller = this.ViewManager.active_view.controller;
                if(this.$el[0].clientWidth != 0){
                    controller.reload();
                    this.reload();
               }
            }, self), parent.autorefresh*150000);
         }
       },
       destroy : function() {
          this._super.apply(this, arguments);
          if(this.refresh_interval){
             clearInterval(this.refresh_interval);
          }
       },
       load_list: function(data) {
            this._super(data);
            if (this.fields_view.arch.attrs.background_colors) {
                this.background_colors = _(this.fields_view.arch.attrs.background_colors.split(';')).chain()
                    .compact()
                    .map(function(color_pair) {
                        var pair = color_pair.split(':'),
                            color = pair[0],
                            expr = pair[1];
                        return [color, py.parse(py.tokenize(expr)), expr];
                    }).value();
            }
        },
       style_for: function (record, td=false) {
            var len;
            var context = _.extend({}, record.attributes, {
                uid: session.uid,
                current_date: moment().format('YYYY-MM-DD')
                // TODO: time, datetime, relativedelta
            });
            var i;
            var pair;
            var expression;
            var style = this._super.apply(this, arguments);
            if (td == 'ranking' && this.background_colors){
                return style += 'background-color: yellow ;color: black';
            }
            if (td && this.background_colors){
                for(i=0, len=this.background_colors.length; i<len; ++i) {
                    pair = this.background_colors[i];
                    var color = pair[0];
                    expression = pair[1];
                    if (py.PY_isTrue(py.evaluate(expression, context))) {
                        if (color == 'yellow'){
                            return style += 'background-color: yellow';'color: black';
                        }
                        return style += 'background-color: ' + color + ';'+'color: white';
                    }
                }
            }
            return style;
       },
    });

});

