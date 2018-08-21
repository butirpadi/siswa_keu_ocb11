# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

class biaya(models.Model):
    _name = 'siswa_keu_ocb11.biaya'
    name = fields.Char(string='Nama', requred=True)
    is_bulanan = fields.Boolean('Bulanan',default=False)
    is_different_by_gender = fields.Boolean('Different by Gender?', default=False)
    is_siswa_baru_only = fields.Boolean('Hanya untuk siswa baru?', default=False)
    is_optional = fields.Boolean('Biaya Opsional?', default=False) 

