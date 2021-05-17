# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from odoo import fields,api,models,_


class pos_user(models.Model):
    _inherit = 'pos.config'

    print_product_summary = fields.Boolean(string="Product Summary Report")
    enable_order_summary = fields.Boolean(string='Enable Order Summary')
    payment_summary = fields.Boolean(string="Payment Summary")
    no_of_copy_receipt = fields.Integer(string="No.of Copy Receipt")
    current_month_date = fields.Boolean(string="Current Month Date")
    signature = fields.Boolean(string="Signature")

#vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
