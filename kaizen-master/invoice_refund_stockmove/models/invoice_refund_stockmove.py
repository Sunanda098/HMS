# -*- coding: utf-8 -*-

from openerp import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.model
    def _get_default_warehouse(self):
        company_id = self.env.user.company_id.id
        warehouse_ids = self.env['stock.warehouse'].search([('company_id', '=', company_id)], limit=1)
        return warehouse_ids

    @api.model
    def _get_picking_type(self):
        stock_picking_type_obj = self.env['stock.picking.type']
        company_id = self.env.user.company_id.id
        res = stock_picking_type_obj.search([('name', '=', 'Receipts'),('company_id', '=', company_id)],
                                                limit=1)
        return res and res[0] or False  

    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse', default=_get_default_warehouse)
    source_location_id = fields.Many2one('stock.location', 'Source Location')
    destination_location_id = fields.Many2one('stock.location', 'Destination Location')

    @api.model
    def invoice_validate(self):
        res = super(AccountInvoice, self).invoice_validate()
        stock_ids = []
        delivery_order_obj = self.env['stock.picking']
        stock_move_obj = self.env['stock.move']
        stock_location_obj = self.env['stock.location']
                 
        for so in self:
            if so.type == 'out_refund':
                picking_type_id = self.env['stock.picking.type'].search([('name', '=', 'Receipts'),('warehouse_id', '=', so.warehouse_id.id)], limit=1)
                location_id = stock_location_obj.search(cr, uid, [('name', '=', 'Partner Locations')], limit=1)
                dic = {
                'partner_id' : so.partner_id.id,
                'date' : fields.datetime.now(), 
                'company_id': so.company_id.id,
                'picking_type_id': picking_type_id[0]
                }
                new_id = delivery_order_obj.create(dic)  
                for line in so.invoice_line:
                    stock_move_dic = {
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.quantity,
                        'product_uom': line.uos_id.id,
                        'date': fields.datetime.now(),
                        'date_expected': fields.datetime.now(),
                        'picking_id': new_id,
                        'invoice_state': 'none',
                        'state': 'draft',
                        'name': line.name,
                    }   
                    stock_move_dic['location_id'] = stock_location_obj.search([('name','=','Customers'),('location_id','=', location_id[0])], limit=1)[0]
                    stock_move_dic['location_dest_id'] = stock_location_obj.search([('name','=','Stock'),('company_id','=', so.company_id.id)], limit=1)[0]
                    stock_move_obj.create(stock_move_dic)  
                delivery_order_obj.action_confirm([new_id])
                delivery_order_obj.action_assign([new_id])
                delivery_order_obj.force_assign([new_id])                
                delivery_order_obj.do_enter_transfer_details([new_id])                    
                for line in so.invoice_line:
                    transfer_id = self.env['stock.pack.operation'].search([('product_id', '=', line.product_id.id),('picking_id','=',new_id)])
                    transfer_id.write({'lot_id': line.lot.id})                

                delivery_order_obj.do_transfer([new_id])                            
            elif so.type == 'in_refund':
                picking_type_id = self.env['stock.picking.type'].search([('name', '=', 'Delivery Orders'),('warehouse_id', '=', so.warehouse_id.id)], limit=1)
                location_id = stock_location_obj.search([('name', '=', 'Partner Locations')], limit=1)
                dic = {
                'partner_id' : so.partner_id.id,
                'date' : fields.datetime.now(), 
                'company_id': so.company_id.id,
                'picking_type_id': picking_type_id[0]
                }
                new_id = delivery_order_obj.create(dic)  
                for line in so.invoice_line:
                    stock_move_dic = {
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.quantity,
                        'product_uom': line.uos_id.id,
                        'date': fields.datetime.now(),
                        'date_expected': fields.datetime.now(),
                        'picking_id': new_id,
                        'invoice_state': 'none',
                        'state': 'draft',
                        'name': line.name,
                    }   
                    stock_move_dic['location_id'] = stock_location_obj.search([('name','=','Stock'),('company_id','=', so.company_id.id)], limit=1)[0]
                    stock_move_dic['location_dest_id'] = stock_location_obj.search([('name','=','Suppliers'),('location_id','=', location_id[0])], limit=1)[0]
                    stock_move_obj.create(stock_move_dic)  
                delivery_order_obj.action_confirm([new_id])
                delivery_order_obj.action_assign([new_id])
                delivery_order_obj.force_assign([new_id])                
                delivery_order_obj.do_enter_transfer_details([new_id])                    
                for line in so.invoice_line:
                    transfer_id = self.env['stock.pack.operation'].search([('product_id', '=', line.product_id.id),('picking_id','=',new_id)])
                    transfer_id.write({'lot_id': line.lot.id})                

                delivery_order_obj.do_transfer([new_id])                            

        return res

