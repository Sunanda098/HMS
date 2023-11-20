# coding=utf-8

from openerp import api, fields, models
from openerp.tools.translate import _
from openerp.exceptions import UserError, ValidationError
import openerp.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    request_srore_id = fields.Many2one('store.request',string="Request")


class ProductUoM(models.Model):
    _inherit = 'product.uom'

    @api.multi
    def _compute_quantity(self, qty, to_unit, round=True, rounding_method='UP'):
        if not self:
            return qty
        self.ensure_one()
        if self.category_id.id != to_unit.category_id.id:
            if self._context.get('raise-exception', True):
                raise UserError(_('Conversion from Product UoM %s to Default UoM %s is not possible as they both belong to different Category!.') % (self.name, to_unit.name))
            else:
                return qty
        amount = qty / self.factor
        if to_unit:
            amount = amount * to_unit.factor
            if round:
                amount = tools.float_round(amount, precision_rounding=to_unit.rounding, rounding_method=rounding_method)
        return amount


class StoreRequest(models.Model):
    _name = 'store.request'
    _rec_name='sequence_number'

    name = fields.Char(string='Name')
    sequence_number = fields.Char(string='Sequence',readonly=1)
    state = fields.Selection([
             ('draft', 'Draft'), ('confirm', 'To Approve'),
             ('approved', 'Approved'),('done', 'Done')],
           'Stages', default='draft')
    
    order_lines = fields.One2many('product.template', 'request_srore_id', string="Stock Moves", copy=True)
    employee_id = fields.Many2one('hr.employee',string="Requested by",)
    priority = fields.Selection([
             ('0', 'Low'), ('1', 'Medium'),
             ('2', 'High'), ('3', 'Highest')],
           'Priority', required=True, default='0')
    picking_type_id = fields.Many2one('stock.picking.type', 'Picking Type', required=True, domain="[('code','=','internal')]")
    move_type = fields.Selection([('direct', 'Partial'), ('one', 'All at once')],'Delivery Method', required=True,help="It specifies goods to be deliver partially or all at once",default='direct')

    move_product_lines = fields.One2many('stock.product', 'picking_id', string="Stock Moves")

    location_id = fields.Many2one('stock.location', required=True, string="Location From", readonly=True, states={'draft': [('readonly', False)]},domain=[('usage','=','internal')])
    location_dest_id = fields.Many2one('stock.location', required=True,string="Location To",readonly=True, states={'draft': [('readonly', False)]},domain=[('usage','=','internal')])
    @api.model
    def create(self, vals):
        res = super(StoreRequest, self).create(vals)
        requests = self.env['store.request'].search([('state','in',['draft','confirm'])])[:-1]
        if requests:
          raise ValidationError(_("You have already request %s in %s stage.") % (requests.name,str(requests.state)))
        res.sequence_number = self.env['ir.sequence'].next_by_code('store.request') or '/'
        return res


    @api.multi
    def confirm(self):
        self.send_mail()
        self.state = 'confirm'

    @api.multi
    def send_mail(self):
        if self.state == 'draft' :
            template = self.env.ref('store_management.product_request_email_template')
            ctx = dict(email1 = self.location_id.partner_id.email,
                    products = self.move_product_lines,
                    store_partner = self.location_dest_id.partner_id.name,
                    department = self.location_dest_id.name,

                    )
            if template:
              template.email_from = self.location_dest_id.partner_id.email
              email = self.env['mail.template'].with_context(ctx).browse(template.id).send_mail(self.id, force_send=True)
        else:
            template = self.env.ref('store_management.product_request_approved_email_template')
            ctx = dict(email1 = self.location_dest_id.partner_id.email,
                    products = self.move_product_lines,
                    store_partner = self.location_id.partner_id.name,
                    )
            if template:
              template.email_from = self.location_id.partner_id.email
              email = self.env['mail.template'].with_context(ctx).browse(template.id).send_mail(self.id, force_send=True)



    @api.onchange('priority')
    def onchange_picking_type(self):
        for pick_type in self:
            picking_type_id = pick_type.env['stock.picking.type'].search([('name','=','Internal Transfers')])[0]
            if picking_type_id :
                pick_type.picking_type_id = picking_type_id.id

    @api.onchange('location_id','location_dest_id')
    def onchange_location(self):
        for location in self:
            if location.location_id and not location.location_id.partner_id :
                raise ValidationError(_("Please Allocate location Owner."))
            if location.location_id and not location.location_id.partner_id.email:
                raise ValidationError(_("Please Allocate location Owner Email."))


    @api.multi
    def approve_request(self):
        self.send_mail()
        if self.state == 'confirm':
            stock_picking_rec = self.env['stock.picking'].create({
                'location_id':self.location_id.id,
                'location_dest_id':self.location_dest_id.id,
                'origin':self.sequence_number,
                'move_type':self.move_type,
                'priority': self.priority,
                'picking_type_id':self.picking_type_id.id,
                'move_lines': [(0, 0, {
                    'name':self.sequence_number,
                    'product_id':val.product_id.id,
                    'product_uom_qty':val.qty_received,
                    'product_uom':val.product_uom.id,
                    'state':'draft',
                    'location_id':self.employee_id.user_id.partner_id.property_stock_customer.id,
                    'location_dest_id': self.employee_id.user_id.partner_id.property_stock_customer.id
                    })\
                    for val in self.move_product_lines],
                })
            stock_picking_rec.action_confirm()
            stock_picking_rec.force_assign()
            wiz_id = self.env['stock.immediate.transfer'].create({'pick_id': stock_picking_rec.id})
            wiz_id.process()
            self.state = 'done'


# class StockPicking(models.Model):
#     _inherit = 'stock.picking'

#     request_sequence = fields.Char('Request Number')


class StockMoveProduct(models.Model):
    _name = 'stock.product'

    name = fields.Char('Name')
    product_id = fields.Many2one('product.product', 'Product', required=True, select=True, domain=[('type', 'in', ['product', 'consu'])])
    picking_id = fields.Many2one('stock.request', 'Transfer Reference')  
    product_uom_qty = fields.Float(
        'Quantity',
        digits=dp.get_precision('Product Unit of Measure'),
        default=1.0, required=True)
    qty_received = fields.Float('Received')
    product_uom = fields.Many2one(
        'product.uom', 'Unit of Measure',related='product_id.uom_id')

    @api.multi 
    @api.onchange('product_id')
    def onchange_product(self):
        res = {}
        if self.product_id:
            product = self.env['product.product'].browse(self.product_id.id)
            res = {'domain':{'product_uom': [('category_id','=',product.uom_id.category_id.id)]}}
        return res
