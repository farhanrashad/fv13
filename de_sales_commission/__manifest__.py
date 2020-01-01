# -*- coding: utf-8 -*-
#############################################################################
#
#    Dynexcel.
#
#    Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Akhilesh N S (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
{
    'name': 'Sales Commission',
    'version': '0.2',
    'summary': """To address a contact, sale or invoice in care of someone else""",
    'description': """Calculate and Print report for Sales Care of commission""",
    'author': "Dynexcel",
    'company': 'Dynexcel',
    'maintainer': 'Dynexcel',
    'website': "https://www.dynexcel.com",
    'category': 'Accounting',
    'depends': ['base','sale','sales_team','account'],
    'data': [
        #'views/res_config_settings_views.xml',
        'views/res_partner_views.xml',
        'security/ir.model.access.csv',
        'data/sales_commission_seq.xml',
        'views/sale_order_views.xml',
        'wizard/sales_commission_invoice_views.xml',
        'views/sales_commission_views.xml',
        #'views/invoice_views.xml',
        #'views/report_care_of_commission_templates.xml',
        #'wizard/care_of_partner_report_view.xml',
        #'reports/report.xml',
    ],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
