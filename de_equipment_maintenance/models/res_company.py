# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = 'res.company'
    
    #maintenance_location_id = fields.Many2one('stock.location')
    
    def _create_maintenance_location(self):
        parent_location = self.env.ref('stock.stock_location_locations_virtual', raise_if_not_found=False)
        
        for company in self:
            maintenance_location = self.env['stock.location'].create({
                'name': _('%s: Maintenance Location') % company.name,
                'usage': 'production',
                'location_id': parent_location.id,
                'company_id': company.id,
            })
            
    def _create_per_company_locations(self):
        super(ResCompany, self)._create_per_company_locations()
        self._create_maintenance_location()
        
        
    @api.model
    def create_missing_maintenance_location(self):
        #company_without_maintenance_loc = self.env['res.company'].search(
        #    [('maintenance_location_id', '=', False)])
        #company_without_maintenance_loc._create_maintenance_location()
        self._create_maintenance_location()
    
    
    