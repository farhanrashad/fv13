{

    'name': 'Invoice Commissions',
    'summary': 'Invoice Commissions for Sales',
    'author': 'Dynexcel',
    'depends':
        [
            'base','hr', 'sale', 'contacts', 'account_accountant', 'sale_management'
        ],
    'data':
        [
            'security/ir.model.access.csv',
            'views/invoice_commission_views.xml',
        ],
    'installable': True,

}