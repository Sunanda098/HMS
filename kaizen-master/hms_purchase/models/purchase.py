# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _


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



class PurchaseOrderInherit(models.Model):
    _inherit = "purchase.order"

    order_line = fields.One2many('purchase.order.line', 'order_id', string='Order Lines', states={}, copy=True)
    state = fields.Selection([
        ('draft', 'RFQ'),
        ('approve_first', '1-Approval'),
        ('approve_secound', '2-Approval'),
        ('purchase', 'Purchase Order'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')
    department_id = fields.Many2one('hospital.department', 'Department', ondelete='restrict')
    first_approve_user = fields.Many2one('res.users', string="First Approved By", default=lambda self: self.env.user, readonly="True")
    secound_approve_user = fields.Many2one('res.users', string="Secound Approved By", default=lambda self: self.env.user, readonly="True")

    @api.multi
    def amount_to_text(self, num):
        return amount_to_text(num)

    @api.multi
    def approval_one(self):
        self.state = 'approve_first'

    @api.multi
    def approval_two(self):
        self.state = 'approve_secound'


    @api.multi
    def button_confirm(self):
        for order in self:
            if order.state not in ['approve_secound']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order.company_id.po_double_validation == 'one_step'\
                    or (order.company_id.po_double_validation == 'two_step'\
                        and order.amount_total < self.env.user.company_id.currency_id.compute(order.company_id.po_double_validation_amount, order.currency_id))\
                    or order.user_has_groups('purchase.group_purchase_manager'):
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
        return True


    @api.multi
    def update_unit_price(self):
        for order in self:
            for data in order.order_line:
                record_id = self.env['stock.picking'].search([('origin','=',self.name)])
                our_data_line = record_id.pack_operation_product_ids.filtered(lambda value:value.product_id.id == data.product_id.id)
                our_data_line.update({
                    'unit_price_one': data.price_unit,
                }) 

class InheritStockPackOperation(models.Model):
    _inherit = 'stock.pack.operation'

    unit_price_one = fields.Float(string='Unit Price(PO)')

    @api.model
    def create(self,vals):
        res = super(InheritStockPackOperation,self).create(vals)
        purchase_id = self.env['purchase.order'].search([('name','=',res.picking_id.origin)])
        our_purchase_line = purchase_id.order_line.filtered(lambda value:value.product_id.id == res.product_id.id)
        for price in self:
            price.unit_price_one = our_purchase_line.price_unit
        return res


class InheritPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    is_free = fields.Integer(string='Free Qty')
    

   
# class InheritAccountInvoiceLines(models.Model):
#     _inherit = 'account.invoice.line'

#     @api.model
#     def create(self,vals):
#         invoice_id = self.env['account.invoice'].browse(vals['invoice_id'])
#         purchase_order_id = self.env['purchase.order'].search([('name','=',invoice_id.origin)])
#         for line in purchase_order_id.order_line:
#             if line.product_id.id == vals['product_id'] and line.is_free == True:
#                 vals['price_unit'] = 0.0
#         return super(InheritAccountInvoiceLines,self).create(vals)