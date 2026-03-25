{
    'name': 'TikTok Shop Connector',
    'version': '1.0',
    'author': 'NgocQuy',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/tiktok_order_views.xml',
        'views/tiktok_menu.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}