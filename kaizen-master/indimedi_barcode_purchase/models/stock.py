# -*- encoding: utf-8 -*-

from openerp import api, fields, models, SUPERUSER_ID, _

def isodd(x):
    return bool(x % 2)

class stock_production_lot(models.Model):
    _inherit = 'stock.production.lot'

    barcode = fields.Char(string='EAN13 Barcode', size=13, help="International Article Number used for product identification.")
    generate_ean = fields.Boolean(string='Generate Ean13', default=False, copy=False)

    _sql_constraints = [('ean13_uniq', 'UNIQUE(barcode)', 'Ean13 must be unique!'),]

    @api.onchange('generate_ean')
    def onchange_generate_ean(self):
        if self.generate_ean:
            ean = ''
            if self.product_id.ean_sequence_id:
                ean = self.product_id.ean_sequence_id.next_by_id()
            elif self.product_id.categ_id.ean_sequence_id:
                ean = self.product_id.categ_id.ean_sequence_id.next_by_id()
            elif self.product_id.company_id and self.product_id.company_id.ean_sequence_id:
                ean = product_id.company_id.ean_sequence_id.next_by_id()
            if len(ean) > 12:
                raise orm.except_orm(_("Configuration Error!"),
                     _("There next sequence is upper than 12 characters. This can't work."
                       "You will have to redefine the sequence or create a new one"))
            else:
                ean = (len(ean[0:6]) == 6 and ean[0:6] or ean[0:6].ljust(6,'0')) + ean[6:].rjust(6,'0')
            sum = 0
            for i in range(12):
                if isodd(i):
                    sum += 3 * int(ean[i])
                else:
                    sum += int(ean[i])
            key = (10 - sum % 10) % 10
            ean13 = ean + str(key)
            self.barcode = ean13

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: