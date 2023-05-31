{
    'name': "Real Estate",
    'version': '1.0',
    'author': "Yonattan",
    'category': 'Real Estate',
    'description': "Desc",
    # 'website': 'https://www.odoo.com/page/crm',
    'depends': ['base'],
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
    ],
    # data files containing optionally loaded demonstration data
    # 'demo': [
    #     'demo/demo_data.xml',
    # ],
    # 'css': ['static/src/css/crm.css'],
    'installable': True,
    'application': True,
    'auto_install': False
}