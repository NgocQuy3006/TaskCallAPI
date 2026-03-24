{
    'name': 'Shopee Connector',
    'version': '1.0',
    'depends': ['base', 'sale', 'product'],
'data': [
    'security/ir.model.access.csv',
    'views/shopee_order_views.xml',
    'views/res_config_settings_views.xml',
],
    'installable': True,
    'application': True,
}