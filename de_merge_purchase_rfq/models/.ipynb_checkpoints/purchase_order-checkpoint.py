# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2020-today Dynexcel Business Solution <www.dynexcel.co>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#
#################################################################################

from odoo import api,fields,models,_
from odoo.exceptions import ValidationError

class PurchaseOrder(models.Model):
    _inherit ='purchase.order'
    
    merge_id = fields.Many2one('purchase.order', string='Merged PO')
    po_merged = fields.Boolean(string='PO Merged')


    
    
    
    # Define function to split purchase ordeline when we click on button
    def btn_merge_rfq(self):
        for record in self: 
            for mergepo in self.merge_id:
                data = []
                for merge_line in record.order_line:
                    if merge_line.merge == True:
                        data.append((0,0,{
                            'order_id': record.name,
                            'date_planned': record.date_order,
                            'product_id': merge_line.product_id.id,
                            'name': merge_line.product_id.name,
                            'product_qty': merge_line.product_qty,
                            'product_uom': merge_line.product_uom.id,
                            'price_unit': merge_line.price_unit,
    #                         'taxes_id': merge_line.taxes_id.id,
                            'price_subtotal': merge_line.price_subtotal,
                                }))                        
                        record.update ({
                        'po_merged': True,
                            })    
                mergepo.order_line = data
                
                for merge_line in record.order_line:
                        if merge_line.merge == True:
                            self.env['purchase.order.line'].browse(merge_line.id).unlink() 
                            record.update ({
                             'merge_id': False,
                              })                  
            
                

