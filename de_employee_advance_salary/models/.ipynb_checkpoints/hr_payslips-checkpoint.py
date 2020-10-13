from odoo import models, fields, api, _
from odoo import exceptions 
from datetime import datetime


class HrPayslipsInherit(models.Model):
    _inherit = 'hr.payslip'
    
    def compute_sheet(self):
#         for other_input in self.input_line_ids:
#             other_input.unlink()
        other_inputs = self.env['hr.payslip.input.type'].search([('code','=', 'ADV')])
        paid_amount = self.env['hr.employee.advance.salary'].search([('employee_id','=', self.employee_id.id),('state','=', 'paid'),('request_date','>=', self.date_from),('confirm_date','<=', self.date_to)])
        data = []
        amount = 0
        for input in other_inputs:
            for sal_amount in paid_amount:            
                amount = amount + sal_amount.amount
            data.append((0,0,{
                            'payslip_id': self.id,
                            'sequence': 1,
                            'code': input.code,
                            'contract_id': self.contract_id.id,
                            'input_type_id': input.id,
                            'amount': amount,
                            }))
        self.input_line_ids = data
        res = super(HrPayslipsInherit, self).compute_sheet()
        
        return res
    
    

    
    

            
            