from openerp import api, fields, models
from openerp.tools.translate import _
from datetime import datetime,timedelta

class RevenueSharing(models.Model):
    _name = "revenue.sharing"
    _rec_name = 'product_id'

    product_id = fields.Many2one('product.product', string="Product/Service")
    type = fields.Selection([('opd','OPD'),('ipd','IPD'),('both','BOTH')], string="Service Type")
    base_price = fields.Float(string="Base Charges")
    discount_type = fields.Selection([('hospital','Hospital Only'),('hos_doc','Hos + Doc'),('doctor','Doctor Only')], string='Discount Type')
    
    attend_doctor_price = fields.Float('Attending Doctor Charges')
    attend_doctor_disc = fields.Float('Attending Doctor (%)')       
    treat_doctor_price = fields.Float('Treating Doctor Charges')
    treat_doctor_disc = fields.Float('Treating Doctor (%)')       
    ksga_price_doc = fields.Float('KSGA Share for Doctor.')    
    hospital_share_doc = fields.Float('Hospital Share for Doctor')
    hospital_share_special = fields.Float('Hospital Share for Specialist')
    ksga_share_special = fields.Float('KSGA Share for Specialist')


    hospital_share_out = fields.Float('Hospital Share for Outsider')
    hospital_share_out_disc = fields.Float('Hospital Share for Outsider Disc.(%)')
    ksga_price_out = fields.Float('KSGA Share for Outsider')
    ksga_price_out_disc = fields.Float('KSGA Share for Outsider Disc.(%)')
    attend_outside_price = fields.Float('Attending Outside Charges')
    attend_outside_disc = fields.Float('Attending Outside Disc.(%)')
    treat_outside_price = fields.Float('Treating Outside Charges')
    treat_outside_disc = fields.Float('Treating Outside Disc.(%)')


    hospital_share_std = fields.Float('Hospital Share for Std')
    hospital_share_std_disc = fields.Float('Hospital Share for Std. Disc.(%)')
    ksga_price_std = fields.Float('KSGA Share for std.')
    ksga_price_std_disc = fields.Float('KSGA Share for std. Disc.(%)')
    attend_std_price = fields.Float('Attending Standard Charges')
    attend_std_disc = fields.Float('Attending Standard Disc.(%)')
    treat_std_price = fields.Float('Treating Standard Charges')
    treat_std_disc = fields.Float('Treating Standard Disc.(%)')


    @api.onchange('product_id')
    def onchange_product_id(self):
        self.base_price = self.product_id.list_price
    
    @api.onchange('attend_outside_disc')
    def onchange_attend_outside_disc(self):
        if self.attend_outside_disc >0:
            self.attend_outside_price = int((self.attend_outside_disc * self.base_price) / 100)
    
    @api.onchange('attend_std_disc')
    def onchange_attend_std_disc(self):
        if self.attend_std_disc >0:
            self.attend_std_price = int((self.attend_std_disc * self.base_price) / 100)
    
    @api.onchange('treat_outside_disc')
    def onchange_treat_outside_disc(self):
        if self.treat_outside_disc >0:
            self.treat_outside_price = int((self.treat_outside_disc * self.base_price) / 100)
    
    @api.onchange('treat_std_disc')
    def onchange_treat_std_disc(self):
        if self.treat_std_disc >0:
            self.treat_std_price = int((self.treat_std_disc * self.base_price) / 100)

    @api.onchange('ksga_price_out_disc')
    def onchange_ksga_price_out_disc(self):
        if self.ksga_price_out_disc >0:
            self.ksga_price_out = int((self.ksga_price_out_disc * self.base_price) / 100)

    @api.onchange('ksga_price_std_disc')
    def onchange_ksga_price_std_disc(self):
        if self.ksga_price_std_disc >0:
            self.ksga_price_std = int((self.ksga_price_std_disc * self.base_price) / 100)

    @api.onchange('hospital_share_std_disc')
    def onchange_hospital_share_std_disc(self):
        if self.hospital_share_std_disc >0:
            self.hospital_share_std = int((self.hospital_share_std_disc * self.base_price) / 100)

    @api.onchange('hospital_share_out_disc')
    def onchange_hospital_share_out_disc(self):
        if self.hospital_share_out_disc >0:
            self.hospital_share_out = int((self.hospital_share_out_disc * self.base_price) / 100)



class RevenueSharingReport(models.TransientModel):
    _name = 'revenue.sharing.report'

    date_from = fields.Date(string='Start Date', default=fields.Date.context_today)
    date_to = fields.Date(string='End Date', default=fields.Date.context_today)
    #department_id = fields.Many2one('hospital.department', ondelete='restrict', string='Department')
    type = fields.Selection([('group','By Service Group'),('service', 'By Service'),('person', 'By Person')], string="Report Type", default='group')
    service_group = fields.Selection([('pathology', 'Pathology'),
                                      ('radiology', 'Radiology'),
                                      ('manometry', 'Manometry'),
                                      ('endoscopy', 'Endoscopy'),], 
                                      string="Service Group")
    product_id = fields.Many2one('product.product', string="Select Service")
    person_id = fields.Many2one('res.partner', string="Person")

    @api.multi
    def print_report(self, data):
        return self.env['report'].get_action(self, 'hms_invoice.revenue_sharing_report_template')
    
    @api.multi
    def get_revenue_sharing_by_service(self):
        return self.env['account.invoice.discount'].search([('product_id','=',self.product_id.id),('date','>=',self.date_from),('date','<=',self.date_to)])
    
    @api.multi
    def get_revenue_sharing_by_person(self):
        return self.env['account.invoice.discount'].search([('by_whom','=',self.person_id.id),('date','>=',self.date_from),('date','<=',self.date_to)])

    @api.multi
    def get_groups(self):
        group_ids = []
        discount_ids = self.env['account.invoice.discount'].search([('product_id.hospital_product_type','=',self.service_group),('date','>=',self.date_from),('date','<=',self.date_to)])
        for discount in discount_ids:
            if discount.product_id not in group_ids:
                group_ids.append(discount.product_id)
        return group_ids

    @api.multi
    def get_revenue_sharing_by_group(self, group_id):
        revenue_ids = self.env['account.invoice.discount'].search([('product_id','=',group_id.id),('date','>=',self.date_from),('date','<=',self.date_to)])
        return revenue_ids
