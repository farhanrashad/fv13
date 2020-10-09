# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    roll = fields.Char(string='Roll', store=True)
    pcs = fields.Char(string='PCS', store=True)

#class StockPicking(models.Model):
#    _inherit = 'stock.picking'

#    @api.model
#    def create(self,vals):
#        po_sale_ref = env['purchase.order'].search([('name','=', self.origin)])
#	for ref in po_sale_ref:
#	    self.update({
 #	     'job_order_new': ref.job_order_id.id,
#	      'ref_sale_new': ref.sale_id.id,
#	      'ref_po_id': ref.id,
#	      })
  #    
#	sale_ref = env['stock.picking'].search([('name','=', self.origin)])
#	for refs in sale_ref: 
#	    self.update({
#	      'ref_sale_new': refs.ref_sale_new.id,
#	      'ref_po_id': refs.ref_po_id.id,
#	      })
 #       res = super(StockPicking,self).create(vals)
  #      return res
  


#class PurchaseOrder(models.Model):
#    _inherit = 'purchase.order'

       

#    def action_view_invoice(self):
#        res = super(PurchaseOrder, self).action_view_invoice()
#        for line in self.order_line:
#            vals= {
#            'total_weight': line.total_weight ,
#            } 
#            move_line = self.env['account.move.line'].update(vals)    
#        return res

 
#    def button_confirm(self):
#        res = super(PurchaseOrder, self).button_confirm()
#        vals= {
#         'job_order_new': self.job_order_id.id ,
#         'ref_sale_new': self.sale_id.id, 
#          } 
#        move = self.env['stock.picking'].update(vals)    
#        return res 





       

   






    


