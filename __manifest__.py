# -*- coding: utf-8 -*-
{
    'name': "Keuangan Siswa",

    'summary': """
        Module Keuangan aplikasi database siswa (siswa_ocb11)""",

    'description': """
        Module Keuangan aplikasi database siswa (siswa_ocb11)
    """,

    'author': "Tepat Guna Karya",
    'website': "http://www.tepatguna.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Education',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','siswa_ocb11'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/biaya.xml',
        # 'views/assign_biaya.xml',
        'views/tahunajaran_jenjang.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}