# # -*- coding: utf-8 -*-

from openerp import api, fields, models

class IrdaCategory(models.Model):
    _name = 'irda.category'

    name = fields.Char(string='Category')
    code = fields.Char('Code', help="Identify Sub category")
    parent_id = fields.Many2one('irda.category', string='Parent', ondelete="restrict", help='Parent Of the Irda Category Model')
    parent_code = fields.Char('Sub Category', help="Identify Parent Code")

    @api.onchange('parent_id')
    def onchange_parent_id(self):
        for parent in self:
            self.parent_code = parent.parent_id.code or False

    @api.multi
    def action_irda_product(self):
        return {
            'name': ('Product'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'product.template',
            'type': 'ir.actions.act_window',
            'domain': [('irda_category_id','=',self.id)],
        }
  

class ProductProduct(models.Model):
    _inherit ='product.template'

    irda_category_id = fields.Many2one('irda.category', string="Irda Category")

class ResCompany(models.Model):
    _inherit ='res.company'

    pan = fields.Char(string="Pan Nos", size=10)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: