# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.tools.translate import _
import datetime
from openerp.exceptions import UserError, RedirectWarning, ValidationError,Warning

def amount_to_text(num):
    '''words = {} convert an integer number into words'''
    units = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
    teens = ['', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', \
             'Seventeen', 'Eighteen', 'Nineteen']
    tens = ['', 'Ten', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', \
            'Eighty', 'Ninety']
    thousands = ['', 'Thousand', 'Million', 'Billion', 'Trillion', 'Quadrillion', \
                 'Quintillion', 'Sextillion', 'Septillion', 'Octillion', \
                 'Nonillion', 'Decillion', 'Undecillion', 'Duodecillion', \
                 'Tredecillion', 'Quattuordecillion', 'Sexdecillion', \
                 'Septendecillion', 'Octodecillion', 'Novemdecillion', \
                 'Vigintillion']
    words = []
    if num == 0: words.append('Zero')
    else:
        numStr = '%d' % num
        numStrLen = len(numStr)
        groups = (numStrLen + 2) / 3
        numStr = numStr.zfill(groups * 3)
        for i in range(0, groups * 3, 3):
            h, t, u = int(numStr[i]), int(numStr[i + 1]), int(numStr[i + 2])
            g = groups - (i / 3 + 1)
            if h >= 1:
                words.append(units[h])
                words.append('Hundred')
            if t > 1:
                words.append(tens[t])
                if u >= 1: words.append(units[u])
            elif t == 1:
                if u >= 1: words.append(teens[u])
                else: words.append(tens[t])
            else:
                if u >= 1: words.append(units[u])
            if (g >= 1) and ((h + t + u) > 0): words.append(thousands[g] + ' ')
    
    return ' '.join(words)

class AccountInvoiceDiscount(models.Model):
    _name = 'account.invoice.discount'
    
    patient_id = fields.Many2one('hms.patient',string="Patient")
    by_whom = fields.Many2one('res.partner','By Whom')
    discount = fields.Integer('Discount')
    debit = fields.Integer('Debit')
    treating_doctor_id = fields.Many2one("hms.physician", string="Treating Doctor")
    attending_doctor_id = fields.Many2one("hms.physician", string="Attending Doctor")
    attending_amount = fields.Integer('Attending Amount')
    treating_amount = fields.Integer('Treating Amount')
    total = fields.Integer('Total')
    date = fields.Date('Date')
    invoice_id = fields.Many2one('account.invoice','Invoice')
    name = fields.Char('Reference No')
    product_id = fields.Many2one('product.product',string="Product")
    hospital_amount = fields.Integer('Hospital Amount')
    invoice_line_id = fields.Many2one('account.invoice.line', string="Invoice Line")
    ksga = fields.Integer('KSGA')
    
class account_initial_payment(models.Model):
    _name = 'account.initial.payment'
    
    journal_id = fields.Many2one('account.journal', string='Payment Method', required=True, domain=[('type', 'in', ('bank', 'cash'))])
    amount = fields.Integer(string='Payment Amount', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.user.company_id.currency_id)
    payment_date = fields.Date(string='Payment Date', default=fields.Date.context_today, required=True, copy=False)
    bank_name = fields.Char(string='Bank Name')
    cheque_no = fields.Char(string='Cheque No.')
    cheque_date = fields.Date(string='Cheque Date')
    card_no = fields.Char(string='Credit Card No')
    card_name = fields.Char(string='Credit Card Name')
    card_ccv = fields.Char(size=3,string='Credit Card CVV No')
    pan_no = fields.Char(string='PAN No')
    invoice_id = fields.Many2one('account.invoice', string="Invoice")
    code = fields.Char(string='Short Code', related='journal_id.code', store=True)
    receipt_number = fields.Char(size=256, string='Receipt Sequence', readonly=True, copy=False)
    is_discount = fields.Boolean('Discount?')
    discount_amount = fields.Integer('Discount Amount')
    by_whom = fields.Many2one('res.partner','Discount given by')
    discount_id = fields.Many2one('account.invoice.discount',string="Discount")
    bill_username = fields.Many2one('res.users', string="User Signature", default=lambda self: self.env.user, readonly="True")

    @api.onchange('discount_amount')
    def onchange_discount_amount(self):
        self.amount = self.amount - self.discount_amount

    @api.multi
    def amount_to_text(self, num):
        return amount_to_text(num)

    @api.multi
    def convert_date(self, date):
        d = datetime.datetime.strptime(date, '%Y-%m-%d')
        ret_date = d.strftime('%d-%b-%Y')
        return ret_date

    @api.multi
    def post(self):
        self.receipt_number = self.env['ir.sequence'].next_by_code('receipt.opd')
        revenue_obj = self.env['revenue.sharing']
        for line in self.invoice_id.invoice_line_ids:
            if line.discount_price > line.price_unit:
                raise Warning(_('Discount should not be greater then Unit Charges'))
            type = None
            if line.invoice_id.appointment_id:
                type = 'opd'
            if line.invoice_id.hospital_id:
                type = 'ipd'
            type = 'opd'
            revenue_id = revenue_obj.search([('type','=',type),('product_id','=',line.product_id.id)])
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.", revenue_id
            if revenue_id:
                attend_type = line.invoice_id.consultant_doctor_id.type
                treat_type = line.invoice_id.treating_doctor_id.type
                debit = 0
                attending_amount = 0
                treating_amount = 0
                hospital_amount = 0
                ksga = 0
                if attend_type=='standard':
                    attending_amount = revenue_id.attend_std_price
                    hospital_amount = revenue_id.hospital_share_std
                    ksga = revenue_id.ksga_price_std
                elif attend_type=='outside':
                    attending_amount = revenue_id.attend_outside_price
                    hospital_amount = revenue_id.hospital_share_out
                    ksga = revenue_id.ksga_price_out
                elif attend_type=='doctor':
                    attending_amount = revenue_id.attend_doctor_price
                    hospital_amount = revenue_id.hospital_share_doc
                    ksga = revenue_id.ksga_price_doc
                elif attend_type=='specialist':
                    special_service = self.env['hms.special.service'].search([('doctor_id','=',line.invoice_id.consultant_doctor_id.id),('product_id','=',line.product_id.id)])
                    if special_service:
                        hospital_amount = revenue_id.hospital_share_special
                        ksga = revenue_id.ksga_share_special
                        attending_amount = special_service[0].amount
                if treat_type=='standard':
                    treating_amount = revenue_id.treat_std_price
                    hospital_amount = revenue_id.hospital_share_std
                elif treat_type=='outside':
                    treating_amount = revenue_id.treat_outside_price
                    hospital_amount = revenue_id.hospital_share_out
                elif treat_type=='doctor':
                    treating_amount = revenue_id.treat_doctor_price
                elif treat_type=='specialist':
                    special_service = self.env['hms.special.service'].search([('doctor_id','=',line.invoice_id.treating_doctor_id.id),('product_id','=',line.product_id.id)])
                    if special_service:
                        treating_amount = special_service[0].amount
                        hospital_amount = special_service[0].hospital_share
                        ksga = special_service[0].ksga_share
                print  ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>treating_amount>>>>>>>>>>>>", treating_amount
                #done
                if line.by_whom and self.invoice_id.consultant_doctor_id.id != self.invoice_id.treating_doctor_id.id:
                    if self.invoice_id.treating_doctor_id and line.by_whom.id==self.invoice_id.treating_doctor_id.user_id.partner_id.id:
                        if (treating_amount + hospital_amount) < line.discount_price:
                            raise Warning(_('You can not give this much of amount as discount'))
                        if line.discount_price >= treating_amount:
                            hospital_amount = hospital_amount - (line.discount_price - treating_amount)
                            treating_amount = 0
                        elif line.discount_price > 0 and line.discount_price < treating_amount:
                            treating_amount = treating_amount - line.discount_price
                    if self.invoice_id.consultant_doctor_id and line.by_whom.id== self.invoice_id.consultant_doctor_id.user_id.partner_id.id:
                        if (treating_amount + hospital_amount) < line.discount_price:
                            raise Warning(_('You can not give this much of amount as discount'))
                        if line.discount_price >= attending_amount:
                            hospital_amount = hospital_amount - (line.discount_price - attending_amount)
                            attending_amount = 0
                        elif line.discount_price > 0 and line.discount_price <= attending_amount:
                            attending_amount = attending_amount - line.discount_price
#                     if self.invoice_id.treating_doctor_id and line.by_whom.id==self.invoice_id.treating_doctor_id.user_id.partner_id.id:
#                         if line.discount_price > 0 and line.discount_price < treating_amount:
#                             treating_amount = treating_amount - line.discount_price
                #done
                if line.by_whom and self.invoice_id.consultant_doctor_id.id == self.invoice_id.treating_doctor_id.id:
                    if self.invoice_id.consultant_doctor_id and line.by_whom.id == self.invoice_id.consultant_doctor_id.user_id.partner_id.id:
                        if line.discount_price > attending_amount and line.discount_price <= (treating_amount + attending_amount):
                            treating_amount = treating_amount - (line.discount_price - attending_amount)
                            attending_amount = 0
                        elif line.discount_price > 0 and line.discount_price < attending_amount:
                            attending_amount = attending_amount - line.discount_price
                        elif line.discount_price > (treating_amount + attending_amount):
                            hospital_amount = hospital_amount - (line.discount_price -(treating_amount + attending_amount))
                            attending_amount = 0
                            treating_amount = 0
                        elif line.discount_price > 0 and line.discount_price < treating_amount:
                            treating_amount = treating_amount - line.discount_price
                vals = {
                        'name':self.receipt_number,
                        'invoice_line_id':line.id,
                        'discount':line.discount_price,
                        'attending_doctor_id':line.invoice_id.consultant_doctor_id.id,
                        'treating_doctor_id':line.invoice_id.treating_doctor_id.id,
                        'attending_amount':attending_amount,
                        'treating_amount':treating_amount,
                        'invoice_id':self.invoice_id.id,
                        'by_whom':line.by_whom.id,
                        'date':self.payment_date,
                        'patient_id':self.invoice_id.patient_id.id,
                        'product_id':line.product_id.id,
                        'hospital_amount': hospital_amount,
                        'ksga':ksga,
                        }
                discount = self.env['account.invoice.discount'].search([('invoice_line_id','=',line.id)])
                if discount:
                    discount.write(vals)
                else:
                    discount_id = self.env['account.invoice.discount'].create(vals)
#                 self.discount_id = discount_id.id
        self.invoice_id.show_payment = True

    @api.multi
    def write(self, vals):
        
#         if vals.has_key('discount_amount') and vals.has_key('by_whom'):
#             invoice_line = self.env['account.invoice.line'].search([('invoice_id','=',self.invoice_id.id),('product_id.hospital_product_type','=','consultation')])
#             invoice_line.price_unit = invoice_line.price_unit - vals['discount_amount']
#             self.amount = invoice_line.price_unit
#             if self.invoice_id.consultant_doctor_id.user_id.partner_id.id == vals['by_whom']:
#                 self.discount_id.attending_amount = vals['discount_amount']
#             else:
#                 vals = {
#                         'name':self.env['ir.sequence'].next_by_code('receipt.opd'),
# #                         'debit':self.invoice_id.consultant_doctor_id.consul_charge,
#                         'attending_amount':vals['discount_amount'],
#                         'invoice_id':self.invoice_id.id,
#                         'by_whom':vals['by_whom'],
#                         'date':self.payment_date,
#                         'patient_id':self.invoice_id.patient_id.id
#                 }
        return super(account_initial_payment,self).write(vals)

class account_invoice(models.Model):
    _inherit = "account.invoice"

    sequence = fields.Char(size=256, string='Hospital Sequence', readonly=True, copy=False)
    patient_id = fields.Many2one('hms.patient',string="Patient")
    stay_day = fields.Char(string='Stay No. of day')
    report_type = fields.Selection([("pharmacy", "Pharmacy Invoice"),
                                    ("consult", "Consultation Invoice"),
                                    ("register","Registration Invoice"),
                                    ("radiology", "Radiology Invoice"),
                                    ("physiotherapy","Physiotherapy Invoice"),
                                    ("lab", "Laboratory Invoice"),
                                    ("procedure", "Procedure Invoice"),
                                    ("hospital", "Hospital Invoice"),
                                    ('claim', 'Claim'), ('inpatient', 'Inpatient'),('outside','Outside Surgery')], string="Invoice Type", default='pharmacy')
    consultant_doctor_id = fields.Many2one("hms.physician", string="Attending Doctor")
    treating_doctor_id = fields.Many2one("hms.physician", string="Treating Doctor")
    hospital_id = fields.Many2one("inpatient.registration", string="Hospitalization")
    appointment_id = fields.Many2one("hms.appointment", string="Appointment")
    receipt_date = fields.Date(string='Receipt Date')
    receipt_number = fields.Char(size=256, string='Receipt Sequence', readonly=True, copy=False)
    physiotherapy_id = fields.Many2one('opd.physiotherapy',string="Physiotherapy")
    state = fields.Selection([
            ('draft','Draft'),
            ('reserved','Initial Payment'),
            ('proforma', 'Pro-forma'),
            ('proforma2', 'Pro-forma'),
            ('open', 'Open'),
            ('paid', 'Paid'),
            ('cancel', 'Cancelled'),
        ], string='Status', index=True, readonly=True, default='draft',
        track_visibility='onchange', copy=False,
        help=" * The 'Draft' status is used when a user is encoding a new and unconfirmed Invoice.\n"
             " * The 'Pro-forma' status is used the invoice does not have an invoice number.\n"
             " * The 'Open' status is used when user create invoice, an invoice number is generated. Its in open status till user does not pay invoice.\n"
             " * The 'Paid' status is set automatically when the invoice is paid. Its related journal entries may or may not be reconciled.\n"
             " * The 'Cancelled' status is used when user cancel invoice.")
    initial_ids = fields.One2many('account.initial.payment','invoice_id',string="Initial Payments")
    show_payment = fields.Boolean('Show Payment')
    invoice_line_ids = fields.One2many('account.invoice.line', 'invoice_id', string='Invoice Lines', oldname='invoice_line',
        readonly=True, states={'draft': [('readonly', False)],'reserved': [('readonly', False)]}, copy=True)
    # patient_clinical_research = fields.Boolean(sring="CRL")
    
    @api.model
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount')
    def _compute_amount(self):
        for rec in self:
            rec.amount_untaxed = sum(line.price_subtotal for line in rec.invoice_line_ids)
            rec.amount_tax = sum(line.amount for line in rec.tax_line_ids)
            rec.amount_total = round(rec.amount_untaxed + rec.amount_tax)

    @api.onchange('patient_id')
    def onchange_patient(self):
        if self.patient_id:
            self.partner_id = self.patient_id.user_id.partner_id.id

    @api.multi
    def amount_to_text(self, num):
        return amount_to_text(num)
    
    @api.multi
    def check_invoicelines(self):
        if not self.invoice_line_ids:
            raise UserError(_('Please create some invoice lines.'))
    
    @api.multi
    def invoice_validate(self):
        res = super(account_invoice,self).invoice_validate()
        print "=========account_invoice============="
        
        return res

    @api.multi
    def action_hospital_inpatient_bill(self):
        return self.env['report'].get_action(self, 'hms_invoice.report_hospital_inpatient_bill_document')
        

#ADDED inherit class to show payment related fields
class AccountVoucher(models.Model):
    _inherit = "account.voucher"

    @api.multi
    def amount_to_text(self, num):
        return amount_to_text(num)

class AccountMove(models.Model):
    _inherit = "account.move"

    report_type = fields.Selection([("pharmacy", "Pharmacy Invoice"),
                                    ("consult", "Consultation Invoice"),
                                    ("register","Registration Invoice"),
                                    ("radiology", "Radiology Invoice"),
                                    ("physiotherapy","Physiotherapy Invoice"),
                                    ("lab", "Laboratory Invoice"),
                                    ("procedure", "Procedure Invoice"),
                                    ("hospital", "Hospital Invoice"),
                                    ('claim', 'Claim'), ('inpatient', 'Inpatient'),('outside','Outside Surgery')], string="Invoice Type", default='pharmacy')

    @api.multi
    def amount_to_text(self, num):
        return amount_to_text(num)

class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    state = fields.Selection(related="invoice_id.state", string="States", store=True)
    hospital_product_type = fields.Selection(related="product_id.hospital_product_type", string="Product Type", store=True)
    discount_price = fields.Float('Discount')
    by_whom = fields.Many2one('res.partner','In Account Of')
    login_username = fields.Many2one('res.users','User', default=lambda self: self.env.user, readonly="1")

    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
        'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id')
    def _compute_price(self):
        currency = self.invoice_id and self.invoice_id.currency_id or None
        price = self.price_unit - self.discount_price
        taxes = False
        if self.invoice_line_tax_ids:
            taxes = self.invoice_line_tax_ids.compute_all(price, currency, self.quantity, product=self.product_id, partner=self.invoice_id.partner_id)
        self.price_subtotal = price_subtotal_signed = taxes['total_excluded'] if taxes else self.quantity * price
        if self.invoice_id.currency_id and self.invoice_id.currency_id != self.invoice_id.company_id.currency_id:
            price_subtotal_signed = self.invoice_id.currency_id.compute(price_subtotal_signed, self.invoice_id.company_id.currency_id)
        sign = self.invoice_id.type in ['in_refund', 'out_refund'] and -1 or 1
        self.price_subtotal_signed = price_subtotal_signed * sign

class AccountPayment(models.Model):
    _inherit = "account.payment"
        
    @api.multi
    def convert_date(self, date):
        d = datetime.datetime.strptime(date, '%Y-%m-%d')
        ret_date = d.strftime('%d-%b-%Y')
        return ret_date

    @api.multi
    def amount_to_text(self, num):
        return amount_to_text(num)
       
        
    #need to add onchange for tds amoutnchange total amount.
    product_id = fields.Many2one('product.product', string="Product")
    patient_id = fields.Many2one('hms.patient',string="Patient")
    receipt_number = fields.Char(size=256, string='Receipt Sequence', readonly=True, copy=False)
    code = fields.Char(string='Short Code', related='journal_id.code', store=True)
    tds_amount = fields.Float(string='TDS Amount')
    received_amount = fields.Float(string='Received Amount')
    bank_name = fields.Char(string='Bank Name')
    cheque_no = fields.Char(string='Cheque No.')
    cheque_date = fields.Date(string='Cheque Date')
    card_no = fields.Char(string='Credit Card No')
    card_name = fields.Char(string='Credit Card Name')
    card_ccv = fields.Char(size=3,string='Credit Card CVV No')
    pan_no = fields.Char(string='PAN No')
    report_type = fields.Selection([("pharmacy", "Pharmacy Invoice"),
                                    ("consult", "Consultation Invoice"),
                                    ("register","Registration Invoice"),
                                    ("radiology", "Radiology Invoice"),
                                    ("physiotherapy","Physiotherapy Invoice"),
                                    ("lab", "Laboratory Invoice"),
                                    ("procedure", "Procedure Invoice"),
                                    ("hospital", "Hospital Invoice"),
                                    ('claim', 'Claim'), ('inpatient', 'Inpatient'),('outside','Outside Surgery')], string="Invoice Type", default='pharmacy')
    months = fields.Selection([("1", "January"),("2", "February"),("3", "March"),("4", "April"), 
            ("5", "May"), ("6", "June"), ("7", "July"), ("8", "August"), 
            ("9", "September"), ("10", "October"), ("11", "November"), ("12", "December"),],default="1",string='Credit Card Expiry Date')
    years = fields.Selection([(year, year) for year in range(2015,2051)], string='Year')

    @api.onchange('patient_id')
    def onchange_patient(self):
        if self.patient_id:
            self.partner_id = self.patient_id.user_id.partner_id.id

    # @api.onchange('patient_id')
    # def onchange_patient(self):
    #     if self.patient_id:
    #         self.ipd_id = self.patient_id.name

    @api.model
    def default_get(self, fields):
        rec = super(AccountPayment, self).default_get(fields)
        invoice_defaults = self.resolve_2many_commands('invoice_ids', rec.get('invoice_ids'))
        if invoice_defaults and len(invoice_defaults) == 1:
            invoice = invoice_defaults[0]
            rec['report_type'] = invoice['report_type']
        return rec

    def get_type(self,obj):
        product_type = []
        if obj.invoice_ids.invoice_line_ids:
            for rec in obj.invoice_ids.invoice_line_ids:
                product_type.append(rec.product_id.hospital_product_type)
        product_type = dict.fromkeys(product_type).keys()
        if 'consultation' in product_type:
            name = 'Consultation'
        else:
            name=''
        for type in product_type:
            if type=='radiology' and not name == '':
                name += ', X-ray'
            elif type=='radiology' and name == '':
                name += 'X-ray'
            if type=='pathology' and not name == '':
                name += ', Pathology'
            elif type=='pathology' and name == '':
                name += 'Pathology'    
            if type=='package' and not name == '':
                name += ', Hospitalization'
            elif type=='package' and name == '':
                name += 'Hospitalization'  
            if type =='physiotherapy' and not name == '':
                name += ', Physiotherapy'
            elif type =='physiotherapy' and name == '':
                name += 'Physiotherapy'
            if type=='manometry' and not name == '':
                name += ', Manometry'
            elif type=='radiology' and name == '':
                name += 'Manometry'
            if type=='endoscopy' and not name == '':
                name += ', Endoscopy'
            elif type=='endoscopy' and name == '':
                name += 'Endoscopy'  
        return  name

    def get_name(self,obj):
        name = []
        if obj.invoice_ids[0].patient_id.first_name:
            name.append(str(obj.invoice_ids[0].patient_id.first_name))
            if obj.invoice_ids[0].patient_id.middel_name:
                name.append(str(obj.invoice_ids[0].patient_id.middel_name[0]))
            if obj.invoice_ids[0].patient_id.last_name:
                name.append(str(obj.invoice_ids[0].patient_id.last_name))
            return ' '.join(name)

    @api.multi
    def post(self):
        res = super(AccountPayment,self).post()
        # if self.invoice_ids and self.invoice_ids[0].patient_id.department_id.name == 'Paediatric':   
        #     self.receipt_number = self.env['ir.sequence'].next_by_code('receipt.padetric')
        if self.invoice_ids and self.invoice_ids[0].patient_id.department_id:
            self.report_type = self.invoice_ids[0].report_type
            if self.invoice_ids[0].report_type == 'claim':
                claim_search = self.env['hms.insurance.claim'].search([('invoice_id','=',self.invoice_ids[0].id)])
                claim_search.action_done()  
            if self.invoice_ids[0].report_type == 'physiotherapy':
                self.receipt_number = self.env['ir.sequence'].next_by_code('receipt.physiotherphy')
            if self.invoice_ids[0].report_type == 'radiology':
                self.receipt_number = self.env['ir.sequence'].next_by_code('receipt.radiology')
            if self.invoice_ids[0].report_type == 'inpatient':
                self.receipt_number = self.env['ir.sequence'].next_by_code('receipt.ipd')
            if self.invoice_ids[0].report_type == 'consult':
                self.receipt_number = self.env['ir.sequence'].next_by_code('receipt.opd')
        return res

    @api.multi
    def _create_payment_entry(self, amount):
        res = super(AccountPayment, self)._create_payment_entry(amount)
        if self.invoice_ids:
            res.report_type = self.invoice_ids[0].report_type
        return res


class ReportGeneralLedger(models.AbstractModel):
    _inherit = 'report.account.report_generalledger'

    def _get_account_move_entry(self, accounts, init_balance, sortby, display_account):
        """
        :param:
                accounts: the recordset of accounts
                init_balance: boolean value of initial_balance
                sortby: sorting by date or partner and journal
                display_account: type of account(receivable, payable and both)

        Returns a dictionary of accounts with following key and value {
                'code': account code,
                'name': account name,
                'debit': sum of total debit amount,
                'credit': sum of total credit amount,
                'balance': total balance,
                'amount_currency': sum of amount_currency,
                'move_lines': list of move line
        }
        """
        cr = self.env.cr
        MoveLine = self.env['account.move.line']
        move_lines = dict(map(lambda x: (x, []), accounts.ids))

        # Prepare initial sql query and Get the initial move lines
        if init_balance:
            init_tables, init_where_clause, init_where_params = MoveLine.with_context(date_from=self.env.context.get('date_from'), date_to=False, initial_bal=True)._query_get()
            init_wheres = [""]
            if init_where_clause.strip():
                init_wheres.append(init_where_clause.strip())
            init_filters = " AND ".join(init_wheres)
            filters = init_filters.replace('account_move_line__move_id', 'm').replace('account_move_line', 'l')
            sql = ("SELECT 0 AS lid, l.account_id AS account_id, '' AS ldate, '' AS lcode, NULL AS amount_currency, '' AS lref, 'Initial Balance' AS lname, COALESCE(SUM(l.debit),0.0) AS debit, COALESCE(SUM(l.credit),0.0) AS credit, COALESCE(SUM(l.debit),0) - COALESCE(SUM(l.credit), 0) as balance, '' AS lpartner_id,\
                '' AS move_name, '' AS mmove_id, '' AS currency_code,\
                NULL AS currency_id,\
                '' AS invoice_id, '' AS invoice_type, '' AS invoice_number,\
                '' AS partner_name\
                FROM account_move_line l\
                LEFT JOIN account_move m ON (l.move_id=m.id)\
                LEFT JOIN res_currency c ON (l.currency_id=c.id)\
                LEFT JOIN res_partner p ON (l.partner_id=p.id)\
                LEFT JOIN account_invoice i ON (m.id =i.move_id)\
                JOIN account_journal j ON (l.journal_id=j.id)\
                WHERE l.account_id IN %s" + filters + ' GROUP BY l.account_id')
            params = (tuple(accounts.ids),) + tuple(init_where_params)
            cr.execute(sql, params)
            for row in cr.dictfetchall():
                move_lines[row.pop('account_id')].append(row)

        sql_sort = 'l.date, l.move_id'
        if sortby == 'sort_journal_partner':
            sql_sort = 'j.code, p.name, l.move_id'

        # Prepare sql query base on selected parameters from wizard
        tables, where_clause, where_params = MoveLine._query_get()
        wheres = [""]
        if where_clause.strip():
            wheres.append(where_clause.strip())
        filters = " AND ".join(wheres)
        filters = filters.replace('account_move_line__move_id', 'm').replace('account_move_line', 'l')

        # Get move lines base on sql query and Calculate the total balance of move lines
        sql = ('SELECT l.id AS lid, l.account_id AS account_id, l.date AS ldate, j.code AS lcode, l.currency_id, l.amount_currency, l.ref AS lref, l.name AS lname, m.report_type AS rtype, COALESCE(l.debit,0) AS debit, COALESCE(l.credit,0) AS credit, COALESCE(SUM(l.debit),0) - COALESCE(SUM(l.credit), 0) AS balance,\
            m.name AS move_name, c.symbol AS currency_code, p.name AS partner_name\
            FROM account_move_line l\
            JOIN account_move m ON (l.move_id=m.id)\
            LEFT JOIN res_currency c ON (l.currency_id=c.id)\
            LEFT JOIN res_partner p ON (l.partner_id=p.id)\
            JOIN account_journal j ON (l.journal_id=j.id)\
            JOIN account_account acc ON (l.account_id = acc.id) \
            WHERE l.account_id IN %s ' + filters + ' GROUP BY l.id, l.account_id, l.date, j.code, l.currency_id, l.amount_currency, l.ref, l.name, m.name, c.symbol, p.name, m.report_type ORDER BY ' + sql_sort)
        params = (tuple(accounts.ids),) + tuple(where_params)
        cr.execute(sql, params)

        for row in cr.dictfetchall():
            balance = 0
            for line in move_lines.get(row['account_id']):
                balance += line['debit'] - line['credit']
            row['balance'] += balance
            move_lines[row.pop('account_id')].append(row)

        # Calculate the debit, credit and balance for Accounts
        account_res = []
        for account in accounts:
            currency = account.currency_id and account.currency_id or account.company_id.currency_id
            res = dict((fn, 0.0) for fn in ['credit', 'debit', 'balance'])
            res['code'] = account.code
            res['name'] = account.name
            res['move_lines'] = move_lines[account.id]
            for line in res.get('move_lines'):
                res['debit'] += line['debit']
                res['credit'] += line['credit']
                res['balance'] = line['balance']
            if display_account == 'all':
                account_res.append(res)
            if display_account == 'movement' and res.get('move_lines'):
                account_res.append(res)
            if display_account == 'not_zero' and not currency.is_zero(res['balance']):
                account_res.append(res)

        return account_res


class TodayReport(models.TransientModel):
    _inherit = 'account.report.general.ledger'

    date_from = fields.Date(string='Start Date', default=fields.Date.context_today)
    date_to = fields.Date(string='End Date', default=fields.Date.context_today)


class TodayReport(models.TransientModel):
    _name = 'account.report.invoice.report'

    date_from = fields.Date(string='Start Date', default=fields.Date.context_today)
    date_to = fields.Date(string='End Date', default=fields.Date.context_today)
    report_type = fields.Selection([
        ("orthopedic", "HOSPITAL"),
#         ('paediatric', 'SHAH HOSPITAL PAEDIATRIC'),
#         ("radiology", "SHAH X-RAY CLINIC"),
#         ("physiotherapy","SHAH HOSPITAL PHYSIOTHERAPY CLINIC")
        ], string="Report Type")

    @api.multi
    def print_report(self, data):
        return self.env['report'].get_action(self, 'hms_invoice.report_invoice_line')

    @api.multi
    def get_invoice_line(self):
        inv_line_obj = self.env['account.invoice.line']
        domain = [('state', '=', 'paid'),
        ('invoice_id.date_invoice', '>=', self.date_from),
        ('invoice_id.date_invoice', '<=', self.date_to)]
        if self.report_type == 'orthopedic':
            domain.append(('hospital_product_type', '=', 'consultation'))
#         elif self.report_type == 'paediatric':
#             domain.append(('|'))
#             domain.append(('hospital_product_type', '=', 'consultation_paediatric'))
#             domain.append(('hospital_product_type', '=', 'vaccination'))
#         if self.report_type == 'physiotherapy':
#             domain.append(('hospital_product_type', '=', 'physiotherapy'))
#         else:
#             domain.append(('hospital_product_type', '=', self.report_type))
#             domain.append(('invoice_id.appointment_id.bill_to_hospital','=',False))
        inv_lines = inv_line_obj.search(domain)
        print "#####inv_lines:",inv_lines
        if inv_lines :
            sorted_lines = inv_lines.sorted(key=lambda r: r.invoice_id.payment_ids[0].receipt_number)
            print "#####sorted_lines:",len(sorted_lines)
            return sorted_lines
        else:
            return False
            # raise UserError('No Invoice Line Found')

class BillToHospitalReport(models.TransientModel):
    _name = 'account.billtohospital.report'

    date_from = fields.Date(string='Start Date', default=fields.Date.context_today)
    date_to = fields.Date(string='End Date', default=fields.Date.context_today)
    report_type = fields.Selection([
#         ("orthopedic", "SHAH HOSPITAl OPD"),
#         ('paediatric', 'SHAH HOSPITAL PAEDIATRIC'),
        ("radiology", "KAIZEN X-RAY CLINIC"),
        ], string="Report Type",default='radiology')

    @api.multi
    def print_report(self, data):
        return self.env['report'].get_action(self, 'hms_invoice.report_billtohospital')

    @api.multi
    def get_invoice_line(self):
        inv_line_obj = self.env['account.invoice.line']
        account_id = False
        if self.report_type == 'radiology':
            account_id = self.env.ref('hms_invoice.bill_to_hosp_radiology')
        if self.report_type == 'physiotherapy':
            account_id = self.env.ref('hms_invoice.bill_to_hosp_physiotherapy')
        domain = [('state', '=', 'paid'),
        ('hospital_product_type', '=', self.report_type),
        ('invoice_id.date_invoice', '>=', self.date_from),
        ('invoice_id.date_invoice', '<=', self.date_to),
        ('account_id','=',account_id.id)]
        inv_lines = inv_line_obj.search(domain)
        # sorted_lines = inv_lines.sorted(key=lambda r: r.invoice_id.payment_ids[0].receipt_number)
        # return sorted_lines
        if inv_lines :
            sorted_lines = inv_lines.sorted(key=lambda r: r.invoice_id.payment_ids[0].receipt_number)
            print "#####sorted_lines:",len(sorted_lines)
            return sorted_lines
        else:
            return False

class DailyReport(models.TransientModel):
    _name = 'account.report.daily.report'

    date_from = fields.Date(string='Start Date', default=fields.Date.context_today)
    date_to = fields.Date(string='End Date', default=fields.Date.context_today)
#     report_type = fields.Selection([
#         ("case", "Case"),
#         ('check', 'Check'),
#         ("credit", "Credit"),
#         ("bank","Bank")], string="Report Type")
    journal_id =fields.Many2one('account.journal','Select Register Type',required=True)
#     report_type = fields.Selection([
#         ("orthopedic", "SHAH HOSPITAL"),
#         ('paediatric', 'SHAH HOSPITAL PAEDIATRIC'),
#         ("radiology", "SHAH X-RAY CLINIC"),
#         ("physiotherapy","SHAH HOSPITAL PHYSIOTHERAPY CLINIC")], string="Report Type")

    report_type = fields.Selection([
                                    ("consult", "KAIZEN HOSPITAL"),
                                    ("radiology", "KAIZEN X-RAY CLINIC"),
                                    ], string="Type", default='consult', required=True)

    @api.multi
    def print_report(self, data):
        return self.env['report'].get_action(self, 'hms_invoice.report_daily_report')

    @api.multi
    def get_payments(self):
        payment_obj = self.env['account.payment']
        domain = [('state', '=', 'posted'),
        ('payment_date', '>=', self.date_from),
        ('payment_date', '<=', self.date_to),
        ('journal_id','=',self.journal_id.id),
        ('report_type','=',self.report_type)]
        payments = payment_obj.search(domain)
        print "===============payments=============",payments,self.report_type
#         domain.append((payments.invoice_ids[0].report_type==self.report_type))
#         payments = payment_obj.search(domain)
        
        sorted_lines = payments.sorted(key=lambda r: r.receipt_number)
        return sorted_lines

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: