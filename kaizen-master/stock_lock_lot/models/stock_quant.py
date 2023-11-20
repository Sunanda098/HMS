# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    locked = fields.Boolean(
        string='Blocked', related="lot_id.locked", default=False,
        store=True)

    @api.model
    def _get_inventory_value(self, quant):
        try:
            return (quant.lot_id.purchase_price / quant.lot_id.purchase_uom.factor_inv) * quant.qty 
        except:
            return super(StockQuant, self)._get_inventory_value(quant)

    @api.model
    def quants_get(self, location, product, qty, domain=None,
                   restrict_lot_id=False, restrict_partner_id=False):
        if domain is None:
            domain = []
        domain += [('locked', '=', False)]
        return super(StockQuant, self).quants_get(
            location, product, qty, domain=domain,
            restrict_lot_id=restrict_lot_id,
            restrict_partner_id=restrict_partner_id)
