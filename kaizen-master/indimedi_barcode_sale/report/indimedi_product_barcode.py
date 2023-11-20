import time
from openerp import api, fields, models
from openerp.report import report_sxw


class indimedi_product_barcode(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(indimedi_product_barcode, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_columns': self._get_columns,
            'get_rows': self._get_rows,
            'get_quantity': self._get_quantity,
            'get_starting_position': self._get_starting_position,
        })
        
    def _get_columns(self, form):
        self.columns = form
        return self.columns
    
        
    def _get_rows(self, form):
        self.rows = form['rows']
        
        
    def _get_quantity(self, form):
        self.quantity = form['quantity']
        
        
        
    def _get_starting_position(self, form):
        self.starting_position = form['starting_position']
        
        
class report_product_barcode(models.AbstractModel):
    _name = 'report.indimedi_barcode_sale.report_product_barcode'
    _inherit = 'report.abstract_report'
    _template = 'indimedi_barcode_sale.report_product_barcode'
    _wrapped_report_class = indimedi_product_barcode
        
