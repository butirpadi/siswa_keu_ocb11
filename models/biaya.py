# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

class biaya(models.Model):
    _name = 'siswa_keu_ocb11.biaya'
    name = fields.Char(string='Nama', requred=True)
    is_bulanan = fields.Boolean('Bulanan',default=False)
    is_different_by_gender = fields.Boolean('Different by Gender?', default=False)
    is_siswa_baru_only = fields.Boolean('Hanya untuk siswa baru?', default=False)
    # harga = fields.Float('Harga', default=0.00, required=True)
    # tahunajarans = fields.One2many('siswa_keu_ocb11.tahunajaran_biaya', inverse_name='biaya_id' , string='Tahun Ajaran')
