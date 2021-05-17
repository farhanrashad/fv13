# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

{
    'name': 'Material Requisitions from Manufacturing / Workorder',
    'version': '1.0',
    'price': 39.0,
    'depends': [
                'mrp',
                'material_purchase_requisitions',
                ],
    'currency': 'EUR',
    'license': 'Other proprietary',
    'summary': """This module allow production team to create Material Requisition during production and work order process.""",
    'description': """

Manufacturing Material Requisition
production Material Requisition
mrp Material Requisition
Material Requisitions from Manufacturing / Workorder
Manufacturing Requisition
production Requisition
mrp Requisition
Manufacturing internal Requisition
production internal Requisition
mrp internal Requisition
work order Requisition
workorder Requisition
work order material Requisition

Material Purchase Requisitions
This module allowed Purchase requisition of employee.
Purchase_Requisition_Via_iProcurement
Purchase Requisitions
Purchase Requisition
iProcurement
Inter-Organization Shipping Network
Online Requisitions
Issue Enforcement
Inventory Replenishment Requisitions
Replenishment Requisitions
MRP Generated Requisitions
generated Requisitions
purchase Sales Orders
Complete Requisitions Status Visibility
Using purchase Requisitions
purchase requisitions
replenishment requisitions
employee Requisition
employee purchase Requisition
user Requisition
stock Requisition
inventory Requisition
warehouse Requisition
factory Requisition
department Requisition
manager Requisition
Submit requisition
Create purchase Orders
purchase Orders
product Requisition
item Requisition
material Requisition
product Requisitions
material purchase Requisition
material Requisition purchase
purchase material Requisition
product purchase Requisition
item Requisitions
material Requisitions
products Requisitions
purchase Requisition Process
Approving or Denying the purchase Requisition
Denying purchase Requisition​
construction managment
real estate management
construction app
Requisition
Requisitions
internal Requisitions
* INHERIT hr.department.form.view (form)
* INHERIT hr.employee.form.view (form)
* INHERIT stock.picking.form.view (form)
purchase.requisition search (search)
purchase.requisition.form.view (form)
purchase.requisition.view.tree (tree)
purchase_requisition (qweb)
Main Features:
allow your employees to Create Purchase Requisition.
Employees can request multiple material/items on single purchase Requisition request.
Approval of Department Head.
Approval of Purchase Requisition Head.
Email notifications to Department Manager, Requisition Manager for approval.
- Request for Purchase Requisition will go to stock/warehouse as internal picking / internal order and purchase order.
- Warehouse can dispatch material to employee location and if material not present then procurment will created by Odoo standard.
- Purchase Requisition user can decide whether product requested by employee will come from stock/warehouse directly or it needs to be purchase from vendor. So we have field on requisition lines where responsible can select Requisition action: 1. Purchase Order 2. Internal Picking. If option 1 is selected then system will create internal order / internal picking request and if option 2 is selected system will create multiple purchase order / RFQ to vendors selected on lines.
- For more details please see Video on live preview or ask us by email...
Internal_Requisition_Via_iProcurement
Internal Requisitions
Internal Requisition
iProcurement
Inter-Organization Shipping Network
Online Requisitions
Issue Enforcement
Inventory Replenishment Requisitions
Replenishment Requisitions
MRP Generated Requisitions
generated Requisitions
Internal Sales Orders
Complete Requisitions Status Visibility
Using Internal Requisitions
purchase requisitions
replenishment requisitions
employee Requisition
employee Internal Requisition
user Requisition
stock Requisition
inventory Requisition
warehouse Requisition
factory Requisition
department Requisition
manager Requisition
Submit requisition
Create Internal Orders
Internal Orders
product Requisition
item Requisition
material Requisition
product Requisitions
item Requisitions
material Requisitions
products Requisitions
Internal Requisition Process
Approving or Denying the Internal Requisition
Denying Internal Requisition​
Added Create Material Requisitions Wizard on Manufacturing Order
Added Create Material Requisitions Wizard on work Order
Create Material Requisitions Wizard on Manufacturing Order
Create Material Requisitions Wizard on work Order
    """,
    'author': 'Probuse Consulting Service Pvt. Ltd.',
    'website': 'http://www.probuse.com',
    'support': 'contact@probuse.com',
    'images': ['static/description/img1.jpg'],
    'live_test_url': 'https://youtu.be/8g6DAu2PYa8',
    'category': 'Manufacturing',
    'data':[
            'wizard/material_purchase_requistion_mrp.xml',
            'wizard/material_purchase_requistion_workorder.xml',
            'views/mrp_view.xml',
            'views/material_purchase_requistion_views.xml',
            'views/mrp_workorder_view.xml',
    ],
    'installable' : True,
    'application' : False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
