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
    # Check https://github.com/flectra/flectra/blob/master/flectra/addons/base/module/module_data.xml
    # for the full list
    'category': 'Education',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','siswa_ocb11','siswa_tab_ocb11'],

    # always loaded
    'data': [
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        'data/ir_default_data.xml',
        'data/ir_sequence_data.xml',
        'views/biaya.xml',
        'views/siswa_biaya.xml',
        'views/tahunajaran_jenjang.xml',
        'views/wizard_keuangan_siswa.xml',
        'views/wizard_report_kas.xml',
        'views/wizard_report_pembayaran_siswa.xml',
        'views/wizard_pembayaran_harian.xml',
        'views/pembayaran.xml',
        'views/res_siswa.xml',
        'views/kas_kategori.xml',
        'views/kas.xml',
        'views/keuangan_dashboard.xml',
        'views/biaya_ta_jenjang.xml',
        'views/tabungan_view.xml',
        'views/potongan_view.xml',
        'views/wizard_batch_create_potongan_view.xml',
        'report/report_kas_template.xml',
        'report/report_kas.xml',
        'report/report_rekap_kas.xml',
        'report/report_bukti_pembayaran.xml',
        'report/report_pembayaran_siswa_per_biaya.xml',
        'report/report_pembayaran_siswa_per_biaya_bulanan.xml',
        'report/report_pembayaran_harian.xml',
        'report/report_pembayaran_harian_detail.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
} 