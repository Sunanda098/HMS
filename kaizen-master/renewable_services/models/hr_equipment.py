# coding=utf-8
from openerp import api, fields, models
from datetime import datetime,timedelta
import time
date_format = "%Y-%m-%d"

class HrEquipment(models.Model):
    _inherit = "hr.equipment"

    def change_color_on_kanban(self):
        color = 0
        today = fields.date.today()
        for record in self:
            some_day = fields.Date.from_string(record.alert_date)
            delta = today - some_day
            if record.active and record.alert_days <= delta.days: 
                color = 2
            record.color = color
            
    alert_days = fields.Integer("Alert Before Days", default=45)
    alert_date = fields.Date("Alert Date")
    active = fields.Boolean("Active")
    color = fields.Integer('Color Index', compute="change_color_on_kanban")


    @api.onchange('alert_days','scrap_date')
    def onchange_alert_days(self):
        if self.alert_days and self.scrap_date:
            end = datetime.strptime(self.scrap_date,'%Y-%m-%d') - timedelta(days=self.alert_days)
            self.alert_date = end
    
    
