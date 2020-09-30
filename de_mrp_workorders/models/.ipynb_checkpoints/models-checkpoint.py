# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from odoo import exceptions
from odoo.exceptions import UserError, ValidationError


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'
    
    qty_production = fields.Float('Original Production Quantity', readonly=True)
    
    

    
    def do_finish(self):
        res = super(MrpWorkorder, self).do_finish()
        self.time_ids.date_end = datetime.today()
        if self.is_last_unfinished_wo == True:
            raw_material =self.env['mrp.production'].search([('name','=',self.production_id.name)])
            for move_line in raw_material.move_raw_ids:
                if move_line.reserved_availability: 
                    move_line.update({
                        'quantity_done' : move_line.reserved_availability,
                    })  
                elif move_line.product_uom_qty: 
                    move_line.update({
                        'quantity_done' : move_line.product_uom_qty,
                    })
                else:
                    pass
        if self.state == 'done':
            pass
        else:
            self.write({
               'state': 'done',
            })     
        return res
    
    def action_open_manufacturing_order(self):
        raw_material =self.env['mrp.production'].search([('name','=',self.production_id.name)])
        for move_line in raw_material.move_raw_ids:
            if move_line.reserved_availability: 
                    move_line.update({
                        'quantity_done' : move_line.reserved_availability,
                    })  
            elif move_line.product_uom_qty: 
                move_line.update({
                    'quantity_done' : move_line.product_uom_qty,
                    })
            else:
                pass
        res = super(MrpWorkorder, self).action_open_manufacturing_order()  
        return res








class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
#     def action_assign_test(self):
#         for move_line in self.move_raw_ids:
#             if move_line.product_uom_qty: 
#                 move_line.update({
#                     'quantity_done' : move_line.product_uom_qty,
#                 })
    
    
    def action_assign(self):
        res = super(MrpProduction, self).action_assign()
        workorders =self.env['mrp.workorder'].search([('production_id','=',self.name)])
        for workorder in workorders:
            for move_raw in self.move_raw_ids:
                for line in workorder.raw_workorder_line_ids:
                    if line.product_id == move_raw.product_id:
                        line.update({
#                                 'qty_reserved' : (move_raw.reserved_availability),
                            })
                    else:
                        pass
        return res
    
            
    def button_mark_done(self):
        for move_line in self.move_raw_ids:
            if move_line.product_uom_qty: 
                move_line.update({
                    'quantity_done' : move_line.product_uom_qty,
                })
        ress = super(MrpProduction, self).button_mark_done()
       
        return ress  
    
   
    routing_f_id = fields.Many2one(
        'mrp.routing', srting='First Routing', store=True)
    routing_s_id = fields.Many2one(
        'mrp.routing', string='Second Routing', store=True)
    routing_t_id = fields.Many2one(
        'mrp.routing', string='Third Routing', store=True)
    routing_fo_id = fields.Many2one(
        'mrp.routing', string='Four Routing', store=True)
    product_f_qty = fields.Float(string='First Routing Quantity')
    product_s_qty = fields.Float(string='Second Routing Quantity')
    product_t_qty = fields.Float(string='Third Routing Quantity')
    product_fo_qty = fields.Float(string='Four Routing Quantity')
    
    
      
            
    
    
    @api.onchange('routing_f_id')
    def onchange_routing(self):
        if self.routing_f_id.id == 13:
            self.update({
                'routing_s_id': 14,
                'routing_t_id': 15,
                'routing_fo_id': 16,
            })
            
        elif self.routing_f_id.id == 14:
            self.update({
                'routing_s_id': 13,
                'routing_t_id': 15,
                'routing_fo_id': 16
            })
            
        elif self.routing_f_id.id == 15:
            self.update({
                'routing_s_id': 14,
                'routing_t_id': 13,
                'routing_fo_id': 16
            })
            
        elif self.routing_f_id.id == 16:
            self.update({
                'routing_s_id': 14,
                'routing_t_id': 15,
                'routing_fo_id': 13
            })

        elif self.routing_f_id.id == 17:
            self.update({
                'routing_s_id': 20,
                'routing_t_id': 19,
                'routing_fo_id': 18
            })

        elif self.routing_f_id.id == 18:
            self.update({
                'routing_s_id': 20,
                'routing_t_id': 19,
                'routing_fo_id': 17
            })
           
        elif self.routing_f_id.id == 19:
            self.update({
                'routing_s_id': 20,
                'routing_t_id': 18,
                'routing_fo_id': 17
            })

        elif self.routing_f_id.id == 20:
            self.update({
                'routing_s_id': 19,
                'routing_t_id': 18,
                'routing_fo_id': 17
            })
        elif self.routing_f_id.id == 21:
            self.update({
                'routing_s_id': 22,
                'routing_t_id': 23,
                'routing_fo_id': 24
            })

        elif self.routing_f_id.id == 22:
            self.update({
                'routing_s_id': 24,
                'routing_t_id': 23,
                'routing_fo_id': 21
            })

        elif self.routing_f_id.id == 23:
            self.update({
                'routing_s_id': 22,
                'routing_t_id': 23,
                'routing_fo_id': 24
            })

        elif self.routing_f_id.id == 24:
            self.update({
                'routing_s_id': 23,
                'routing_t_id': 22,
                'routing_fo_id': 21
            })
        else:
            pass
                        
    
    
                
    def button_plans(self):
        total_quantity = 0.0
        if self.product_f_qty:
            total_quantity = total_quantity + self.product_f_qty
        if self.product_s_qty:
            total_quantity = total_quantity + self.product_s_qty
        if self.product_t_qty:
            total_quantity = total_quantity + self.product_t_qty
        if self.product_fo_qty:
            total_quantity = total_quantity + self.product_fo_qty 
        if total_quantity > self.product_qty:
            raise exceptions.ValidationError('Routing Quantity must be equal to MO Quantity To Consume')            
        else:        
            if self.routing_f_id != '' and self.product_f_qty != 0.0:

                quantity = max(self.product_f_qty - sum(self.move_finished_ids.filtered(lambda move: move.product_id == self.product_id).mapped('quantity_done')), 0)
                quantity = self.product_id.uom_id._compute_quantity(quantity, self.product_uom_id)

                fval = {
                    'name': self.name,
                    'production_id': self.id,
                    'workcenter_id': self.routing_f_id.id,
    #                 'qty_production': self.product_f_qty,
                    'date_planned_start': self.date_planned_start,
                    'date_planned_finished': self.date_planned_start,                             
                    'product_uom_id': self.product_id.uom_id.id,
                    'is_user_working': True,
                    'quality_check_todo': True,
                    'is_last_step': True,
                    'skipped_check_ids': [],
                    'is_last_lot': True,
                    'operation_id': self.routing_f_id.operation_ids.id,
                    'duration_expected': self.routing_f_id.operation_ids.time_cycle,
                    'state':'ready' or 'pending',
                    'qty_production': self.product_f_qty,
                    'company_id': self.company_id.id,
                    'company_id': self.company_id.id,
                    'qty_remaining': self.product_f_qty,                            
                    'qty_producing': quantity,
                    'consumption': self.bom_id.consumption,
    #                  'raw_workorder_line_ids': [(0, 0, flines)]

                }
                workorders = self.env['mrp.workorder'].create(fval)
                for line in self.move_raw_ids:
                    for lines in self.bom_id.bom_line_ids:
                        quant= 0.0 
                        if line.product_id.id == lines.product_id.id:
                            quant = lines.product_qty
                            flines = {
                                'raw_workorder_id': workorders.id,
                                'product_id': line.product_id.id,
                                'qty_to_consume': (line.product_uom_qty / self.product_qty) * self.product_f_qty ,
                                'qty_reserved': (line.reserved_availability / self.product_qty) * self.product_f_qty,
                                'product_uom_id': line.product_uom.id,
            #                     'qty_done': self.product_f_qty,

                            }

                            workorder_lines = self.env['mrp.workorder.line'].create(flines)
            else:
                pass

            if self.routing_s_id != '' and self.product_s_qty != 0.0:
                work_orders_line = self.env['mrp.workorder.line']
                quantity = max(self.product_s_qty - sum(self.move_finished_ids.filtered(lambda move: move.product_id == self.product_id).mapped('quantity_done')), 0)
                quantity = self.product_id.uom_id._compute_quantity(quantity, self.product_uom_id)

                sval = {
                    'name': self.name,
                    'production_id': self.id,
                    'workcenter_id': self.routing_s_id.id,
                    'date_planned_start': self.date_planned_start,
                    'date_planned_finished': self.date_planned_start,             
                    'product_uom_id': self.product_id.uom_id.id,
                    'is_user_working': True,
                    'quality_check_todo': True,
                    'is_last_step': True,
                    'skipped_check_ids': [],
                    'is_last_lot': True,
                    'operation_id': self.routing_s_id.operation_ids.id,
                    'duration_expected': self.routing_s_id.operation_ids.time_cycle,
                    'state':'ready' or 'pending',
                    'qty_production': self.product_s_qty,
                    'company_id': self.company_id.id,

                    'qty_remaining': self.product_s_qty,               
                    'qty_producing': quantity,
                    'consumption': self.bom_id.consumption,
    #                  'raw_workorder_line_ids': [(0, 0, slines)]

                }
                workorders = self.env['mrp.workorder'].create(sval)
                for line in self.move_raw_ids:
                    for lines in self.bom_id.bom_line_ids:
                        quant= 0.0 
                        if line.product_id.id == lines.product_id.id:
                            quant = lines.product_qty
                            slines = {
                                'raw_workorder_id': workorders.id,
                                'product_id': line.product_id.id,
                                'qty_to_consume': (line.product_uom_qty / self.product_qty) * self.product_s_qty,
                                'qty_reserved': (line.reserved_availability / self.product_qty) * self.product_s_qty,
                                'product_uom_id': line.product_uom.id,
            #                     'qty_done': self.product_s_qty,
                            }
                            workorder_lines = self.env['mrp.workorder.line'].create(slines)
            else:
                pass

            if self.routing_t_id != '' and self.product_t_qty != 0.0:
                work_ordert_line = self.env['mrp.workorder.line']
                quantity = max(self.product_t_qty - sum(self.move_finished_ids.filtered(lambda move: move.product_id == self.product_id).mapped('quantity_done')), 0)
                quantity = self.product_id.uom_id._compute_quantity(quantity, self.product_uom_id)

                tval = {
                    'name': self.name,
                    'production_id': self.id,
                    'workcenter_id': self.routing_t_id.id,
                    'date_planned_start': self.date_planned_start,
                    'date_planned_finished': self.date_planned_start,
                    'company_id': self.company_id.id,
                    'product_uom_id': self.product_id.uom_id.id,
                    'operation_id': self.routing_t_id.operation_ids.id,
                    'duration_expected': self.routing_t_id.operation_ids.time_cycle,
                    'state':'ready' or 'pending',
                    'qty_production': self.product_t_qty,
                    'company_id': self.company_id.id,
                    'is_user_working': True,
                    'quality_check_todo': True,
                    'is_last_step': True,
                    'skipped_check_ids': [],
                    'is_last_lot': True,
                    'qty_remaining': self.product_t_qty,               
                    'qty_producing': quantity,
                    'consumption': self.bom_id.consumption,
    #                  'raw_workorder_line_ids': [(0, 0, tlines)]
                }
                workorders = self.env['mrp.workorder'].create(tval)
                for line in self.move_raw_ids:
                    for lines in self.bom_id.bom_line_ids:
                        quant= 0.0 
                        if line.product_id.id == lines.product_id.id:
                            quant = lines.product_qty
                            tlines = {
                                'raw_workorder_id': workorders.id,                    
                                'product_id': line.product_id.id,
                                'qty_to_consume': (line.product_uom_qty / self.product_qty) * self.product_t_qty,
                                'qty_reserved': (line.reserved_availability / self.product_qty) * self.product_t_qty,
                                'product_uom_id': line.product_uom.id,       
            #                     'qty_done': self.product_t_qty,
                            }
                            workorder_lines = self.env['mrp.workorder.line'].create(tlines)
            else:
                pass

            if self.routing_fo_id != '' and self.product_fo_qty != 0.0:
                work_orderfo_line = self.env['mrp.workorder.line']
                quantity = max(self.product_fo_qty - sum(self.move_finished_ids.filtered(lambda move: move.product_id == self.product_id).mapped('quantity_done')), 0)
                quantity = self.product_id.uom_id._compute_quantity(quantity, self.product_uom_id)

                foval = {
                    'name': self.name,
                    'production_id': self.id,
                    'workcenter_id': self.routing_fo_id.id,
                    'date_planned_start': self.date_planned_start,
                    'date_planned_finished': self.date_planned_start,
                    'company_id': self.company_id.id,
                    'product_uom_id': self.product_id.uom_id.id,
                    'operation_id': self.routing_fo_id.operation_ids.id,
                    'duration_expected': self.routing_fo_id.operation_ids.time_cycle,
                    'state':'ready' or 'pending',
    #                 'qty_production': self.product_fo_qty,
                     'qty_production': self.product_fo_qty, 
                     'company_id': self.company_id.id,
                    'is_user_working': True,
                    'quality_check_todo': True,
                    'is_last_step': True,
                    'skipped_check_ids': [],
                    'is_last_lot': True,
                     'qty_remaining': self.product_fo_qty,               
                    'qty_producing': quantity,
                    'consumption': self.bom_id.consumption,
    #                 'raw_workorder_line_ids': [(0, 0, folines)]
                } 
                workorders = self.env['mrp.workorder'].create(foval)
                for line in self.move_raw_ids:
                    for lines in self.bom_id.bom_line_ids:
                        quant= 0.0 
                        if line.product_id.id == lines.product_id.id:
                            quant = lines.product_qty
                            folines = {
                                'raw_workorder_id': workorders.id,                    
                                'product_id': line.product_id.id,
                                'qty_to_consume': (line.product_uom_qty / self.product_qty) * self.product_fo_qty ,
                                'qty_reserved':  (line.reserved_availability / self.product_qty) * self.product_fo_qty , 
                                'product_uom_id': line.product_uom.id,                  
            #                     'qty_done': self.product_fo_qty,                   
                            }
                            workorder_lines = self.env['mrp.workorder.line'].create(folines)
            else:
                pass

    
