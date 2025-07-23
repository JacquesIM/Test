{
    'name': 'Tax Rate Table',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Date-based Tax Rates like Currency Exchange',
    'description': 'Manage variable tax rates by date and currency.',
    'depends': ['account'],
    'data': [
    'security/ir.model.access.csv',
    'views/sale_order_view.xml',
    'views/tax_rate_views.xml',
    'views/tax_rate_action.xml',
    'views/tax_rate_menu.xml',
],
    'installable': True,
}