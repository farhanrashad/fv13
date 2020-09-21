from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import format_date


class MoBeforhandWizard(models.TransientModel):
    _name = 'mrp.mo.beforehand.wizard'
    _description = 'Create PO from MO'

    mrp_id = fields.Many2many('mrp.production',string="Manufacturing Order")
    mo_line_ids = fields.One2many('mrp.mo.beforehand.wizard.line','mo_id',string="Manufacturing Order")

    

    
    
    
class MoBeforhandWizardLine(models.TransientModel):
    _name = 'mrp.mo.beforehand.wizard.line'
    _description = 'Create PO from MO'

    product_id = fields.Many2one('product.product',string="Product")
    product_uom_qty = fields.Float(string='Qty to consume')
    on_hand_qty = fields.Float(string="Quantity On Hand")
    forcast_qty = fields.Float(string="Forcast Quantity")
    mo_id = fields.Many2one('mrp.mo.beforehand.wizard',string="Product")    

