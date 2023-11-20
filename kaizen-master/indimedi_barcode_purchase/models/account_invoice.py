# -*- encoding: utf-8 -*-

from openerp import api, fields, models, SUPERUSER_ID, _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    get_product_ean = fields.Char(string='Add Product', size=13, help="Read a product barcode to add it as new Line.")

    @api.onchange('get_product_ean')
    def onchange_product_ean(self):
        if not self.get_product_ean:
            return
        qty = 1.0
        product_obj = self.env['product.product']
        lot_ids = self.env['stock.production.lot'].search([('barcode','=',self.get_product_ean)], limit=1)
        if lot_ids:
            product = lot_ids.product_id
            batch_no = lot_ids.id
            price_unit = lot_ids.product_id.standard_price if self.type=='in_invoice' else lot_ids.product_id.lst_price
            uom = lot_ids.product_id.uom_po_id.id 
            uos = lot_ids.purchase_uom
        else:
            prod_ids = product_obj.search(['|',('barcode','=',self.get_product_ean),('default_code','=',self.get_product_ean)], limit=1)
            if not prod_ids:
                warning = {'title': _('Warning!'),
                    'message': _("There is no product with Barcode or Reference: %s") % (self.get_product_ean),
                }
                self.get_product_ean = False
                return {'warning':warning}
            batch_no = False
            price_unit = prod_ids.standard_price
            uom = prod_ids.uom_po_id.id
            product = prod_ids.id
        flag = 1
        xorder_line = []
        for o_line in self.invoice_line_ids:
            if o_line.product_id.id :
                flag = 0
                xorder_line.append((0,0,{
                    'product_id': o_line.product_id.id,
                    'name': o_line.product_id.name,
                   # 'invoice_line_tax_id': o_line.invoice_line_tax_id,
                    'partner_id' : self.partner_id and self.partner_id.id,
                    'quantity' : (o_line.quantity + 1),
                    'price_unit': o_line.price_unit,
                    'uom_id': o_line.uom_id and o_line.uom_id.id,
                    'state' : 'draft',
                }))
        if flag:
            xorder_line.append((0,0, {
            'product_id': product.id,
            'name':product.name,
            #'invoice_line_tax_id': [(6, 0, product.invoice_line_tax_ids.ids)],
            'partner_id' : self.partner_id.id,
            'quantity' : 1,
            'uos_id': uos.id,
            'lot': batch_no,
            'price_unit': price_unit,
            'uom_id': uom ,
            'state' : 'draft',
        }))
        self.get_product_ean = False
        self.invoice_line_ids = xorder_line

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: