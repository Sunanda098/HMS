# -*- coding: utf-8 -*-

from openerp import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    manufacturer = fields.Many2one('res.partner', 'Manufacturer')
    manufacturer_pname = fields.Char('Manufacturer Product Name')
    manufacturer_pref = fields.Char('Manufacturer Product Code')
    manufacturer_purl = fields.Char('Manufacturer Product URL')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: