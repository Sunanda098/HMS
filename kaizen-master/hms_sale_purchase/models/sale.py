# -*- coding: utf-8 -*-

from openerp import api, fields, models
from openerp.tools.translate import _

class Sale(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _get_picking_type(self):
        stock_picking_obj = self.env['stock.picking.type']
        picking_type_id = stock_picking_obj.search([('name', '=', 'Delivery Orders')],limit=1)
          

    patient_id = fields.Many2one('hms.patient',string="Patient")
    physician_id = fields.Many2one('hms.physician', string='Prescribing Doctor')
    picking_type_id = fields.Many2one('stock.picking.type',string='Picking Type')
    picking_id = fields.Many2one('stock.picking',string='Delivery Order')
    sale_on_cost = fields.Boolean(string='Sale On Cost')                         

    _defaults={
        'picking_type_id': _get_picking_type,
    }

    @api.v7
    def action_button_confirm(self, cr, uid, ids, context=None):
        lot_obj = self.pool('stock.production.lot')
        for line in self.browse(cr, uid, ids, context=context).order_line:
            if line.batch_no and line.batch_no.qty_count:
                if line.batch_no.qty_lot >= line.product_uom_qty:
                    lot_obj.write(cr, uid, line.batch_no.id, {'qty_lot': line.batch_no.qty_lot - line.product_uom_qty}, context=context)
        return super(sale, self).action_button_confirm(cr, uid, ids, context=context)

    
    @api.onchange('sale_on_cost')
    def sale_on_cost_change(self):
        sale_order_line_obj = self.env['sale.order.line']
        res = []
        if self.sale_on_cost:
            for line in self.order_line:
                if line.batch_no:
                        res.append((1, line.id, {'price_unit': line.batch_no.purchase_price / line.batch_no.purchase_uom.factor_inv,
                                            'price_subtotal': (line.batch_no.purchase_price / line.batch_no.purchase_uom.factor_inv) * line.product_uom_qty,
                                        }))
            self.order_line = res
        else:
            for line in self.order_line:
                if line.batch_no:
                    res.append((1, line.id, {'price_unit': line.batch_no.sale_price,
                                    'price_subtotal': line.batch_no.sale_price * line.product_uom_qty,
                                }))
            self.order_line = res
    
    @api.model
    def action_view_picking(self):
        mod_obj = self.env['ir.model.data']
        act_obj = self.env['ir.actions.act_window']

        result = mod_obj.get_object_reference('stock', 'action_picking_tree')
        id = result and result[1] or False
        result = act_obj.read()
        #compute the number of invoices to display
        picking_ids = []
        for so in self:
            picking_ids += [so.picking_id.id]
        #choose the view_mode accordingly
        if len(picking_ids)>1:
            result['domain'] = "[('id','in',["+','.join(map(str, picking_ids))+"])]"
        else:
            res = mod_obj.get_object_reference('stock', 'view_picking_form')
            result['views'] = [(res and res[1] or False, 'form')]
            result['res_id'] = picking_ids and picking_ids[0] or False
        return result
    
    @api.model
    def action_invoice_create(grouped=False, states=None, date_invoice = False):
        if states is None:
            states = ['confirmed', 'done', 'exception']
        res = False
        invoices = {}
        invoice_ids = []
        invoice = self.env['account.invoice']
        sale_order_line_obj = self.env['sale.order.line']
        partner_currency = {}
        # If date was specified, use it as date invoiced, usefull when invoices are generated this month and put the
        # last day of the last month as invoice date
        if self.date_invoice:
            context = dict(context or {}, date_invoice=date_invoice)
        for o in self:
            currency_id = o.pricelist_id.currency_id.id
            if (o.partner_id.id in partner_currency) and (partner_currency[o.partner_id.id] <> currency_id):
                raise osv.except_osv(
                    _('Error!'),
                    _('You cannot group sales having different currencies for the same partner.'))

            partner_currency[o.partner_id.id] = currency_id
            lines = []
            for line in o.order_line:
                if line.invoiced:
                    continue
                elif (line.state in states):
                    lines.append(line.id)
            created_lines = obj_sale_order_line.invoice_line_create(lines)
            if created_lines:
                invoices.setdefault(o.partner_invoice_id.id or o.partner_id.id, []).append((o, created_lines))
        if not invoices:
            for o in self:
                for i in o.invoice_ids:
                    if i.state == 'draft':
                        return i.id
        for val in invoices.values():
            if grouped:
                res = self._make_invoice(val[0][0], reduce(lambda x, y: x + y, [l for o, l in val], []))
                invoice_ref = ''
                origin_ref = ''
                for o, l in val:
                    invoice_ref += (o.client_order_ref or o.name) + '|'
                    origin_ref += (o.origin or o.name) + '|'
                    o.write({'state': 'progress'})
                    cr.execute('insert into sale_order_invoice_rel (order_id,invoice_id) values (%s,%s)', (o.id, res))
                    self.invalidate_cache(['invoice_ids'], [o.id])
                #remove last '|' in invoice_ref
                if len(invoice_ref) >= 1:
                    invoice_ref = invoice_ref[:-1]
                if len(origin_ref) >= 1:
                    origin_ref = origin_ref[:-1]
                invoice.write({'origin': origin_ref, 'name': invoice_ref, 'consultant_doctor_id': o.physician_id.id})
            else:
                for order, il in val:
                    res = self._make_invoice(order, il)
                    invoice_ids.append(res)
                    order.write({'state': 'progress'})
                    cr.execute('insert into sale_order_invoice_rel (order_id,invoice_id) values (%s,%s)', (order.id, res))
                    self.invalidate_cache(['invoice_ids'], [order.id])
        return res

    @api.model
    def action_ship_create(self):
        """Create the required procurements to supply sales order lines, also connecting
        the procurements to appropriate stock moves in order to bring the goods to the
        sales order's requested location.

        :return: True
        """
        procurement_obj = self.env['procurement.order']
        sale_line_obj = self.env['sale.order.line']
        for order in self:
            proc_ids = []
            vals = self._prepare_procurement_group(order)
            if not order.procurement_group_id:
                group_id = self.env["procurement.group"].create(vals)
                order.write({'procurement_group_id': group_id})

            for line in order.order_line:
                #Try to fix exception procurement (possible when after a shipping exception the user choose to recreate)
                if line.procurement_ids:
                    #first check them to see if they are in exception or not (one of the related moves is cancelled)
                    procurement_obj.check([x.id for x in line.procurement_ids if x.state not in ['cancel', 'done']])
                    line.refresh()
                    #run again procurement that are in exception in order to trigger another move
                    proc_ids += [x.id for x in line.procurement_ids if x.state in ('exception', 'cancel')]
                    procurement_obj.reset_to_confirmed(proc_ids)
                elif sale_line_obj.need_procurement([line.id]):
                    if (line.state == 'done') or not line.product_id:
                        continue
                    vals = self._prepare_order_line_procurement(order, line, group_id=order.procurement_group_id.id)
                    proc_id = procurement_obj.create(vals)
                    proc_ids.append(proc_id)
            #Confirm procurement order such that rules will be applied on it
            #note that the workflow normally ensure proc_ids isn't an empty list
            print "proc_ids", order, proc_ids
            procurement_obj.run(proc_ids)

            #if shipping was in exception and the user choose to recreate the delivery order, write the new status of SO
            if order.state == 'shipping_except':
                val = {'state': 'progress', 'shipped': False}

                if (order.order_policy == 'manual'):
                    for line in order.order_line:
                        if (not line.invoiced) and (line.state not in ('cancel', 'draft')):
                            val['state'] = 'manual'
                            break
                order.write(val)

            self.action_stock_move(order)
        return True
    
    @api.model
    def action_stock_move(order):
        stock_ids = []
        delivery_order_obj = self.env['stock.picking']     
        stock_move_obj = self.env['stock.move']      
        stock_location_obj = self.env['stock.location']
                 
#        for so in self.browse(cursor, user, ids, context=context):
        delivery_order_obj.action_confirm(order.picking_ids.id)
        delivery_order_obj.force_assign(order.picking_ids.id)
        delivery_order_obj.do_enter_transfer_details(order.picking_ids.id)
        for line in order.order_line:
            transfer_id = self.env['stock.pack.operation'].search([('product_id', '=', line.product_id.id),('picking_id','=',order.picking_ids.id)])
            transfer_id.write({'lot_id': line.batch_no.id})

        delivery_order_obj.do_transfer(order.picking_ids.id) 
        return True
    
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_id = fields.Many2one('product.product',string='Product', domain=[('sale_ok', '=', True),('hospital_product_type', '=', 'medicament')], change_default=True, readonly=True, states={'draft': [('readonly', False)]}, ondelete='restrict')
    batch_no = fields.Many2one("stock.production.lot",string="Batch Number")
    exp_date = fields.Datetime(string="Expiry Date")

    @api.onchange('batch_no')
    def onchange_batch(self):
        if not self.batch_no:
            return {'value': {}}
        self.exp_date = self.batch_no.use_date
        
    def _prepare_order_line_invoice_line(self, line, account_id=False):
        """Prepare the dict of values to create the new invoice line for a
           sales order line. This method may be overridden to implement custom
           invoice generation (making sure to call super() to establish
           a clean extension chain).

           :param browse_record line: sale.order.line record to invoice
           :param int account_id: optional ID of a G/L account to force
               (this is used for returning products including service)
           :return: dict of values to create() the invoice line
        """
        res = {}
        if not line.invoiced:
            if not account_id:
                if line.product_id:
                    account_id = line.product_id.property_account_income.id
                    if not account_id:
                        account_id = line.product_id.categ_id.property_account_income_categ.id
                    if not account_id:
                        raise osv.except_osv(_('Error!'),
                                _('Please define income account for this product: "%s" (id:%d).') % \
                                    (line.product_id.name, line.product_id.id,))
                else:
                    prop = self.env['ir.property'].get(cr, uid,
                            'property_account_income_categ', 'product.category',
                            context=context)
                    account_id = prop and prop.id or False
            uosqty = self._get_line_qty(line)
            uos_id = self._get_line_uom(line)
            pu = 0.0
            if uosqty:
                pu = round(line.price_unit * line.product_uom_qty / uosqty,
                        self.env['decimal.precision'].precision_get('Product Charges'))
            fpos = line.order_id.fiscal_position or False
            account_id = self.env['account.fiscal.position'].map_account(fpos, account_id)
            if not account_id:
                raise osv.except_osv(_('Error!'),
                            _('There is no Fiscal Position defined or Income category account defined for default properties of Product categories.'))
            res = {
                'name': line.name,
                'sequence': line.sequence,
                'origin': line.order_id.name,
                'account_id': account_id,
                'price_unit': pu,
                'quantity': uosqty,
                'discount': line.discount,
                'uos_id': uos_id,
                'product_id': line.product_id.id or False,
                'invoice_line_tax_id': [(6, 0, [x.id for x in line.tax_id])],
                'account_analytic_id': line.order_id.project_id and line.order_id.project_id.id or False,
                'lot': line.batch_no.id,
                'life_date': line.exp_date,
            }

        return res

class AccountVoucher(models.Model):
    _inherit = 'account.voucher'

    # advance_account_id = fields.Many2one('account.account',string='Advance Account', required=False,readonly=True, states={'draft': [('readonly', False)]})

    def button_proforma_voucher(self):
        res = super(AccountVoucher, self).button_proforma_voucher()
        invoice_obj = self.env['account.invoice']
        picking_obj = self.env['stock.picking']
        so_obj = self.env['sale.order']
        pick_ids = []
        for data in invoice_obj.browse(context.get('active_ids')):
            if data.origin:
                pick_ids = picking_obj.search([('name','=', data.origin)])
            if not pick_ids and data.origin:
                pick_ids = picking_obj.search([('origin','=', data.origin)])
            for pick in picking_obj.browse(pick_ids):
                so_ids = so_obj.search([('name','=',pick.origin)])
                if data.state == 'paid':
                    for order in so_obj.browse(so_ids):
                        self.env['sale.order.line'].write([line.id for line in order.order_line], {'state': 'done'})
                    so_ids.write({'state': 'done'})
        super(AccountVoucher, self).button_proforma_voucher()
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: