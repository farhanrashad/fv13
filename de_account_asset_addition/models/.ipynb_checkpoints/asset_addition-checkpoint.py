# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        for line in self.move_line_ids_without_package:
            assets =self.env['account.asset'].search([('name','=',line.asset_id.name)])
            if line.asset_id.name == assets.name: 
                assets.update({
                     'picking_id' : self.name,
                    })  
        return res

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    asset_id = fields.Many2one('account.asset', string="Asset")
    
    
class AccountAsset(models.Model):
    _inherit = 'account.asset'

    picking_id = fields.Char(string="Value Adjustment")    

