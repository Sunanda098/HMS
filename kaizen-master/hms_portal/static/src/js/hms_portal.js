
odoo.define('hms_portal', function(require) {
    'use strict';
    require('website.website');

    $('.slotchanged').on('change', "select[name='slot_date']", function () {
        var $select = $("select[name='slot_lines']");
        $select.find("option:not(:first)").hide();
        var nb = $select.find("option[data-slot-id="+($(this).val() || 0)+"]").show().size();
        $select.parent().toggle(nb>1);
    });
    $('.slotchanged').find("select[name='slot_date']").change();

   
});
