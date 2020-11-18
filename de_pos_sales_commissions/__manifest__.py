{

    'name': 'Pos sales Commissions',
    'description': 'For daily needs data',
    'author': 'dynexcel',
    'depends':
        [
            'base',
            'sale',
            'sales_team',
            'hr_payroll',
            'hr',
            'point_of_sale',
            'account',
        ],
    'data':
        [
            'security/ir.model.access.csv',
            'views/pos_sales.xml',
            'views/report_wizard.xml',
        ],
    'installable': True,

}