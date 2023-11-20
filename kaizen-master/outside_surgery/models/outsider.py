from openerp import api, fields, models
from openerp.tools.translate import _


class SurgeryOutside(models.Model):
    _name = 'surgery.outside'

#onchange Block as it was hard code for shah hospital -14 Feb
    # @api.model
    # def _get_default_dr(self):
    #     dr_id = self.env['hms.physician'].search([('name','ilike','Dr. Manish Shah')],limit=1)
    #     if dr_id:
    #         return dr_id[0]
    #     else:
    #         return False

    @api.model
    def _get_surgery(self):
        return self.env.ref("hms_hospitalization.outside_surgery_product_1")

    @api.multi
    def _get_total(self):
        for record in self:
            record.total_amount = record.received_amount + record.tds_amount

    name = fields.Char(string='code', copy=False)
    product_id = fields.Many2one('product.product', ondelete='cascade', string='Surgery', required=1, default=_get_surgery)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ], default='draft', string='Status')
    partner_id = fields.Many2one('res.partner', string='Name')
    towards = fields.Char(string='Towards')
    primary_physician = fields.Many2one ('hms.physician', ondelete="restrict", string='Surgeon')
    date_surgery = fields.Date(string='Date', default=fields.Date.context_today)
    tds_amount = fields.Float(string='TDS Amount')
    received_amount = fields.Float(string='Received Amount')
    total_amount = fields.Float(compute='_get_total', string="Total Amount")
    bank_name = fields.Char(string='Bank Name')
    cheque_no = fields.Char(string='Cheque No.')
    cheque_date = fields.Date(string='Cheque Date', default=fields.Date.context_today)
    invoice_id = fields.Many2one('account.invoice','Account')
    report_type = fields.Selection([("pharmacy", "Pharmacy Invoice"),
                                    ("consult", "Consultation Invoice"),
                                    ("register","Registration Invoice"),
                                    ("radiology", "Radiology Invoice"),
                                    ("physiotherapy","Physiotherapy Invoice"),
                                    ("lab", "Laboratory Invoice"),
                                    ("procedure", "Procedure Invoice"),
                                    ("hospital", "Hospital Invoice"),
                                    ('claim', 'Claim'), ('inpatient', 'Inpatient'),
                                    ('outside','Outside Surgery')], string="Invoice Type", default='outside')
    
    
    @api.model
    def create(self, values):
        if values.get('name', 'Outside Surgery Receipt#') == 'Outside Surgery Receipt#':
            values['name'] = self.env['ir.sequence'].next_by_code('surgery.outside') or 'Outside Surgery Receipt#'
        return super(SurgeryOutside, self).create(values)

    @api.onchange('received_amount','tds_amount')
    def onchange_amount(self):
        if self.received_amount or self.tds_amount:
            self.total_amount = self.received_amount + self.tds_amount

    @api.multi
    def action_done(self):
        self.state = 'done'


    @api.multi
    def action_create_invoice(self):
        imd = self.env['ir.model.data']
        action = imd.xmlid_to_object('account.action_invoice_tree1')
        list_view_id = imd.xmlid_to_res_id('account.invoice_tree')
        form_view_id = imd.xmlid_to_res_id('account.invoice_form')
        account_invoice_obj = self.env['account.invoice']
        account_invoice_line_obj = self.env['account.invoice.line'] 
        for order_id in self:
            inv = {
                'partner_id': order_id.partner_id.id,
                'account_id': order_id.partner_id.property_account_receivable_id.id,
                'date_invoice': fields.date.today(),
                'origin': self.name,
                'report_type':'outside',
                'consultant_doctor_id':order_id.primary_physician.id,
                'treating_doctor_id':order_id.primary_physician.id,
            }
            inv_id = account_invoice_obj.create(inv)
            if order_id.product_id :
                account_id = order_id.product_id.property_account_income_id.id
                if not account_id:
                    prop = self.env['ir.property'].get('property_account_income_categ_id', 'product.category')
                    account_id = prop and prop.id or False
                inv_line = {
                    'product_id': order_id.product_id.id,
                    'invoice_id': inv_id.id,
                    'price_unit':order_id.total_amount,
                    'account_id': order_id.product_id.categ_id.property_account_income_categ_id.id,
                    'uom_id': order_id.product_id.uom_id.id,
                    'quantity': 1,
                    'name':  order_id.product_id.name
                }
                acc = account_invoice_line_obj.create(inv_line)
        self.invoice_id = inv_id.id
        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [[form_view_id, 'form'],[list_view_id, 'tree'],[False, 'graph'], [False, 'kanban'], [False, 'calendar'], [False, 'pivot']],
            'target': action.target,
            'res_model': action.res_model,
            'res_id': inv_id.id,
            'domain': [
                ('report_type', 'in', ['outside'])
            ],
            #'context': context,
        }
        return result

    @api.multi
    def action_view_invoice(self):
        invoice_ids = self.mapped('invoice_id')
        imd = self.env['ir.model.data']
        action = imd.xmlid_to_object('account.action_invoice_tree1')
        list_view_id = imd.xmlid_to_res_id('account.invoice_tree')
        form_view_id = imd.xmlid_to_res_id('account.invoice_form')
        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [[list_view_id, 'tree'], [form_view_id, 'form'], [False, 'graph'], [False, 'kanban'], [False, 'calendar'], [False, 'pivot']],
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
            'domain': [('report_type', 'in', ['outside']),('id','=',self.invoice_id.id)],
        }
        if len(invoice_ids) > 1:
            result['domain'] = "[('id','in',%s)]" % invoice_ids.ids
        elif len(invoice_ids) == 1:
            result['views'] = [(form_view_id, 'form'), (list_view_id, 'tree')]
            result['res_id'] = invoice_ids.ids[0]
        else:
            result = {'type': 'ir.actions.act_window_close'}
        return result


class AccountPayment(models.Model):
    _inherit = "account.payment"

    towards = fields.Char(string='Towards')
    report_type = fields.Selection([("pharmacy", "Pharmacy Invoice"),
                                    ("consult", "Consultation Invoice"),
                                    ("register","Registration Invoice"),
                                    ("radiology", "Radiology Invoice"),
                                    ("physiotherapy","Physiotherapy Invoice"),
                                    ("lab", "Laboratory Invoice"),
                                    ("procedure", "Procedure Invoice"),
                                    ("hospital", "Hospital Invoice"),
                                    ('claim', 'Claim'), ('inpatient', 'Inpatient'),
                                    ('outside','Outside Surgery')], string="Invoice Type", default='outside')
    

    # @api.model
    # def default_get(self, fields):
    #     rec = super(AccountPayment, self).default_get(fields)
    #     if rec['report_type'] == 'outside':
    #             outside_obj = self.env['surgery.outside'].search([('invoice_id','in',rec['invoice_ids'][0][2])])
    #             rec['journal_id'] = self.env.ref('hms_invoice.check_payment_journal_1').id
    #             rec['received_amount'] = outside_obj.received_amount
    #             rec['tds_amount'] = outside_obj.tds_amount
    #             rec['bank_name'] = outside_obj.bank_name
    #             rec['cheque_no'] = outside_obj.cheque_no
    #             rec['cheque_date'] = outside_obj.cheque_date
    #             rec['towards'] = outside_obj.towards
    #     return rec

    @api.multi
    def post(self):
        res = super(AccountPayment,self).post()
        if self.invoice_ids and self.invoice_ids[0].patient_id.department_id:
            self.report_type = self.invoice_ids[0].report_type
            if self.report_type == 'outside':
                self.receipt_number = self.env['ir.sequence'].next_by_code('receipt.outside')
                outside_search = self.env['surgery.outside'].search([('invoice_id','=',self.invoice_ids[0].id)])
                for outside in outside_search:
                    outside.action_done()
        return res

